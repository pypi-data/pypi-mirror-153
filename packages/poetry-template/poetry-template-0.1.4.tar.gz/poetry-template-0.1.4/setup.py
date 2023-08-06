# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_template',
 'poetry_template.package_one',
 'poetry_template.package_two']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['poetry-template = poetry_template.runner:run']}

setup_kwargs = {
    'name': 'poetry-template',
    'version': '0.1.4',
    'description': 'A minimal, strictly structured Python project template.',
    'long_description': '## Python Project Template\n\n```\nAfter creating a new git repository copy over:\n* docs\n* poetry_template\n* tests\n* pyproject.toml\n* README.md\n\nGo through the project and change the placeholder values. pyproject.toml contains the list of the most important values present throughout the project.\n\nFinally, delete this note.\n```\n\n```\n# Note: Install Python 3\n# Update pip and install virtualenv (dependency encapsulator) and black (linter; IDE needs to be restarted)\n\n# Note: install Poetry for Linux\n$: curl -sSL https://install.python-poetry.org | python3 -\n\n# Note: install Poetry for Windows\n$: (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -\n\n$: curl -sSL https://install.python-poetry.org | python3 - --uninstall\n```\n\n```\n# Note: `.toml` project name and package have to match (poetry-template; poetry_template)\n$: poetry install  # install all dependencies\n```\n\n### dist\n\n```\n$: pip install dist/poetry_template-0.1.4-py3-none.any.whl\n\n$: poetry-template\n```\n\n### docs\n\n```\n$: poetry shell\n$: cd docs\n# Note: review source/conf.py and source/index.rst\n$: make html\n# Note: see docs in docs/build/apidocs/index.html\n```\n\n### poetry_template\n\n```\n$: poetry run poetry-template --help\n$: poetry run python ./poetry_template/runner.py --help\n\n$: poetry run python ./poetry_template/runner.py -x 2 -y -1 -tuple A B C -list D -list E -list F -move rock\n```\n\n### tests\n\n```\n$: poetry run pytest --durations=0\n```\n\n```\n$: poetry run pytest --cov=poetry_template --cov-report=html tests\n# Note: see coverage report in htmlcov/index.html\n# Note: exclude directories from coverage report through .coveragerc\n```\n\n### poetry.lock\n\nDependencies, Python version and the virtual environment are managed by `Poetry`.\n\n```\n$: poetry search Package-Name\n$: poetry add [-D] Package-Name[==Package-Version]\n```\n\n### pyproject.toml\n\nDefine project entry point and metadata.\n\n\n### Linters\n\n```\n$: poetry run black .\n```\n\n### MyPy\n\n```\n$: poetry run mypy ./poetry_template ./tests\n```\n\n### cProfile\n\n```\n$: poetry run python ./poetry_template/profiler.py\n```\n\n### Build and publish\n\n```\n$: poetry build\n\n# Note: get the token from your PiPy account\n$: poetry config pypi-token.pypi PyPI-Api-Access-Token\n```\n\n```\n$: poetry publish --build\n```\n\n```\nhttps://pypi.org/project/poetry-template/\n```\n',
    'author': 'Mislav Jaksic',
    'author_email': 'jaksicmislav@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MislavJaksic/Python-Project-Template',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
