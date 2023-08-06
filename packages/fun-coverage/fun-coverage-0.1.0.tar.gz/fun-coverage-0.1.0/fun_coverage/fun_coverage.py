"""
Script to output function coverage from the line coverage of coverage.py.
"""
from dataclasses import dataclass
from typing import List, Optional

import argparse
import ast
import sys
from re import match
from termcolor import cprint

from coverage import Coverage
from coverage.report import get_analysis_to_report

FUNCTION_DEF_REGEX = r"\s*(async )?def "


@dataclass
class FuncInfo:
    """Information on a function retrieved from static parsing of a Python source file."""

    # Line number of the `def` or `async def` statement for this function
    def_lineno: int
    # Line number of the first statement (docstrings excluded) of the function,
    # or None if there is no such statement (which can happen in a docstring-only function).
    first_statement: Optional[int]


@dataclass
class FileFuncAnalysis:
    """
    Function-level analysis of a source file.
    """

    filename: str
    # Line numbers for all non-excluded functions in the file
    funcs: List[int]
    # Like `funcs`, but only including the functions that weren't covered
    missing: List[int]

    @property
    def n_funcs(self):
        return len(self.funcs)

    @property
    def n_missing(self):
        return len(self.missing)


def fatal_err(err_msg):
    cprint(f"FAIL {err_msg}", "red", attrs=["bold"])
    sys.exit(1)


def get_funcs(filename: str, included_lines: List[int]) -> List[FuncInfo]:
    """
    Return a list of `FuncInfo` objects for non-excluded functions in `filename`.

    A function is considered to be excluded if its `def` or `async def` statement is not part of
    `included_lines`.

    :param filename: filename of the Python source code file to analyze
    :param included_lines: list of line numbers to include
    """
    funcs = []
    with open(filename) as f:
        tree = ast.parse(f.read())
    with open(filename) as f:
        lines = f.read().splitlines()

    for item in ast.walk(tree):
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            def_lineno = item.lineno
            if not match(FUNCTION_DEF_REGEX, lines[def_lineno - 1]):
                # ast returns decorators as functions, so we make sure this
                # looks like a normal function definition. (note that `lines`
                # starts indexing at 0, so we need to subtract 1).
                continue
            if def_lineno not in included_lines:
                # Ignore non-included functions
                continue
            child_nodes = item.body
            if ast.get_docstring(item):
                child_nodes = child_nodes[1:]
            first_statement = None
            if child_nodes:
                first_statement = child_nodes[0].lineno
            funcs.append(FuncInfo(def_lineno, first_statement))

    return funcs


def get_missing(funcs: List[FuncInfo], lines_covered: List[int]) -> List[int]:
    """
    Return a list of the line numbers of all missed functions.

    The line number of a function is the line of its `def` or `async def` statement.

    A function is missed if the first statement after its `def` or `async def` statement is
    not executed (docstrings aren't counted as statements, in line with coverage.py).

    :param funcs: list of `FuncInfo` objects, to analyze as missing or not
    :param lines_covered: list of line numbers covered
    """
    missing = []
    for func in funcs:
        if func.first_statement and func.first_statement not in lines_covered:
            missing.append(func.def_lineno)
    return missing


def compute_pc_covered(n_funcs: int, n_missing: int) -> float:
    """
    Return the percentage of functions covered, from `n_funcs` and `n_missing`, as a float between 0 and 1.

    If `n_funcs` is 0, the returned percentage is 1.

    :param n_funcs: the total number of functions
    :param n_missing: the number of functions that weren't covered
    """
    if n_funcs == 0:
        return 1
    else:
        return 1 - (n_missing / n_funcs)


def gen_report(file_analyses: List[FileFuncAnalysis]) -> float:
    """
    Output a text report from `file_analyses` similar to the text report of `coverage report`.

    Return the global function-level coverage percentage, as a float between 0 and 1.

    :param file_analyses: list of `FileFuncAnalysis` objects, one for each source file to include in the report
    """
    col_sep_width = 3
    name_width = max(len(file_analysis.filename) for file_analysis in file_analyses)
    funcs_width = 5
    miss_width = 4
    cover_width = 5
    line_format = (" " * col_sep_width).join(
        [
            f"{{:<{name_width}}}",
            f"{{:>{funcs_width}}}",
            f"{{:>{miss_width}}}",
            f"{{:>{cover_width}}}",
            "{}",
        ]
    )
    header = line_format.format("Name", "Funcs", "Miss", "Cover", "Missing")
    print(header)
    print("-" * len(header))
    for file_analysis in file_analyses:
        pc_covered = compute_pc_covered(file_analysis.n_funcs, file_analysis.n_missing)
        missing_str = ", ".join([str(missing) for missing in file_analysis.missing])
        print(
            line_format.format(
                file_analysis.filename,
                file_analysis.n_funcs,
                file_analysis.n_missing,
                f"{pc_covered:.0%}",
                missing_str,
            )
        )
    total_funcs = sum(file_analysis.n_funcs for file_analysis in file_analyses)
    total_misses = sum(file_analysis.n_missing for file_analysis in file_analyses)
    total_pc_covered = compute_pc_covered(total_funcs, total_misses)
    print("-" * len(header))
    print(line_format.format("TOTAL", total_funcs, total_misses, f"{total_pc_covered:.0%}", ""))
    print()
    return total_pc_covered


def check_against_min_coverage(pc_covered: float, min_pc_covered: float) -> None:
    """
    Raise a fatal error if `pc_covered` is strictly smaller than `min_pc_covered`.

    :param pc_covered: the percentage of functions covered
    :param min_pc_covered: the minimum accepted percentage of functions covered
    """
    if pc_covered < min_pc_covered:
        fatal_err(
            f"Required function coverage of {min_pc_covered:.2%} not reached. Total coverage: {pc_covered:.2%}"
        )
    else:
        cprint(
            f"Required function coverage of {min_pc_covered:.2%} reached. Total coverage: {pc_covered:.2%}",
            "green",
        )


def parse_args(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze the output of coverage.py to extract function coverage from line coverage"
    )
    parser.add_argument(
        "--cov-file",
        type=str,
        default=".coverage",
        help="Which coverage file to analyze (default .coverage in the current directory)",
    )
    parser.add_argument(
        "--cov-fail-under",
        type=float,
        default=None,
        metavar="MIN",
        help="Fail if the total coverage is strictly less than MIN (a percentage between 0 and 100)",
    )
    return parser.parse_args(args)


def main(cov_file: str, cov_fail_under: Optional[int]) -> None:
    """
    Programmatic entry point.

    Implementation caveat: we need information on excluded lines, which depends on the configuration
    file used, not the .coverage file `cov_file`. This function creates a `Coverage` object, supplying
    no configuration file in particular. Creating a `Coverage` object like this will result in the same
    configuration file used as in the initial invocation of `coverage`, UNLESS this previous invocation
    used a non-standard path for the configuration file (e.g. pytest-cov --cov-config=...). In that
    case, this script will potentially be wrong, as that configuration file might specify a non-standard
    set of lines to exclude.

    :param cov_file: full or relative path to the coverage file to analyze
    :param cov_fail_under: fail if this number is not None and is strictly greater than the total coverage
    """
    coverage = Coverage(data_file=cov_file)
    coverage_data = coverage.get_data()
    coverage_data.read()
    file_analyses = []
    for fr, analysis in get_analysis_to_report(coverage, None):
        funcs = get_funcs(fr.filename, analysis.statements)
        missing = get_missing(funcs, coverage_data.lines(fr.filename))
        func_linenos = [func.def_lineno for func in funcs]
        file_analyses.append(
            FileFuncAnalysis(filename=fr.relname, funcs=func_linenos, missing=missing)
        )
    total_pc_covered = gen_report(file_analyses)
    if cov_fail_under is not None:
        min_pc_covered = cov_fail_under / 100
        check_against_min_coverage(total_pc_covered, min_pc_covered)


def script_entry_point() -> None:
    args = parse_args(sys.argv[1:])
    main(args.cov_file, args.cov_fail_under)
