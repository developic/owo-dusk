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
import shutil
from utils.colors import COLORS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ensure_files():
    created = []
    os.makedirs(os.path.join(BASE_DIR, "config"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "utils", "data"), exist_ok=True)
    stats_path = os.path.join(BASE_DIR, "utils", "data", "stats.json")
    if not os.path.exists(stats_path):
        with open(stats_path, "w") as f:
            f.write("{}")
        created.append(os.path.relpath(stats_path, BASE_DIR))

    template_files = {
        os.path.join(BASE_DIR, "templates", "tokens.txt"):
            os.path.join(BASE_DIR, "tokens.txt"),

        os.path.join(BASE_DIR, "templates", "settings.json"):
            os.path.join(BASE_DIR, "config", "settings.json"),

        os.path.join(BASE_DIR, "templates", "global_settings.json"):
            os.path.join(BASE_DIR, "config", "global_settings.json"),

        os.path.join(BASE_DIR, "templates", "captcha.toml"):
            os.path.join(BASE_DIR, "config", "captcha.toml"),

        os.path.join(BASE_DIR, "templates", "danger.toml"):
            os.path.join(BASE_DIR, "config", "danger.toml"),

        os.path.join(BASE_DIR, "templates", "misc.json"):
            os.path.join(BASE_DIR, "config", "misc.json"),

        os.path.join(BASE_DIR, "templates", "webhookContent.json"):
            os.path.join(BASE_DIR, "config", "webhookContent.json"),

        os.path.join(BASE_DIR, "templates", "instructions"):
            os.path.join(BASE_DIR, "config", "instructions"),

        os.path.join(BASE_DIR, "templates", "weekly_runtime.json"):
            os.path.join(BASE_DIR, "utils", "data", "weekly_runtime.json"),
    }

    for src, dst in template_files.items():
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            created.append(os.path.relpath(dst, BASE_DIR))

    return created
