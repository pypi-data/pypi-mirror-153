# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snapsheets']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.12,<2.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'docopt>=0.6.2,<0.7.0',
 'icecream>=2.1.2,<3.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['snapsheets = snapsheets.core:cli',
                     'snapsheets-next = snapsheets.next:cli']}

setup_kwargs = {
    'name': 'snapsheets',
    'version': '0.6.0',
    'description': 'Getting tired of downloading Google Spreadsheets one by one from the browser ?',
    'long_description': '![GitLab pipeline](https://img.shields.io/gitlab/pipeline/qumanote/snapsheets?style=for-the-badge)\n![PyPI - Licence](https://img.shields.io/pypi/l/snapsheets?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/snapsheets?style=for-the-badge)\n![PyPI - Status](https://img.shields.io/pypi/status/snapsheets?style=for-the-badge)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snapsheets?style=for-the-badge)\n\n\n# Snapsheets\n\nGetting tired of downloading Google Spreadsheets one by one from the browser ?\n\nThis package enables to wget Google Spreadsheets without login.\n(Spreadsheets should be shared with public link)\n\n\n---\n\n\n# Usage : as python module\n\n```python\n>>> from snapsheets import Sheet\n>>> url = "https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"\n>>> sheet = Sheet(url=url, desc="Get Sample Sheet")\n>>> sheet.snapshot()\n📣 Get Sample Sheet\n🤖 Downloaded snapd/snapsheet.xlsx\n🚀 Renamed to snapd/20220602T225044_snapsheet.xlsx\n```\n\n---\n# Usage : as CLI\n\n```bash\n$ snapsheets -h\nusage: snapsheets [-h] [--config CONFIG] [--url URL] [-v]\n\noptional arguments:\n  -h, --help       show this help message and exit\n  --config CONFIG  set config directory (default: ./config/\n  --url URL        copy and paste an URL of the Google spreadsheet\n```\n\n```bash\n$ snapsheets --url "https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"\n📣 snapsheet\n🤖 Downloaded snapd/snapsheet.xlsx\n🚀 Renamed to snapd/20220602T224856_snapsheet.xlsx\n```\n\n- Use ``--url`` option to download single spreadsheet.\n- Downloaded file is temporarily named as ``snapsheet.xlsx``, then renamed with current-time based prefix.\n- (More options might be added later)\n\n---\n## Usage : with configuration files\n\n- This is useful when you have lots of files to download.\n- Make ``./config/`` directory and place your TOML/YAML configuration files.\n  - If ``./config/`` does not exist, it will search from ``. (current directory)``.\n- Downloaded files are saved to ``./snapd/`` directory\n  - If ``./snapd/`` does not exit, it will be saved in ``. (current directory)``.\n  - (Options to switch directory might be added later)\n\n```bash\n$ snapsheets\n📣 Example for Snapshot module (in TOML)\n🤖 Downloaded snapd/snapsheet.xlsx\n🚀 Renamed to snapd/2021_toml_sample1.xlsx\n📣 20210304_storage_comparison\n🤖 Downloaded snapd/snapsheet.xlsx\n🚀 Renamed to snapd/20210412_toml_sample2.xlsx\n```\n\n---\n\n# Next version\n\n- いまのバージョンはデフォルトで設定ファイルを読み込むようになっている\n- いま考えるとなんだかよく分からない仕様になっている\n- 設定ファイルがない場合は、エラーがでて止まるように変更したい\n- ついでに設定ファイルの内容を簡素化しようと考えている\n\n\n```bash\n$ snapsheets-next -h\n```\n\n```bash\n$ snapsheets-next --url "https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"\n📣 Add description here.\n🤖 Downloaded snapshot.csv\n🚀 Renamed snapshot.csv to _snapshot.csv\n```\n\n```python\n>>> from snapsheets.next import Sheet\n>>> url = https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"\n>>> filename = "snapsheet.csv"\n>>> description = "Get sample sheet"\n>>> sheet = Sheet(url=url, filename=filename, description=description)\n>>> sheet.snapshot()\n📣 Get sample sheet\n🤖 Downloaded snapsheet.csv\n🚀 Renamed snapsheet.csv to 20220602_snapsheet.csv\n```\n\n\n---\n\n# Other requirements\n\n- Install ``wget`` if your system doesn\'t have them\n- Make your spreadsheet available with shared link (OK with read-only)\n\n---\n\n# Documents\n\n- https://qumanote.gitlab.io/snapsheets/\n\n---\n\n# PyPI package\n\n- https://pypi.org/project/snapsheets/\n\n![PyPI - Downloads](https://img.shields.io/pypi/dd/snapsheets?style=for-the-badge)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/snapsheets?style=for-the-badge)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/snapsheets?style=for-the-badge)\n',
    'author': 'shotakaha',
    'author_email': 'shotakaha+py@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://qumanote.gitlab.io/snapsheets/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
