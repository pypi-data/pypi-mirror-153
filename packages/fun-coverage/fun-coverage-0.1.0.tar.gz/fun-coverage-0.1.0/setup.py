# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fun_coverage']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=6.3.2,<7.0.0', 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['fun-coverage = '
                     'fun_coverage.fun_coverage:script_entry_point']}

setup_kwargs = {
    'name': 'fun-coverage',
    'version': '0.1.0',
    'description': 'Report function-level code coverage from the statement-level coverage of coverage.py',
    'long_description': "# fun-coverage\n\nfun-coverage is a tool to extract *function coverage* from the *statement (= line) coverage* of [coverage.py](https://github.com/nedbat/coveragepy).\n\n## Installation\nThe simplest way to install fun-coverage is with pip:\n```shell\npip install coverage\n```\n\n## Getting started\nAfter installing the package, a `fun-coverage` command will be available.\n\nYou need to run coverage.py first. For example, if you're using it through [pytest-cov](https://github.com/pytest-dev/pytest-cov/):\n```shell\npytest --cov=<my_module> <my_module_tests>\n```\n\nOnce this is done, simply run:\n```shell\nfun-coverage\n```\n\nThis will print a text report similar to the one of coverage.py, but for functions. The report will include the line numbers of the missed functions.\n\nFor example, this is the output of `fun-coverage` run on its example test suite (as a preliminary step of its actual test suite):\n```\nName                                                                            Funcs   Miss   Cover   Missing\n--------------------------------------------------------------------------------------------------------------\ntests/example_test_suite/src/__init__.py                                            0      0    100%\ntests/example_test_suite/src/async_function.py                                      1      0    100%\ntests/example_test_suite/src/covered_function_with_partially_covered_lines.py       1      0    100%\ntests/example_test_suite/src/docstring_only_function.py                             1      0    100%\ntests/example_test_suite/src/excluded_function.py                                   0      0    100%\ntests/example_test_suite/src/methods.py                                             2      2      0%   6, 9\ntests/example_test_suite/src/non_covered_function.py                                1      1      0%   1\n--------------------------------------------------------------------------------------------------------------\nTOTAL                                                                               6      3     50%\n```\n\n## How it works\nfun-coverage looks for functions and methods in the source code files concerned by a previous round of statement coverage measurement, then marks them as hit if and only if their first statement has been hit.\n\nSpecifically, this starts from the `.coverage` file left by coverage.py. This is configurable with the `--cov-file` flag.\n\n## Command-line options\n```\nusage: fun-coverage [--cov-file COV_FILE] [--cov-fail-under MIN]\n\n  --cov-file COV_FILE   Which coverage file to analyze (default .coverage in the current directory)\n  --cov-fail-under MIN  Fail if the total coverage is strictly less than MIN (a percentage between 0 and 100)\n```\n\n## Excluding code from fun-coverage\nIf the line containing the `def` or `async def` statement for a function is [excluded](https://coverage.readthedocs.io/en/latest/excluding.html) from coverage.py, then fun-coverage ignores that entire function.\n\n## Compatibility\nfun-coverage has been tested with `coverage==6.4`, and `pytest-cov==3.0.0`.\n\n## Development\nThis section only applies if you wish to contribute to the project.\n\n### pre-commit\nThis project uses [pre-commit](https://pre-commit.com/). Please [install it](https://pre-commit.com/#install), then activate it to run automatically on `git commit`:\n```shell\npre-commit install\n```\n### Tests\nRun the test suite with:\n```shell\nmake test\n```\n",
    'author': 'Red Balloon Security',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/redballoonsecurity/fun-coverage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
