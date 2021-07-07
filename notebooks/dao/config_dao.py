import json

from notebooks import db

SERVER_SELECT = "select settings from discord_server where server_cod=%s;"
SERVER_UPDATE = "update discord_server set settings = %s where server_cod=%s;"


CONFIGS = {"private_pack"}


def validate(config):
    return config in CONFIGS


def get_all_config(server_cod):
    data = db.make_select(SERVER_SELECT, [server_cod])
    if len(data) == 0:
        raise Exception("Invalid Server Cod")
    return json.loads(data[0]['settings'])


def set_all_config(server_cod, configs):
    configs = json.dumps(configs)
    db.make_query(SERVER_UPDATE, [configs, server_cod])


def get_config(server_cod, config):
    return get_all_config(server_cod).get(config)


def set_config(server_cod, config, value):
    data = get_all_config(server_cod)
    data[config] = value
    set_all_config(server_cod, data)


if __name__ == '__main__':
    pass