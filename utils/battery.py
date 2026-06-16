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
