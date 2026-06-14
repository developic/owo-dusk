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

# Standard Library
import os
import signal
import threading

# Third-Party Libraries
import discord
from discord import SyncWebhook
from queue import Queue

# Local
import utils.state as state
from utils.notification import notify
from utils.webhook import webhookSender
from utils.runtime_handler import start_runtime_loop
from utils.captcha_solver.yescaptcha import captchaClient
from utils.bot_runner import fetch_json, run_bots
from utils.database import create_database
from website import web_start
from utils.system import (
    compare_versions,
    clear,
    printBox,
    get_local_ip,
    misc_dict,
    console
)
from utils.loader import (
    global_settings_dict,
    captcha_settings_dict,
    console_width,
)
from utils.constants import (
    owo_dusk_api,
    owoPanel,
    version
)
from utils.battery import start_battery_check, on_mobile
from utils.quest_helper.quest import QuestHandler

import client


"""Ctrl+c detect"""


def handle_sigint(signal_number, frame):
    print("\nCtrl+C detected. stopping code!")
    os._exit(0)

clear()

"""FLASK APP"""

start_battery_check()

# ----------STARTING BOT----------#

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_sigint)
    notify(
        "OwO-Dusk starting... If any issue arises visit out discord support server (link available in console or github)",
        "Starting OwO-Dusk! :>",
    )

    if not misc_dict["console"]["compactMode"]:
        console.print(owoPanel)
        console.rule(f"[bold blue1]version - {version}", style="navy_blue")
    version_json = fetch_json(f"{owo_dusk_api}/version.json", "version info")

    if compare_versions(version, version_json["version"]):
        printBox(
            f"""Update Detected - {version_json["version"]}
    Changelog:-
        {version_json["changelog"]}""",
            "bold gold3",
        )
        if version_json["important_update"]:
            printBox("It is recommended to update....", "bold light_yellow3")

    tokens_and_channels = [
        line.strip().split() for line in open("tokens.txt", "r", encoding="utf-8")
    ]
    token_len = len(tokens_and_channels)

    printBox(f"-Received {token_len} tokens.".center(console_width - 2), "bold magenta")

    # Create database or modify if required
    create_database()

    # Weekly runtime thread
    start_runtime_loop()

    if global_settings_dict.website.enabled:
        # Start website
        web_thread = threading.Thread(
            target=web_start,
            args=(
                global_settings_dict.website.port,
                global_settings_dict.website.enableHost,
                version,
                global_settings_dict.website.password,
            ),
        )
        web_thread.start()
        # get ip
        ip = get_local_ip()
        printBox(
            f"Website Dashboard: http://{ip}:{global_settings_dict.website.port}".center(
                console_width - 2
            ),
            "dark_magenta",
        )
    try:
        if misc_dict["news"]:
            news_json = fetch_json(f"{owo_dusk_api}/news.json", "news")
            if news_json.get("available"):
                printBox(
                    f"{news_json.get('content', 'no content found..? this is an error! should be safe to ignore')}".center(
                        console_width - 2
                    ),
                    f"bold {news_json.get('color', 'white')}",
                    title=news_json.get("title", "???"),
                )
    except Exception as e:
        print(f"Error - {e}, while attempting to fetch news")

    if not misc_dict["console"]["hideStarRepoMessage"]:
        console.print(
            "Star the repo in our github page if you want us to continue maintaining this proj :>.",
            style="thistle1",
        )

        if global_settings_dict.webhook.enabled:
            webhook = SyncWebhook.from_url(global_settings_dict.webhook.webhookUrl)

            color = discord.Color(0xC48DC3)
            emb = discord.Embed(
                title="Star the github repo!",
                description="Starring the GitHub repo motivates us to keep adding new and better features! It takes less than 5 minutes to do that, so do star the GitHub repo at https://github.com/owo-dusk/owo-dusk .",
                color=color,
            )
            emb.set_thumbnail(
                url="https://cdn.discordapp.com/emojis/723856770249916447.gif"
            )

            webhook.send(embed=emb, username="OwO-Dusk")

    console.rule(style="navy_blue")

    client.webhook_handler = webhookSender(global_settings_dict.webhook.webhookUrl)
    client.global_quest_handler = QuestHandler(api=global_settings_dict.ocrApi)
    client.hcaptcha_solver = None
    if (
        captcha_settings_dict["image_solver"]["enabled"]
        or captcha_settings_dict["hcaptcha_solver"]["enabled"]
    ):
        console.print(
            "Be Warned, Captcha solving is not well tested.. You are using on your own risk..",
            style="orange_red1",
        )
        if captcha_settings_dict["hcaptcha_solver"]["enabled"]:
            # Setup hcaptcha solver..
            client.hcaptcha_solver = captchaClient(
                captcha_settings_dict["hcaptcha_solver"]["api_key"]
            )
            if client.hcaptcha_solver.balance == 0:
                console.print(
                    "Yescaptcha API has no balance...",
                    style="orange_red1",
                )
                os._exit(0)
            else:
                bal = client.hcaptcha_solver.balance
                console.print(
                    f"Yescaptcha API has a balance of {bal}, which is approximately {round(bal / 30)} hcaptcha solves.",
                    style="tan",
                )

    if (
        global_settings_dict.captcha.toastOrPopup
        and not on_mobile
        and not misc_dict["hostMode"]
    ):
        from utils.popup import popup_main_loop
        state.popup_queue = Queue()

        bot_threads = threading.Thread(target=run_bots, args=(tokens_and_channels,))
        bot_threads.daemon = True
        bot_threads.start()

        popup_main_loop()
    else:
        run_bots(tokens_and_channels)
