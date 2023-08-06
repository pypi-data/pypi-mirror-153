# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['armasec', 'armasec.schemas']

package_data = \
{'': ['*']}

install_requires = \
['auto-name-enum>=2,<3',
 'fastapi>=0.68.0,<0.69.0',
 'httpx>=0,<1',
 'py-buzz>=3.1.0,<4.0.0',
 'pytest>=6.2.5,<7.0.0',
 'python-jose[cryptography]>=3.2.0,<4.0.0',
 'respx>=0.17.1,<0.18.0',
 'snick>=1.3.0,<2.0.0']

entry_points = \
{'pytest11': ['pytest_armasec = armasec.pytest_extension']}

setup_kwargs = {
    'name': 'armasec',
    'version': '0.10.2',
    'description': 'Injectable FastAPI auth via OIDC',
    'long_description': '.. image:: https://img.shields.io/github/workflow/status/omnivector-solutions/armasec/test_on_push/main?label=main-build&logo=github&style=plastic\n   :alt: main build\n.. image:: https://img.shields.io/github/issues/omnivector-solutions/armasec?label=issues&logo=github&style=plastic\n   :alt: github issues\n.. image:: https://img.shields.io/github/issues-pr/omnivector-solutions/armasec?label=pull-requests&logo=github&style=plastic\n   :alt: pull requests\n.. image:: https://img.shields.io/github/contributors/omnivector-solutions/armasec?logo=github&style=plastic\n   :alt: github contributors\n\n.. image:: https://img.shields.io/pypi/pyversions/armasec?label=python-versions&logo=python&style=plastic\n   :alt: python versions\n.. image:: https://img.shields.io/pypi/v/armasec?label=pypi-version&logo=python&style=plastic\n   :alt: pypi version\n\n.. image:: https://img.shields.io/pypi/l/armasec?style=plastic\n   :alt: license\n\n.. figure:: https://github.com/omnivector-solutions/armasec/blob/main/docs-source/_static/logo.png?raw=true\n   :alt: Logo\n   :align: center\n   :width: 80px\n\n   An Omnivector Solutions initiative\n\n=========\n Armasec\n=========\n\nAdding a security layer on top of your API can be difficult, especially when working with an OIDC\nplatform. It\'s hard enough to get your OIDC provider configured correctly. Armasec aims to take the\npain out of securing your APIs routes.\n\nArmasec is an opinionated library that attemtps to use the most obvious and commonly used workflows\nwhen working with OIDC and making configuration as simple as possible.\n\nWhen using the\n`Armasec <https://github.com/omnivector-solutions/armasec/blob/main/armasec/armasec.py>`_ helper\nclass, you only need two configuration settings to get going:\n\n#. Domain: the domain of your OIDC provider\n#. Audience: An optional setting that restricts tokens to those intended for your API.\n\nThat\'s it! Once you have those settings dialed in, you can just worry about checking the permissions\nscopes of your endpoints\n\n\nDocumentation\n=============\n\nDocumentation is hosted hosted on ``github.io`` at\n`the Armasec homepage <https://omnivector-solutions.github.io/armasec/>`_\n\n\nQuickstart\n==========\n\n#. Install ``armasec`` and ``uvicorn``:\n\n   $ pip install armasec\n\n\n#. Minimal Example (example.py)\n\n.. code-block:: python\n\n   import os\n\n   from armasec import Armasec\n   from fastapi import FastAPI, Depends\n\n\n   app = FastAPI()\n   armasec = Armasec(\n       os.environ.get("ARMASEC_DOMAIN"),\n       audience=os.environ.get("ARMASEC_AUDIENCE"),\n   )\n\n   @app.get("/stuff", dependencies=[Depends(armasec.lockdown("read:stuff"))])\n   async def check_access():\n       return dict(message="Successfully authenticated!")\n\n#. Run the app\n\n   $ uvicorn --host 0.0.0.0 example:app\n\n\nLicense\n=======\n\nDistributed under the MIT License. See `LICENSE` for more information.\n',
    'author': 'Omnivector Solutions',
    'author_email': 'info@omnivector.solutions',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/omnivector-solutions/armasec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
