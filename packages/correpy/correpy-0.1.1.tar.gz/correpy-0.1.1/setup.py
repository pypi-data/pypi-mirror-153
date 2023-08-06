# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['correpy',
 'correpy.domain',
 'correpy.domain.entities',
 'correpy.parsers',
 'correpy.parsers.brokerage_notes',
 'correpy.parsers.brokerage_notes.b3_parser']

package_data = \
{'': ['*']}

install_requires = \
['PyMuPDF>=1.19.4,<2.0.0']

setup_kwargs = {
    'name': 'correpy',
    'version': '0.1.1',
    'description': 'CorrePy (Corretagem Python) é uma lib responsável por parsear notas de corretagem no padrão B3 (Sinacor) e retornar os dados no formato JSON.',
    'long_description': '[![thiagosalvatore](https://circleci.com/gh/thiagosalvatore/correpy.svg?style=shield)](https://app.circleci.com/pipelines/github/thiagosalvatore/correpy?branch=main&filter=all)\n[![PyPI version](https://badge.fury.io/py/correpy.svg)](https://badge.fury.io/py/correpy)\n# CorrePy\nCorrePy (Corretagem Python) é uma lib responsável por parsear notas de corretagem no padrão B3 (Sinacor) e retornar os\ndados em um formato estruturado para que você possa utilizar em suas aplicações.\n\n## Instalação\nEste projeto suporta qualquer versão do python >= 3.8\n\n`pip install correpy`\n\n## Como usar\nDepois de instalada, sua utilização é extremamente simples. Primeiramente vamos precisar abrir o PDF com a nota de corretagem.\nSe você estiver utilizando essa lib em uma API, você precisará transformar seu arquivo PDF em BytesIO.\n\n```python\nimport io\n\nwith open(\'path to your pdf file\', \'rb\') as f:\n    content = io.BytesIO(f.read())\n    content.seek(0)\n```\n\nO conteúdo da sua nota de corretagem estará na variável `content` e é ela quem iremos usar para inicializar a nossa lib.\nSe a sua nota de corretagem possuir senha, você precisará informar também, caso contrário o parser nâo irá funcionar.\n\n```python\nimport io\n\nfrom correpy.parsers.brokerage_notes.b3_parser.b3_parser import B3Parser\n\nwith open(\'path to your pdf file\', \'rb\') as f:\n    content = io.BytesIO(f.read())\n    content.seek(0)\n    \n    brokerage_notes = B3Parser(brokerage_note=content, password="password").parse_brokerage_note()\n```\n\n### Resultado\nDepois de efetuar o parser da sua nota de corretagem, `correpy` irá retornar uma lista no formato abaixo. Os valores de cada campo serão explicados em seguida.\n\n```python\n[\n    BrokerageNote(\n        reference_date=date(2022, 5, 2),\n        settlement_fee=Decimal("7.92"),\n        registration_fee=Decimal("0"),\n        term_fee=Decimal("0"),\n        ana_fee=Decimal("0"),\n        emoluments=Decimal("1.58"),\n        operational_fee=Decimal("0"),\n        execution=Decimal("0"),\n        custody_fee=Decimal("0"),\n        taxes=Decimal("0"),\n        others=Decimal("0"),\n        transactions=[\n            Transaction(\n                transaction_type=TransactionType.SELL,\n                amount=54,\n                unit_price=Decimal(\'24.99\'),\n                security=Security(\n                    name=\'BBSEGURIDADE ON NM\'\n                )\n            ),\n            Transaction(\n                transaction_type=TransactionType.BUY,\n                amount=200,\n                unit_price=Decimal(\'17.29\'),\n                security=Security(\n                    name=\'MOVIDA ON NM\'\n                )\n            )\n        ]\n    )\n]\n```\n\n### Descrição das entidades\nAbaixo você pode encontrar a descrição de cada um dos campos retornados. \n\n#### Brokerage Note\n\n| BrokerageNote    |                                     |\n|------------------|-------------------------------------|\n| reference_date   | Data do pregão                      |\n| settlement_fee   | Taxa de liquidação                  |\n| registration_fee | Taxa de registro                    |\n| term_fee         | Taxa de termo/opções                |\n| ana_fee          | Taxa A.N.A                          |\n| emoluments       | Emolumentos                         |\n| operational_fee  | Taxa Operacional                    |\n| execution        | Execução                            |\n| custody_fee      | Taxa de custódia                    |\n| taxes            | Impostos                            |\n| others           | Outros                              |\n| transactions     | Lista de [transações](#transaction) |\n\n#### Transaction\n\n| Transaction          |                                                            |\n|----------------------|------------------------------------------------------------|\n| transaction_type     | Enum com o tipo de transação (BUY - compra, SELL - venda)  |\n| amount               | Quantidade                                                 |\n| unit_price           | Valor unitário                                             |\n| security             | Objeto [Security](#security) representando um título       |\n| source_witheld_taxes | IRRF retido na fonte (0.005% sobre o valor total de venda) |\n\n#### Security\n| Security |                         |\n|----------|-------------------------|\n| name     | Especificação do título |\n\n\n## Como contribuir\nEstamos utilizando poetry para gerenciar o projeto e suas dependencias.\n\nEste projeto ainda está em evolução e qualquer PR é bem vindo. Algumas ferramentas estão sendo utilizadas para melhorar a qualidade do código:\n\n1. MyPy para checagem estática de tipos\n2. PyLint\n3. Black\n4. isort\n\nPara verificar se o seu código continua de acordo com os critérios definidos, basta rodar `./pipeline/lint.sh`.',
    'author': 'Thiago  Salvatore',
    'author_email': 'thiago.salvatore@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thiagosalvatore/correpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
