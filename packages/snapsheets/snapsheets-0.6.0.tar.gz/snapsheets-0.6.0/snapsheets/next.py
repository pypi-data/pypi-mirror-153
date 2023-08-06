import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import pendulum
import tomli
from icecream import ic
from snapsheets import __version__


@dataclass
class Sheet:
    """
    A class for single spreadsheet information

    Parameters
    -------
    url: str
        URL of Google spreadsheet.
    filename: str o Path
        output filename.
    description: str
        description of a sheet.
    datefmt: str
        datetime prefix for backup filename.
    skip: bool
        set to True if you want to skip.
    """

    url: str
    filename: str
    description: str
    datefmt: str = "%Y%m%d"
    skip: bool = False

    def __post_init__(self) -> None:

        p = urlparse(self.url)
        if p.netloc not in ["docs.google.com"]:
            error = f"URL should start with 'https://docs.google.com/' : {self.url}"
            ic(error)
            sys.exit()

        p = Path(self.filename)
        self.suffix = p.suffix
        self.fmt = self.get_fmt()

        self.key = self.get_key()
        self.gid = self.get_gid()
        self.export_url = self.get_export_url()

    def get_fmt(self) -> str:
        """Get ``FORMAT`` from given filename.

        Returns
        -------
        str
            FORMAT ("xlsx", "ods", "csv", "tsv")
        """
        ok = ["xlsx", "ods", "csv", "tsv"]
        fmt = Path(self.filename).suffix.strip(".")
        if fmt not in ok:
            error = f"{fmt} is a wrong format. Select from {ok}."
            ic(error)
            sys.exit()
        return fmt

    def get_key(self) -> str:
        """Get ``KEY`` from given URL.

        Returns
        -------
        str
            KEY
        """
        p = urlparse(self.url)
        key = p.path.split("/")[3]
        return key

    def get_gid(self) -> str:
        """Get ``GID`` from given URL. Set ``gid=0`` if not found.

        Returns
        -------
        str
            GID
        """
        p = urlparse(self.url)
        gid = p.fragment.split("=")[1]
        return gid

    def get_export_url(self) -> str:
        """
        Generate export URL from given arguments.

        Returns
        -------
        str
            export URL
        """
        path = f"https://docs.google.com/spreadsheets/d/{self.key}/export"
        query = f"format={self.fmt}"
        if self.gid:
            query += f"&gid={self.gid}"
        url = f"{path}?{query}"
        return url

    def download(self) -> None:
        """
        Download spreadsheet.
        Filename can be modified in config file.
        """
        cmd = ["wget", "--quiet", "-O", self.filename, self.export_url]
        cmd = [str(c) for c in cmd if c]
        if self.skip:
            info = f"Skipped downloading {self.filename}."
            ic(info)
        else:
            subprocess.run(cmd)
            print(f"🤖 Downloaded {self.filename}")

    def backup(self) -> None:
        """
        Rename downloaded file with current datetime prefix.
        Prefix can be modified in config file.
        """

        now = pendulum.now().strftime(self.datefmt)
        savef = self.filename
        p = Path(self.filename)
        fname = f"{now}_{p.name}"
        movef = Path(p.parent, fname)
        if self.skip:
            info = f"Skipped renaming {self.filename}"
            ic(info)
        else:
            shutil.move(savef, movef)
            print(f"🚀 Renamed {savef} to {movef}")

    def snapshot(self) -> None:
        """Run ``download()`` & ``backup()``"""
        print(f"📣 {self.description}")
        self.download()
        self.backup()


@dataclass
class Book:
    fname: str = "config.toml"

    def __post_init__(self) -> None:
        p = Path(self.fname)
        if not p.exists():
            error = f"Unable to locate config file/directory. Perhaps you need to create a new config / file/directory. : {p}"
            ic(error)
            sys.exit()

        self.fnames = self.get_fnames()
        self.config = self.load_config()
        self.sheets = self.get_sheets()

    def get_fnames(self) -> list[Path]:
        """
        Get list of config files.

        Returns
        -------
        list[Path]
            list of config files
        """
        p = Path(self.fname)
        print(p)
        if p.is_file():
            return [p]

        fnames = sorted(p.glob("*.toml"))
        return fnames

    def load_config(self) -> dict:
        """Load configurations.

        Returns
        -------
        dict
            configuration in dict-object
        """
        config = {}
        for fname in self.fnames:
            with fname.open("rb") as f:
                _config = tomli.load(f)
                config.update(_config)
        return config

    def get_sheets(self) -> list[Sheet]:
        """
        Get list of sheets in configuration.

        Returns
        -------
        list[Sheet]
            list of Sheet objects
        """
        sheets = self.config.get("sheets")
        if sheets is None:
            return []

        sheets = []
        for sheet in self.config["sheets"]:
            url = sheet.get("url")
            filename = sheet.get("filename")
            desc = sheet.get("desc")
            datefmt = sheet.get("datefmt")
            skip = sheet.get("skip")
            _sheet = Sheet(
                url=url, filename=filename, description=desc, datefmt=datefmt, skip=skip
            )
            sheets.append(_sheet)
        return sheets

    def snapshots(self) -> None:
        """
        Take a snapshot of sheets.
        """

        for sheet in self.sheets:
            sheet.snapshot()


def cli() -> None:
    """
    Command Line Interface for snapsheets.
    """
    ic.enable()

    parser = argparse.ArgumentParser(description="snapsheets")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--config",
        metavar="config",
        default="config.toml",
        help="set config file or directory.",
    )
    group.add_argument("--url", metavar="url", help="set URL of Google spreadsheet.")
    parser.add_argument(
        "-o", metavar="filename", default="snapshot.csv", help="set output filename."
    )
    parser.add_argument(
        "-d",
        metavar="description",
        default="Add description here.",
        help="set description of a spreadsheet.",
    )
    parser.add_argument(
        "-t",
        metavar="format",
        default="",
        help="set datetime prefix for backup filename.",
    )
    parser.add_argument("-v", "--version", action="version", version=f"{__version__}")
    parser.add_argument("--skip", action="store_true", help="skip file")

    args = parser.parse_args()

    if args.url:
        sheet = Sheet(
            url=args.url,
            filename=args.o,
            description=args.d,
            datefmt=args.t,
            skip=args.skip,
        )
        sheet.snapshot()
    else:
        book = Book(args.config)
        book.snapshots()


if __name__ == "__main__":
    cli()
