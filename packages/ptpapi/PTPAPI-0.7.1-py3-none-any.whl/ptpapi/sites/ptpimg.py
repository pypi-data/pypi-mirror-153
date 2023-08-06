from pathlib import Path

import requests

from ptpapi.config import config


class PTPIMG(object):
    def __init__(self, api_key=None):
        self.api_key = api_key or config.get("PTPIMG", "api_key")

    def upload(self, source):
        data = {"api_key": self.api_key}
        files = {}
        if Path(source).exists():
            files["file-upload"] = Path(source).open("rb")
        else:
            data["link-upload"] = source
        response = requests.post("https://ptpimg.me/upload.php", data=data, files=files)
        response.raise_for_status()
        try:
            rjson = response.json()[0]
            return "https://ptpimg.me/{0}.{1}".format(rjson["code"], rjson["ext"])
        except (ValueError, KeyError):
            logger.exception(
                "Got an exception while loading JSON response from ptpimg.me. Response: '{0}'.".format(
                    str(response.text())
                )
            )
            raise
