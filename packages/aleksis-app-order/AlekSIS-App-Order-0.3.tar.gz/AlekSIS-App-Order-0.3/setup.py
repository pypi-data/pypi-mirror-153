# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aleksis',
 'aleksis.apps.order',
 'aleksis.apps.order.migrations',
 'aleksis.apps.order.templatetags',
 'aleksis.apps.order.util']

package_data = \
{'': ['*'],
 'aleksis.apps.order': ['locale/*',
                        'locale/ar/LC_MESSAGES/*',
                        'locale/de_DE/LC_MESSAGES/*',
                        'locale/fr/LC_MESSAGES/*',
                        'locale/la/LC_MESSAGES/*',
                        'locale/nb_NO/LC_MESSAGES/*',
                        'locale/tr_TR/LC_MESSAGES/*',
                        'static/*',
                        'templates/order/*',
                        'templates/templated_email/*']}

install_requires = \
['aleksis-core>=2.0,<3.0',
 'blabel>=0.1.4,<0.2.0',
 'html2text>=2020.1.16,<2021.0.0']

entry_points = \
{'aleksis.app': ['order = aleksis.apps.order.apps:DefaultConfig']}

setup_kwargs = {
    'name': 'aleksis-app-order',
    'version': '0.3',
    'description': 'AlekSIS (School Information System)\u200a—\u200aApp Order (Manage orders)',
    'long_description': 'AlekSIS\u200a—\u200aUnofficial App Order (Manage orders)\n==============================================\n\nAlekSIS\n-------\n\nThis is an **unofficial** application for use with the `AlekSIS`_ platform.\n\nFeatures\n--------\n\nThis application can be used to create order forms and manage orders e. g. for school clothes.\n\nLicence\n-------\n\n::\n\n  Copyright © 2020, 2021 Jonathan Weth <dev@jonathanweth.de>\n  Copyright © 2021 Hangzhi Yu <yuha@katharineum.de>\n\n  Licenced under the EUPL, version 1.2 or later\n\nPlease see the LICENCE.rst file accompanying this distribution for the\nfull licence text or on the `European Union Public Licence`_ website\nhttps://joinup.ec.europa.eu/collection/eupl/guidelines-users-and-developers\n(including all other official language versions).\n\n.. _AlekSIS: https://edugit.org/AlekSIS/AlekSIS\n.. _European Union Public Licence: https://eupl.eu/\n',
    'author': 'Jonathan Weth',
    'author_email': 'dev@jonathanweth.de',
    'maintainer': 'Jonathan Weth',
    'maintainer_email': 'dev@jonathanweth.de',
    'url': 'https://edugit.org/hansegucker/AlekSIS-App-Order',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
