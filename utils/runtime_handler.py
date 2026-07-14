import json
import threading
import time

import utils.timestamp as utils
from utils.errors import suppress_and_log

path = "utils/data/weekly_runtime.json"


@suppress_and_log("Weekly Runtime Updater")
def handle_weekly_runtime(path="utils/data/weekly_runtime.json"):
    while True:
        with open(path, "r", encoding="utf-8") as config_file:
            weekly_runtime_dict = json.load(config_file)
        weekday = utils.get_weekday()

        if weekly_runtime_dict[weekday][0] == 0:
            weekly_runtime_dict[weekday][0], weekly_runtime_dict[weekday][1] = (
                time.time(),
                time.time(),
            )
        else:
            weekly_runtime_dict[weekday][1] = time.time()

        with open(path, "w", encoding="utf-8") as f:
            json.dump(weekly_runtime_dict, f, indent=4)
        # update every 15 seconds
        time.sleep(15)


@suppress_and_log("Weekly Runtime Update Starter")
def start_runtime_loop(path="utils/data/weekly_runtime.json"):
    with open(path, "r", encoding="utf-8") as config_file:
        weekly_runtime_dict = json.load(config_file)

    now = time.time()
    last_checked = weekly_runtime_dict.get("last_checked", 0)

    if now - last_checked > 604800:  # 604800 -> seconds in a week
        for day in map(str, range(7)):
            weekly_runtime_dict[day] = [0, 0]

    weekly_runtime_dict["last_checked"] = now

    with open(path, "w", encoding="utf-8") as f:
        json.dump(weekly_runtime_dict, f, indent=4)

    loop_thread = threading.Thread(target=handle_weekly_runtime, daemon=True)
    loop_thread.start()
