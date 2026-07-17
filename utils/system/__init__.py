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

from utils.system.system import on_mobile

from . import system

try:
    from . import battery
except ImportError:
    battery = None
try:
    from . import notification
except ImportError:
    notification = None

if not on_mobile:
    from . import popup

# we were about to check how suitable imports gonna look with this setup.


# This shuts Ruff warnings.
__all__ = ["battery", "notification", "popup", "system"]
