# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['joseki', 'joseki.data', 'joseki.data.afgl_1986', 'joseki.data.rfm']

package_data = \
{'': ['*']}

install_requires = \
['Pint>=0.17',
 'click>=7.0',
 'molmass>=2021.6.18',
 'netCDF4>=1.5.7',
 'numpy>=1.22.1',
 'pandas>=1.2.4',
 'requests>=2.25.1',
 'scipy>=1.6.3',
 'xarray>=0.18.2']

entry_points = \
{'console_scripts': ['joseki = joseki.__main__:main']}

setup_kwargs = {
    'name': 'joseki',
    'version': '1.3.0',
    'description': 'Joseki',
    'long_description': "Joseki\n======\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/joseki.svg\n   :target: https://pypi.org/project/joseki/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/joseki\n   :target: https://pypi.org/project/joseki\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/joseki\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/joseki/latest.svg?label=Read%20the%20Docs\n   :target: https://joseki.readthedocs.io/\n   :alt: Read the documentation at https://joseki.readthedocs.io/\n.. |Tests| image:: https://github.com/nollety/joseki/workflows/Tests/badge.svg\n   :target: https://github.com/nollety/joseki/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/nollety/joseki/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/nollety/joseki\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* *AFGL Atmospheric Constituent Profiles (0-120 km)* data sets in\n  `csv <https://en.wikipedia.org/wiki/Comma-separated_values>`_ and\n  `netCDF <https://www.unidata.ucar.edu/software/netcdf/>`_ formats.\n* Atmospheric profiles from `RFM <http://eodg.atm.ox.ac.uk/RFM/>`_\n* Atmospheric profile interpolation on altitude.\n* Projection of the nodes-based profile on the corresponding centers-based altitude mesh.\n* Command-line interface.\n* Python API.\n\n\nRequirements\n------------\n\n* Python 3.8+\n\n\nInstallation\n------------\n\nYou can install *Joseki* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install joseki\n\n\nPython API\n----------\n\nPlease see the `User Guide`_ for basic use.\nFor more details, refer to the `API Reference`_.\n\n\nCommand-line interface\n----------------------\n\nPlease see the `Command-line Reference`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*Joseki* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s\n`Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/nollety/joseki/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Command-line Reference: https://joseki.readthedocs.io/en/latest/cli.html\n.. _User Guide: https://joseki.readthedocs.io/en/latest/user_guide.html\n.. _API Reference: https://joseki.readthedocs.io/en/latest/reference.html\n",
    'author': 'Yvan Nollet',
    'author_email': 'yvan.nollet@rayference.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nollety/joseki',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
