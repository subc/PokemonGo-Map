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


class MapUpdateFromUrl2(Command):
    """
    from
    https://pmap.kuku.lu/#35.716047157966635,139.77214336395267,15
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
        count = set_data(point, data)
        return count


def set_data(point, data):
    pokemon_count = len(data)
    print("pokemon count:{}".format(pokemon_count))
    for record in data:
        try:
            _, id_raw, loc_raw, expire_low, _2 = record
        except:
            continue

        pokemon_id = id_raw.replace("id=", "")
        loc = loc_raw.replace("loc=", "").split(",")
        expire = long(expire_low.replace("tol=", ""))
        print "ZZZZ:", pokemon_id, loc, expire

        # time
        disappear_time = int(expire / 1000)
        diff = datetime.fromtimestamp(disappear_time) - datetime.now()
        expire_time = diff.seconds - 10  # 10秒短く設定しておく
        if expire_time <= 20:
            continue

        # other
        lat = loc[0]
        lon = loc[1]
        set_kvs(point, pokemon_id, lat, lon, disappear_time)

    # for monitor
    update_pokemon_count(point, pokemon_count)
    return pokemon_count


def get_from_url(x, y, count=5):
    """
    curl 'https://map_data.goradar.io/
    raw_data?pokemon=true&pokestops=true&gyms=false&scanned=false
    &swLat=35.6437875&swLng=139.6813787&neLat=35.7437875&neLng=139.8813787'

    -H 'origin: https://map.goradar.io'
    -H 'accept-encoding: gzip, deflate, sdch, br'
    -H 'accept-language: ja,en-US;q=0.8,en;q=0.6'
    -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    -H 'accept: application/json, text/javascript, */*; q=0.01'
    -H 'referer: https://map.goradar.io/'
    -H 'authority: map_data.goradar.io' --compressed

    :return:
    """
    if count <= 0:
        print("error retry count is {}".format(count))
        raise ValueError, "retry is over"

    lat = fuzzy(x)
    lon = fuzzy(y)

    base = "curl 'https://sv-db{db}.pmap.kuku.lu/_dbserver.php?action=viewData&sv=undefined&research_key=&loc1={lat}6693448&loc2={lon}7519534&_=14704399{f5}' -H 'Origin: https://pmap.kuku.lu' -H 'Accept-Encoding: gzip, deflate, sdch, br' -H 'Accept-Language: ja,en-US;q=0.8,en;q=0.6' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36' -H 'Accept: */*' -H 'Referer: https://pmap.kuku.lu/' -H 'Connection: keep-alive' --compressed"
    base = "curl 'https://sv-db.pmap.kuku.lu/_dbserver.php?action=viewData&fort=&pokesource=&history_pokemonid=&sv=undefined&research_key=&loc1={lat}76496555&loc2={lon}9633792&_=1472977897840' -H 'Origin: https://pmap.kuku.lu' -H 'Accept-Encoding: gzip, deflate, sdch, br' -H 'Accept-Language: ja,en-US;q=0.8,en;q=0.6' -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36' -H 'Accept: */*' -H 'Referer: https://pmap.kuku.lu/' -H 'Connection: keep-alive' --compressed"
    c = base.format(lat=lat, lon=lon, db=random.randint(2, 3), f5=random.randint(10000, 99999))
    print c
    output = cmdline(c).stdout.readlines()
    output_str = ''.join(output)

    data = [r.split(";") for r in output_str.split("\n")]

    if not len(data):
        print("500 error retry... {}".format(count))
        time.sleep(2)
        return get_from_url(x, y, count=count-1)

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
    result = float('%03.7f' % base)
    return result
