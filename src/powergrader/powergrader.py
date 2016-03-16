#!/usr/bin/env python3
import click

# Local helpers file
from helpers import *

from os import mkdir, removedirs, listdir
from os.path import join, isdir

import subprocess
import json

import sys, inspect

MANIFEST_NAME = "manifest.json"

@click.group()
def cli():
    pass

@cli.command('import')
@click.argument('input', type=click.Path(exists=True))
@click.argument('name')
@click.argument('id', required=False)
def ingest(input, name, id):
    """ Import a new file into powergrader """
    exname = mangle_ex_name(name, id)

    # Ensure that all required folders exist
    builddirs()

    # Create folder for exercise
    mkdir(get_ex_dir(exname))

    # Create results folder
    mkdir(get_ex_results_dir(exname))

    # Untar exercise file into results folder
    cmd = ['tar', '-xf', input, "-C", get_ex_results_dir(exname)]

    p = subprocess.Popen(cmd)

    p.wait()

    # If tar fails, clean up again
    if p.returncode != 0:
        removedirs(get_ex_dir(exname))

    # Generate manifest into folder

    manifest = {}

    manifest["name"] = exname
    manifest["exname"] = name
    manifest["exid"] = id

    manifest["testcases"] = []

    # TODO Generate file list based on first result set
    manifest["files"] = []


    with open(join(get_ex_dir(exname), MANIFEST_NAME), 'w') as f:
        json.dump(manifest, f, indent=4)

@cli.command()
@click.argument('ex')
def grade(ex):
    """Run all processors on given exercises' results."""
    from processors.base import BaseProcessor
    from processors.diff import DiffProcessor

    exdir = get_ex_dir(ex)

    if not isdir(exdir):
        click.secho("Exercise %s (%s) not found." % (ex, exdir), bold=True, fg='red')
        return

    result_dir = get_ex_results_dir(ex)
    users = listdir(result_dir)

    # TODO Parse manifest to obtain file list and test cases
    with open(join(exdir, 'manifest.json')) as man_file:
        manifest = json.load(man_file)

    testcases = manifest['testcases']
    filenames = manifest['files']


    b = BaseProcessor(ex, filenames, testcases)
    d = DiffProcessor(ex, filenames, testcases)

    # List of all processors, run in this order
    procs = [
        b,
        d
    ]

    click.secho("Grading %s (%s):" % (ex, exdir), bold=True)
    click.echo()

    for user in users:
        resdir = join(result_dir, user)

        if(isdir(resdir)):
            deductions = []
            issues = []

            for processor in procs:
                d = processor.process(user)
                deductions.append(d)

                if d['deductions']:
                    issues.append(processor.get_name())



            if issues:
                click.secho("%s: %s" % (user, issues), fg='red')
            else:
                click.secho("%s: OK" % user, fg='green')

            with open(join(resdir, 'result.json'), 'w') as f:
                json.dump(deductions, f, indent=4)


if __name__ == '__main__':
    cli()
