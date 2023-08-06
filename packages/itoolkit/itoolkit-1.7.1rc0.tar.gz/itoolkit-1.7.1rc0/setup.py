# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['itoolkit',
 'itoolkit.db2',
 'itoolkit.lib',
 'itoolkit.rest',
 'itoolkit.transport']

package_data = \
{'': ['*'], 'itoolkit': ['doc/*']}

setup_kwargs = {
    'name': 'itoolkit',
    'version': '1.7.1rc0',
    'description': 'IBM i XMLSERVICE toolkit for Python',
    'long_description': "Python XMLSERVICE Toolkit\n=========================\n\n[![Build Status](https://github.com/IBM/python-itoolkit/actions/workflows/build.yml/badge.svg?branch=v1&event=push)](https://github.com/IBM/python-itoolkit/actions/workflows/build.yml)\n[![Latest version released on PyPi](https://img.shields.io/pypi/v/itoolkit.svg)](https://pypi.python.org/pypi/itoolkit)\n[![Python Version Support](https://img.shields.io/pypi/pyversions/itoolkit.svg)](https://pypi.org/project/itoolkit/)\n[![Documentation Status](https://readthedocs.org/projects/python-itoolkit/badge/?version=latest)](https://python-itoolkit.readthedocs.io/en/latest/?badge=latest)\n\n\nitoolkit is a Python interface to the\n[XMLSERVICE](https://github.com/IBM/xmlservice) toolkit for the\n[IBM i](https://en.wikipedia.org/wiki/IBM_i) platform.\n\n```python\nfrom itoolkit import *\nfrom itoolkit.transport import DatabaseTransport\nimport ibm_db_dbi\n\nconn = ibm_db_dbi.connect()\nitransport = DatabaseTransport(conn)\nitool = iToolKit()\n\nitool.add(iCmd5250('wrkactjob', 'WRKACTJOB'))\nitool.call(itransport)\nwrkactjob = itool.dict_out('wrkactjob')\n\nprint(wrkactjob)\n```\n\nFor more, check out the [samples](samples).\n\nSupported Python Versions\n-------------------------\n\npython-itoolkit currently supports Python 2.7 and Python 3.4+.\n\n:warning: Note: python-itoolkit 1.x will be the last series to support Python\n2.7, 3.4, and 3.5. These versions will no longer be supported in python-itoolkit 2.0.\n\nFeature Support\n---------------\n\n- Call ILE programs & service programs\n- Call CL Commands\n- Call PASE shell commands\n\nDocumentation\n-------------\n\nThe docs can be found at <http://python-itoolkit.readthedocs.io/en/latest>\n\nInstallation\n------------\n\nYou can install itoolkit simply using `pip`:\n\n```bash\npython -m pip install itoolkit\n```\n\nTests\n-----\n\nTo test the installed itoolkit\n\n```bash\npython -m pytest\n```\n\nTo test the local code:\n\n```bash\nPYTHONPATH=src python -m pytest\n```\n\nContributing\n------------\n\nPlease read the [contribution guidelines](CONTRIBUTING.md).\n\nReleasing a New Version\n-----------------------\n\nRun the following commands\n\n```\n# checkout and pull the latest code from master\ngit checkout master\ngit pull\n\n# bump to a release version (a tag and commit are made)\nbumpversion release\n\n# build the new distribution and upload to PyPI\npoetry publish --build\n\n# bump to the new dev version (a commit is made)\nbumpversion --no-tag patch\n\n# push the new tag and commits\ngit push origin master --tags\n```\n\nLicense\n-------\n\nMIT - See [LICENSE](LICENSE)\n",
    'author': 'Kevin Adler',
    'author_email': 'kadler@us.ibm.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/IBM/python-itoolkit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
