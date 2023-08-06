# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mirror_up', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=2.3.1,<3.0.0',
 'format-byte>=1.1.1,<2.0.0',
 'httpx==0.23.0',
 'multivolumefile>=0.2.3,<0.3.0',
 'notify-py>=0.3.3,<0.4.0',
 'pyperclip>=1.8.2,<2.0.0',
 'python-dotenv==0.20.0',
 'trio>=0.20.0,<0.21.0',
 'typer>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'mirror-up',
    'version': '0.1.6',
    'description': 'Upload files to online mirroring services.',
    'long_description': '=========\nmirror-up\n=========\n\n.. image:: https://readthedocs.org/projects/mirror-up/badge/?version=latest\n        :target: https://mirror-up.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\nUpload your files to MirrorAce\n\n\nQuickstart\n--------------\n\nInstall the package from PyPi\n\n.. code-block:: console\n\n        $ pip install mirror-up\n\nCreate an account at MirrorAce and set your environment variables\n\n.. code-block:: console\n\n        MirAce_K=     # MirrorAce API key\n        MirAce_T=   # MirrorAce API Token\n        ZIP_SAVE=    # Path where to store temp files\n\nUpload the file/folder at a given path to MirrorAce\n\n.. code-block:: console\n\n        $ python -m mirror_up mirror_ace upload PATH...\n\nUpload all files inside given folder as separate uploads\n\n.. code-block:: console\n\n        $ python -m mirror_up mirror_ace folder PATH...\n\n* Free software: MIT\n* Documentation: https://mirror-up.readthedocs.io.\n\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Mycsina',
    'author_email': 'mycsina@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mycsina/mirror_up',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
