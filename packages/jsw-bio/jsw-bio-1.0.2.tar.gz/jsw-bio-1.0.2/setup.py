# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsw_bio', 'jsw_bio.base']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'jsw-nx>=1.0.92,<2.0.0',
 'nltk>=3.7,<4.0',
 'psutil>=5.9.0,<6.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'jsw-bio',
    'version': '1.0.2',
    'description': 'Jsw for biography.',
    'long_description': "# jsw-bio\n> Jsw for biography.\n\n## installation\n```shell\npip install jsw-bio -U\n```\n\n## usage\n```python\nimport jsw_bio as bio\n\n## common methods\n# get fasta/genbank url\nbio.url('7EU9_A', 'fasta')\nbio.url('7EU9_A', 'gb')\n```\n",
    'author': 'feizheng',
    'author_email': '1290657123@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://js.work',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
