# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mypyliextester']

package_data = \
{'': ['*']}

install_requires = \
['mypyliex==22.06.01-4']

entry_points = \
{'console_scripts': ['my_python_library_example_tester = '
                     'mypyliextester.main:main']}

setup_kwargs = {
    'name': 'mypyliextester',
    'version': '22.6.1.post6',
    'description': 'Project description',
    'long_description': '# MLE README file',
    'author': 'Tadeusz Miszczyk',
    'author_email': 'tadeusz.miszczyk@bshg.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/8tm/my_python_library_example_tester',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
