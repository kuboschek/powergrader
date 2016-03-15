#!/usr/bin/env python

import datetime
from helpers import get_ex_dir, get_ex_solution

class BaseProcessor(object):
    def __init__(self, exname, filenames, testcases):
        self.exname = exname
        self.ex_dir = get_ex_dir(exname)
        self.filenames = filenames
        self.testcases = testcases

        self.procname = "base"

    def get_name(self):
        return self.procname

    def run(self, uname):
        """Generate list of deductions"""

        out = [{
            'comment': 'BaseProcessor processed %s for %s' % (self.exname, uname),
            'percentage': 0,
            'suggestion': True
        }]

        return out

    def process(self, uname):
        """Output object of deductions"""

        out = {
            'generated-by': self.procname,
            'timestamp': datetime.datetime.now().isoformat(),
            'deductions': self.run(uname)
        }

        return out
