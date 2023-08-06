# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virustotal_tddschn']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['vtpy = virustotal_tddschn.virustotal_sum_search:main']}

setup_kwargs = {
    'name': 'virustotal-tddschn',
    'version': '0.1.6',
    'description': 'VirusTotal Utility Scripts',
    'long_description': '',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tddschn/virustotal-tddschn',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
