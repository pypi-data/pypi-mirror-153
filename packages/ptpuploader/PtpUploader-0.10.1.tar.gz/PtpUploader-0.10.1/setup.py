# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['PtpUploader',
 'PtpUploader.ImageHost',
 'PtpUploader.InformationSource',
 'PtpUploader.Job',
 'PtpUploader.Source',
 'PtpUploader.Tool',
 'PtpUploader.web',
 'PtpUploader.web.management.commands',
 'PtpUploader.web.migrations']

package_data = \
{'': ['*'],
 'PtpUploader.web': ['static/*',
                     'static/script/*',
                     'static/skin-win8/*',
                     'static/source_icon/*',
                     'templates/*']}

install_requires = \
['Django>=3.2.8,<4.0.0',
 'Unidecode>=1.3.2,<2.0.0',
 'Werkzeug>=2.0.2,<3.0.0',
 'cinemagoer>=2022.1.26,<2023.0.0',
 'dynaconf>=3.1.7,<4.0.0',
 'guessit>=3.3.1,<4.0.0',
 'pyrosimple>=1.1.0,<2.0.0',
 'rarfile>=4.0,<5.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['PtpUploader = PtpUploader.manage:run',
                     'ReleaseInfoMaker = PtpUploader.ReleaseInfoMaker:run']}

setup_kwargs = {
    'name': 'ptpuploader',
    'version': '0.10.1',
    'description': 'A small uploader for a mildly popular movie site',
    'long_description': None,
    'author': 'kannibalox',
    'author_email': 'kannibalox@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kannibalox/PtpUploader',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.7,<4.0',
}


setup(**setup_kwargs)
