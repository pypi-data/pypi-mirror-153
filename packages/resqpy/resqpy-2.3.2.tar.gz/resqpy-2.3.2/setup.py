# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resqpy',
 'resqpy.derived_model',
 'resqpy.fault',
 'resqpy.grid',
 'resqpy.lines',
 'resqpy.model',
 'resqpy.multiprocessing',
 'resqpy.multiprocessing.wrappers',
 'resqpy.olio',
 'resqpy.olio.data',
 'resqpy.organize',
 'resqpy.property',
 'resqpy.rq_import',
 'resqpy.strata',
 'resqpy.surface',
 'resqpy.time_series',
 'resqpy.unstructured',
 'resqpy.well']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=3.2,<4.0',
 'joblib>=1.1.0,<2.0.0',
 'lasio>=0.29,<0.30',
 'lxml>=4.6,<5.0',
 'numba>=0.52,<1.0',
 'numpy>=1.19,<2.0',
 'pandas>=1.1,<2.0',
 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'resqpy',
    'version': '2.3.2',
    'description': 'Python API for working with RESQML models',
    'long_description': '# resqpy: Python API for working with RESQML models\n\n[![License](https://img.shields.io/pypi/l/resqpy)](https://github.com/bp/resqpy/blob/master/LICENSE)\n[![Documentation Status](https://readthedocs.org/projects/resqpy/badge/?version=latest)](https://resqpy.readthedocs.io/en/latest/?badge=latest)\n[![Python CI](https://github.com/bp/resqpy/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/bp/resqpy/actions/workflows/ci-tests.yml)\n![Python version](https://img.shields.io/pypi/pyversions/resqpy)\n[![PyPI](https://img.shields.io/pypi/v/resqpy)](https://badge.fury.io/py/resqpy)\n![Status](https://img.shields.io/pypi/status/resqpy)\n[![codecov](https://codecov.io/gh/bp/resqpy/branch/master/graph/badge.svg)](https://codecov.io/gh/bp/resqpy)\n\n## Introduction\n\n**resqpy** is a pure Python package which provides a programming interface (API) for\nreading, writing, and modifying reservoir models in the RESQML format. It gives\nyou the ability to work with reservoir models programmatically, without having\nto know the details of the RESQML standard.\n\nThe package is written and maintained by bp, and is made available under the MIT\nlicense as a contribution to the open-source community.\n\n**resqpy** was created by Andy Beer. For enquires about resqpy, please contact\nNathan Lane (Nathan.Lane@bp.com)\n\n### Documentation\n\nSee the complete package documentation on\n[readthedocs](https://resqpy.readthedocs.io/).\n\n### About RESQML\n\nRESQML™ is an industry initiative to provide open, non-proprietary data exchange\nstandards for reservoir characterization, earth and reservoir models. It is\ngoverned by the [Energistics\nconsortium](https://www.energistics.org/portfolio/resqml-data-standards/).\n\nResqpy provides specialized classes for a subset of the RESQML high level object\nclasses, as described in the docs. Furthermore, not all variations of these\nobject types are supported; for example, radial IJK grids are not yet catered\nfor, although the RESQML standard does allow for such grids.\n\nIt is envisaged that the code base will be expanded to include other classes of\nobject and more fully cover the options permitted by the RESQML standard.\n\nModification functionality at the moment focuses on changes to grid geometry.\n\n## Installation\n\nResqpy can be installed with pip:\n\n```bash\npip install resqpy\n```\n\nAlternatively, to install your working copy of the code in "editable" mode:\n\n```bash\npip install -e /path/to/repo/\n```\n\n## Contributing\n\nContributions of all forms are welcome and encouraged! Please feel free to open\nissues on the GitHub issue tracker, or submit Pull Requests. Instructions with how to set up your own development environment can be found at [Development environment setup](https://github.com/bp/resqpy/blob/master/docs/CONTRIBUTING.rst#development-environment-setup). Please read the\n[Contributing Guide](docs/CONTRIBUTING.rst) before submitting patches.\n',
    'author': 'BP',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bp/resqpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
