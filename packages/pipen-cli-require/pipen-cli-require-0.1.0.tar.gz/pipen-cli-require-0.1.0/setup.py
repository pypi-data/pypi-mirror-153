# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipen_cli_require']

package_data = \
{'': ['*']}

install_requires = \
['pipen-annotate>=0.0,<0.1', 'pipen>=0.3,<0.4']

entry_points = \
{'pipen_cli': ['cli-require = pipen_cli_require:PipenCliRequirePlugin']}

setup_kwargs = {
    'name': 'pipen-cli-require',
    'version': '0.1.0',
    'description': 'A pipen cli plugin to check requirements for processes of a pipeline',
    'long_description': '# pipen-cli-require\n\nChecking the requirements for processes of a pipeline\n\n## Install\n\n```shell\npip install -U pipen-cli-require\n```\n\n## Usage\n\n### Defining requirements of a process\n\n```python\n# example_pipeline.py\nfrom pipen import Pipen, Proc\n\nclass P1(Proc):\n    """Process 1\n\n    Requires:\n        - name: pipen\n          message: Run `pip install -U pipen` to install\n          check: |\n            {{proc.lang}} -c "import pipen"\n        - name: liquidpy\n          message: Run `pip install -U liquidpy` to install\n          check: |\n            {{proc.lang}} -c "import liquid"\n        - name: nonexist\n          message: Run `pip install -U nonexist` to install\n          check: |\n            {{proc.lang}} -c "import nonexist"\n    """\n    input = "a"\n    output = "outfile:file:out.txt"\n    lang = "python"\n\n# Setup the pipeline\n# Must be outside __main__\n# Or define a function to return the pipeline\npipeline = Pipen(...)\n\nif __name__ == \'__main__\':\n    # Pipeline must be executed with __main__\n    pipeline.run()\n```\n\n## Checking the requirements via the CLI\n\n```shell\n> pipen require -v -n 2 tests/example_pipeline.py:example_pipeline\n\nChecking requirements for pipeline: EXAMPLE_PIPELINE\n│\n└── P1: Process 1\n    ├── ✔️ pipen\n    ├── ✔️ liquidpy\n    └── x nonexist: Run `pip install -U nonexist` to install\n        └── Traceback (most recent call last):\n              File "<string>", line 1, in <module>\n            ModuleNotFoundError: No module named \'nonexist\'\n\n```\n\n## Checking requirements with runtime arguments\n\nFor example, when I use a different python to run the pipeline:\n\nAdd this to the head of `example_pipeline.py`:\n\n```python\nfrom pipen_args import args as _\n```\n\nSee also `tests/pipen_args_pipeline.py`\n\nThen specify the path of the python to use:\n\n```shell\npipen require tests/example_pipeline.py:example_pipeline --P1.lang /path/to/another/python\n```\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
