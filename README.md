C++ Grade Tools

Features
- [ ] Create diff matrix
- [ ] Compile all projects
- [ ] valgrind on all projects
- [ ] Check output of all projects
- [ ] Generate grade suggestion
- [ ] Take grade updates, with comments, store in user folder
- [ ] Generate grade result file
- [ ] (input grades on grader)
- [ ] (parse C comments into grade deductions)

Processors:
* `00-base.py` — Python base class
* `20-diff.py` — Diffs files, generates
* `30-compile.py` — Compiles project
* `40-testcases.py` — Runs attached testcases on solutions
* `50-valgrind.py` — Check for memory leaks on all solutions
* `60-comments.py` - Process TA comments

Each processor takes a file, info about the exercise, and returns a list of grade deductions

Folder structure:
* `input` - input files
    * `/<ex-name> - <ex-id>`
        * `/manifest.json`
        * `/results.tar`
        * `/results`
            * `/<username>`
                * `/<user files>`
                * `/result.json`
* `output` - grade lists here
    * /`<ex-name>.json`
* `processors` - scripts run on results
    * `/<num> - <script name>.py`
* `testcases` - testcases for results
    * `/<testcase name>`
        * `in` - input for program
        * `out` - output for program
* `powergrader.py` - main cmd script

manifest.json:
* name of task
* corresponding testcases
* filenames of given files

result.json:
* generated deductions (from processors)
    * generated - by
    * timestamp
        * comment
        * percentage
        * suggestion == true | false

Command structure:

ex := exid | exname

* pg
    * import <file> <name> <id> — imports a new tarball from Grader
    * grade <ex> — run processors on given exercise
    * test <testname> *NYI*
        * link <ex> — mark given test as relevant for exercise
        * create — create a new test interactively *NYI*
        * create <in> <out> — create a new test from files *NYI*
        * show - show testcase *NYI*
        * edit | edit in | edit out — edit testcase files *NYI*
        * delete — delete testcase *NYI*
    * show <ex> — grade summary for exercise
    * show <ex> <username> — show deductions for given user *NYI*
    * review <ex> <username> — review grade suggestions for given solution *NYI*
    * open <ex> — open exercise folder *NYI*
    * open <ex> <username> — open user’s solution *NYI*
