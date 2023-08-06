# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pseudocode']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pseudo = pseudocode.pseudo:run']}

setup_kwargs = {
    'name': 'pseudo-9608',
    'version': '0.3.2',
    'description': 'An interpreter for 9608 pseudocode',
    'long_description': '# An interpreter for 9608 pseudocode\n\nPseudo is an interpreter for 9608 pseudocode, a pseudocode syntax used in Cambridge International AS & A Level Computer Science.\n\n## Setup\n\n```\npip install pseudo-9608\n```\n\n## Usage\n\n### Running pseudocode on a file\n\n```\nimport pseudocode\n\npseudocode.runFile(\'myfile.pseudo\')\n```\n\n### Running pseudocode on a string\n\n```\nimport pseudocode\n\ncode = """\nOUTPUT "Hello World!"\n"""\n\npseudocode.run(code)\n```\n\n# Chapters\n\nThis project is also an attempt to write a programming book in a new style. Each chapter of this book is written as a pull request.\n\n- [01a Scanning](https://github.com/nyjc-computing/pseudo/pull/1)\n- [01b Tokens](https://github.com/nyjc-computing/pseudo/pull/2)\n- [02 Expressions](https://github.com/nyjc-computing/pseudo/pull/3)\n- [03 Evaluation](https://github.com/nyjc-computing/pseudo/pull/8)\n- [04 Statements](https://github.com/nyjc-computing/pseudo/pull/9)\n- [05 Interpreting](https://github.com/nyjc-computing/pseudo/pull/10)\n- [06a Variables](https://github.com/nyjc-computing/pseudo/pull/11)\n- [06b Assignment](https://github.com/nyjc-computing/pseudo/pull/12)\n- [06c Retrieving variables](https://github.com/nyjc-computing/pseudo/pull/13)\n- [07 Resolving](https://github.com/nyjc-computing/pseudo/pull/14)\n- [08 Static typing](https://github.com/nyjc-computing/pseudo/pull/15)\n- [09 Conditionals](https://github.com/nyjc-computing/pseudo/pull/17)\n- [10 Loops](https://github.com/nyjc-computing/pseudo/pull/18)\n- [11 Input](https://github.com/nyjc-computing/pseudo/pull/19)\n- [12a Procedures](https://github.com/nyjc-computing/pseudo/pull/20)\n- [12b Procedure calls](https://github.com/nyjc-computing/pseudo/pull/22)\n- [12c Passing by reference](https://github.com/nyjc-computing/pseudo/pull/24)\n- [13a Functions](https://github.com/nyjc-computing/pseudo/pull/25)\n- [13b Loose ends](https://github.com/nyjc-computing/pseudo/pull/26)\n- [14a Reading from source](https://github.com/nyjc-computing/pseudo/pull/28)\n- [14b Line numbers](https://github.com/nyjc-computing/pseudo/pull/29)\n- [14c Referencing source code](https://github.com/nyjc-computing/pseudo/pull/30)\n- [14d Column info](https://github.com/nyjc-computing/pseudo/pull/31)\n- [15 File IO](https://github.com/nyjc-computing/pseudo/pull/32)\n- [16a OOP: Expressions](https://github.com/nyjc-computing/pseudo/pull/34)\n- [16b OOP: Statements](https://github.com/nyjc-computing/pseudo/pull/35)\n- [16c OOP: Expression Statements](https://github.com/nyjc-computing/pseudo/pull/36)\n- [16d OOP: Variables](https://github.com/nyjc-computing/pseudo/pull/37)\n- [16e OOP: Values](https://github.com/nyjc-computing/pseudo/pull/38)\n- [16f OOP: Frames](https://github.com/nyjc-computing/pseudo/pull/40)\n- [16g OOP: Error reporting](https://github.com/nyjc-computing/pseudo/pull/41)\n- [16h OOP: Tokens](https://github.com/nyjc-computing/pseudo/pull/43)\n- [17 Statement hierarchies](https://github.com/nyjc-computing/pseudo/pull/44)\n- [18a Boolean](https://github.com/nyjc-computing/pseudo/pull/45)\n- [18b Logical operators](https://github.com/nyjc-computing/pseudo/pull/48)\n- [18c Fix: logical operators](https://github.com/nyjc-computing/pseudo/pull/49) (This is an addendum to 18b)\n- [19 REALs](https://github.com/nyjc-computing/pseudo/pull/51)\n- [20 Packaging](https://github.com/nyjc-computing/pseudo-9608/pull/52)\n- [21a Test: Data passing](https://github.com/nyjc-computing/pseudo-9608/pull/53)\n- [21b Test: Checking output](https://github.com/nyjc-computing/pseudo-9608/pull/54)\n- [21c Test: Checking Errors](https://github.com/nyjc-computing/pseudo-9608/pull/55)\n- [22a Scoping: Recursion](https://github.com/nyjc-computing/pseudo-9608/pull/56)\n- [22b Scoping: System](https://github.com/nyjc-computing/pseudo-9608/pull/57)\n- [23a Object: Scopes](https://github.com/nyjc-computing/pseudo-9608/pull/58)\n- [23b Object: Attributes](https://github.com/nyjc-computing/pseudo-9608/pull/59)\n- [23c Object: ARRAY](https://github.com/nyjc-computing/pseudo-9608/pull/60)\n- [24a Improvements: type annotation](https://github.com/nyjc-computing/pseudo-9608/pull/61)\n- [24b Improvements: Decoupling](https://github.com/nyjc-computing/pseudo-9608/pull/64)\n- [24c Improvements: Type Relationship](https://github.com/nyjc-computing/pseudo-9608/pull/65)\n- [24d Improvements: Parser](https://github.com/nyjc-computing/pseudo-9608/pull/67)\n- [24e Improvements: Resolver](https://github.com/nyjc-computing/pseudo-9608/pull/69)\n- [24f Improvements: Interpreter](https://github.com/nyjc-computing/pseudo-9608/pull/70)\n- [24g Improvements: Pseudo](https://github.com/nyjc-computing/pseudo-9608/pull/71)\n- [25a Automation: Testing](https://github.com/nyjc-computing/pseudo-9608/pull/72)',
    'author': 'JS Ng',
    'author_email': 'ngjunsiang@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nyjc-computing/pseudo-9608',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
