#!/usr/bin/env python3
import click

# Local helpers file
from helpers import *

from os import mkdir, removedirs
from os.path import join

import subprocess
import json

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
        json.dump(manifest, f)

if __name__ == '__main__':
    cli()
