# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omicidx',
 'omicidx.geo',
 'omicidx.ontologies',
 'omicidx.scripts',
 'omicidx.sra']

package_data = \
{'': ['*']}

install_requires = \
['Click',
 'aiohttp>=3.6.2,<4.0.0',
 'biopython==1.75',
 'httpx>=0.22.0,<0.23.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic',
 'requests>=2.22,<3.0',
 'sd_cloud_utils',
 'sphinx_click>=2.3.2,<3.0.0',
 'tenacity>=8.0.1,<9.0.0',
 'trio>=0.19.0,<0.20.0']

entry_points = \
{'console_scripts': ['omicidx_tool = omicidx.scripts.geo:cli']}

setup_kwargs = {
    'name': 'omicidx',
    'version': '1.2.4',
    'description': 'The OmicIDX project collects, reprocesses, and then republishes metadata from multiple public genomics repositories. Included are the NCBI SRA, Biosample, and GEO databases. Publication is via the cloud data warehouse platform Bigquery, a set of performant search and retrieval APIs, and a set of json-format files for easy incorporation into other projects.',
    'long_description': '',
    'author': 'Sean Davis',
    'author_email': 'seandavi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/omicidx/omicidx-parsers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
