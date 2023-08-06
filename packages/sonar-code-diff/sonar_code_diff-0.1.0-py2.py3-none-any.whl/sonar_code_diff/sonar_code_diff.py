"""Main module."""

import filecmp

def diff_directories(test_dir:str, truth_dir:str) -> str:
    dircmp = filecmp.dircmp(test_dir, truth_dir)
    common_files = dircmp.common_files
    print(common_files)
