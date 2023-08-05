# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bbdirtree']

package_data = \
{'': ['*']}

install_requires = \
['tabulate>=0.8.9,<0.9.0']

setup_kwargs = {
    'name': 'bb-dirtree',
    'version': '0.1.3',
    'description': 'Create a nice looking directory tree with options',
    'long_description': '\n# DirTree\n\n##### - create a nice looking directory tree\n==============================================\n\n## Installation:\n================\n\n##### _**Windows:**_\n\n```bash\npy -m pip install "BB-DirTree"\n```\n\n##### _**Linux/Mac:**_\n\n```bash\npython -m pip install "BB-DirTree"\n```\n\n## DirTree usage\n================\n\n##### _**Windows:**_\n\n```bash\npy -m bbdirtree [OPTIONS] [ARGS]\n```\n\n##### _**Linux/Mac:**_\n\n```bash\npython -m bbdirtree [OPTIONS] [ARGS]\n```\n\n### _**Options:**_\n\n**Short**  | **Long**       | **Description**\n---------- | -------------- | ---------------------------------------------------------\n-b         |   --base-dir   |  Set base directory <br> *Uses current directory if not specified*\n-d         |   --depth      |  Integer to set the depth of directory tree <br> *ex: \'0\' will only print the base directory list*\n-D         |   --dotfiles   |  Include hidden files in tree\n-e         |   --exclude    |  Filenames/directories to exclude from the tree <br> *See Exclusions*\n-h         |   --help       |  This help message\n-q         |   --qt-html    |  Print in html format for use with QT\n-r         |   --regex      |  Use regex to include/exclude files/directories in tree <br> *See Regex*\n\n>It is recommended to quote all paths\n\n### *Exclusions*\n\n>Provide names of files or directories to exclude. To exclude multiple files/directories, quote entire list and seperate with a colon (**:**). Add a forward slash (**/**) to specify a directory name to exclude.\n\n##### **Example:**\n  \n```bash\npython -m bbdirtree --exclude "excluded dir:excluded file"\n```\n\n### *Regex*\n\n>Prefix regex with *include=* or *exclude=*\n\n>Seperate each regex with a space, quoting each individual argument.\n\n##### _**Examples:**_\n\n```bash\npython -m bbdirtree --regex "exclude=.*\\.ini$"\n\n    # will exclude any files that have a *.ini* extension.\n\npython -m bbdirtree --regex "include=.*\\.mp3$"\n\n    # will include only files with a *.mp3* extension.\n```\n\n>This has no effect on directories\n\n>Multiple regex can be used by specifying **--regex** multiple times.\n\n## License\n==========\n\n<pre>\n    MIT License\n\n    Copyright (c) [year] [fullname]\n\n    Permission is hereby granted, free of charge, to any person obtaining a copy\n    of this software and associated documentation files (the "Software"), to deal\n    in the Software without restriction, including without limitation the rights\n    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n    copies of the Software, and to permit persons to whom the Software is\n    furnished to do so, subject to the following conditions:\n\n    The above copyright notice and this permission notice shall be included in all\n    copies or substantial portions of the Software.\n\n    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n    SOFTWARE.\n</pre>\n\n## CHANGELOG\n============\n\n#### v0.1.0 - 5-29-2022\n\n- initial release\n\n#### v0.1.1 - 5-30-2022\n\n- changed name from DirTree to BB-DirTree\n- added README.md\n\n#### v0.1.2 = 5-31-2022\n\n- added a changelog to README.md\n- made corrections to help message\n\n#### v0.1.3 = 5-31-2022\n\n- added support for windows hidden files\n',
    'author': 'Erik Beebe',
    'author_email': 'beebeapps_feedback@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
