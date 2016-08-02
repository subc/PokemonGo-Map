# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime
from threading import local
import redis
import ast
gyms = {}
tls_kvs = local()


def _get_redis_host(config, point):
    redis_hosts = config.get('REDIS_HOSTS')
    redis_server_count = len(redis_hosts)
    return redis_hosts[point % redis_server_count]


def get_client(point):
    key = "redis_client:{}".format(str(point))
    if not hasattr(tls_kvs, key):
        from app import conf
        config = conf()
        host = _get_redis_host(config, point)
        port = config.get('REDIS_PORT')
        db = point
        assert host, host
        assert port, port
        # print("redis db is {}: host:{} port:{}".format(db, host, port))
        setattr(tls_kvs, key, redis.Redis(host=host, port=port, db=db))
    return getattr(tls_kvs, key)


# pokemon
def get_pokemon_key(point, _key):
    return "poke:{0:04d}:".format(int(point)) + _key


def get_pokemon(key, point=10):
    pokemon = get_client(point=point).get(key)
    if pokemon:
        return ast.literal_eval(pokemon)
    return None


def get_all_pokemon(point=10):
    result = []
    for key in get_pokemon_keys(point=point):
        result.append(get_pokemon(key, point=point))
    return result


def set_pokemon(key, value, point=10):
    diff = datetime.fromtimestamp(value['disappear_time']) - datetime.now()
    diff_sec = diff.seconds - 10  # 10秒短く設定しておく
    diff_sec = min(900, diff_sec)  # 最大値は15分
    if diff_sec > 0:
        get_client(point=point).setex(get_pokemon_key(point, key), value, diff_sec)


def get_pokemon_keys(point=10):
    keys = get_client(point=point).keys(get_pokemon_key(point, "*"))
    if keys:
        return keys
    return []


# gym
def get_gym_key(point, _key):
    return "gym:{0:04d}:".format(int(point)) + _key


def get_gym(key, point=10):
    import ast
    gym = get_client(point=point).get(key)
    if gym:
        return ast.literal_eval(gym)
    return None


def get_all_gym(point=10):
    result = []
    for key in get_gym_keys(point=point):
        result.append(get_gym(key, point=point))
    return result


def set_gym(key, value, point=10):
    get_client(point=point).setex(get_gym_key(point, key), value, 900)


def get_gym_keys(point=10):
    keys = get_client(point=point).keys(get_gym_key(point, "*"))
    if keys:
        return keys
    return []


# acc switch
def get_acc_version(point):
    """
    return True or False
    1. key両方ない ... True 内部でA(expire 6h) B(expire 12h)作る
    2. key両方ある ... True
    3. keyAだけある ... True
    4. keyBだけある ... False

    :rtype: bool
    """
    base = "ACC:SWICH:{}"
    key_a = base.format("A")
    key_b = base.format("B")

    exist_a = key_is_exist(point, key_a)
    exist_b = key_is_exist(point, key_b)

    # 1. key両方ない ... True 内部でA(expire 6h) B(expire 12h)作る
    if exist_a is False and exist_b is False:
        timeout_a = 3600 * 6
        timeout_b = 3600 * 12
        client = get_client(point)

        # create A, B
        client.setex(key_a, 1, timeout_a)
        client.setex(key_b, 1, timeout_b)
        return True

    # 2. key両方ある ... True
    if exist_a and exist_b:
        return True

    # 3. keyAだけある ... True
    if exist_a and exist_b is False:
        return True

    # 4. keyBだけある ... False
    if exist_a is False and exist_b:
        return False

    raise ValueError


def force_change_account(point):
    version = get_acc_version(point)
    client = get_client(point)
    base = "ACC:SWICH:{}"
    key_a = base.format("A")
    key_b = base.format("B")

    if version:
        client.delete(key_a)
    else:
        client.delete(key_b)


def key_is_exist(point, key):
    client = get_client(point)
    return bool(client.exists(key))


# status monitor
def get_monitor_account_key(_id):
    return 'MONITOR:ACC:{}'.format(_id)


def set_monitor_account(data):
    key = get_monitor_account_key(data['username'])
    client = get_client(0)
    client.lpush(key, data)
    client.expire(key, 3600 * 72)
    return


def get_all_monitor_account():
    key_ast = get_monitor_account_key('*')
    client = get_client(0)
    keys = client.keys(key_ast)

    result = []
    for key in keys:
        result.append(get_monitor_account(key))
    return result


def get_monitor_account(key):
    client = get_client(0)
    _l = client.lrange(key, 0, -1)
    return [ast.literal_eval(data) for data in _l]


# pokemon count
def get_pokemon_count_key(point):
    return "CT:POKE:{}".format(point)


def update_pokemon_count(point, value):
    client = get_client(point)
    key = get_pokemon_count_key(point)
    now = datetime.now()
    client.setex(key, "{},{}".format(value, now), 3600)
    return


def get_pokemon_count(point):
    client = get_client(point)
    key = get_pokemon_count_key(point)
    return client.get(key)


# profiler level
def get_profiler_account_level_key():
    return "PROFILE:ACCOUNT"


def set_profiler_account_level(username, level):
    client = get_client(0)
    key = get_profiler_account_level_key()
    client.hset(key, username, level)
    client.expire(key, 3600 * 24 * 7)


def get_profiler_account_level():
    client = get_client(0)
    key = get_profiler_account_level_key()
    return client.hgetall(key)


# profiler point
def get_point_access_key(point):
    return "PROFILE:POINT:{}".format(point)


def incr_point_access(point):
    client = get_client(301)
    key = get_point_access_key(point)
    client.incr(key)
    client.expire(key, 3600 * 24 * 7)


def get_all_point_access():
    client = get_client(301)
    key_ast = get_point_access_key('*')
    result = []
    for key in client.keys(key_ast):
        result.append((key, int(client.get(key))))
    return sorted(result, key=lambda x: x[1], reverse=True)
