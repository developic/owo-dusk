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

import os, json, time, threading

from utils.system import is_termux
from utils.loader import (
    misc_dict,
    global_settings_dict,
    console_width,
    console
)

on_mobile = is_termux()
psutil = None

if not on_mobile and not misc_dict["hostMode"]:
    try:
        if global_settings_dict.batteryCheck.enabled:
            import psutil
    except Exception as e:
        print(f"ImportError: {e}")


# For battery check
def batteryCheckFunc():
    cnf = global_settings_dict.batteryCheck
    try:
        if on_mobile:
            while True:
                time.sleep(cnf.refreshInterval)
                try:
                    battery_status = os.popen("termux-battery-status").read()
                except Exception as e:
                    console.print(
                        f"system - Battery check failed!! - {e}".center(
                            console_width - 2
                        ),
                        style="red ",
                    )
                battery_data = json.loads(battery_status)
                percentage = battery_data["percentage"]
                console.print(
                    f"system - Current battery •> {percentage}".center(
                        console_width - 2
                    ),
                    style="blue ",
                )
                if percentage < int(cnf.minPercentage):
                    break
        else:
            while True:
                time.sleep(cnf.refreshInterval)
                try:
                    battery = psutil.sensors_battery()
                    if battery is not None:
                        percentage = int(battery.percent)
                        console.print(
                            f"system - Current battery •> {percentage}".center(
                                console_width - 2
                            ),
                            style="blue ",
                        )
                        if percentage < int(cnf.minPercentage):
                            break
                except Exception as e:
                    console.print(
                        f"-system - Battery check failed!! - {e}".center(
                            console_width - 2
                        ),
                        style="red ",
                    )
    except Exception as e:
        print("battery check", e)
    os._exit(0)


def start_battery_check():
    if global_settings_dict.batteryCheck.enabled:
        loop_thread = threading.Thread(target=batteryCheckFunc, daemon=True)
        loop_thread.start()
