#!/usr/bin/env python
"""Module for CompileProcessor, compiles C sources into executable."""

import subprocess
from os.path import join

from helpers import get_ex_solution

from processors.base import BaseProcessor

class CompileProcessor(BaseProcessor):
    """Compile files into exectuable"""
    def get_name(self):
        return "compile"

    def syntax_check(self, path):
        """Syntax check a single source file"""
        out = []

        syntax_cmd = ["g++", "-fsyntax-only", "-Wall", "-Wpedantic"]
        syntax_cmd.append(path)

        syntax_proc = subprocess.Popen(syntax_cmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
        syntax_proc.wait()


        if syntax_proc.returncode != 0:
            out.append({
                'comment': "Compile errors found: {0}".format(path),
                'percentage': 0,
                'suggestion': True,
                'description': [str(line.rstrip()) for line in syntax_proc.stdout]
            })

        return out

    def run(self, uname):
        """Generate list of deductions"""

        out = []

        sol_dir = get_ex_solution(self.exname, uname)
        exec_path = join(sol_dir, "solution")
        src_files = [join(sol_dir, fname) for fname in self.filenames]

        # Syntax check each file
        for fname in src_files:
            syntax_err = self.syntax_check(fname)

            if syntax_err:
                out.extend(syntax_err)

        # Compile files into executable
        compile_cmd = ["g++", "-Wall", "-Wpedantic", "-o", exec_path]
        compile_cmd.extend(src_files)

        compile_proc = subprocess.Popen(compile_cmd,
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.STDOUT)

        compile_proc.wait()


        # Check for compile errors
        if compile_proc.returncode != 0:
            out.append({
                'comment': "Compile / link errors found in {0}.".format(uname),
                'percentage': 50,
                'suggestion': True
            })

        return out
