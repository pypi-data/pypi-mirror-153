"""Console script for sonar_code_diff."""
from dataclasses import dataclass
from email.policy import default
import json
import os
from typing import List, Optional
import click

import filecmp
import difflib


@dataclass
class Diff:
    file: str
    lines: List[int]

def diff_file(test_file:str, truth_file:str) -> Optional[Diff]:
    ret: Optional[Diff] = None
    lines: List[str] = []
    prev_start = ''
    prev_diff = ''
    with open(test_file, errors="replace") as test_file_fd:
        with open(truth_file, errors="replace") as truth_file_fd:
            try:
                differ = difflib.Differ()
                test_file_lines = [line.strip() for line in test_file_fd.readlines()]
                truth_file_lines = [line.strip() for line in truth_file_fd.readlines()]
                diff = differ.compare(test_file_lines, truth_file_lines)
            except:
                raise
            line_index = 1
            for possible_diff in diff:
                current_start = possible_diff[0]
                if current_start == '+' and prev_start == ' ':
                    lines.append(line_index)
                elif current_start == '-':
                    lines.append(line_index)
                if current_start == ' ' or current_start == '-':
                    line_index += 1
                prev_start = current_start
                prev_diff = possible_diff
            if lines:
                ret = Diff(test_file, lines)
    return ret

def diff_directories(test_dir:str, truth_dir:str, ret:List[Diff]) -> None:
    dircmp = filecmp.dircmp(test_dir, truth_dir)
    for common_dir in dircmp.common_dirs:
        diff_directories(os.path.join(test_dir, common_dir), os.path.join(truth_dir, common_dir), ret)
    for common_file in dircmp.common_files:
        diff = diff_file(os.path.join(test_dir, common_file), os.path.join(truth_dir, common_file))
        if diff:
            ret.append(diff)


@click.group()
def main():
    pass

@main.command(help="Perform a diff between TESTDIR and TRUTHDIR and output a sonarqube compatible report")
@click.argument("test_dir")
@click.argument("truth_dir")
@click.option("--report_file", default="code_diff.report", help="Name of report file to create")
def diff(test_dir, truth_dir, report_file):
    ret: List[Diff] = []
    diff_directories(test_dir, truth_dir, ret)
    issues = []
    for diff_file in ret:
        for line in diff_file.lines:
            issues.append({
                "engineId": "sonar_code_diff",
                "ruleId": "rule2",
                "severity": "INFO",
                "type": "CODE_SMELL",
                "primaryLocation": {
                    "message": "difference discovered between file under test and original",
                    "filePath": diff_file.file,
                    "startLine": line
                }

            })
    output = {
        "issues": issues
    }
    with open(report_file, "w+") as fd:
        json.dump(output, fd, indent=4)
    click.echo(f"Wrote report to: {report_file}")

if __name__ == "__main__":
    main()  # pragma: no cover
