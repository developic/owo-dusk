import logging
from threading import Thread
import requests
from utils.system import printBox
from utils.battery import on_mobile
from utils.loader import global_settings_dict

def fetch_json(url, description="data"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        printBox(f"Failed to fetch {description}: {e}", "bold red")
        return {}

def run_bot(token, channel_id, global_settings_dict, token_len):
    from client import MyClient
    try:
        logging.getLogger("discord.client").setLevel(logging.ERROR)

        while True:
            client = MyClient(token, channel_id, global_settings_dict, token_len)

            try:
                client.run(token, log_level=logging.ERROR)
            except Exception as e:
                printBox(f"Unknown error when running bot: {e}", "bold red")
            if on_mobile:
                break

    except Exception as e:
        printBox(f"Error starting bot: {e}", "bold red")

def run_bots(tokens_and_channels):
    threads = []
    for token, channel_id in tokens_and_channels:
        thread = Thread(
            target=run_bot,
            args=(token, channel_id, global_settings_dict, len(tokens_and_channels)),
        )
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

