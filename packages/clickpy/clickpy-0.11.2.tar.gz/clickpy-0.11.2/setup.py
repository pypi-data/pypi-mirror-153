# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clickpy', 'clickpy.strategy']

package_data = \
{'': ['*']}

install_requires = \
['PyAutoGUI>=0.9.53,<0.10.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['clickpy = clickpy:cli']}

setup_kwargs = {
    'name': 'clickpy',
    'version': '0.11.2',
    'description': 'Automated mouse clicking script',
    'long_description': "# clickpy\n\nAutomated mouse clicker script using [PyAutoGUI][1] and [Typer][2].\n\nThis app will randomly click your mouse between 1 second and 3 minutes, to prevent your screen and apps from sleeping or displaying an `away` status.\n\nThe rational behind the random interval is: if the mouse contiually clicked every second or millisecond, it could easily be detected as an automated process.\n\nThe random interval provides a sembalance of feasability, although the interval could be reduced and extended as needed, or move the cursor after a couple consecutive clicks. (Possibe future feature?)\n\nPyAutoGUI provides a simple interface to the mouse, and Typer provides simple cli parsing. You can find out more about these libraries with the links provided above.\n\n## Installation\n\nThis package supports Python 3.6 through 3.9. It does not support any version of Python 2, nor any version of 3 lower than 3.6. Please upgrade our Python version, if possible.\n\nI highly recommend using [pipx][3] for installing standalone packages, as it adds a layer of isolation to your installation. But pip will also work.\n\n```bash\npipx install clickpy\n# -- or --\npip install clickpy\n```\n\nIf you're using macOS or Linux, you may have to install additional dependencies for PyAutoGUI to work properly. Please review their [docs][4] for additional information.\n\nWindows users don't have to install any additional software.\n\nTo uninstall, type in your terminal:\n\n```bash\npipx uninstall clickpy\n# -- or --\npip uninstall clickpy\n```\n\n## Running\n\nOnce this package is installed, and any additional dependencies too, run the app like so:\n\n```bash\nclickpy\n```\n\nTo stop it, press `ctrl+c`.\n\nThere are 3 flags you can use; `-d` will display debug information, `-f` will speed the app up to 1 click every second, and `--help` will display the help menu.\n\n## For Developers\n\nPlease read [contributing.md](./CONTRIBUTING.md) for more information about this repo, how it's maintained and developed. And feel free to make PRs.\n\n[1]: https://github.com/asweigart/pyautogui\n[2]: https://github.com/tiangolo/typer\n[3]: https://github.com/pypa/pipx\n[4]: https://github.com/asweigart/pyautogui/blob/master/docs/install.rst\n",
    'author': 'fitzypop',
    'author_email': 'fitzypop@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fitzypop/clickpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.11,<4.0.0',
}


setup(**setup_kwargs)
