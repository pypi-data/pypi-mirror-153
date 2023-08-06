# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pseudocode']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pseudo = pseudocode:main']}

setup_kwargs = {
    'name': 'pseudo-9608',
    'version': '0.5.0a0',
    'description': 'An interpreter for 9608 pseudocode',
    'long_description': '# An interpreter for 9608 pseudocode\n[![Run on Repl.it](https://replit.com/badge/github/nyjc-computing/pseudo-9608)](https://replit.com/@nyjc-computing/pseudo-9608)\n\nPseudo is an interpreter for 9608 pseudocode, a pseudocode syntax used in Cambridge International AS & A Level Computer Science.\n\nThe latest version is 0.4.1.\n\n## Setup\n\n```\npip install pseudo-9608\n```\n\n## Usage\n\nTo try `pseudo` without installing it, fork the Replit repl at\nhttps://replit.com/@nyjc-computing/pseudocode-repl.\n\n### Shell: Running with a pseudocode file\n\n```\n$ pseudo myfile.pseudo\n```\n\nThis will run the pseudocode interpreter on the file `myfile.pseudo`.\n\n### Python: Running with a pseudocode file\n\n```\nimport pseudocode\n\npseudocode.runFile(\'myfile.pseudo\')\n```\n\nThis will run the pseudocode interpreter on the file `myfile.pseudo`.\n\n### Python: Running with a pseudocode string\n\n```\nimport pseudocode\n\ncode = """\nOUTPUT "Hello World!"\n"""\n\npseudocode.run(code)\n```\n\nThis will run the pseudocode interpreter on the string `code`.\n\n# Build Instructions\n\nI don\'t have a build process for Windows yet; if you are experienced in this area and can offer help, please contact me!\n\nOn Unix, Linux:\n```\npoetry build\npoetry install\n```\n\nThis will install Pseudo as `pseudo`.\n\n# Chapters\n\nThis project is also an attempt to write a programming book in a new style. Each chapter of this book is written as a pull request.\n\nLinks to each chapter\'s pull request can be found in [CONTENTS.md](/CONTENTS.md).\n',
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
