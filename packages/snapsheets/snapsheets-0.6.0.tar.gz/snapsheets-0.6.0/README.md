![GitLab pipeline](https://img.shields.io/gitlab/pipeline/qumanote/snapsheets?style=for-the-badge)
![PyPI - Licence](https://img.shields.io/pypi/l/snapsheets?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/snapsheets?style=for-the-badge)
![PyPI - Status](https://img.shields.io/pypi/status/snapsheets?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snapsheets?style=for-the-badge)


# Snapsheets

Getting tired of downloading Google Spreadsheets one by one from the browser ?

This package enables to wget Google Spreadsheets without login.
(Spreadsheets should be shared with public link)


---


# Usage : as python module

```python
>>> from snapsheets import Sheet
>>> url = "https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"
>>> sheet = Sheet(url=url, desc="Get Sample Sheet")
>>> sheet.snapshot()
📣 Get Sample Sheet
🤖 Downloaded snapd/snapsheet.xlsx
🚀 Renamed to snapd/20220602T225044_snapsheet.xlsx
```

---
# Usage : as CLI

```bash
$ snapsheets -h
usage: snapsheets [-h] [--config CONFIG] [--url URL] [-v]

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  set config directory (default: ./config/
  --url URL        copy and paste an URL of the Google spreadsheet
```

```bash
$ snapsheets --url "https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"
📣 snapsheet
🤖 Downloaded snapd/snapsheet.xlsx
🚀 Renamed to snapd/20220602T224856_snapsheet.xlsx
```

- Use ``--url`` option to download single spreadsheet.
- Downloaded file is temporarily named as ``snapsheet.xlsx``, then renamed with current-time based prefix.
- (More options might be added later)

---
## Usage : with configuration files

- This is useful when you have lots of files to download.
- Make ``./config/`` directory and place your TOML/YAML configuration files.
  - If ``./config/`` does not exist, it will search from ``. (current directory)``.
- Downloaded files are saved to ``./snapd/`` directory
  - If ``./snapd/`` does not exit, it will be saved in ``. (current directory)``.
  - (Options to switch directory might be added later)

```bash
$ snapsheets
📣 Example for Snapshot module (in TOML)
🤖 Downloaded snapd/snapsheet.xlsx
🚀 Renamed to snapd/2021_toml_sample1.xlsx
📣 20210304_storage_comparison
🤖 Downloaded snapd/snapsheet.xlsx
🚀 Renamed to snapd/20210412_toml_sample2.xlsx
```

---

# Next version

- いまのバージョンはデフォルトで設定ファイルを読み込むようになっている
- いま考えるとなんだかよく分からない仕様になっている
- 設定ファイルがない場合は、エラーがでて止まるように変更したい
- ついでに設定ファイルの内容を簡素化しようと考えている


```bash
$ snapsheets-next -h
```

```bash
$ snapsheets-next --url "https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"
📣 Add description here.
🤖 Downloaded snapshot.csv
🚀 Renamed snapshot.csv to _snapshot.csv
```

```python
>>> from snapsheets.next import Sheet
>>> url = https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"
>>> filename = "snapsheet.csv"
>>> description = "Get sample sheet"
>>> sheet = Sheet(url=url, filename=filename, description=description)
>>> sheet.snapshot()
📣 Get sample sheet
🤖 Downloaded snapsheet.csv
🚀 Renamed snapsheet.csv to 20220602_snapsheet.csv
```


---

# Other requirements

- Install ``wget`` if your system doesn't have them
- Make your spreadsheet available with shared link (OK with read-only)

---

# Documents

- https://qumanote.gitlab.io/snapsheets/

---

# PyPI package

- https://pypi.org/project/snapsheets/

![PyPI - Downloads](https://img.shields.io/pypi/dd/snapsheets?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dw/snapsheets?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/snapsheets?style=for-the-badge)
