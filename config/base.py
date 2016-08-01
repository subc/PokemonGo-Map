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
    "AIzaSyANot6E0gUmvYIgnlAY0I4-2PDRjKdxpwo",  # id.s
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
    "AIzaSyBLNSCvL_DPF-bm4-8u43X2SgpHr6rGvUw",  # SandraBanks707
    "AIzaSyANjwju1A_LVNfrHY4wYHqBorKOT6G5ELQ",  # LauraWade535
    "AIzaSyDJ_bPyT9jBDupTCWgZDApHmfdG76oh3z8",  # ArrothilGrender45
    "AIzaSyABT4IIfrdCYDyRdVMHUzSjtzhV3xjjlPM",  # ssandisarma
    "AIzaSyD7KOdhaXgHMpCYBgEUXvVSFcqg0MjnfDM",  # mkane3353
    "AIzaSyDvGu_yu_ylj5Y3qpRuONTX7qei-n6yblY",  # dasvula477
    "AIzaSyDGrEY3_ubnBbXQBSP8O8DvDPBPguktzkw",  # rahapallib421
    "AIzaSyDVLehyAJxSC7hbx-ELp1cozX-ToeF3ZEQ",  # rajinkhamar0
    "AIzaSyCIZFNyz4ULvT7wr1QjZIQZkgezG9hwq6E",  # dmartib34
    "AIzaSyCY16MEV0NaaMiVyh72l0goKapdtat73WE",  # ammdsummy66
    "AIzaSyCc77NZw2diWy-ILKrTx63TjZ3Z2aYetx8",  # soykats226
    "AIzaSyBaoTeSykOafQODVpeUieGkDw2QOkDTEFI",  # rgraj8235
    "AIzaSyDaWVFMEi-eEPfKSEMGbLpW6VJMasaZBAI",  # tanitany941
    "AIzaSyBGi72Ogs65u9LvQsMtfLLu2FL3XgzUod4",  # mandrokane641
    "AIzaSyB9V9VIm1EiODClS9VV986lzAEeqFJvjsI",  # vgoa880
    "AIzaSyDULl5SVxcMH3v1PY9QdggqRsZKKVtFQ9w",  # atapprotap822
    "AIzaSyC-y_JPcrIg1qJFMKVWj8_85dgT90MzZO4",  # andrsonj718
    "AIzaSyAuyY4kuOD6d1VKPLcBkTlQqDEmNKN9opg",  # socotsaire998
    "AIzaSyBbdYL69Zkelr5IcG4V-Orzk8itNaPvlNU",  # krases365
    "AIzaSyDpNl2VKh49vlCFNLH362WjTnvhaSLLpVo",  # katlod716
    # 0801 昼
    "AIzaSyAW5A1iGvpRZpNSg-XCBvEB8hKnG_Vf4Y8",  # noradebra66
    "AIzaSyAq4u30aPJ4f82yyXuzsmdVQZPm6StncOM",  # carlajulia672
    "AIzaSyCKJqSAKCWOK5j7Gcz6UJ6LbZgYDIrCR9I",  # ruthmyrtle881
    "AIzaSyCX4MglTaqeu71GGSiSam6inMRv3xy4TW8",  # mariannastephanie643
    "AIzaSyAxl8c-OzJQoCZEWe09h0399dmy4bEP7lA",  # caroldolores605
    "AIzaSyCJ9AeM9ISmE_ETTEXlklJaHodNAIle7s4",  # patriciajanet326
    "AIzaSyBkiq93q-cOZ8h878FrQC45rhIJ-HEWcW4",  # jennydominga21
    "AIzaSyCIa5bh_wbggzz5U87ReaoBX9Zh300iH9E",  # carrielauren759
    "AIzaSyBM-vWFAjgOTL8qZyzO0Z2v3w9IHow75Js",  # jessicamarjorie942
    "AIzaSyAhNe--spaPcWkdV4rYJwHUKIXGn3kjJpk",  # dorothycharles274
    "AIzaSyBarY1V1xDVhuQZ4Tlysqllx6JUbfq3_-s",  # pamelaearnestine908
    "AIzaSyDL_DOAiqLOkN23jl3YtCnZnWH54iokPPs",  # lorisharyl95
    "AIzaSyCps4LWmiF-GHqCxJK6RZk2wmwXcJv41x0",  # andrearuby393
    "AIzaSyBPw2sQUpSVyOm0L5bBKyXmwsae8dZR_Vo",  # lindadebbie103
    "AIzaSyAGCv0Inzlws6HEQxxCh7BxlNMo8b3VhdI",  # mildredjessie694
    "AIzaSyArwC8dR382qvYDHgqNVvNNWcAT71EAhx8",  # d43688990
    "AIzaSyCOG5sdIer-J8Uogho0_ByPu5pv-d5zpjY",  # hm3153040
    "AIzaSyA9x4GjGLBxocj0tUoyND0r5yIQwkxwFCo",  # jennajacalyn28
    "AIzaSyAZOI1M4-LLKamTDp6RqKoKALfqUzSNF48",  # diannairene38
    "AIzaSyBuX0fZsVJSzcfsjX-xPo3OyOkeOYB8_dM",  # barbaramarie30
    # 0801 夜
    "AIzaSyB9025Q4RZ6H2bYSGJvQoE8jOhOXqmu11Y",  # jennifergloria678
    "AIzaSyCoViWDvgBVJs0F__VubJhqJh2kOA93MrA",  # pearlpeggy024
    "AIzaSyBDDZtHzNGPYt_IIXryZKAM3JTr3lpCwNQ",  # ireneteresa836
    "AIzaSyAA3B296PrDqo6oUgZMx2dKOq107fJA4M8",  # evelyneana801
    "AIzaSyBDrNL2RW0YUwJHsdnqg58UDO8N-OuNpmI",  # bethmae619
    "AIzaSyAgBinFRof1BnMWiK9lMiXdVOROdF4AiLI",  # kayebeverley372
    "AIzaSyCVEvVUz0tn9djCz_BieX3FoR1hmRm2jU0",  # vickidalia24
    "AIzaSyCZg4baF7SXzDAs3sybsK6RLMcMFcS68ME",  # sherylangeline026
    "AIzaSyAweh68UVHsyObhE9y6_0cpGXMh-xFcnaI",  # elizabethheather27
    "AIzaSyDW1kPOgOBJO9noeKx7r6CszFphkK2KogI",  # lauriejuana724
    # 0802 朝
    "AIzaSyAHji52ccwbBYQty48zpbFoVk3y7Asih3o",  # charlenejessica540
    "AIzaSyCxnGsgo0zRGfZeF5bsvA89WCLN26lX3Jg",  #priscillasocorro6
    "AIzaSyBd04xXbhtQ6ALEyT5ZFDAYjv7XEjQHCq4",  #jerriejoann96
    "AIzaSyB73cFGh7x6cZdI9XaKq9MajN48HCFZzjo",  #dianekaren651
    "AIzaSyAuQ-spVtyoy8Q7AJ2Lhcpckuqbke8wzvI",  #ashleymarjorie8
    "AIzaSyCOEVyVVU1OwYTrcXmm3RZ9IjqHi7EaJBM",  #kathleenmelissa799
    "AIzaSyCLUEedyc2NzRFDEH14y935Resfbcr8uK0",  #amandataylorc709
    "AIzaSyDIhcH6c0HbhT-SC4qYGMhn043K302x7Is",  #cnthtrina
    "AIzaSyAroDccFIqn1RhrNjLqpITVLWcOwKIkIzg",  #jllcaitlin
    "AIzaSyB5BmGc7BVpKWAZhjyqaWeF26IBka3nn18",  #alicecnth
    # 0802 朝2
]

"""
from config.base import *
_ = GOOGLEMAPS_KEYS
p1 = len(_)
p2 = len(list(set(_)))
assert p1 == p2, "{}:{}".format(p1, p2)
p1
p2
"""