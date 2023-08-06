# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wikimedia_cli',
 'wikimedia_cli.commands',
 'wikimedia_cli.commands.wikipedia',
 'wikimedia_cli.commands.wiktionary']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27,<3.0']

extras_require = \
{'docs': ['Sphinx>=4.4', 'furo>=2022', 'myst-parser>=0.17.0']}

entry_points = \
{'console_scripts': ['wiki = wikimedia_cli.cli:main']}

setup_kwargs = {
    'name': 'wikimedia-cli',
    'version': '0.1.0',
    'description': 'Minimally dependent CLI for Wikimedia projects',
    'long_description': '# wikimedia-cli\n\n[![Documentation status](https://readthedocs.org/projects/wikimedia-cli/badge/?version=latest)](https://wikimedia-cli.readthedocs.io/en/latest/?badge=latest)\n[![Build status](https://img.shields.io/github/workflow/status/g3ner1c/wikimedia-cli/Test%20package)](https://www.codefactor.io/repository/github/g3ner1c/wikimedia-cli)\n[![CodeFactor](https://www.codefactor.io/repository/github/g3ner1c/wikimedia-cli/badge)](https://www.codefactor.io/repository/github/g3ner1c/wikimedia-cli)\n[![Open issues](https://img.shields.io/github/issues/g3ner1c/wikimedia-cli)](https://github.com/g3ner1c/wikimedia-cli/issues)\n[![Open PRs](https://img.shields.io/github/issues-pr/g3ner1c/wikimedia-cli)](https://github.com/g3ner1c/wikimedia-cli/pulls)\n[![Repo stars](https://img.shields.io/github/stars/g3ner1c/wikimedia-cli?style=social)](https://github.com/g3ner1c/wikimedia-cli/stargazers)\n\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/wikimedia-cli)](https://pypi.org/project/tetris/)\n[![PyPI version](https://img.shields.io/pypi/v/wikimedia-cli)](https://pypi.org/project/tetris/)\n\nA minimally dependent Wikimedia CLI written in Python\n\n[In early developement](#ideas-and-todo)\n\n## Currently supported Wikimedia projects\n\n- [Wikipedia](https://www.wikipedia.org/) - The free encyclopedia\n- [Wiktionary](https://www.wiktionary.org/) - The free dictionary\n\n## Documentation\n\nDocumentation is available on **[ReadTheDocs](https://wikimedia-cli.readthedocs.io/en/latest/)**\n\n- [Installation](https://wikimedia-cli.readthedocs.io/en/latest/installation.html)\n\nTo build the documentation locally, make sure you are in the root project directory and run:\n\n```bash\npip install Sphinx furo myst-parser\ncd docs\nmake html\n```\n\nDocumentation will be built in the `docs/_build/html` directory\n\n## Ideas and TODO\n\n- Wiktionary and Wikipedia article formatting (e.g. bold, italics, colors, links, images, etc.)\n- Wiktionary Improvements\n  - Summary\n  - Breakdown of phrase properties (e.g. definition, usage, synonyms, entomology, etc.)\n- Other wikimedia wikis\n  - Wikimedia commons\n  - Wikidata\n  - Wikinews\n  - Wikibooks\n- Revision history\n- Main page and ITN/Ongoing\n- Packaging\n  - AUR\n',
    'author': 'Sky "g3ner1c" H.',
    'author_email': 'g3ner1c-sky@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/g3ner1c/wikimedia-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
