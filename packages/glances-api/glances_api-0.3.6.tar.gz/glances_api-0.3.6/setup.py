# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glances_api']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23,<1']

setup_kwargs = {
    'name': 'glances-api',
    'version': '0.3.6',
    'description': 'Python API for interacting with Glances',
    'long_description': 'python-glances-api\n==================\n\nA Python client for interacting with `Glances <https://nicolargo.github.io/glances/>`_.\n\nThis module is not official, developed, supported or endorsed by Glances.\n\nInstallation\n------------\n\nThe module is available from the `Python Package Index <https://pypi.python.org/pypi>`_.\n\n.. code:: bash\n\n    $ pip3 install glances_api\n\nOr on a Fedora-based system or on a CentOS/RHEL machine with has EPEL enabled.\n\n.. code:: bash\n\n    $ sudo dnf -y install python3-glances-api\n\n\nFor Nix or NixOS is `pre-packed module <https://search.nixos.org/packages?channel=unstable&query=glances-api>`_\navailable. The lastest release is usually present in the ``unstable`` channel.\n\n.. code:: bash\n\n    $ nix-env -iA nixos.python3Packages.glances-api\n\nUsage\n-----\n\nThe file ``example.py`` contains an example about how to use this module.\n\nLicense\n-------\n\n``python-glances-api`` is licensed under MIT, for more details check LICENSE.\n',
    'author': 'Fabian Affolter',
    'author_email': 'fabian@affolter-engineering.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/home-assistant-ecosystem/python-glances-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
