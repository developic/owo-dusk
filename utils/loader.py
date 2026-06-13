import json
import utils.configs as config_models
import tomllib
from rich.console import Console

def load_accounts_dict(file_path="utils/stats.json"):  # dead code btw
    with open(file_path, "r", encoding="utf-8") as config_file:
        return json.load(config_file)


with open("config/global_settings.json", "r", encoding="utf-8") as config_file:
    global_settings_dict = config_models.configs.FetchGlobalSettings(
        json.load(config_file)
    )

with open("config/webhookContent.json", "r", encoding="utf-8") as config_file:
    webhook_data_dict = json.load(config_file)


with open("config/captcha.toml", "rb") as f:
    captcha_settings_dict = tomllib.load(f)

with open("config/danger.toml", "rb") as f:
    danger_settings_dict = tomllib.load(f)

with open("config/misc.json", "r", encoding="utf-8") as f:
    misc_dict = json.load(f)

console = Console()
console.rule("[bold blue1]:>", style="navy_blue")
console_width = console.size.width