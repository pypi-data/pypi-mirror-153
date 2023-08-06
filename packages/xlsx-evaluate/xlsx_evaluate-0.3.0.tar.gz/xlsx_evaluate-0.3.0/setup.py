# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xlsx_evaluate', 'xlsx_evaluate.functions']

package_data = \
{'': ['*']}

install_requires = \
['jsonpickle>=2.2.0,<3.0.0',
 'mock>=4.0.3,<5.0.0',
 'numpy-financial>=1.0.0,<2.0.0',
 'numpy>=1.22.4,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.4.2,<2.0.0',
 'scipy>=1.8.1,<2.0.0',
 'yearfrac>=0.4.7,<0.5.0']

setup_kwargs = {
    'name': 'xlsx-evaluate',
    'version': '0.3.0',
    'description': 'Calculate XLSX formulas',
    'long_description': '# Calculate XLSX formulas\n\n[![CI](https://github.com/devind-team/xlsx_evaluate/workflows/Release/badge.svg)](https://github.com/devind-team/devind-django-dictionaries/actions)\n[![Coverage Status](https://coveralls.io/repos/github/devind-team/xlsx_evaluate/badge.svg?branch=main)](https://coveralls.io/github/devind-team/devind-django-dictionaries?branch=main)\n[![PyPI version](https://badge.fury.io/py/xlsx-evaluate.svg)](https://badge.fury.io/py/xlsx_evaluate)\n[![License: MIT](https://img.shields.io/badge/License-MIT-success.svg)](https://opensource.org/licenses/MIT)\n\n**xlsx_evaluate** - python library to convert excel functions in python code without the need for Excel itself within the scope of supported features.\n\nThis library is fork [xlcalculator](https://github.com/bradbase/xlcalculator). Use this library.\n\n# Summary\n\n- [Currently supports](docs/support.rst)\n- [Supported Functions](docs/support_functions.rst)\n- [Adding/Registering Excel Functions](docs/support_functions.rst)\n- [Excel number precision](docs/number_precision.rst)\n- [Test](docs/test.rst)\n\n# Installation\n\n```shell\n# pip\npip install xlsx-evaluate\n# poetry\npoetry add xlsx-evaluate\n```\n\n\n# Example\n\n```python\ninput_dict = {\n    \'B4\': 0.95,\n    \'B2\': 1000,\n    "B19": 0.001,\n    \'B20\': 4,\n    \'B22\': 1,\n    \'B23\': 2,\n    \'B24\': 3,\n    \'B25\': \'=B2*B4\',\n    \'B26\': 5,\n    \'B27\': 6,\n    \'B28\': \'=B19 * B20 * B22\',\n    \'C22\': \'=SUM(B22:B28)\',\n  }\n\nfrom xlsx_evaluate import ModelCompiler\nfrom xlsx_evaluate import Evaluator\n\ncompiler = ModelCompiler()\nmy_model = compiler.read_and_parse_dict(input_dict)\nevaluator = Evaluator(my_model)\n\nfor formula in my_model.formulae:\n    print(f\'Formula {formula} evaluates to {evaluator.evaluate(formula)}\')\n\n# cells need a sheet and Sheet1 is default.\nevaluator.set_cell_value(\'Sheet1!B22\', 100)\nprint(\'Formula B28 now evaluates to\', evaluator.evaluate(\'Sheet1!B28\'))\nprint(\'Formula C22 now evaluates to\', evaluator.evaluate(\'Sheet1!C22\'))\n```\n\n# TODO\n\n- Do not treat ranges as a granular AST node it instead as an operation ":" of\n  two cell references to create the range. That will make implementing\n  features like ``A1:OFFSET(...)`` easy to implement.\n\n- Support for alternative range evaluation: by ref (pointer), by expr (lazy\n  eval) and current eval mode.\n\n    * Pointers would allow easy implementations of functions like OFFSET().\n\n    * Lazy evals will allow efficient implementation of IF() since execution\n      of true and false expressions can be delayed until it is decided which\n      expression is needed.\n\n- Implement array functions. It is really not that hard once a proper\n  RangeData class has been implemented on which one can easily act with scalar\n  functions.\n\n- Improve testing\n\n- Refactor model and evaluator to use pass-by-object-reference for values of\n  cells which then get "used"/referenced by ranges, defined names and formulas\n\n- Handle multi-file addresses\n\n- Improve integration with pyopenxl for reading and writing files [example of\n  problem space](https://stackoverflow.com/questions/40248564/pre-calculate-excel-formulas-when-exporting-data-with-python)',
    'author': 'Victor',
    'author_email': 'lyferov@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devind-team/xlsx_evaluate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
