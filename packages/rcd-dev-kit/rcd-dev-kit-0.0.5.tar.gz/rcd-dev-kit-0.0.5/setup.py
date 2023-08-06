# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rcd_dev_kit',
 'rcd_dev_kit.database_manager',
 'rcd_dev_kit.dataclass_manager',
 'rcd_dev_kit.decorator_manager',
 'rcd_dev_kit.file_manager',
 'rcd_dev_kit.pandas_manager',
 'rcd_dev_kit.sql_utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.36,<2.0.0',
 'boto3>=1.22.7,<2.0.0',
 'botocore>=1.25.7,<2.0.0',
 'elasticsearch>=8.2.0,<9.0.0',
 'google-api-python-client>=2.47.0,<3.0.0',
 'google-cloud-storage>=2.3.0,<3.0.0',
 'google>=3.0.0,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'snowflake-connector-python>=2.7.7,<3.0.0',
 'sqlalchemy-redshift>=0.8.9,<0.9.0',
 'sqlparse>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'rcd-dev-kit',
    'version': '0.0.5',
    'description': 'Interact with OIP ecosystem.',
    'long_description': '# rcd_dev_kit\n\nrcd-utils is a Python package for manipulating data and interacting with OIP ecosystem.\n\n## Installation\n```bash\npip install rcd-utils\n```\n\n## Modules\n    database_manager\n    decorator_manager\n    file_manager\n    pandas_manager\n\n## Feedback\nAny questions or suggestions?\nPlease contact package maintainer.\n\n# python-sdk\nRefer to book https://py-pkgs.org/01-introduction for best practices\n\n# Maintainers\nThis package is using poetry for pkg management, it must be installed locally if you are maintaining the package.  \nFor testing install pydev with poetry `poetry add --dev pytest`\n\n### Build Package \n`poetry build`\n\n### Publish Package\n`poetry publish`\n\n#TODO: restructure package to use src parent folder as per recommendation\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`rcd_dev_kit` was created by RCD. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`rcd_dev_kit` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).',
    'author': 'Davi FACANHA',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/OpenInnovationProgram/rcd-dev-kit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
