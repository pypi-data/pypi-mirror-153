import os
import math
import shutil
import logging
import argparse
import subprocess
from pathlib import Path

import guessit
from pprint import pprint
from peewee import SqliteDatabase, CharField, Model, IntegerField
from jinja2 import Template

import ptpapi
from ptpapi.sites.ptpimg import PTPIMG
from ptpapi.config import config

db = SqliteDatabase("upload.db")


class UploadException(Exception):
    pass


class Release(Model):
    name = CharField(unique=True)  # Uniquely identifies the path in base_dir
    title = CharField(null=True)
    year = IntegerField(null=True)
    ptp_movie_id = CharField(null=True)  # Used to skip having to add movie info
    image = CharField(null=True)  # Poster
    container = CharField(null=True)
    codec = CharField(null=True)
    source = CharField(null=True)
    resolution = CharField(null=True)
    upload_type = CharField(null=True)
    remaster_title = CharField(null=True)
    subtitles = CharField(null=True)

    class Meta:
        database = db


class PtpUpload(object):
    """Currently only handles a single file"""

    def __init__(self, path):
        logger = logging.getLogger()
        self.path = Path(path).resolve()
        if not self.path.exists():
            logger.critical("Path %s does not exist", path)
        release_name = self.path.stem
        self.basedir = Path(config.get("Upload", "basedir")).joinpath(release_name)
        if not self.basedir.is_dir():
            self.basedir.mkdir()
        self.api = ptpapi.login()
        self.upload_info = self.api.upload_info()  # Cache for later use
        db.connect()
        db.create_tables([Release])
        release = Release.select().where(Release.name == release_name)
        if release.exists():
            self.release = release.get()
        else:
            self.release = Release(name=release_name)
            self.release.save()

    def upload(self):
        self.take_screenshots()
        self.create_data()
        self.build_upload_data()
        self.validate_upload_data()
        self.mktorrent()
        self.submit()

    def submit(self):
        # description = self.create_description()
        torrent_path = self.basedir.joinpath("PTP {}.torrent".format(self.release.name))
        description = self.create_description()
        params = {"groupid": str(self.release.ptp_movie_id)}
        data = {
            "release_desc": description,
            "source": self.release.source,
            "resolution": self.release.resolution,
            "codec": self.release.codec,
            "container": self.release.container,
            "subtitles": self.release.subtitles.split(","),
            "remaster_title": self.release.remaster_title,
        }

        pprint(data)
        print("Description::")
        print("---")
        print(description)
        print("---")
        return
        print("Source: {}".format(self.release.source))
        print("Torrent: {}".format(torrent_path))
        print("Subtitles: {}".format(self.release.subtitles))
        print("Remaster Title: {}".format(self.release.remaster_title))
        return
        print("Existing torrents::")
        print("---")
        for t in ptpapi.movie.Movie(ID=str(self.release.ptp_movie_id))["Torrents"]:
            print(t["ReleaseName"])
        print("---")

    def build_upload_data(self):
        # Guessit stuff
        guessed = guessit.guessit(self.release.name)
        if not self.release.ptp_movie_id:
            if not self.release.title and "title" in guessed:
                self.release.title = guessed["title"]
            if not self.release.year and "year" in guessed:
                self.release.year = guessed["year"]
        if not self.release.container and "container" in guessed:
            self.release.container = guessed["container"]
        if not self.release.source and "source" in guessed:
            self.release.source = guessed["source"]
        if not self.release.codec and "video_codec" in guessed:
            if self.release.codec == "h.264":
                raw_video_codec = guessit.guessit(
                    self.release.name, options={"advanced": True}
                )["video_video_codec"].raw
                if raw_video_codec == "x264":
                    self.release.codec = "x264"
            else:
                self.release.codec = guessed["video_codec"]
        # Mediainfo stuff
        mediainfo = self.read_mediainfo()
        for l in mediainfo.split("\n"):
            if l.startswith("Writing library") and "x264" in l.split(" "):
                self.release.codec = "x264"
        # Formatting
        self.release.save()

    def validate_upload_data(self):
        # Existence checks
        must_exist = ["source", "subtitles"]
        if not self.release.ptp_movie_id:
            must_exist += ["title", "year", "image", "imdb_id"]
        for f in must_exist:
            if not getattr(self.release, f):
                raise UploadException("Required field '{}' not set".format(f))
        # Non-other checks
        for f in ["container", "codec", "source", "resolution"]:
            if (
                getattr(self.release, f) is not None
                and getattr(self.release, f) not in self.upload_info[f + "s"]
            ):
                raise UploadException(
                    "Unknown value '{}' for field '{}'".format(
                        getattr(self.release, f), f
                    )
                )
        print("OK: " + self.release.name)

    def create_data(self):
        # "Copy" data from target to base path
        data_dir = self.basedir.joinpath("data")
        if not data_dir.is_dir():
            data_dir.mkdir()
        if self.path.is_file() and not data_dir.joinpath(self.path.name).exists():
            self.path.link_to(data_dir.joinpath(self.path.name))
        elif self.path.is_dir():
            shutil.copytree(self.path, data_dir, copy_function=os.link)

    def mktorrent(self):
        logger = logging.getLogger()
        data_dir = self.basedir.joinpath("data")
        torrent_path = self.basedir.joinpath("PTP {}.torrent".format(self.release.name))
        if not torrent_path.is_file():
            data_size = sum(
                f.stat().st_size for f in data_dir.glob("**/*") if f.is_file()
            )
            piece_size = max(min(int(math.log(data_size) / math.log(2)) - 9, 24), 15)
            cmd = [
                "mktorrent",
                "-p",
                "-s",
                "PTP",
                "-l",
                str(piece_size),
                "-o",
                str(torrent_path),
                "-a",
                self.upload_info["announce"],
                str(list(data_dir.iterdir())[0]),
            ]
            result = subprocess.run(cmd)
            if result.returncode > 0:
                logger.debug(" ".join(cmd))
                raise RuntimeError("mktorrent returned {}".format(result.returncode))

    def validated_allowed(self):
        pass

    def create_description(self):
        template_str = """{% for name, data in files.items() %}
{{ data.mediainfo }}
{% for s in data.screenshots %}
[img]{{ s }}[/img]
{% endfor %}
{% endfor %}"""
        template = Template(template_str)
        files = {}
        files[self.path.name] = {
            "mediainfo": self.read_mediainfo(),
            "screenshots": self.upload_screenshots(),
        }
        return template.render(release_name=self.release.name, files=files)

    def build_data_dir(self):
        data_dir = self.basedir.joinpath("data")
        if not data_dir.is_dir():
            data_dir.mkdir()
        if not data_dir.joinpath(self.path.name).is_file():
            self.path.link_to(data_dir.joinpath(self.path.name))

    def read_mediainfo(self):
        output = self.basedir.joinpath("mediainfo")
        if not output.is_dir():
            output.mkdir()
        result = subprocess.run(["mediainfo", str(self.path)], stdout=subprocess.PIPE)
        if result.returncode > 0:
            raise RuntimeError("mediainfo returned {}".format(returncode))
        return result.stdout.decode()

    def take_screenshots(self, num=5):
        logger = logging.getLogger()
        screenshot_dir = self.basedir.joinpath("screenshots")
        if not screenshot_dir.is_dir():
            screenshot_dir.mkdir()
        for i in range(0, 50, 50 // num):
            output = self.basedir.joinpath("screenshots", "{}.png".format(i))
            if not output.exists():
                cmd = [
                    "mpv",
                    "--no-config",
                    "--no-audio",
                    "--no-sub",
                    "--frames=1",
                    "--start={}%".format(i),
                    "--screenshot-format=png",
                    "--screenshot-png-compression=9",
                    "--vf=lavfi=[scale='max(iw,iw*sar)':'max(ih/sar,ih)']",
                    "--o={}".format(output),
                    str(self.path),
                ]
                result = subprocess.run(cmd)
                if result.returncode > 0:
                    logger.debug(" ".join(cmd))
                    raise RuntimeError("mpv returned {}".format(result.returncode))

    def upload_screenshots(self):
        screenshots = []
        img_host = PTPIMG()
        for img in self.basedir.joinpath("screenshots").glob("*.png"):
            screenshots.append(img_host.upload(str(img)))
        return screenshots


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Idempotent upload utility")
    parser.add_argument("origin", help="A source to upload")
    parser.add_argument("-m", "--ptp-movie-id")
    parser.add_argument("--container")
    parser.add_argument("--year")
    parser.add_argument("--source")
    parser.add_argument("--remaster-title")
    parser.add_argument("--subtitles", default="44")
    parser.add_argument("--type", default="Feature Film")
    parser.add_argument(
        "--debug",
        help="Print lots of debugging statements",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Be verbose",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    parser.add_argument(
        "-q",
        "--quiet",
        help="Hide most messages",
        action="store_const",
        dest="loglevel",
        const=logging.CRITICAL,
    )

    parser.add_argument("--release-name", default=None, help="Release name")
    parser.add_argument("-i", "--id", help="ID, either PTP or IMDb", required=True)

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    u = PtpUpload(args.origin)
    for field in [
        "ptp_movie_id",
        "container",
        "source",
        "year",
        "subtitles",
        "remaster_title",
    ]:
        if getattr(args, field):
            setattr(u.release, field, getattr(args, field))
    u.upload()
    db.close()
