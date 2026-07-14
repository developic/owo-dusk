# This file is part of owo-dusk.
#
# Copyright (c) 2024-present EchoQuill
#
# Portions of this file are based on code by EchoQuill, licensed under the
# GNU General Public License v3.0 (GPL-3.0).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import os

import requests

CATBOX_API = "https://litterbox.catbox.moe/resources/internals/api.php"


def upload_file(file_path: str) -> str | None:
    """
    Uploads file to catbox.moe and returns url from 
    provided file path
    """
    try:
        data = {"reqtype": "fileupload",
        "time": "72h"}

        with open(file_path, "rb") as f:
            files = {
                "fileToUpload": (os.path.basename(file_path), f, "application/octet-stream")
            }
            response = requests.post(CATBOX_API, data=data, files=files, timeout=2)

        return response.text.strip() if response.status_code == 200 else None
    except Exception:
        # Its fine if this fails, no need to error.
        return None
