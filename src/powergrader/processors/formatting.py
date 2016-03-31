#!/usr/bin/env python
"""Module for FormattingProcessor, checks formatting of code."""

import subprocess
from os.path import join

from helpers import get_ex_solution

from processors.base import BaseProcessor

class FormattingProcessor(BaseProcessor):
    """Checks for line length as well as usage of only ASCII characters"""

    MAX_LINE_LENGTH = 80

    def get_name(self):
        return "formatting"

    def line_length(self, path):
        """Check line lengths in file"""
        out = []

        exceeded = 0
        line_numbers = []


        with open(path) as length_file:
            for idx, line in enumerate(length_file):
                if len(line) > self.MAX_LINE_LENGTH:
                    exceeded += 1
                    line_numbers.append(
                        "Line {0}: {1} chars".format(idx, len(line))
                        )


        if exceeded:
            out.append({
                'comment': "Line length exceeded {0} times.".format(exceeded),
                'percentage': 5,
                'suggestion': False,
                'description': line_numbers
            })

        return out

    def run(self, uname):
        """Generate list of deductions"""

        out = []

        sol_dir = get_ex_solution(self.exname, uname)
        exec_path = join(sol_dir, "solution")
        src_files = [join(sol_dir, fname) for fname in self.filenames]

        # Check formatting in each file
        for fname in src_files:
            length_errors = self.line_length(fname)

            if length_errors:
                out.append(length_errors)

        return out
