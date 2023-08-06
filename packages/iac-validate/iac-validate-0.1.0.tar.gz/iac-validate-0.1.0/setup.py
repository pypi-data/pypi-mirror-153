# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iac_validate', 'iac_validate.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'errorhandler>=2.0.1,<3.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'yamale>=4.0.3,<5.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=2.0.0,<3.0.0']}

entry_points = \
{'console_scripts': ['iac-validate = iac_validate.cli.main:main']}

setup_kwargs = {
    'name': 'iac-validate',
    'version': '0.1.0',
    'description': 'A CLI tool to perform syntactic and semantic validation of YAML files.',
    'long_description': '[![Tests](https://github.com/netascode/iac-validate/actions/workflows/test.yml/badge.svg)](https://github.com/netascode/iac-validate/actions/workflows/test.yml)\n![Python Support](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-informational "Python Support: 3.6, 3.7, 3.8, 3.9, 3.10")\n\n# iac-validate\n\nA CLI tool to perform syntactic and semantic validation of YAML files.\n\n```shell\n$ iac-validate -h\nUsage: iac-validate [OPTIONS] PATH\n\n  A CLI tool to perform syntactic and semantic validation of YAML files.\n\nOptions:\n  --version              Show the version and exit.\n  -v, --verbosity LVL    Either CRITICAL, ERROR, WARNING, INFO or DEBUG\n  -s, --schema FILE      Path to schema file.\n  -r, --rules DIRECTORY  Path to semantic rules.\n  -h, --help             Show this message and exit.\n```\n\nSyntactic validation is done by providing a [Yamale](https://github.com/23andMe/Yamale) schema and validating all YAML files against that schema. Semantic validation is done by providing a set of rules (implemented in Python) which are then validated against the YAML data. Every rule is implemented as a Python class and should be placed in a `.py` file located in the `--rules` path.\n\nEach `.py` file must have a single class named `Rule`. This class must have the following attributes: `id`, `description` and `severity`. It must implement a `classmethod()` named `match` that has a single function argument `data` which is the data read from all YAML files. It should return a list of strings, one for each rule violation with a descriptive message. A sample rule can be found below.\n\n```python\nclass Rule:\n    id = "101"\n    description = "Verify child naming restrictions"\n    severity = "HIGH"\n\n    @classmethod\n    def match(cls, data):\n        results = []\n        try:\n            for child in data["root"]["children"]:\n                if child["name"] == "FORBIDDEN":\n                    results.append("root.children.name" + " - " + str(child["name"]))\n        except KeyError:\n            pass\n        return results\n```\n',
    'author': 'Daniel Schmidt',
    'author_email': 'danischm@cisco.com',
    'maintainer': 'Daniel Schmidt',
    'maintainer_email': 'danischm@cisco.com',
    'url': 'https://github.com/netascode/iac-validate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
