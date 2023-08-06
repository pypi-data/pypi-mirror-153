"""Console script for sonar_code_diff."""
from dataclasses import dataclass
import fnmatch
import json
import os
from typing import List, Optional
import click

import filecmp
import difflib


@dataclass
class Diff:
    """Used to keep track of lines that are different on a file"""

    file: str
    lines: List[int]


def diff_file(test_file: str, truth_file: str) -> Optional[Diff]:
    """Compare a file under test and the version of it that has come
       from a verified source

    Args:
        test_file (str): File that you are checking for changes
        truth_file (str): File that you know is correct

    Returns:
        Optional[Diff]: None if nothing is different, otherwise return
                        a Diff with the filename and a list of lines that
                        are different.
    """
    ret: Optional[Diff] = None
    lines: List[int] = []
    prev_start = ""
    with open(test_file, errors="replace") as test_file_fd:
        with open(truth_file, errors="replace") as truth_file_fd:
            differ = difflib.Differ()
            test_file_lines = [line.strip() for line in test_file_fd.readlines()]
            truth_file_lines = [line.strip() for line in truth_file_fd.readlines()]
            diff = differ.compare(test_file_lines, truth_file_lines)

            # Follow ndiff rules with the following code.  The first character
            # in the ndiff determines the result of the line.  An empty space
            # means the lines are the same, a "-" means it is new on the left.
            # A "+" means it is new on the right, and a "?" means it isn't on
            # either side.  If there is a "+" but the previous line wasn't a
            # " " then the "+" is indicating what the right side has that is
            # different from the left.
            line_index = 1
            for possible_diff in diff:
                current_start = possible_diff[0]
                if current_start == "+" and prev_start == " ":
                    lines.append(line_index)
                elif current_start == "-":
                    lines.append(line_index)
                if current_start == " " or current_start == "-":
                    line_index += 1
                prev_start = current_start
            if lines:
                ret = Diff(test_file, lines)
    return ret


def diff_directories(test_dir: str, truth_dir: str, ret: List[Diff]) -> None:
    """Top level function that is recursive and is used to update
       the `ret' which is a list of Diffs that have been discovered between
       two directories that are expected to be the same.

    Args:
        test_dir (str): Path to directory that you are testing for differences
        truth_dir (str): Path to directory that you know contains
                         un-tampered code
        ret (List[Diff]): List of Diff instances for all discovered differences
    """
    dircmp = filecmp.dircmp(test_dir, truth_dir)
    for common_dir in dircmp.common_dirs:
        diff_directories(
            os.path.join(test_dir, common_dir), os.path.join(truth_dir, common_dir), ret
        )
    for common_file in dircmp.common_files:
        diff = diff_file(
            os.path.join(test_dir, common_file), os.path.join(truth_dir, common_file)
        )
        if diff:
            ret.append(diff)


@click.group()
def main():
    pass


@main.command(
    help="Perform a diff between TESTDIR and TRUTHDIR and output a "
    + "sonarqube compatible report"
)
@click.argument("test_dir")
@click.argument("truth_dir")
@click.option(
    "--report_file",
    default="code_diff.report",
    help="Name of report file " + "to create",
)
@click.option(
    "--ignore_file",
    default=None,
    help="Line separated list of glob style file patterns to ignore",
)
def diff(test_dir, truth_dir, report_file, ignore_file):
    # First determine if there are any glob patterns of files that we want to
    # ignore.  The idea here would be to ignore any files that initially fail
    # the scan but you have verified that they are safe.
    ignore_patterns = []
    if ignore_file is not None and os.path.exists(ignore_file):
        with open(ignore_file) as ignore_file_fd:
            ignore_patterns = [
                pattern.strip() for pattern in ignore_file_fd.readlines()
            ]

    # get the list of Diffs between the directories
    ret: List[Diff] = []
    diff_directories(test_dir, truth_dir, ret)

    # put together the SonarQube issue report that can be imported
    issues = []
    for diff_file in ret:
        ignore = False
        for ignore_pattern in ignore_patterns:
            if fnmatch.fnmatch(diff_file.file, ignore_pattern):
                ignore = True
                break
        if ignore:
            continue
        for line in diff_file.lines:
            issues.append(
                {
                    "engineId": "sonar_code_diff",
                    "ruleId": "rule2",
                    "severity": "INFO",
                    "type": "CODE_SMELL",
                    "primaryLocation": {
                        "message": "difference discovered between file "
                        + "under test and original",
                        "filePath": diff_file.file,
                        "startLine": line,
                    },
                }
            )
    output = {"issues": issues}
    with open(report_file, "w+") as fd:
        json.dump(output, fd, indent=4)

    click.echo(f"Wrote report to: {report_file}")


if __name__ == "__main__":
    main()  # pragma: no cover
