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

import logging
from threading import Thread

import requests

import utils.system as syst
from utils.errors import suppress_and_log, suppress_and_log_block
from utils.loader import global_settings_dict


def fetch_json(url, description="data"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        syst.system.print_box(f"Failed to fetch {description}: {e}", "bold red")
        return {}


@suppress_and_log("Run Bot")
def run_bot(token, channel_id, global_settings_dict, token_len):
    from core.client import MyClient

    logging.getLogger("discord.client").setLevel(logging.ERROR)

    with suppress_and_log_block("Client Run"):
        client = MyClient(token, channel_id, global_settings_dict, token_len)
        client.run(token, log_level=logging.ERROR)


def run_bots(tokens_and_channels):
    threads = []

    with suppress_and_log_block("Run Bot starter loop"):
        for token, channel_id in tokens_and_channels:
            thread = Thread(
                target=run_bot,
                args=(
                    token,
                    channel_id,
                    global_settings_dict,
                    len(tokens_and_channels),
                ),
            )
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()
