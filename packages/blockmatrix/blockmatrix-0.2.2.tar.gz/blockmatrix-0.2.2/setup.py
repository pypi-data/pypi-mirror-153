# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blockmatrix']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0', 'seaborn>=0.11.2,<0.12.0', 'vg>=2.0.0,<3.0.0']

extras_require = \
{'channels': ['mne>=0.24.1,<0.25.0'], 'solver': ['toeplitz>=0.3.2,<0.4.0']}

setup_kwargs = {
    'name': 'blockmatrix',
    'version': '0.2.2',
    'description': 'Utilities to handle blockmatrices, especially covariance matrices.',
    'long_description': '# blockmatrix\n\nA python package to provide easier working with block-structured matrices. Currently, this\ncode mostly serves my purposes, i.e., manipulating block-structured covariance matrices\nand applying high-dimensional estimation techniques to them.\n\nThis package is also available on PyPi.\n\n## Usage\n\nAs of now unfortunately only the code and the docstrings are available as documentation.\n\nRunning the `examples/main_spatiotemporal_manipulations.py` showcases some of the\nfunctionality and visualizations.\n\n## Todos\n\n- [ ] Documentation\n- [ ] Testing\n- [x] Implementation of sklearn style covariance estimators\n  - Moved to ToeplitzLDA package\n- [x] Abstract mne channels away\n  - Using optional mne dependency\n- [x] Reduce unnecessary dependencies\n  - `toeplitz` is now optional\n',
    'author': 'Jan Sosulski',
    'author_email': 'mail@jan-sosulski.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jsosulski/blockmatrix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
