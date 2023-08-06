# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kfp_toolbox', 'kfp_toolbox.cli']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-aiplatform>=1.7,<2.0', 'kfp>=1.8,<2.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['kfp-toolbox = kfp_toolbox.cli.main:main']}

setup_kwargs = {
    'name': 'kfp-toolbox',
    'version': '0.2.0',
    'description': 'The toolbox for kfp (Kubeflow Pipelines SDK)',
    'long_description': '# kfp-toolbox\n\n*kfp-toolbox* is a Python library that provides useful tools for kfp (Kubeflow Pipelines SDK).\n\n[![PyPI](https://img.shields.io/pypi/v/kfp-toolbox.svg)](https://pypi.org/project/kfp-toolbox/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kfp-toolbox.svg)](https://pypi.org/project/kfp-toolbox/)\n[![Python Tests](https://github.com/speg03/kfp-toolbox/actions/workflows/python-tests.yml/badge.svg)](https://github.com/speg03/kfp-toolbox/actions/workflows/python-tests.yml)\n[![codecov](https://codecov.io/gh/speg03/kfp-toolbox/branch/main/graph/badge.svg)](https://codecov.io/gh/speg03/kfp-toolbox)\n\n\n## Installation\n\n```\npip install kfp-toolbox\n```\n\n\n## Usage\n\n### `spec`\n\n```python\nfrom kfp_toolbox import spec\n```\n\nThe `spec` decorator specifies the computing resources to be used by the component.\n\nTo apply this to a Python function-based component, it must be added outside of the `component` decorator.\n\n```python\n@spec(cpu="2", memory="16G")\n@dsl.component\ndef component_function():\n    ...\n```\n\nFor other components, wrap the component as a function.\n\n```python\ncomponent = kfp.components.load_component_from_file("path/to/component.yaml")\ncomponent = spec(cpu="2", memory="16G")(component)\n```\n\nIf multiple `spec` decorators are stacked, the one placed further out will take precedence. For example, suppose you have created an alias `default_spec`. If you want to overwrite part of it, place a new `spec` decorator outside of the `default_spec` decorator to overwrite it.\n\n```python\ndefault_spec = spec(cpu="2", memory="16G")\n\n@spec(cpu="1")\n@default_spec\n@dsl.component\ndef component_function():\n    ...\n```\n\nSee all available options here:\n\n|option|type|description|examples|\n|---|---|---|---|\n|name|str|Display name|`"Component NAME"`|\n|cpu|str|CPU limit|`"1"`, `"500m"`, ... ("m" means 1/1000)|\n|memory|str|Memory limit|`"512K"`, `"16G"`, ...|\n|gpu|str|GPU limit|`"1"`, `"2"`, ...|\n|accelerator|str|Accelerator type|`"NVIDIA_TESLA_K80"`, `"TPU_V3"`, ...|\n|caching|bool|Enable caching|`True` or `False`|\n',
    'author': 'Takahiro Yano',
    'author_email': 'speg03@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/speg03/kfp-toolbox',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
