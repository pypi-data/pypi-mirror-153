## No CAP: Typing to ConfigArgParse

Write once with inspection of type hinted python objects from Python's standard library [typing](https://docs.python.org/3/library/typing.html) to generate a ConfigArgParser.
[ConfigArgParser](https://github.com/bw2/ConfigArgParse) is a drop in replacement for python's argparse that adds support for parsing configuration files and environment variables in addition to argparse's command line interface.
Type hinting your python objects should be enough to generate a hierarchical ConfigArgParser automtically through inspection.

If you want to generate a ConfigArgParser from your docstrings, see [docstr](https://github.com/prijatelj/docstr), which will depend upon this project.

Considering using `typing_inspect`.
