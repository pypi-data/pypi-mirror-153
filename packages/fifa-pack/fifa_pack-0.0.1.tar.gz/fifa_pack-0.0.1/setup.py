# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fifa_pack']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'bs4>=0.0.1,<0.0.2',
 'certifi>=2022.5.18,<2023.0.0',
 'chardet>=4.0.0,<5.0.0',
 'charset-normalizer>=2.0.12,<3.0.0',
 'idna>=3.3,<4.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2022.1,<2023.0',
 'requests>=2.27.1,<3.0.0',
 'six>=1.16.0,<2.0.0',
 'soupsieve>=2.3.2,<3.0.0',
 'urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'fifa-pack',
    'version': '0.0.1',
    'description': 'the package whichcontains utility functions for the main repo',
    'long_description': '# fifa_pack\n\nthe package whichcontains utility functions for the main repo\n\n## Installation\n\n```bash\n$ pip install fifa_pack\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`fifa_pack` was created by chole Zhang Jinghan Xu Mingting Fu MukeW Wang ShiyangZhang Tony Liang. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`fifa_pack` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'chole Zhang Jinghan Xu Mingting Fu MukeW Wang ShiyangZhang Tony Liang',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
