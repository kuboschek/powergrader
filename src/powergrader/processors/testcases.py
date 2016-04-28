#!/usr/bin/env python

import datetime
import subprocess
from difflib import unified_diff

from os.path import isfile,join

from helpers import get_ex_dir, get_ex_solution, get_test_in_path, get_test_out_path
from processors.base import BaseProcessor

class TestCaseProcessor(BaseProcessor):
    """Checks generated binaries against provided testcases."""

    DEFAULT_TIMEOUT = 5
    timeout = DEFAULT_TIMEOUT


    def get_name(self):
        return "testcases"

    def run(self, uname):
        """Generate list of deductions"""

        out = []

        sol_dir = get_ex_solution(self.exname, uname)
        exec_path = join(sol_dir, "solution")
        test_out = join(sol_dir, "test_out")

        if not isfile(exec_path):
            return

        for test in self.testcases:
            in_path = get_test_in_path(test)
            out_path = get_test_out_path(test)

            test_proc = subprocess.Popen([exec_path],
                            stdin=open(in_path),
                            stdout=open(test_out, "w+"))
            try:
                test_proc.wait(timeout=self.timeout)
            except TimeoutExpired:
                out.append({
                    'comment': "Execution timed out after {0}s.".format(self.timeout),
                    'percentage': 0,
                    'suggestion': True,
                    'description': []
                })

            # Compare output to expected output
            with open(test_out) as actual_out:
                with open(out_path) as expected_out:
                    res = list(unified_diff(
                            list(actual_out), list(expected_out),
                            fromfile="actual", tofile="expected"))

                    if res:
                        out.append({
                            'comment': "Incorrect output in testcase {0}.".format(test),
                            'percentage': 30,
                            'suggestion': False,
                            'description': res
                        })



        return out
