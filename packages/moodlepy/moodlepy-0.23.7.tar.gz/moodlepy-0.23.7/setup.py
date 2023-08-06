# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moodle',
 'moodle.auth',
 'moodle.auth.email',
 'moodle.base',
 'moodle.base.general',
 'moodle.base.preference',
 'moodle.block',
 'moodle.core',
 'moodle.core.auth',
 'moodle.core.backup',
 'moodle.core.badges',
 'moodle.core.block',
 'moodle.core.blog',
 'moodle.core.calendar',
 'moodle.core.cohort',
 'moodle.core.comment',
 'moodle.core.competency',
 'moodle.core.completion',
 'moodle.core.course',
 'moodle.core.customfield',
 'moodle.core.enrol',
 'moodle.core.files',
 'moodle.core.grades',
 'moodle.core.message',
 'moodle.core.notes',
 'moodle.core.user',
 'moodle.core.webservice',
 'moodle.enrol',
 'moodle.enrol.guest',
 'moodle.enrol.manual',
 'moodle.enrol.self',
 'moodle.mod',
 'moodle.mod.assign',
 'moodle.mod.book',
 'moodle.mod.chat',
 'moodle.mod.data',
 'moodle.mod.folder',
 'moodle.mod.forum',
 'moodle.mod.lesson',
 'moodle.mod.page',
 'moodle.mod.resource',
 'moodle.mod.url',
 'moodle.mod.workshop',
 'moodle.tool',
 'moodle.tool.mobile',
 'moodle.utils']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0', 'cattrs>=1.7.1,<2.0.0', 'requests>=2.24.0,<3.0.0']

extras_require = \
{'ujson': ['ujson==5.2.0']}

entry_points = \
{'console_scripts': ['moodle = moodle.__main__:main']}

setup_kwargs = {
    'name': 'moodlepy',
    'version': '0.23.7',
    'description': 'Python wrapper for moodle web service.',
    'long_description': "# moodlepy\n\n[![PyPi Package Version](https://img.shields.io/pypi/v/moodlepy)](https://pypi.org/project/moodlepy/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/moodlepy)](https://pypi.org/project/moodlepy/)\n[![LICENSE](https://img.shields.io/github/license/hexatester/moodlepy)](https://github.com/hexatester/moodlepy/blob/master/LICENSE)\n[![Tests](https://github.com/hexatester/moodlepy/workflows/Tests/badge.svg)](https://github.com/hexatester/moodlepy/actions?query=workflow%3ATests)\n[![codecov](https://codecov.io/gh/hexatester/moodlepy/branch/master/graph/badge.svg)](https://codecov.io/gh/hexatester/moodlepy)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Mypy](https://img.shields.io/badge/Mypy-enabled-brightgreen)](https://github.com/python/mypy)\n\nPython wrapper for moodle web service.\n\n## Introduction\n\nThis library provide a pure Python interface for [Moodle Web Service](https://docs.moodle.org/dev/Web_services). It's compatible with Python versions 3.7+\n\n> Install moodlepy==0.22.2 for python 3.6 support.\n\n## Installing\n\nYou can install or upgrade moodlepy with:\n\n```bash\npip install moodlepy --upgrade\n```\n\nOr you can install from source with:\n\n```bash\ngit clone https://github.com/hexatester/moodlepy\ncd moodlepy\npython setup.py install\n```\n\n## Usage\n\nExample usage\n\n```python\nfrom moodle import Moodle\nurl = 'https://my.domain/webservice/rest/server.php'\ntoken = 'super secret token'\nmoodle = Moodle(url, token)\ndict_site_info = moodle('core_webservice_get_site_info')\nsite_info = moodle.core.webservice.get_site_info()  # return typed site_info\n\nprint(dict_site_info)\nprint(site_info)\n\n# or\nfrom moodle import Mdl\nfrom moodle.core.webservice import BaseWebservice\n\nmoodle = Mdl(url, token)\nwebservice = BaseWebservice(moodle)\nsite_info2 = webservice.get_site_info()\n\nassert site_info == site_info2\n```\n\n❗️ If the function area does not have a type in the [support table](#moodle-web-service-support), the return value is in accordance with the [Moodle web service documentation](https://sandbox.moodledemo.net/admin/webservice/documentation.php), wich mostly dict.\n\nIn the future all of [Web service functions](https://docs.moodle.org/dev/Web_service_API_functions) will be covered by moodlepy.\n\n# Moodle Web Service support\n\n| Area                 | Functions | Types | Tests | Status |\n| -------------------- | --------- | ----- | ----- | ------ |\n| auth_email           | A         | A     |       |        |\n| block                | A         | A     |       |        |\n| core_auth            | A         | A     |       |        |\n| core_backup          | A         | A     |       |        |\n| core_badge           | A         | A     | A     |        |\n| core_blog            | A         | A     | A     |        |\n| core_calendar        | A         | A     |       |        |\n| core_cohort          | A         | A     |       |        |\n| core_comment         | A         | A     |       |        |\n| core_competency      |           |       |       |        |\n| core_completion      | A         | A     |       |        |\n| core_course          |           |       |       |        |\n| core_customfield     | A         | A     |       |        |\n| core_enrol           |           |       |       |        |\n| core_fetch           |           |       |       |        |\n| core_files           |           |       |       |        |\n| core_filters         |           |       |       |        |\n| core_form            |           |       |       |        |\n| core_get             |           |       |       |        |\n| core_grades          | A         |       |       |        |\n| core_grading         |           |       |       |        |\n| core_group           |           |       |       |        |\n| core_h5p             |           |       |       |        |\n| core_message         | A         |       |       |        |\n| core_notes           | A         | A     |       |        |\n| core_output          |           |       |       |        |\n| core_question        |           |       |       |        |\n| core_rating          |           |       |       |        |\n| core_role            |           |       |       |        |\n| core_search          |           |       |       |        |\n| core_session         |           |       |       |        |\n| core_tag             |           |       |       |        |\n| core_update          |           |       |       |        |\n| core_user            |           |       |       |        |\n| core_webservice      | A         | A     | A     | A      |\n| enrol_guest          | A         | A     |       |        |\n| enrol_manual         | A         | A     |       |        |\n| enrol_self           | A         | A     |       |        |\n| gradereport_overview |           |       |       |        |\n| gradereport_user     |           |       |       |        |\n| gradingform_guide    |           |       |       |        |\n| gradingform_rubric   |           |       |       |        |\n| local_mobile         |           |       |       |        |\n| message_airnotifier  |           |       |       |        |\n| message_popup        |           |       |       |        |\n| mod_assign           |           |       |       |        |\n| mod_book             |           |       |       |        |\n| mod_chat             | A         |       |       |        |\n| mod_choice           |           |       |       |        |\n| mod_data             | A         |       |       |        |\n| mod_feedback         |           |       |       |        |\n| mod_folder           | A         | A     |       |        |\n| mod_forum            |           |       |       |        |\n| mod_glossary         |           |       |       |        |\n| mod_imscp            |           |       |       |        |\n| mod_label            |           |       |       |        |\n| mod_lesson           |           |       |       |        |\n| mod_lti              |           |       |       |        |\n| mod_page             | A         | A     |       |        |\n| mod_quiz             |           |       |       |        |\n| mod_resource         | A         | A     |       |        |\n| mod_scorm            |           |       |       |        |\n| mod_survey           |           |       |       |        |\n| mod_url              | A         | A     |       |        |\n| mod_wiki             |           |       |       |        |\n| mod_workshop         | A         |       |       |        |\n| report_competency    |           |       |       |        |\n| report_insights      |           |       |       |        |\n| tool_analytics       |           |       |       |        |\n| tool_lp              |           |       |       |        |\n| tool_mobile          | A         | A     |       |        |\n| tool_templatelibrary |           |       |       |        |\n| tool_usertours       |           |       |       |        |\n| tool_xmldb           |           |       |       |        |\n",
    'author': 'hexatester',
    'author_email': 'habibrohman@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hexatester.github.io/moodlepy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
