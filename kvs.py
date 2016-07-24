# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime
import thread
from threading import local
from module import Gym
import redis
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
    import ast
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
    if diff_sec > 0:
        get_client(point=point).setex(get_pokemon_key(point, key), value, diff.seconds)


def delete_pokemon(key, point=10):
    get_client(point=point).delete(get_pokemon_key(point, key))


def get_pokemon_keys(point=10):
    keys = get_client(point=point).keys(get_pokemon_key(point, "*"))
    if keys:
        return keys
    return []


# gym
def get_gym(key, point=10):
    return gyms[key]


def get_all_gym(point=10):
    print("gyms", gyms)
    return gyms


def set_gym(key, value, point=10):
    gyms[key] = value


def delete_gym(key, point=10):
    del gyms[key]


def get_gym_keys(point=10):
    return gyms.keys()


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


def key_is_exist(point, key):
    client = get_client(point)
    return bool(client.exists(key))
