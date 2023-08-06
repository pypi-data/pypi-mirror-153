# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miv',
 'miv.io',
 'miv.signal',
 'miv.signal.filter',
 'miv.signal.spike',
 'miv.statistics',
 'miv.visualization']

package_data = \
{'': ['*']}

install_requires = \
['PyWavelets>=1.3.0,<2.0.0',
 'elephant>=0.11.1,<0.12.0',
 'matplotlib>=3.5.2,<4.0.0',
 'neo>=0.10.2,<0.11.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'quantities>=0.13.0,<0.14.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'scipy>=1.8.1,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'tqdm>=4.64.0,<5.0.0',
 'viziphant>=0.2.0,<0.3.0']

extras_require = \
{'docs': ['Sphinx[docs]>=4.5.0,<5.0.0',
          'sphinx-rtd-theme[docs]>=1.0.0,<2.0.0',
          'sphinx-book-theme[docs]>=0.3.2,<0.4.0',
          'readthedocs-sphinx-search[docs]>=0.1.2,<0.2.0',
          'sphinx-autodoc-typehints[docs]>=1.18.1,<2.0.0',
          'myst-parser[docs]>=0.17.2,<0.18.0',
          'numpydoc[docs]>=1.3.1,<2.0.0',
          'sphinx-togglebutton[docs]>=0.3.1,<0.4.0',
          'sphinx-copybutton[docs]>=0.5.0,<0.6.0',
          'myst-nb[docs]>=0.15.0,<0.16.0']}

setup_kwargs = {
    'name': 'miv-os',
    'version': '0.0.6',
    'description': 'Python software for analysis and computing framework used in MiV project.',
    'long_description': "<div align='center'>\n<h1> MiV-OS: Spike Analysis and Computing Framework </h1>\n\n[![License][badge-LICENSE]][link-LICENSE]\n[![Release pypi][badge-pypi]][link-pypi]\n[![Build Status][badge-CI]][link-CI]\n[![Documentation Status][badge-docs-status]][link-docs-status]\n[![Downloads][badge-pepy-download-count]][link-pepy-download-count]\n[![codecov][badge-codecov]][link-codecov]\n\n[//]: # (Remove this line for the first release)\n_The package is under pre-alpha development. First Alpha release target mid-May 2022._\n\n</div>\n\n---\n\nPython analysis and computing framework developed for Mind-in-Vitro(MiV) project.\n\n## Installation\n[![PyPI version][badge-pypi]][link-pypi]\n\nMiV-OS is compatible with Python 3.8+. The easiest way to install is using python installation package (PIP)\n\n~~~bash\n$ pip install MiV-OS\n~~~\n\n## Documentation\n[![Documentation Status][badge-docs-status]][link-docs-status]\n\nDocumentation of the package is available [here][link-docs-status]\n\n## Contribution\n\nIf you would like to participate, please read our [contribution guideline](CONTRIBUTING.md)\n\nThe development of MiV-OS is lead by the [Gazzola Lab][link-lab-website] at the University of Illinois at Urbana-Champaign.\n\n## List of publications and submissions\n\n## Citation\n\n```\n@misc{MiV-OS,\n  author = {Gazzola Lab},\n  title = {MiV-OS: Analysis and Computation Framework on MiV System and Simulator},\n  year = {2022},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/GazzolaLab/MiV-OS}},\n}\n```\n\nWe ask that any publications which use MiV-OS package to cite the following papers:\n\n```\n```\n\n## Developers ✨\n_Names arranged alphabetically_\n- Arman Tekinalp\n- Andrew Dou\n- Austin Ellis-Mohr\n- [Frithjof Gressmann](https://github.com/frthjf)\n- Gaurav Upadhyay\n- [Seung Hyun Kim](https://github.com/skim0119)\n\n[//]: # (Collection of URLs.)\n\n[link-lab-website]: http://mattia-lab.com/\n[link-docs-status]: https://miv-os.readthedocs.io/en/latest/?badge=latest\n[link-CI]: https://github.com/GazzolaLab/MiV-OS/actions\n[link-LICENSE]: https://github.com/GazzolaLab/MiV-OS/blob/main/LICENSE\n[link-pypi]: https://badge.fury.io/py/MiV-OS\n[link-pepy-download-count]: https://pepy.tech/project/MiV-OS\n[link-codecov]: https://codecov.io/gh/GazzolaLab/MiV-OS\n\n[//]: # (Collection of Badges)\n\n[badge-docs-status]: https://readthedocs.org/projects/miv-os/badge/?version=latest\n[badge-CI]: https://github.com/GazzolaLab/MiV-OS/workflows/CI/badge.svg\n[badge-LICENSE]: https://img.shields.io/apm/l/atomic-design-ui.svg?style=flat\n[badge-pypi]: https://badge.fury.io/py/MiV-OS.svg\n[badge-pepy-download-count]: https://pepy.tech/badge/MiV-OS\n[badge-codecov]: https://codecov.io/gh/GazzolaLab/MiV-OS/branch/main/graph/badge.svg?token=OM5LYWF5KP\n",
    'author': 'GazzolaLab',
    'author_email': 'skim449@illinois.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mindinvitro.illinois.edu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
