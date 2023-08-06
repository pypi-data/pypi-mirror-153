# mypy: ignore-errors
"""Snapsheets

Wget Google spreadsheet

Usage:
    snapsheets [-h] [-n NAME] [--fmt FMT] [--saved SAVED] [--datefmt DATEFMT] url

Required:
    url                   copy and paste an URL of the Google spreadsheet

Options:
    -h, --help            show this help message and exit
    -n NAME, --name NAME  set stem for downloaded file (default: snapshot)
    --fmt FMT             set download format. (default: csv)
    --saved SAVED         set download directory. (default: ./snapd/)
    --datefmt DATEFMT     set backup prefix.
"""

import argparse
import logging
import logging.handlers
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pendulum
import toml
import yaml
from icecream import ic

ic.disable()

__version__ = "0.5.7"


@dataclass
class Logger:
    """Logger
    ロガーを扱うクラス
    """

    logd: str = "."
    logf: str = None
    size: int = 1000000
    backups: int = 10

    def setup(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        if self.logf is not None:
            logf = Path(self.logd) / self.logf
            self.logf = str(logf)
            fh = self.rotating_file_handler()
            logger.addHandler(fh)

        fh = self.stream_handler()
        logger.addHandler(fh)
        return logger

    def file_handler(self):
        fh = logging.FileHandler(self.logf)
        fh.setLevel(logging.DEBUG)
        fmt = (
            "%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s",
            "%Y-%m-%dT%H:%M:%S",
        )
        formatter = logging.Formatter(fmt)
        fh.setFormatter(formatter)
        return fh

    def stream_handler(self):
        fh = logging.StreamHandler()
        fh.setLevel(logging.INFO)
        fmt = "%(asctime)s - %(levelname)s - %(message)s", "%H:%M:%S"
        formatter = logging.Formatter(fmt)
        fh.setFormatter(formatter)
        return fh

    def rotating_file_handler(self):
        fh = logging.handlers.RotatingFileHandler(
            self.logf, maxBytes=size, backupCount=backups
        )
        fh.setLevel(logging.DEBUG)
        fmt = (
            "%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s",
            "%Y-%m-%dT%H:%M:%S",
        )
        formatter = logging.Formatter(fmt)
        fh.setFormatter(formatter)
        return fh


@dataclass
class Config:
    """Config
    設定を扱うクラス
    """

    confd: str = "./config/"
    saved: str = "./snapd/"
    logd: str = "./varlogs/"
    logf: str = None
    size: int = 1000000
    backups: int = 10

    def __post_init__(self) -> None:
        self.check_paths()
        self.load_config()
        return

    @staticmethod
    def check_path(path: str) -> str:
        """Check path

        ディレクトリが存在するかチェックする。
        ディレクトリが存在しない場合はカレントディレクトリに変更する。
        """
        _path = Path(path)
        if not _path.is_dir():
            path = "."
            warning = f"Directory {_path} not found. Switch to current directory."
            ic(warning)
        return path

    def check_paths(self) -> None:
        """Check paths

        デフォルトのパスが存在するかチェックする。
        パスがない場合はカレントディレクトリに変更する。
        """
        self.confd = self.check_path(self.confd)
        self.saved = self.check_path(self.saved)
        self.logd = self.check_path(self.logd)
        return

    def reset_config(self):
        self.confg = "./config/"
        self.saved = "./snapd/"
        self.logd = "./varlogs/"
        self.logf = None
        self.size = 1000000
        self.backups = 10

    def set_logger(self):
        logd = self.logd
        logf = self.logf
        size = log.size
        backups = log.backups
        logger = Logger(logd=logd, logf=logf, size=size, backups=backups)
        self.logger = logger.setup()
        return

    def get_fnames(self, pattern: str) -> List[Path]:
        p = Path(self.confd)
        fnames = sorted(p.glob(pattern))
        n = len(fnames)
        if n == 0:
            warning = f"No file found : {n} / {pattern}"
            ic(warning)
        return n, fnames

    def load_yaml(self) -> Dict[Any, Any]:
        config: Dict[Any, Any] = {}
        n, fnames = self.get_fnames("*.yml")
        info = f"Number of YAMLs: {n}"
        ic(info)
        for i, fname in enumerate(fnames):
            info = f"Loaded YAMLs [{i+1}/{n}]: {fname}"
            ic(info)
            with open(fname) as f:
                c = yaml.safe_load(f)
                config.update(c)
        return config

    def load_toml(self) -> Dict[Any, Any]:
        """Load configurations from TOMLs

        設定を読み込んだ辞書型をリターンする

        - 初めて読み込む場合 : TOMLを直接代入してOK
        - 2回目以降 : シートの情報だけ追記
        """
        config: Dict[Any, Any] = {}
        config.setdefault("tool", {})
        config.setdefault("sheets", {})
        debug = f"config.setdefault: {config}"
        ic(debug)
        n, fnames = self.get_fnames("*.toml")
        info = f"Number of TOMLs: {n}"
        ic(info)
        for i, fname in enumerate(fnames):
            info = f"==> Load TOMLs [{i+1}/{n}]: {fname}"
            ic(info)
            _loaded = toml.load(fname)
            config = self.update_config(config, _loaded)
        return config

    def update_config(self, config, new):
        """update config"""
        # debug = f"current config: {config}"
        # ic(debug)

        _sheets = new.get("sheets")
        _tool = new.get("tool")

        if _sheets is not None:
            config["sheets"].update(_sheets)
        if _tool is not None:
            config["tool"].update(_tool)

        # debug = f"updated config: {config}"
        # ic(debug)
        return config

    def load_config(self) -> None:
        config: Dict[Any, Any] = {}
        c = self.load_yaml()
        config.update(c)
        c = self.load_toml()
        config.update(c)
        self._config = config
        return

    def get_config(self):
        """Get pyproject-like configuration

        [tool.snapsheets]
        """
        if self._config.get("tool"):
            cfg = self._config.get("tool").get("snapsheets")
        else:
            cfg = self._config.get("snapsheets")

        if cfg is None:
            error = "None found. Check your configuration."
            ic(error)
            sys.exit(1)
        return cfg

    def sections(self) -> List[str]:
        return sorted(self._config.keys())

    def volumes(self) -> Optional[str]:
        _volumes = self._config.get("volumes")
        _cfg = self.get_config()
        if _cfg:
            _volumes = _cfg.get("volumes")
        return _volumes

    def options(self) -> Optional[str]:
        _options = self._config.get("options")
        _cfg = self.get_config()
        if _cfg:
            _options = _cfg.get("options")
        return _options

    def datefmt(self) -> Optional[str]:
        _datefmt = self._config.get("datefmt")
        _cfg = self.get_config()
        if _cfg:
            _datefmt = _cfg.get("datefmt")
        return _datefmt

    def sheets(self) -> Any:
        _sheets = self._config.get("sheets")
        return _sheets

    def sheet_names(self) -> Any:
        sheets = self.sheets()
        names = sorted(sheets.keys())
        return names

    def sheet(self, name: str) -> Any:
        sheets = self.sheets()
        return sheets.get(name)


@dataclass
class Sheet(Config):
    """Sheet
    スプレッドシート1枚を扱うクラス
    """

    url: Union[str, Optional[str]] = None
    key: Optional[str] = None
    gid: Optional[str] = None
    fmt: str = "xlsx"
    desc: Optional[str] = "snapsheet"
    fname: Optional[str] = None
    name: Optional[str] = "snapsheet"
    datefmt: Optional[str] = "%Y%m%dT%H%M%S"
    skip: bool = False

    def __post_init__(self) -> None:
        self.check_paths()
        self.set_name()
        self.set_savef()

        if self.url is not None:
            self.set_key_gid_from_url()
        else:
            msg = f"URL : {self.url} / key : {self.key}"
            ic(msg)
        return

    def set_name(self):
        warning = "fname will be deprecated. Use name instead."
        if self.fname is not None:
            self.name = self.fname
            ic(warning)
        return

    def set_savef(self) -> None:
        fmt = f".{self.fmt}"
        name = Path(self.name)
        self.savef = Path(self.saved) / name.with_suffix(fmt)
        return

    def set_key_gid_from_url(self) -> None:
        url = self.url
        if url.startswith("https://"):
            self.key = url.split("/")[-2]
            self.gid = url.split("#")[-1].split("=")[1]
        else:
            self.key = self.url
            self.gid = None
        return

    def info(self) -> None:
        ic(self.confd)
        ic(self.saved)
        ic(self.url)
        ic(self.key)
        ic(self.gid)
        ic(self.fmt)
        ic(self.desc)
        ic(self.name)
        ic(self.savef)
        ic(self.export_url())
        return

    def load(self, sheet: Dict[str, Any]) -> None:
        self.url = sheet.get("url")
        self.desc = sheet.get("desc")
        self.gid = sheet.get("gid")
        self.fmt = sheet.get("format")
        self.fname = sheet.get("stem")
        self.name = sheet.get("name")
        self.datefmt = sheet.get("datefmt")
        return

    def export_url(self) -> str:
        if self.key is None:
            self.set_key_gid_from_url()
            msg = f"Got key from URL : {self.url}"
            ic(msg)

        self.check_fmt()
        fmt = self.fmt
        key = self.key
        gid = self.gid
        path = f"https://docs.google.com/spreadsheets/d/{key}/export"
        query = f"format={fmt}"
        if not str(gid) == "None":
            query += f"&gid={gid}"
        url = f"{path}?{query}"
        return url

    def check_fmt(self) -> None:
        fmt = self.fmt
        ok = ["xlsx", "ods", "csv", "tsv"]
        if fmt not in ok:
            msg = f"{fmt} is a wrong format. Select from {ok}. ... Exit."
            ic(msg)
            sys.exit()
        return

    def download(self) -> str:
        url = self.export_url()
        savef = str(self.savef)
        cmd = ["wget", "--quiet", "-O", savef, url]
        cmd = [str(c) for c in cmd if c]
        if self.skip:
            info = f"Skipped downloading {savef}"
            ic(info)
        else:
            subprocess.run(cmd)
            print(f"🤖 Downloaded {savef}")
        return savef

    def backup(self) -> str:
        datefmt = self.datefmt
        now = pendulum.now().strftime(datefmt)

        fmt = f".{self.fmt}"
        fname = Path(f"{now}_{self.name}")
        movef = Path(self.saved) / fname.with_suffix(fmt)
        savef = str(self.savef)
        movef = str(movef)
        if self.skip:
            info = f"Skipped renaming {savef}"
            ic(info)
        else:
            shutil.move(savef, movef)
            print(f"🚀 Renamed to {movef}")
        return str(movef)

    def snapshot(self):
        print(f"📣 {self.desc}")
        self.download()
        movef = self.backup()
        return movef


@dataclass
class Book(Config):
    """Book
    複数のシートを扱うクラス
    """

    sheets: List[Sheet] = field(default_factory=list)

    def __post_init__(self):
        self.check_paths()
        self.load_config()

        names = self.get_sheet_names()
        for name in names:
            _sheet = self.make_sheet(name)
            self.add_sheet(_sheet)
        return

    def get_sheet_names(self):
        names = sorted(self._config.get("sheets").keys())
        return names

    def get_sheet_dict(self, name: str):
        sheet = self._config.get("sheets").get(name)
        return sheet

    def make_sheet(self, name: str) -> Sheet:
        """
        Make Sheet object from configuration file

        Parameters
        ----------
        name : str
            Name of sheet in configuration file

        Returns
        -------
        Sheet
            Sheet
        """
        _sheet = self.get_sheet_dict(name)
        url = _sheet.get("url")
        sheet = Sheet(
            confd=self.confd,
            saved=self.saved,
            logd=self.logd,
            url=url,
        )
        sheet.fname = _sheet.get("name")
        sheet.name = _sheet.get("name")
        sheet.desc = _sheet.get("desc")
        sheet.fmt = _sheet.get("format")
        sheet.datefmt = _sheet.get("datefmt")
        sheet.skip = _sheet.get("skip")
        return sheet

    def add_sheet(self, sheet: Sheet) -> None:
        """
        Add Sheet object to Book object.
        Skip when sheet.skip = True.

        Parameters
        ----------
        sheet : Sheet
            設定ファイルから作成した Sheet オブジェクト
        """
        if sheet.skip:
            info = f"Skipped : {sheet.name}"
        else:
            info = f"Add sheet : {sheet.name}"
            self.sheets.append(sheet)
        ic(info)
        return

    def snapshots(self) -> None:
        """
        Take snapshots of all sheet in the Book
        """
        _sheets = self.sheets
        n = len(_sheets)
        for i, sheet in enumerate(_sheets):
            name = sheet.name
            desc = sheet.desc
            info = f"[{i+1}/{n}] {name} - {desc}"
            ic(info)
            sheet.snapshot()
        return

    def export_urls(self) -> None:
        """
        Show export URLs
        """
        _sheets = self.sheets
        n = len(_sheets)
        for i, sheet in enumerate(_sheets):
            url = sheet.export_url()
            info = f"[{i+1}/{n}] {url}"
            print(info)
        return


def cli() -> None:
    """
    Command Line Interface for Snapsheets
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", default="./config/", help="set config directory (default: ./config/"
    )
    parser.add_argument("--url", help="copy and paste an URL of the Google spreadsheet")
    parser.add_argument("-v", "--version", action="store_true", help="show version")
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit()

    if args.url:
        sheet = Sheet(url=args.url)
        sheet.snapshot()
    else:
        book = Book(confd=args.config)
        book.snapshots()

    return


if __name__ == "__main__":

    cli()
