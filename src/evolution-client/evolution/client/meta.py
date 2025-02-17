import os
import json

APP_DIR_NAME = ".evolution"

HOME_DIR = os.path.expanduser("~")
APP_DIR = os.path.join(HOME_DIR, APP_DIR_NAME)
CONFIG_DIR = os.path.join(APP_DIR, "config.json")

os.makedirs(APP_DIR, exist_ok=True)


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")


def load_config():
    if not os.path.exists(CONFIG_DIR):
        return {}
    with open(CONFIG_DIR, "r") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_DIR, "w") as f:
        json.dump(config, f)

def update_config(key, value):
    config = load_config()
    config[key] = value
    save_config(config)
