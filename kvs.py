# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import redis
pokemons = {}


def get_pokemon(key):
    return pokemons[key]


def get_all_pokemon():
    return pokemons


def set_pokemon(key, value):
    pokemons[key] = value


def delete_pokemon(key):
    del pokemons[key]


def get_pokemon_keys():
    return pokemons.keys()
