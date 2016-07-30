# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.password import *

REDIS_HOSTS = ['127.0.0.1']
REDIS_PORT = 6379
AUTO_REFRESH = 2000
# LAT, LON = (float(35.687971), float(139.7544148))
LAT, LON = (float(35.683885), float(139.712122))
ZOOM = 14
STEP_LIMIT = 9
DISPLAY_GYM = True
DISPLAY_POKE_STOP = False


# PokemonGo-Map/locales/pokemon.en.json
LOCALE = "en"

IS_LOCAL = True
IS_PRODUCTION = False
IS_MAINTENANCE = False

# KEY
GOOGLEMAPS_KEYS = [
    "AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4",  # id.s
    "AIzaSyAVreVNXS9WsfEBP3u5shGUnR27QCg2680",  # sub33
    "AIzaSyBCwfqt2qXfzfzkonj-vB8aGKbwGeAlVz4",  # kt.me
    "AIzaSyDER1RwjdUbygOk1TyA1Tigm11ADmHYrrY",  # kt.me.a
    "AIzaSyDqbUsSLmGsVVVXePcGOvN6pJNzvYARPhM",  # hoge001@pgo.tok
    "AIzaSyACtwPg-NqsPXw5gNyXpVZVKALgZpgKfrc",  # subc1-5
    "AIzaSyAN3VQBs-WYM5cbgvShmrm6DXVAvMiHSRw",  # subc.nikuniku001
    "AIzaSyB8vj0YnREgurq4V1397v7nidmWX-BW_DI",  # sn 2
    "AIzaSyCkKw146lBvcJtlTZqAV2mm3anOHieNrCA",  # sn 3
    "AIzaSyCbBZkGw23wXiwTuRKSOm03wJXgCdv-Dyc",  # sn 4
    "AIzaSyDew3u2VsV9_XQrN8dsAqJ8YHGs0sOTQyI",  # sn 5
]
