#!/usr/bin/env python3
"""Wrapper script for cppcheck."""
import sys
from typing import List

from hooks.utils import StaticAnalyzerCmd


class CppcheckCmd(StaticAnalyzerCmd):
    """Class for the cppcheck command."""

    command = "cppcheck"
    lookbehind = "Cppcheck "

    def __init__(self, args: List[str]):
        super().__init__(self.command, self.lookbehind, args)
        self.parse_args(args)
        # quiet for stdout purposes
        self.add_if_missing(["-q"])
        # make cppcheck behave as expected for pre-commit
        self.add_if_missing(["--error-exitcode=1"])
        # Per https://github.com/pocc/pre-commit-hooks/pull/30, suppress missingIncludeSystem messages
        self.add_if_missing(
            ["--suppress=unmatchedSuppression", "--suppress=missingIncludeSystem", "--suppress=unusedFunction"]
        )

    def run(self):
        """Run cppcheck"""
        for filename in self.files:
            self.run_command([filename] + self.args)
            self.exit_on_error()


def main(argv: List[str] = sys.argv):
    cmd = CppcheckCmd(argv)
    cmd.run()


if __name__ == "__main__":
    main()
