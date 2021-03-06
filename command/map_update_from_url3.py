# -*- coding: utf-8 -*-
import traceback

from flask_script import Command, Option
from kvs import get_all_pokemon, set_pokemon, get_pokemon_keys, update_pokemon_count
from datetime import datetime
import time
import random
import ujson
from points import POINTS
from subprocess import PIPE, Popen


class MapUpdateFromUrl3(Command):
    """
    redis確認する
    """
    option_list = (
        Option('-p', '--point', default=None, required=True, help='update map in range point'),
        Option('-ns', '--nosleep', default=False, required=False, help='no sleep mode'),
    )

    def run(self, point, nosleep):
        self.init()
        try:
            self._run(int(point), nosleep)
        except:
            print(traceback.format_exc())

        if not nosleep:
            time.sleep(30)
        print("finish")

    def init(self):
        pass

    def _run(self, point, nosleep):
        x, y, f = POINTS[point]
        data = get_from_url(x, y)
        set_data(point, data)


def set_data(point, data):
    pokemon_count = len(data['pokemons'])
    print("pokemon count:{}".format(pokemon_count))
    for pokemon in data['pokemons']:
        # time
        disappear_time = int(pokemon['disappear_time'] / 1000)
        diff = datetime.fromtimestamp(disappear_time) - datetime.now()
        expire_time = diff.seconds - 10  # 10秒短く設定しておく
        if expire_time <= 20:
            continue

        # other
        pokemon_id = pokemon['pokemon_id']
        lat = pokemon['latitude']
        lon = pokemon['longitude']
        print "goradarXXXX", pokemon_id, lat, lon
        set_kvs(point, pokemon_id, lat, lon, disappear_time)

    # for monitor
    update_pokemon_count(point, pokemon_count)


def get_from_url(x, y, count=5):
    """
    curl 'https://api.goradar.io/raw_data?&swLat=35.683732&swLng=139.692352&neLat=35.694723&neLng=139.700689&pokemon=true&pokestops=false&gyms=false' -H ':authority: api.goradar.io' -H 'cookie: __cfduid=d24cea22ee8ee917f9cbb63b056356fec1470442248' -H 'accept: application/json' -H 'user-agent: GoRadar/13 CFNetwork/758.5.3 Darwin/15.6.0' -H 'accept-language: ja-jp'  --compressed


    :return:
    """
    if count <= 0:
        print("error retry count is {}".format(count))
        raise ValueError, "retry is over"

    _f = 0.02
    lat = fuzzy(x - _f)
    lat2 = fuzzy(x + _f)
    lon = fuzzy(y - _f)
    lon2 = fuzzy(y + _f)
    f5 = random.randint(10000, 99999)
    f5_2 = random.randint(10000, 99999)

    base = "curl 'https://api.goradar.io/raw_data?&swLat={lat}&swLng={lon}&neLat={lat2}&neLng={lon2}&pokemon=true&pokestops=false&gyms=false' -H ':authority: api.goradar.io' -H 'cookie: __cfduid=d24cea22ee8ee917f9cbb63b0{f5}fec14704{f5_2}' -H 'accept: application/json' -H 'user-agent: GoRadar/13 CFNetwork/758.5.3 Darwin/15.6.0' -H 'accept-language: ja-jp'  --compressed"
    c = base.format(lat=lat, lon=lon, lat2=lat2, lon2=lon2, f5=f5, f5_2=f5_2)
    print c
    output = cmdline(c).stdout.readlines()
    output_str = ''.join(output)

    if "Internal Server Error" in output_str:
        print("500 error retry... {}".format(count))
        time.sleep(2)
        return get_from_url(x, y, count=count-1)

    data = ujson.decode(output_str)
    return data


def set_kvs(point, pokemon_id, lat, lon, disappear_time):
    assert type(disappear_time) == int
    _ = {
        'id': pokemon_id,
        'lat': lat,
        'lng': lon,
        'disappear_time': disappear_time,
    }
    key = '{}:{}:{}:{}'.format(_['id'],
                               _['lat'],
                               _['lng'],
                               _['disappear_time'],
                               )
    set_pokemon(key, _, point=point)


def cmdline(command):
    """
    コマンドを実行する。shell=Trueの場合シェル経由で実行する。
    :param command: str
    :return: Popen
    """
    return Popen(
        args=command,
        stdout=PIPE,
        stderr=PIPE,
        shell=True
    )


def fuzzy(p):
    """
    0.002が最大
    """
    roulet = [0.0000076, 0.0000075, 0.0000074, 0.0000066, 0.0000064,
              0.0000062, 0.0000061, 0.0000054, 0.0000053, 0.0000051,
              0.0000048, 0.0000045, 0.0000044, 0.0000038, 0.0000033,
              0.0000029, 0.0000027, 0.0000025, 0.0000022, 0.0000021,
              0.0000018, 0.0000016, 0.0000013, 0.0000002, 0.0000001]
    f = random.choice(roulet)
    base = p + f
    result = float('%03.6f' % base)
    return result
