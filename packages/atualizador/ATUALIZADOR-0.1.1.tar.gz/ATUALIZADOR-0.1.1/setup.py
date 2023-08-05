# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atualizador',
 'atualizador.SRC-BOVESPA',
 'atualizador.SRC-CORRELACAO',
 'atualizador.SRC-CRYPTO',
 'atualizador.SRC-DERIBIT',
 'atualizador.SRC-ESTUDOS',
 'atualizador.SRC-TEDESCO',
 'atualizador.funcoes_mod',
 'atualizador.tests',
 'atualizador.tests.Ajustes']

package_data = \
{'': ['*'], 'atualizador': ['docs/*']}

install_requires = \
['numpy>=1.22.4,<2.0.0', 'pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'atualizador',
    'version': '0.1.1',
    'description': 'Utilizado para atualizar dados de interesse da DIAX_LAB',
    'long_description': None,
    'author': 'VitorKruel102',
    'author_email': 'vkruel.programador@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
