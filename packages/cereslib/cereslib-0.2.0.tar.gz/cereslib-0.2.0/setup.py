# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cereslib', 'cereslib.dfutils', 'cereslib.enrich', 'cereslib.events', 'tests']

package_data = \
{'': ['*'], 'tests': ['data/*', 'data/enrich/*', 'data/events/*']}

install_requires = \
['grimoirelab-toolkit>=0.2.0,<0.3.0',
 'numpy<=1.18.3',
 'pandas>=0.22.0,<=0.25.3',
 'scipy>=1.5,<2.0',
 'six>=1.16.0,<2.0.0']

setup_kwargs = {
    'name': 'cereslib',
    'version': '0.2.0',
    'description': 'GrimoireLab: Unify, eventize and enrich information from Perceval',
    'long_description': "# Ceres [![Build Status](https://github.com/chaoss/grimoirelab-cereslib/workflows/tests/badge.svg)](https://github.com/chaoss/grimoirelab-cereslib/actions?query=workflow:tests+branch:master+event:push) [![Coverage Status](https://coveralls.io/repos/github/chaoss/grimoirelab-cereslib/badge.svg?branch=master)](https://coveralls.io/github/chaoss/grimoirelab-cereslib?branch=master)\n\nCeres is a library that aims at dealing with data in general,\nand software development data in particular.\n\nThe initial goal of Ceres is to parse information in several ways\nfrom the [Perceval](https://github.com/grimoirelab/perceval) tool\nin the [GrimoireLab project](https://github.com/grimoirelab).\n\nHowever, the more code is added to this project, the more generic\nmethods are found to be useful in other areas of analysis.\n\nThe following are the areas of analysis that Ceres can help at:\n\n## Eventize\n\nThe 'eventizer' helps to split information coming from Perceval.\nIn short, Perceval produces JSON documents and those can be consumed\nby Ceres and by the 'eventizing' side of the library.\n\nBy 'eventizing', this means the process to parse a full Perceval JSON\ndocument and produce a Pandas DataFrame with certain amount of information.\n\nAs an example, a commit contains information about the commit itself, and\nthe files that were 'touched' at some point. Depending on the granularity\nof the analysis Ceres will work in the following way:\n\n* Granularity = 1: This is the first level and produces 1 to 1 relationship\n  with the main items in the original data source. For example 1 commit would \n  be just 1 row in the resultant dataframe. This would be a similar case for\n  a code review process in Gerrit or in Bugzilla for tickets.\n* Granularity = 2: This is the second level and depends on the data source\n  how in depth this goes. In the specific case of commits, this would return\n  n rows in the dataframe. And there will be as many rows as files where \n  'touched' in the original data source.\n\n\n## Format\n\nThe format part of the library contains some utils that are useful for\nsome basic formatting actions such as having a whole column in the Pandas\ndataframe with the same string format.\n\nAnother example would be the use of the format utils to cast from string\nto date using datetuils and applying the method to a whole column of a \ngiven dataframe.\n\n## Filter\n\nThe filter utility basically removes rows based on certain values in\ncertain cells of a dataframe.\n\n## Data Enrich\n\nThis is the utility most context-related together with the eventizing\nactions. This will add or modify one or more columns in several ways.\n\nThere are several examples such as taking care of the surrogates enabling\nUTF8, adding new columns based on some actions on others, adding the gender\nof the name provided in another column, and others.\n\n\n# How can you help here?\n\nThis project is still quite new, and the development is really slow, so\nany extra hand would be really awesome, even giving directions, pieces\nof advice or feature requests :).\n\nAnd of course, using the software would be great!\n\n# Where to start?\n\nThe examples folder contains some of the clients I've used for some\nanalysis such as the gender analysis or to produce dataframes that help\nto understand the areas of the code where developers are working.\n\nThose are probably a good place to have a look at.\n\n\n",
    'author': 'GrimoireLab Developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://chaoss.github.io/grimoirelab/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
