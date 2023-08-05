# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['amhelpers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'amhelpers',
    'version': '0.1.0',
    'description': 'A collection of handy utilities.',
    'long_description': '# amhelpers\n\nA collection of handy utilities.\n\n## Installation\n\n```bash\n$ pip install amhelpers\n```\n\n## License\n\n`amhelpers` was created by Anton Matsson. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`amhelpers` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Anton Matsson',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
