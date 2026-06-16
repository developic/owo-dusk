import os
import time
import threading

def watch_configs(paths, on_change, interval=2):
    last_state = {}

    for p in paths:
        try:
            last_state[p] = os.path.getmtime(p)
        except FileNotFoundError:
            last_state[p] = None

    last_trigger = 0

    while True:
        time.sleep(interval)
        changed = False

        for p in paths:
            try:
                mtime = os.path.getmtime(p)
            except FileNotFoundError:
                mtime = None

            if last_state.get(p) != mtime:
                last_state[p] = mtime
                changed = True

        # debounce (prevents spam reloads)
        if changed:
            now = time.time()
            if now - last_trigger > 1.5:
                last_trigger = now
                try:
                    on_change()
                except Exception as e:
                    print(f"[ConfigWatcher] callback error: {e}")

def start_config_watcher(paths, on_change, interval=2):
    thread = threading.Thread(
        target=watch_configs,
        args=(paths, on_change, interval),
        daemon=True
    )
    thread.start()
    return thread