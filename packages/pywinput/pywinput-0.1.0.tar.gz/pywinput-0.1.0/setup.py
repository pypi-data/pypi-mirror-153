# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywinput']

package_data = \
{'': ['*']}

install_requires = \
['keyboard>=0.13.5,<0.14.0', 'mouse>=0.7.1,<0.8.0', 'pywin32>=304,<305']

setup_kwargs = {
    'name': 'pywinput',
    'version': '0.1.0',
    'description': 'A wrapper for pywin32 that adds some extra functionality and solves common issues.',
    'long_description': "\n# Pywinput\nA wrapper for pywin32 that allows for simulating keyboard and mouse input within background windows\n\n## Installation\n\n#### Pip\n\n```\npip install pywinput\n```\n\n#### Poetry\n    \n```\npoetry add pywinput\n```\n\n\n## Usage\n\n```python\nfrom pywinput import Window, Key, Button\n\nif __name__ == '__main__':\n    win = Window.create(\n        title='My Test Window',\n        x=400,\n        y=400,\n        width=200,\n        height=200,\n    )\n    win.show()\n    win.text = 'My new window title'\n```\n\n\n\n\n\n\n",
    'author': 'Kyle Oliver',
    'author_email': '56kyleoliver@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/56kyle/pywinput',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
