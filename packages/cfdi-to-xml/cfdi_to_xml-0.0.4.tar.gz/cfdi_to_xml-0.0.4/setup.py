# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cfdi_to_xml', 'cfdi_to_xml.cfdv40']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.8.0,<5.0.0', 'requests>=2.27.1,<3.0.0', 'xsdata>=22.4,<23.0']

setup_kwargs = {
    'name': 'cfdi-to-xml',
    'version': '0.0.4',
    'description': 'Library to create XML fiel from CFDI representation.',
    'long_description': '# CFDI to XML\n\nLibrearía para crear una representación XML de un CFDI a partir de un modelo "simple"\n',
    'author': 'Moises Navarro',
    'author_email': 'moisalejandro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
