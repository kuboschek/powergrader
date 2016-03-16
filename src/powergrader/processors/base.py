#!/usr/bin/env python

import datetime
from helpers import get_ex_dir

class BaseProcessor(object):
    """Do nothing processor."""
    def __init__(self, exname, filenames, testcases):
        self.exname = exname
        self.ex_dir = get_ex_dir(exname)
        self.filenames = filenames
        self.testcases = testcases

    def get_name(self):
        return "base"

    def run(self, uname):
        """Generate list of deductions"""

        out = []

        return out

    def process(self, uname):
        """Output object of deductions"""

        out = {
            'generated-by': self.get_name(),
            'timestamp': datetime.datetime.now().isoformat(),
            'deductions': self.run(uname)
        }

        return out
