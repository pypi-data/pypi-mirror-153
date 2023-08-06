# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['failure_analysis']

package_data = \
{'': ['*']}

install_requires = \
['jellyfish>=0.9.0,<0.10.0',
 'lxml>=4.9.0,<5.0.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'sklearn>=0.0,<0.1']

entry_points = \
{'console_scripts': ['failures-analysis = '
                     'failure_analysis.failure_analysis:main']}

setup_kwargs = {
    'name': 'failures-analysis',
    'version': '1.0.0',
    'description': ' failures-analysis package provides fast and reliable way to find and group similar failures in test automation.',
    'long_description': '# Failure analysis\nTests failure analysis package provides fast and reliable way to find and group similar failures in your CI/CD\npipeline. When failure grouping and similarity scoring is done automatically by a machine, it will free\nresources from development team member to fix the most important failures in their CI/CD pipeline. It is tedious\nwork for a human to download, open and read all the test failures and analyse which failures belong to the same group.\nThe failure-analysis package solves this problem by processing xunit xml files using cosine similiarity and Levenshtein distance to find similar\nfailures from the test results.\n\nTest failure analysis package supports calculating similiarities with the following algorithms. \n\n- Sequence Matcher from Pythons diff library https://docs.python.org/3/library/difflib.html\n- Jaro-Winkler distance using jellyfish library https://pypi.org/project/jellyfish/\n- Jaccard index using jellyfish library https://pypi.org/project/jellyfish/\n- Levenshtein ratio using jellyfish library https://pypi.org/project/jellyfish/\n- Cosine similiarty using sklearn https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html\n\nWhile it supports five different algorithms, best performing algorithms (cosine similiarity and levenshtein ratio) are only currently calculated.\n\nResults and the reason why only cosine and levenshtein deemed good enough are published here: LINK TO THE FIRST PUBLICATION\n\n# Features\n- List of test that have the same failure\n\n# Parameters\n- `--xxx` to be defined\n',
    'author': 'Tatu Aalto',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/F-Secure/failures-analysis',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
