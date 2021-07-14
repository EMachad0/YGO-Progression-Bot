import json

from notebooks.dao.discord_server_dao import get_discord_server, update_server

CONFIGS = {"private_pack", "ban_list"}


def validate(config):
    return config in CONFIGS


def get_server_settings(server_cod):
    return get_discord_server(server_cod).settings


def get_config(server_cod, config):
    settings = get_server_settings(server_cod)
    return json.loads(settings).get(config)


def update_config(server_cod, key, value):
    settings = get_server_settings(server_cod)
    settings = json.loads(settings)
    settings[key] = value
    update_server(server_cod, {'settings': json.dumps(settings)})
