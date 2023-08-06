# mypy: ignore-errors
"""
snapsheets.config.py
"""
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pendulum
import toml
import yaml
from deprecated import deprecated
from icecream import ic

_config = "Run set_default_config() first"


@deprecated(version="0.2.3", reason="Will be removed.")
def get_config() -> Any:
    """
    Return config

    Returns
    -------
    dict
        current config
    """
    return _config


@deprecated(
    version="0.2.3",
    reason="Will be removed. Testing migration to config.Config.load_config()",
)
def set_config(fname: str) -> Any:
    """
    Set config

    Parameters
    ----------
    fname : str
        filename of config in yaml format

    Returns
    -------
    dict
        config
    """
    with open(fname, "r") as f:
        config = yaml.safe_load(f)
    return config


@deprecated(
    version="0.2.3",
    reason="Will be removed. Testing migration to config.Config.load_config()",
)
def set_default_config() -> Any:
    """
    Set default config

    Returns
    -------
    dict
        config
    """
    here = Path(__file__).resolve().parent
    fname = str(here / "config.yml")
    return set_config(fname)


@deprecated(
    version="0.2.3",
    reason="Will be removed. Testing migration to config.Config.load_config()",
)
def add_config(fname: str) -> Any:
    """
    Update config

    Parameters
    ----------
    fname : str
        filename of config in yaml format

    Returns
    -------
    dict
        updated config
    """
    config = get_config()
    add = set_config(fname)
    config.update(add)
    return config


@deprecated(version="0.2.3", reason="Will be removed.")
def show_config() -> None:
    """
    Show config
    """
    import pprint

    config = get_config()
    pprint.pprint(config)
    return


@deprecated(
    version="0.2.3",
    reason="Will be removed. Testing migration to config.Config.volumes()",
)
def volumes() -> Any:
    """
    List volumes

    Returns
    -------
    dict
        list of volumes
    """
    config = get_config()
    return config.get("volumes")


@deprecated(
    version="0.2.3",
    reason="Will be removed. Testing migration to config.Config.options()",
)
def options() -> Any:
    """
    List options

    Returns
    -------
    dict
        list of options
    """
    config = get_config()
    return config.get("options")


@deprecated(
    version="0.2.3",
    reason="Will be removed. Testing migration to config.Config.sheets()",
)
def sheets() -> Any:
    """
    List spreadsheets

    Returns
    -------
    list
        list of spreadsheets
    """
    config = get_config()
    return list(config.get("sheets").keys())


@deprecated(
    version="0.2.2",
    reason="Will be removed. Testing migration to config.Config.sheet(name)",
)
def sheet(name: str) -> Any:
    """
    Show spreadsheet info

    Parameters
    ----------
    name : str
        name of spreadsheet

    Returns
    -------
    dict
        spreadsheet info
    """
    config = get_config()
    return config.get("sheets").get(name)


# Set default config
_config = set_default_config()


@deprecated(version="0.4.0", reason="Will be removed. Use core.Config")
@dataclass
class Config:
    path: str = ""
    confd: str = "."
    saved: str = "."

    def __post_init__(self) -> None:
        ic("__post_init__")
        self.path = self.confd
        return

    def get_fnames(self, fmt: str) -> List[Path]:
        p = Path(self.path)
        fnames = sorted(p.glob(fmt))
        return fnames

    def load_yaml(self) -> Dict[Any, Any]:
        config: Dict[Any, Any] = {}
        fnames = self.get_fnames("*.yml")
        n = len(fnames)
        ic("Loaded YAML files: ", n)
        for fname in fnames:
            with open(fname) as f:
                c = yaml.safe_load(f)
                config.update(c)
        return config

    def load_toml(self) -> Dict[Any, Any]:
        config: Dict[Any, Any] = {}
        fnames = self.get_fnames("*.toml")
        n = len(fnames)
        ic("Loaded TOML files: ", n)
        for fname in fnames:
            c = toml.load(fname)
            config.update(c)
        return config

    def load_config(self) -> Dict[Any, Any]:
        config: Dict[Any, Any] = {}
        c = self.load_yaml()
        config.update(c)
        c = self.load_toml()
        config.update(c)
        self.config = config

        # self.volumes = config.get("volumes")
        # self.options = config.get("options")
        # self.datefmt = config.get("datefmt")
        return config

    def sections(self) -> List[str]:
        return sorted(self.config.keys())

    def volumes(self) -> Optional[str]:
        return self.config.get("volumes")

    def options(self) -> Optional[str]:
        return self.config.get("options")

    def datefmt(self) -> Optional[str]:
        return self.config.get("datefmt")

    def sheets(self) -> Any:
        return self.config.get("sheets")

    def sheet_names(self) -> Any:
        sheets = self.sheets()
        names = sorted(sheets.keys())
        return names

    def sheet(self, name: str) -> Any:
        sheets = self.sheets()
        return sheets.get(name)


@deprecated(version="0.4.0", reason="Will be removed. Use core.Sheet")
@dataclass
class Sheet(Config):
    url: Union[str, Optional[str]] = None
    key: Optional[str] = None
    gid: Optional[str] = None
    fmt: str = "xlsx"
    desc: Optional[str] = None
    fname: Optional[str] = "snapshot"

    def __post_init__(self) -> None:
        fmt = f".{self.fmt}"
        fname = Path(self.fname)
        self.savef = Path(self.saved) / fname.with_suffix(fmt)

        if self.url is not None:
            self.set_key_gid_from_url()
        else:
            msg = f"URL : {self.url} / key : {self.key}"
            ic(msg)
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
        ic(self.fname)
        ic(self.savef)
        ic(self.export_url())
        return

    def load(self, sheet: Dict[str, Any]) -> None:
        self.url = sheet.get("url")
        self.desc = sheet.get("desc")
        self.gid = sheet.get("gid")
        self.fmt = sheet.get("format")
        self.fname = sheet.get("stem")
        self.datefmt = sheet.get("datefmt")
        return

    def export_url(self):
        if self.key is None:
            self.get_key_gid_from_url()
            msg = f"Got key from URL : {self.url}"
            ic(msg)

        fmt = self.fmt
        key = self.key
        gid = self.gid

        ok = ["xlsx", "ods", "csv", "tsv"]
        if fmt not in ok:
            msg = f"{fmt} is a wrong format. Select from {preset}. ... Exit."
            ic(msg)
            sys.exit()

        path = f"https://docs.google.com/spreadsheets/d/{key}/export"
        query = f"format={fmt}"
        if not str(gid) == "None":
            query += f"&gid={gid}"
        url = f"{path}?{query}"
        return url

    def download(self) -> str:
        url = self.export_url()
        savef = str(self.savef)
        cmd = ["wget", "--quiet", "-O", savef, url]
        cmd = [str(c) for c in cmd if c]
        subprocess.run(cmd)
        print(f"🚀 {savef}")
        return savef

    def backup(self) -> str:
        datefmt = "%Y%m%dT%H%M%S"
        now = pendulum.now().strftime(datefmt)

        fmt = f".{self.fmt}"
        fname = Path(f"{now}_{self.fname}")
        movef = Path(self.saved) / fname.with_suffix(fmt)

        savef = str(self.savef)
        movef = str(movef)
        shutil.move(savef, movef)
        print(f"🚚 {movef}")
        return movef

    def snapshot(self):
        print(f"📝 {self.desc}")
        self.download()
        movef = self.backup()
        return movef


@deprecated(version="0.4.0", reason="Will be removed. Use core.Book")
@dataclass
class Book(Sheet):
    def export_url(self):
        ok = ["xlsx", "ods"]
        if fmt not in ok:
            msg = f"{fmt} is a wrong format. Select from {preset}. ... Exit."
            ic(msg)
            sys.exit()
        path = f"https://docs.google.com/spreadsheets/d/{key}/export"
        query = f"format={fmt}"
        if not str(gid) == "None":
            query += f"&gid={gid}"
        url = f"{path}?{query}"
        return url
