#!/usr/bin/env python3
"""Powergrader is a tool to evaluate given C/C++ source files for grading."""
# Local helpers file
# from helpers import *

from os import mkdir, removedirs, listdir, rmdir, rename
from os.path import join, isdir, isfile, normpath, basename, splitext

import subprocess
import json

import click

from helpers import builddirs, get_ex_dir, get_ex_results_dir, mangle_ex_name, get_test_dir

MANIFEST_NAME = "manifest.json"
RESULT_NAME = "result.json"

@click.group()
def cli():
    """Top-level CLI"""
    pass

@cli.command('import')
@click.argument('file', type=click.Path(exists=True))
def ingest(file):
    """ Import a new file into powergrader """

    # Generate exercise name from
    exname = splitext(basename(normpath(file)))[0]

    # Ensure that all required folders exist
    builddirs()

    # Create folder for exercise
    mkdir(get_ex_dir(exname))

    # Create results folder
    mkdir(get_ex_results_dir(exname))

    # Untar exercise file into results folder
    cmd = ['tar', '-xf', file, "-C", get_ex_results_dir(exname)]

    untar = subprocess.Popen(cmd)

    untar.wait()

    # If tar fails, clean up again
    if untar.returncode != 0:
        removedirs(get_ex_dir(exname))
        click.secho("Importing exercise {0} failed.".format(exname), fg='red')
        return

    # Get list of result directories
    files_at = join(get_ex_results_dir(exname), exname)
    result_dirs = filter(isdir,
                 [join(files_at, path)
                  for path in listdir(files_at)])

    # Move all subfolders one level up
    for r in result_dirs:
        uname = basename(normpath(r))
        rename(r, join(get_ex_results_dir(exname), uname))

    # Delete original folder
    rmdir(files_at)

    # Generate manifest into folder
    manifest = {}

    manifest["name"] = exname
    manifest["exname"] = exname

    manifest["testcases"] = []

    # TODO Generate file list based on first result set
    manifest["files"] = []

    with open(join(get_ex_dir(exname), MANIFEST_NAME), 'w') as man_file:
        json.dump(manifest, man_file, indent=4)

@cli.command()
@click.argument('ex')
def grade(ex):
    """Run all processors on exercise results"""
    from processors.base import BaseProcessor
    from processors.diff import DiffProcessor
    from processors.compile import CompileProcessor
    from processors.formatting import FormattingProcessor
    from processors.testcases import TestCaseProcessor

    exdir = get_ex_dir(ex)

    if not isdir(exdir):
        click.secho("Exercise %s (%s) not found." % (ex, exdir), bold=True, fg='red')
        return

    result_dir = get_ex_results_dir(ex)

    # TODO Parse manifest to obtain file list and test cases
    with open(join(exdir, 'manifest.json')) as man_file:
        manifest = json.load(man_file)

    # List of all processors, run in this order
    proc_classes = [
        BaseProcessor,
        DiffProcessor,
        FormattingProcessor,
        CompileProcessor,
        TestCaseProcessor,
    ]

    # Instantiate each processor
    procs = [proc_cls(ex, manifest['files'], manifest['testcases']) for proc_cls in proc_classes]

    click.secho("Grading %s (%s):" % (ex, exdir), bold=True)
    click.echo()

    for user in listdir(result_dir):
        resdir = join(result_dir, user)

        if isdir(resdir):
            deductions = []
            issues = []

            for processor in procs:
                out = processor.process(user)
                deductions.append(out)

                if out['deductions']:
                    issues.append(processor.get_name())



            if issues:
                click.secho("%s: %s" % (user, issues), fg='red')
            else:
                click.secho("%s: OK" % user, fg='green')

            with open(join(resdir, RESULT_NAME), 'w') as res_file:
                json.dump(deductions, res_file, indent=4)

@cli.command()
@click.argument('ex')
@click.argument('uname', required=False)
def show(ex, uname):
    result_dir = get_ex_results_dir(ex)

    if not isdir(result_dir):
        click.secho("Exercise {0} not found ({1})".format(ex, result_dir), fg='red')
        return

    if uname:
        user_dir = join(result_dir, uname)
        if not isdir(user_dir):
            click.secho("User {0} not found ({1})".format(uname, user_dir), fg='red')
            return
        # TODO Show detailed grading for user
    else:
        # Print grade summary
        for user in listdir(result_dir):
            resdir = join(result_dir, user)

            if isdir(resdir):
                with open(join(resdir, RESULT_NAME)) as res_file:
                    result = json.load(res_file)

                percentage = 100
                suggest = 100

                for proc in result:
                    if proc['deductions']:
                        for d in proc['deductions']:
                            suggest -= d['percentage']

                            if not d['suggestion']:
                                percentage -= d['percentage']

                color = 'red' if percentage < 50 else 'yellow' if percentage < 100 else 'green'
                suggest = "({0}%)".format(suggest) if suggest != percentage else ""
                click.secho("{0}: {1}% {2}".format(user, percentage, suggest), fg=color)

IN_FILE = 'in'
OUT_FILE = 'out'

@cli.group()
@click.argument('name')
@click.pass_context
def test(ctx, name):
    """Commands for editing test cases for exercises"""
    ctx.obj['TEST_NAME'] = name

@test.command()
@click.argument('file_in', type=click.Path(exists=True), required=False)
@click.argument('file_out', type=click.Path(exists=True), required=False)
@click.pass_context
def create(ctx, file_in, file_out):
    """Create a new testcase NYI"""
    print("TODO")

@test.command()
@click.argument('ex')
@click.pass_context
def link(ctx, ex):
    """Mark a test as relevant to this exercise"""
    problem = ""
    test_name = ctx.obj['TEST_NAME']

    # Find test directory
    testdir = get_test_dir(test_name)

    if not (isdir(testdir) and isfile(join(testdir, IN_FILE)) and isfile(join(testdir, OUT_FILE))):
        problem = "No such test."

    # Find manifest for exercise
    exdir = get_ex_dir(ex)

    if not isdir(exdir):
        problem = "No such exercise."

    if problem != "":
        click.secho(problem, fg='red')
        return

    with open(join(get_ex_dir(ex), MANIFEST_NAME)) as man_file:
        manifest = json.load(man_file)

    # Actually append the testcase
    if manifest['testcases'].count(test_name) == 0:
        manifest['testcases'].append(test_name)

    # Rewind to the beginning
    with open(join(get_ex_dir(ex), MANIFEST_NAME), 'w') as man_f:
        json.dump(manifest, man_f, indent=4)

    return

if __name__ == '__main__':
    cli(obj={})
