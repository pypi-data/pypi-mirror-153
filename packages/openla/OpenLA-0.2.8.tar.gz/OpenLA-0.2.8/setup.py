# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['OpenLA', 'OpenLA.data_classes']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.2,<4.0.0', 'numpy>=1.18.15,<2.0.0', 'pandas>=1.3,<2.0']

setup_kwargs = {
    'name': 'openla',
    'version': '0.2.8',
    'description': 'Open source library for e-Book log analysis',
    'long_description': "# OpenLA: open-source library for e-book log analysis \n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/OpenLA.svg)](https://pypi.org/project/OpenLA/)\n[![Coverage](https://limu.ait.kyushu-u.ac.jp/~openLA/_images/coverage.svg)](https://github.com/limu-research/openla/)\n[![Package Status](https://img.shields.io/pypi/status/OpenLA.svg)](https://pypi.org/project/OpenLA/)\n[![License](https://img.shields.io/pypi/l/OpenLA.svg)](https://github.com/limu-research/openla/blob/main/LICENSE)\n[![Downloads](https://static.pepy.tech/personalized-badge/OpenLA?period=month&units=international_system&left_color=black&right_color=orange&left_text=PyPI%20downloads%20per%20month)](https://pepy.tech/project/OpenLA)\n[![Documentation](https://img.shields.io/badge/api-reference-blue.svg)](https://limu.ait.kyushu-u.ac.jp/~openLA/)\n\n## Introduction\n\nOpenLA is an open-source library for e-book log analysis.\n\nThis Python library helps reduce redundant development when preprocessing e-book logs:\ncalculating reading times for each learner, counting up operations, page-wise summary of student behavior, etc.\n\n![OpenLA concept](https://github.com/limu-research/openla/raw/main/source/images/OpenLA_concept.jpg?openla=2022-04-12)\n\n## API concept\n\nFour preprocessing processes are essential and common in e-book log analysis: getting course information, converting the log into a form suitable for analysis, extracting the required information, and visualizing the data.\n\nIn order to improve efficiency and reduce reiteration in these processes, OpenLA provides the corresponding four modules: Course Information, Data Conversion, Data Extraction, and Data Visualization.\n\n![Preprocessing flow](https://github.com/limu-research/openla/raw/main/source/images/OpenLA_structure.jpg?openla=2022-04-12)\n\n## Installation\n\nOpenLA is [available on PyPi](https://pypi.org/project/OpenLA/). You can install it with `pip`.\n\n```sh\npip install OpenLA\n```\n\nOpenLA works on python 3.7, 3.8, 3.9 and 3.10.\n\nBelow are the versions of OpenLA's main dependencies we use for testing, but you probably do not need to worry about this.\n\n- python 3.7: matplotlib 3.5.2, numpy 1.21.6, pandas 1.3.5\n- python 3.8 or newer: matplotlib 3.5.2, numpy 1.22.3, pandas 1.4.2\n\n## Datasets for OpenLA\n\nThe dataset used in this library has the same structure as the open source ones used to conduct [Data Challenge Workshops in LAK19 and LAK20](https://sites.google.com/view/lak20datachallenge).\n\nWe target [BookRoll](https://www.let.media.kyoto-u.ac.jp/en/project/digital-teaching-material-delivery-system-bookroll/) logs, but logs from other systems can be adapted.\n\nThe dataset may include up to four types of files.\n\n### Course\\_#\\_EventStream.csv\n\n- Data of the logged activity data from learners' interactions with the BookRoll system\n- Columns: `userid`, `contentsid`, `operationname`, `pageno`, `marker`, `memo_length`, `devicecode`, and `eventtime`\n\n### Course\\_#\\_LectureMaterial.csv\n\n- Information about the length of the lecture materials used\n- Columns: `lecture`, `contentsid`, and `pages`\n\n### Course\\_#\\_LectureTIme.csv\n\n- Information about the schedule of the lectures\n- Columns: `lecture`, `starttime`, and `endtime`\n\n### Course\\_#\\_QuizScore.csv\n\n- Data on the final score for each student\n- Columns: `userid` and `score`\n\nNote: from version 0.2.1, OpenLA can treat grading data, which was not present in the LAK19 and LAK20 datasets.\n\n### Course\\_#\\_GradePoint.csv\n\n- Data on the final grade for each student\n- Columns: `userid` and `grade`\n\nWhere `#` is the course id. BookRoll is an e-book system to record learning activities.\n\nIf you need a sample dataset, please contact openla@limu.ait.kyushu-u.ac.jp .\n\n## Documentation\n\n[Read the docs](https://limu.ait.kyushu-u.ac.jp/~openLA/) for detailed information about all the modules, and for code examples.\n\nFor more information about BookRoll and the learning analytics platform on which the data was collected, please refer to the following:\n\n- Brendan Flanagan, Hiroaki Ogata, Integration of Learning Analytics Research and Production Systems While Protecting Privacy, Proceedings of the 25th International Conference on Computers in Education (ICCE2017), pp.333-338, 2017.\n- Hiroaki Ogata, Misato Oi, Kousuke Mohri, Fumiya Okubo, Atsushi Shimada, Masanori Yamada, Jingyun Wang, and Sachio Hirokawa, Learning Analytics for E-Book-Based Educational Big Data in Higher Education, In Smart Sensors at the IoT Frontier, pp.327-350, Springer, Cham, 2017.\n",
    'author': 'LIMU',
    'author_email': 'repository@limu.ait.kyushu-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
