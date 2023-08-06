# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auto_pytest_mg', 'auto_pytest_mg.test_models']

package_data = \
{'': ['*']}

install_requires = \
['inflection>=0.5.1,<0.6.0',
 'isort>=5.10.1,<6.0.0',
 'rich>=12.4.4,<13.0.0',
 'typer[all]>=0.4.0,<0.5.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=4.5.0,<5.0.0']}

entry_points = \
{'console_scripts': ['auto_pytest_mg = auto_pytest_mg.__main__:main']}

setup_kwargs = {
    'name': 'auto-pytest-mg',
    'version': '0.8.0',
    'description': 'Awesome `auto_pytest_mg` is a Python cli/package created with https://github.com/TezRomacH/python-package-template',
    'long_description': '# auto_pytest_mg (Automatic pytest Mock Generator)\n\n<div align="center">\n\n[![Python Version](https://img.shields.io/pypi/pyversions/auto_pytest_mg.svg)](https://pypi.org/project/auto_pytest_mg/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![Coverage Report](assets/images/coverage.svg)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/rozelie/auto_pytest_mg/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![GitHub](https://img.shields.io/badge/GitHub%20-58a6ff.svg)](https://github.com/psf/black)\n[![PyPi](https://img.shields.io/badge/PyPi%20-003d61.svg)](https://pypi.org/project/auto-pytest-mg/)\n</div>\n\n\nauto_pytest_mg generates a test skeleton for a given python file. This skeleton includes:\n- fixtures that mock all non-standard library imported names\n- a boilerplate test for every class method and property\n- a boilerplate test for every function\n- `mocker` and `mg` fixtures for all tests\n  - `mocker`: [pytest-mock](https://pypi.org/project/pytest-mock/)\n  - `mg`: [pytest-mocker-generator](https://github.com/pksol/pytest-mock-generator) \n    - If you\'re unfamiliar with pytest-mock-generator, you can read up on usage information in their [README](https://github.com/pksol/pytest-mock-generator#readme).\n\n\nIt is not auto_pytest_mg\'s goal to produce the entirety of the test. The creation of test mocks and \nasserts is delegated to pytest-mocker-generator via the `mg` fixture and the \n`mg.generate_uut_mocks_with_asserts(...)` call.\n\nThis package is a static analysis tool and will not execute any of your code.\n\n\n## Usage\n```bash\n# install the package\npip install auto_pytest_mg\n\n# go to project\'s source root\ncd my_project\n\n# pass the file to generate tests for\nauto_pytest_mg my_project/my_file.py\n```\n\n# Example\n\nSource file located at `my_project/my_file.py`\n```python\n# my_project/my_file.py\nimport requests\n\nclass MyClass:\n\n    def __init__(self, a: int):\n        self.a = a\n\n    def method(self) -> int:\n        return self.a\n\n\ndef get(url: str) -> requests.Response:\n    return requests.get(url)\n```\n\nRunning `auto_pytest_mg my_project/my_file.py` will then output to stdout the generated test file:\n\n```python\nimport pytest\n\nfrom my_project.my_file import get, MyClass\n\n\nMODULE_PATH = "my_project.my_file"\n\n\n@pytest.fixture\ndef mock_requests(mocker):\n    return mocker.patch(f"{MODULE_PATH}.requests")\n\n\n\n@pytest.fixture\ndef my_class(mocker):\n    a = mocker.MagicMock()\n    return MyClass(a=a)\n\n\nclass TestMyClass:\n    def test__init__(self, mocker):\n        a = mocker.MagicMock()\n\n        my_class_ = MyClass(a=a)\n\n    def test_method(self, mocker, mg, my_class):\n        mg.generate_uut_mocks_with_asserts(my_class.method)\n\n        result = my_class.method()\n\n\n      \ndef test_get(mocker, mg):\n    url = mocker.MagicMock()\n    mg.generate_uut_mocks_with_asserts(get)\n\n    result = get(url=url)\n```\n\n## Similar packages\n- [pyguin](https://pynguin.readthedocs.io/en/latest/)\n  - Executes given source code and uses a genetic algorithm to produce test cases\n  - Can output to unittest/pytest test styles\n- [pythoscope](https://github.com/mkwiatkowski/pythoscope)\n  - Last updated in 2016\n  - Performs static analysis, does not run your code.\n  - Outputs unittest test style only\n\n## Development\nSee [DEVELOPMENT.md](./DEVELOPMENT.md)\n\n\n## License\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/rozelie/auto_pytest_mg/blob/master/LICENSE) for more details.\n\n\n## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)\n',
    'author': 'auto_pytest_mg',
    'author_email': 'ryan.ozelie@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/auto_pytest_mg/auto_pytest_mg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
