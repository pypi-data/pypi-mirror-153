# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['intersight_auth']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=37.0.2,<38.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'intersight-auth',
    'version': '0.1.2',
    'description': 'Intersight Authentication helper for requests',
    'long_description': '# intersight-auth\n\nThis module provides an authentication helper for requests to make it easy to make [Intersight API](https://intersight.com/apidocs/introduction/overview/) calls using [requests](https://requests.readthedocs.io/en/latest/). \n\n## Install\n\n```\npip install intersight-auth\n```\n\n## Example\n\n```\nimport sys\n\nfrom intersight_auth import IntersightAuth\nfrom requests import Session\n\nsession = Session()\nsession.auth = IntersightAuth("key.pem", "XYZ/XYZ/XYZ")\n\nresponse = session.get("https://intersight.com/api/v1/ntp/Policies")\n\nif not response.ok:\n    print(f"Error: {response.status_code} {response.reason}")\n    sys.exit(1)\n\nfor policy in response.json()["Results"]:\n    print(f"{policy[\'Name\']}")\n```\n\n',
    'author': 'Chris Gascoigne',
    'author_email': 'cgascoig@cisco.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cgascoig/intersight-auth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
