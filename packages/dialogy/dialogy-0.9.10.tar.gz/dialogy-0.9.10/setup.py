# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dialogy',
 'dialogy.base',
 'dialogy.base.entity_extractor',
 'dialogy.base.input',
 'dialogy.base.output',
 'dialogy.base.plugin',
 'dialogy.cli',
 'dialogy.constants',
 'dialogy.plugins',
 'dialogy.plugins.text',
 'dialogy.plugins.text.calibration',
 'dialogy.plugins.text.canonicalization',
 'dialogy.plugins.text.classification',
 'dialogy.plugins.text.combine_date_time',
 'dialogy.plugins.text.duckling_plugin',
 'dialogy.plugins.text.lb_plugin',
 'dialogy.plugins.text.list_entity_plugin',
 'dialogy.plugins.text.list_search_plugin',
 'dialogy.plugins.text.merge_asr_output',
 'dialogy.plugins.text.slot_filler',
 'dialogy.plugins.text.voting',
 'dialogy.types',
 'dialogy.types.entity',
 'dialogy.types.entity.amount_of_money',
 'dialogy.types.entity.base_entity',
 'dialogy.types.entity.credit_card_number',
 'dialogy.types.entity.deserialize',
 'dialogy.types.entity.duration',
 'dialogy.types.entity.keyword',
 'dialogy.types.entity.numerical',
 'dialogy.types.entity.people',
 'dialogy.types.entity.time',
 'dialogy.types.entity.time_interval',
 'dialogy.types.intent',
 'dialogy.types.plugin',
 'dialogy.types.signal',
 'dialogy.types.slots',
 'dialogy.types.utterances',
 'dialogy.utils',
 'dialogy.workflow']

package_data = \
{'': ['*']}

install_requires = \
['MarkupSafe==2.0.1',
 'attrs>=20.3.0,<21.0.0',
 'copier>=5.1.0,<6.0.0',
 'jiwer>=2.2.0,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.3.2,<2.0.0',
 'pydash>=4.9.3,<5.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2020.4,<2021.0',
 'requests>=2.25.1,<3.0.0',
 'scipy>=1.7.1,<2.0.0',
 'sklearn>=0.0,<0.1',
 'stanza>=1.3.0,<2.0.0',
 'thefuzz>=0.19.0,<0.20.0',
 'tqdm>=4.62.2,<5.0.0',
 'types-pytz>=2021.3.5,<2022.0.0',
 'types-requests>=2.27.11,<3.0.0',
 'types-setuptools>=57.4.10,<58.0.0',
 'xgboost>=1.5.2,<2.0.0']

entry_points = \
{'console_scripts': ['dialogy = dialogy.cli:main']}

setup_kwargs = {
    'name': 'dialogy',
    'version': '0.9.10',
    'description': 'Dialogy is a library for building and managing SLU applications.',
    'long_description': None,
    'author': 'Amresh Venugopal',
    'author_email': 'amresh.venugopal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skit-ai/dialogy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
