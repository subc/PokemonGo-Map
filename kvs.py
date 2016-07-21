# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from module import Gym
import redis


pokemons = {}
gyms = {}


def get_pokemon(key):
    return pokemons[key]


def get_all_pokemon():
    print "pokemons", pokemons
    return pokemons


def set_pokemon(key, value):
    pokemons[key] = value


def delete_pokemon(key):
    del pokemons[key]


def get_pokemon_keys():
    return pokemons.keys()


# gym
def get_gym(key):
    return gyms[key]


def get_all_gym():
    print("gyms", gyms)
    return gyms


def set_gym(key, value):
    gyms[key] = value


def delete_gym(key):
    del gyms[key]


def get_gym_keys():
    return gyms.keys()
