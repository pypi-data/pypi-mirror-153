# mypy: ignore-errors

"""
Google Spreadsheet を wget を使ってダウンロードする
"""

import datetime
import logging
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional, Union

import pendulum
from deprecated import deprecated
from icecream import ic

from . import config, log

# import logging


# _logger = log.chandler(__name__, logging.INFO)


@deprecated(version="0.3.0", reason="Will be removed.")
def make_url(key: str, gid: str, fmt: str) -> str:
    """
    Make spreadsheet URL for export

    Parameters
    ----------
    key : str
        spredsheet ID
    gid : int or None
        sheet ID
    fmt : str
        save format

    Returns
    -------
    str
        exported URL
    """
    _formats = ["xlsx", "ods", "pdf", "zip", "csv", "tsv"]
    if fmt not in _formats:
        # _logger.error(f'"{fmt}" is a wrong format. Pick from {_formats}. ... Exit.')
        sys.exit()

    path = f"https://docs.google.com/spreadsheets/d/{key}/export"
    query = f"format={fmt}"
    if not str(gid) == "None":
        query += f"&gid={gid}"
    url = f"{path}?{query}"
    return url


@deprecated(version="0.3.0", reason="Will be removed.")
def get_url(name: str) -> str:
    """
    Get spreadsheet URL for export with name

    Parameters
    ----------
    name : str
        name of spreadsheet

    Returns
    -------
    str
        spreadsheet URL for export
    """
    sheets = config.sheets()
    if name not in sheets:
        # _logger.error(f'"{name}" is not in sheet list. Pick from {sheets}. ... Exit.')
        sys.exit()
    sheet = config.sheet(name)
    key = sheet.get("key")
    gid = sheet.get("gid")
    fmt = sheet.get("format")
    return make_url(key, gid, fmt)


@deprecated(version="0.3.0", reason="Will be removed.")
def get_cmd(name: str, fname: Union[str, Path], by: str) -> List[Any]:
    """
    Get download command list

    Pass this list to subprocess

    Parameters
    ----------
    name : str
        name of spreadsheet
    fname : str
        download filename
    by : str
        wget or curl

    Returns
    -------
    list
        commands passed to subprocess
    """
    commands = ["wget", "curl"]
    if by not in commands:
        # _logger.error(f'"{by}" is not in command list. Pick from {commands}. ... Exit.')
        sys.exit()

    url = get_url(name)
    options = config.options().get(by)
    if by == "wget":
        cmd = ["wget", options, "-O", fname, url]
    else:
        url = f'"{url}"'
        cmd = ["curl", options, "-o", fname, "-L", url]

    # drop None value in cmd
    cmd = [str(c) for c in cmd if c]
    msg = (" ").join(cmd)
    # _logger.debug(msg)
    return cmd


@deprecated(
    version="0.3.0",
    reason="Will be removed. Switch to core.Sheet.download",
)
def download(
    name: str, stem: str = "snapshot", snapd: str = ".", by: str = "wget"
) -> Union[str, Path]:
    """
    Download spreadsheet

    Parameters
    ----------
    name : str
        name of spreadsheet
    stem : str
        download filename
    by : str
        wget or curl

    Returns
    -------
    str
        downloaded filename
    """
    # _logger.info(f"ダウンロードするよ : {name}")
    fmt = config.sheet(name).get("format")
    fname = Path(snapd) / f"{stem}.{fmt}"
    cmd = get_cmd(name, fname, by)
    subprocess.run(cmd)
    # _logger.info(f"ダウンロードしたよ : {fname}")
    return fname


@deprecated(version="0.3.0", reason="Will be removed. Switch to core.Sheet.backup")
def backup(
    src: Union[str, Path],
    stem: Optional[Any] = None,
    snapd: str = ".",
    datefmt: str = "%Y%m%dT%H%M%S",
) -> Union[str, Path]:
    """
    Backup snapshot

    Parameters
    ----------
    src : str
        source file
    datefmt : str, optional
        dateformat, by default '%Y%m%dT%H%M%S'
    stem : str, optional
        backup filename, by default None
    snapd : str, optional
        backup directory, by default '.'

    Returns
    -------
    str
        backedup filename
    """
    src = Path(src)
    fmt = src.suffix
    # stem を指定していない場合は、srcから取得
    if not stem:
        stem = src.stem
    dt = datetime.datetime.now().strftime(datefmt)
    fname = Path(snapd) / f"{dt}_{stem}{fmt}"
    # _logger.info(f"移動するよ : {src.name}")
    # shutil.copy(src, dst)
    shutil.move(str(src), fname)
    # _logger.info(f"移動したよ : {fname.name}")
    return fname


@deprecated(
    version="0.3.0",
    reason="Will be removed. Switch to core.Sheet.snapshot",
)
def snapshot(
    name: str,
    stem: str = "snapshot",
    snapd: str = ".",
    datefmt: str = "%Y%m%dT%H%M%S",
    by: str = "wget",
) -> Union[str, Path]:
    """
    Make snapshot (download & backup) of spreadsheet

    Parameters
    ----------
    name : str
        name of spreadsheet
    by : str
        wget or curl
    datefmt : str, optional
        dateformat, by default '%Y%m%dT%H%M%S'
    stem : str, optional
        download filename, by default 'snapshot'
    snapd : str, optional
        download directory, by default '.'

    Returns
    -------
    str
        download filename
    """
    fname = download(name, stem=stem, snapd=snapd, by=by)
    fname = backup(fname, stem=stem, snapd=snapd, datefmt=datefmt)
    return fname


@deprecated(version="0.3.0", reason="Will be removed")
def get(name: str, by: str) -> Union[str, Path]:
    """
    Get snapshot

    返り値をスナップショットのファイル名にしてあるので、
    そのまま pandas などで読み込んで使うことができる。

    Parameters
    ----------
    name : str
        name of spreadsheet
    by : str
        wget or curl

    Returns
    -------
    str
        filename of snapshot
    """
    # Config : volume
    v = config.volumes()
    snapd = v.get("snapd")
    # Config : sheet
    s = config.sheet(name)
    stem = s.get("stem")
    datefmt = s.get("datefmt")
    fname = snapshot(name, stem=stem, snapd=snapd, datefmt=datefmt, by=by)
    return fname


@deprecated(
    version="0.4.0",
    reason="Will be removed. Use core.Sheet class.",
)
@dataclass
class Gsheet:
    path: str = ""

    @deprecated(
        version="0.4.0",
        reason="Will be removed",
    )
    def load_config(self) -> None:
        cfg = config.Config()
        cfg.path = self.path
        cfg.load_config()
        self.config = cfg
        return

    @deprecated(
        version="0.4.0",
        reason="Will be removed",
    )
    def get_url(self, name: str) -> str:
        sheet = self.config.sheet(name)
        fmt = sheet.get("format")
        key = sheet.get("key")
        gid = sheet.get("gid")

        _formats = ["xlsx", "ods", "pdf", "zip", "csv", "tsv"]
        if fmt not in _formats:
            _logger.error(f'"{fmt}" is a wrong format. Pick from {_formats}. ... Exit.')
            sys.exit()

        path = f"https://docs.google.com/spreadsheets/d/{key}/export"
        query = f"format={fmt}"
        if not str(gid) == "None":
            query += f"&gid={gid}"
        url = f"{path}?{query}"
        return url

    @deprecated(
        version="0.4.0",
        reason="Will be removed",
    )
    def get_snapd(self) -> str:
        volumes = self.config.volumes()
        return volumes.get("snapd")

    @deprecated(
        version="0.4.0",
        reason="Will be removed",
    )
    def get_fname(self, name: str) -> Path:
        snapd = self.get_snapd()
        sheet = self.config.sheet(name)
        stem = sheet.get("stem")
        fmt = sheet.get("format")
        fname = Path(snapd) / f"{stem}.{fmt}"
        return fname

    @deprecated(
        version="0.4.0",
        reason="Will be removed",
    )
    def wget(self, name: str) -> Path:
        options = self.config.options().get("wget")
        fname = self.get_fname(name)
        url = self.get_url(name)
        cmd = ["wget", options, "-O", fname, url]
        cmd = [str(c) for c in cmd if c]
        try:
            subprocess.run(cmd)
            # _logger.info(f"🚀 {fname}")
        except FileNotFoundError as e:
            msg = f"No {e.filename} found. Please install 'wget'."
            # _logger.critical(msg)
            msg = f"For macOS, run 'brew install wget' if you are Homebrewer."
            # _logger.critical(msg)
            sys.exit()
        return fname

    @deprecated(
        version="0.4.0",
        reason="Will be removed. Switch to core.Sheet.download",
    )
    def download(self, name: str) -> Path:
        fname = self.wget(name)
        return fname

    @deprecated(
        version="0.4.0",
        reason="Will be removed. Switch to core.Sheet.backup",
    )
    def backup(self, name: str) -> Path:
        snapd = self.get_snapd()
        src = Path(self.get_fname(name))
        stem = src.stem
        fmt = src.suffix
        datefmt = self.config.sheet(name).get("datefmt")
        dt = pendulum.now().strftime(datefmt)
        fname = Path(snapd) / f"{dt}_{stem}{fmt}"
        # shutil.copy(src, dst)
        shutil.move(str(src), str(fname))
        # _logger.info(f"🚚  {fname}")
        return fname

    @deprecated(
        version="0.4.0",
        reason="Will be removed. Switch to core.Sheet.snapshot",
    )
    def snapshot(self, name: str) -> Union[str, Path]:
        """
        対象シートを指定してスナップショットを保存する
        """
        desc = self.config.sheet(name).get("desc")
        # _logger.info(f"📝 {name} : {desc}")
        fname = self.download(name)
        fname = self.backup(name)
        return fname

    @deprecated(
        version="0.4.0",
        reason="Will be removed. Switch to core.Book.snapshots",
    )
    def snapshots(self):
        """
        設定ファイルに記載した全てのシートのスナップショットを保存する
        """
        names = self.config.sheet_names()
        fnames = []
        for name in names:
            # _logger.info("-" * 88)
            fname = self.snapshot(name)
            fnames.append(fname)
        return fnames
