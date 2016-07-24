# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.password import *

REDIS_HOSTS = ['127.0.0.1']
REDIS_PORT = 6379
AUTO_REFRESH = 2000
# LAT, LON = (float(35.687971), float(139.7544148))
LAT, LON = (float(35.683885), float(139.712122))
ZOOM = 14
GOOGLEMAPS_KEY = "AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4"
STEP_LIMIT = 9
DISPLAY_GYM = False
DISPLAY_POKE_STOP = False


# PokemonGo-Map/locales/pokemon.en.json
LOCALE = "en"

IS_LOCAL = True
IS_PRODUCTION = False
