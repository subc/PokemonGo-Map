# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime
import thread
from threading import local
from module import Gym
import redis
gyms = {}
tls = local()


# redis
def get_client(point):
    key = "redis_client:{}".format(str(point))
    if not hasattr(tls, key):
        from example import get_args
        args = get_args()
        host = args.redishost
        port = args.redisport
        db = point
        print("redis db is {}".format(db))
        setattr(tls, key, redis.Redis(host=host, port=port, db=db))
    return getattr(tls, key)


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
    diff_sec = diff.seconds - 10 + 10000000 # 10秒短く設定しておく
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
