#!/usr/bin/env python3

from os import mkdir, makedirs
from os.path import expanduser, join

INPUT_DIR = "input"
OUTPUT_DIR = "output"
PROC_DIR = "processors"
TEST_DIR = "testcases"

ALL_DIRS = [
    INPUT_DIR,
    OUTPUT_DIR,
    PROC_DIR,
    TEST_DIR
]


RESULTS_DIR = "results"


# Base directory finding + creation

def gethomedir():
    """Return users home directory."""
    return expanduser("~")

def getbasedir():
    """Return powergraders home directory"""
    return join(gethomedir(), ".powergrader")

def builddirs(parent=getbasedir()):
    """Create folder structure required for powergrader"""
    for name in ALL_DIRS:
        try:
            makedirs(join(parent,name))
        except FileExistsError:
            pass # Keep going even when some folders already exist



# Exercise directories
def get_ex_dir(exname, parent=getbasedir()):
    """Returns directory for certain exercise"""
    return join(parent, INPUT_DIR, exname)

def get_ex_results_dir(exname, parent=getbasedir()):
    return join(get_ex_dir(exname), RESULTS_DIR)

def get_ex_solution(exname, uname):
    """Returns folder for specific exercise solution"""
    return join(getbasedir(), INPUT_DIR, exname, RESULTS_DIR, uname)


# Name mangling
def mangle_ex_name(exname, exid):
    """Returns composite id for exercise"""
    if exid:
        return exname + "-" + exid
    else:
        return exname
