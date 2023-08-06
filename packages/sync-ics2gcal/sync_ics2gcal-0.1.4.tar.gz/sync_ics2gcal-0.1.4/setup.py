# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sync_ics2gcal']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0',
 'fire==0.4.0',
 'google-api-python-client==2.49.0',
 'google-auth==2.6.6',
 'icalendar==4.0.9',
 'pytz==2022.1']

entry_points = \
{'console_scripts': ['manage-ics2gcal = sync_ics2gcal.manage_calendars:main',
                     'sync-ics2gcal = sync_ics2gcal.sync_calendar:main']}

setup_kwargs = {
    'name': 'sync-ics2gcal',
    'version': '0.1.4',
    'description': 'Sync ics file with Google calendar',
    'long_description': '# sync_ics2gcal\n\n[![PyPI version](https://badge.fury.io/py/sync-ics2gcal.svg)](https://badge.fury.io/py/sync-ics2gcal)\n![Python package status](https://github.com/b4tman/sync_ics2gcal/workflows/Python%20package/badge.svg)\n\nPython scripts for sync .ics file with Google calendar\n\n## Installation\n\nTo install from [PyPI](https://pypi.org/project/sync-ics2gcal/) with [pip](https://pypi.python.org/pypi/pip), run:\n\n```sh\npip install sync-ics2gcal\n```\n\nOr download source code and install using poetry:\n\n```sh\n# install poetry\npip install poetry\n# install project and deps to virtualenv\npoetry install\n# run\npoetry run sync-ics2gcal\n```\n\n## Configuration\n\n### Create application in Google API Console\n\n1. Create a new project: [console.developers.google.com/project](https://console.developers.google.com/project)\n2. Choose the new project from the top right project dropdown (only if another project is selected)\n3. In the project Dashboard, choose "Library"\n4. Find and Enable "Google Calendar API"\n5. In the project Dashboard, choose "Credentials"\n6. In the "Service Accounts" group, click to "Manage service accounts"\n7. Click "Create service account"\n8. Choose service account name and ID\n9. Go back to "Service Accounts" group in "Credentials"\n10. Edit service account and click "Create key", choose JSON and download key file.\n\n### Create working directory\n\nFor example: `/home/user/myfolder`.\n\n1. Save service account key in file `service-account.json`.\n2. Download [sample config](https://github.com/b4tman/sync_ics2gcal/blob/develop/sample-config.yml) and save to file `config.yml`. For example:\n\n```sh\nwget https://raw.githubusercontent.com/b4tman/sync_ics2gcal/develop/sample-config.yml -O config.yml\n```\n\n3. *(Optional)* Place source `.ics` file, `my-calendar.ics` for example.\n\n### Configuration parameters\n\n* `start_from` - start date:\n  * full format datetime, `2018-04-03T13:23:25.000001Z` for example\n  * or just `now`\n* *(Optional)* `service_account` - service account filename, remove it from config to use [default credentials](https://developers.google.com/identity/protocols/application-default-credentials)\n* *(Optional)* `logging` - [config](https://docs.python.org/3.8/library/logging.config.html#dictionary-schema-details) to setup logging\n* `google_id` - target google calendar id, `my-calendar@group.calendar.google.com` for example\n* `source` - source `.ics` filename, `my-calendar.ics` for example\n\n## Usage\n\n### Manage calendars\n\n```sh\nmanage-ics2gcal GROUP | COMMAND\n```\n\n**GROUPS**:\n\n* **property** - get/set properties (see [CalendarList resource](https://developers.google.com/calendar/v3/reference/calendarList#resource)), subcommands:\n  - **get** - get calendar property\n  - **set** - set calendar property\n\n**COMMANDS**:\n\n* **list** - list calendars\n* **create** - create calendar\n* **add_owner** - add owner to calendar\n* **remove** - remove calendar\n* **rename** - rename calendar\n\n\nUse **-h** for more info.\n\n### Sync calendar\n\njust type:\n\n```sh\nsync-ics2gcal\n```\n\n## How it works\n\n![How it works](how-it-works.png)\n',
    'author': 'Dmitry Belyaev',
    'author_email': 'b4tm4n@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/b4tman/sync_ics2gcal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
