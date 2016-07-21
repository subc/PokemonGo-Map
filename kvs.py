# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import thread
from threading import Thread, local
from module import Gym
import redis

pokemons = {}
gyms = {}
tls = local()


# redis
def get_client(point=10):
    key = "redis_client:{}".format(str(point))
    if not hasattr(tls, key):
        from example import get_args
        args = get_args()
        host = args.redishost
        port = args.redisport
        db = point
        setattr(tls, key, redis.Redis(host=host, port=port, db=db))
    return getattr(tls, key)


# pokemon
def get_pokemon(key, point=10):
    print get_client()
    return pokemons[key]


def get_all_pokemon(point=10):
    print "pokemons", pokemons
    return pokemons


def set_pokemon(key, value, point=10):
    pokemons[key] = value


def delete_pokemon(key, point=10):
    del pokemons[key]


def get_pokemon_keys(point=10):
    return pokemons.keys()


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
