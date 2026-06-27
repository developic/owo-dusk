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

import time


def generate_nonce():
    """Generate a Discord-style snowflake nonce."""
    now = int(time.time() * 1000)
    a = now - 1420070400000
    r = a << 22
    return str(r)


def check_list_index(idx: int, item: list):
    if 0 <= idx < len(item):
        return True, item[idx]
    return False, None
