#!/usr/bin/env python
"""Module for DiffProcessor, diffs files to find plagiarism"""
from os import listdir
from os.path import join, isdir

from difflib import SequenceMatcher

from processors.base import BaseProcessor
from helpers import get_ex_solution, get_ex_results_dir

class DiffProcessor(BaseProcessor):
    """Diffs all resultsets of all students, to find plagiarism."""
    def __init__(self, *args, **kwargs):
        super(DiffProcessor, self).__init__(*args, **kwargs)
        self.similarity_warning = 0.7 # Warn when 70% similar

    def get_name(self):
        return "diff"

    def run(self, uname):
        """Diff everything, to find copied solutions."""
        out = []

        users = listdir(get_ex_results_dir(self.exname))

        for fname in self.filenames:
            with open(join(get_ex_solution(self.exname, uname), fname)) as own_copy:
                own_data = own_copy.read()

                for user in users:
                    res_dir = get_ex_solution(self.exname, user)

                    if not isdir(res_dir):
                        continue

                    if user == uname:
                        continue

                    with open(join(get_ex_solution(self.exname, user), fname)) as their_copy:
                        their_data = their_copy.read()
                        similarity = SequenceMatcher(None, own_data, their_data).ratio()

                        if similarity > self.similarity_warning:
                            text = "Similarity: {0}/{1} -> {2}/{3} = {4}"
                            text = text.format(uname, fname, user, fname, similarity)

                            out.append({
                                'comment': text,
                                'percentage': 100,
                                'suggestion': True
                            })
        return out
