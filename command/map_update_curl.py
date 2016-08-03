# -*- coding: utf-8 -*-
from flask_script import Command, Option
from points import POINTS
from kvs import get_all_pokemon, set_pokemon, get_pokemon_keys
from datetime import datetime
from kvs import get_all_pokemon
import time
import requests
import random
import ujson
from constants.rarity import RARE_POKEMON
from constants.pop_pokemon import POP_POKEMONS
from points import POINTS


class MapUpdateCurl(Command):
    """
    redis確認する
    """
    option_list = (
        Option('-p', '--point', default=None, required=True, help='update map in range point'),
        Option('-ns', '--nosleep', default=False, required=False, help='no sleep mode'),
    )

    def run(self, point, nosleep):
        self.init()
        self._run(int(point), nosleep)
        if not nosleep:
            time.sleep(5)
        print("finish")

    def init(self):
        pass

    def _run(self, point, nosleep):
        limit_pokemon = random.randint(20, 30)
        count = len(get_pokemon_keys(point=point))
        print "total_pokemon_count:{}".format(count)
        if count > limit_pokemon:
            print "SLEEP 60SEC  pokemon is over"
            if not nosleep:
                s = random.randint(80, 170)
                time.sleep(s)
            return
        x, y, f = POINTS[point]
        pop_pokemon(x, y, point, limit_pokemon - count, nosleep=nosleep)

def pop_pokemon(lat, lon, point, limit, nosleep=False):
    steps = get_steps(lat, lon, point)
    random.shuffle(steps)

    for i in xrange(limit):
        x, y = steps[i]
        lot_and_set_kvs(x, y, point)
        if not nosleep:
            time.sleep(random.randint(2, 10))


def get_steps(lat, lon, point):
    pokemon_count = 0
    pos = 1
    x = 0
    y = 0
    dx = 0
    dy = -1
    # steplimit2 = int(step_limit**2 * float(1.5625))
    steplimit2 = 11 * 11
    steps = []
    for step in range(steplimit2):
        # print('looping: step {} of {}'.format((step+1), steplimit2))
        # debug('steplimit: {} x: {} y: {} pos: {} dx: {} dy {}'.format(steplimit2, x, y, pos, dx, dy))
        # Scan location math
        if -steplimit2 / 2 < x <= steplimit2 / 2 and -steplimit2 / 2 < y <= steplimit2 / 2:
            # print 'scan:', x * 0.002 + lat, y * 0.002 + lon, 0
            pass
        if x == y or x < 0 and x == -y or x > 0 and x == 1 - y:
            (dx, dy) = (-dy, dx)

        (x, y) = (x + dx, y + dy)
        steps.append((x * 0.002 + lat, y * 0.002 + lon))
    return steps


def lot_and_set_kvs(o_lat, o_lon, point):
    pokemon_id = lot_pokemon()
    if not pokemon_id:
        return

    unix = int(time.mktime(datetime.now().timetuple()))
    lat = fuzzy(o_lat)
    lon = fuzzy(o_lon)
    print "pokemon:{} {}:{}".format(pokemon_id, lat, lon)

    _ = {
        'id': pokemon_id,
        'lat': lat,
        'lng': lon,
        'disappear_time': unix + random.randint(100, 840),
    }
    key = '{}:{}:{}:{}'.format(_['id'],
                               _['lat'],
                               _['lng'],
                               _['disappear_time'],
                               )
    set_pokemon(key, str(_), point=point, expire=100)


def fuzzy(p):
    """
    0.002が最大
    """
    r = [0.0000001, 0.0000002, 0.0000003, -0.0000001, -0.0000002, -0.0000003]
    f = float(random.randint(1, 20000)) / (10000 * 1000)
    base = p + f
    result = float('%03.7f' % base)
    return result


def lot_pokemon():
    """
    121回スキャンで30が目標
    レアは4匹
    ノーマル26匹
    外れ91匹
    """
    normal_ids = []
    rare_ids = []
    for pokemon_id in POP_POKEMONS:
        if pokemon_id in RARE_POKEMON:
            rare_ids.append(pokemon_id)
        else:
            normal_ids.append(pokemon_id)

    z = random.randint(1, 122)
    if z >= 120:
        # rare
        rare_id = random.choice(rare_ids)

        # カイリュー、カビゴン, リザードン, サンダース禁止
        if rare_id in [149, 143, 5, 6, 135]:
            return normarise()

        # リザードン沸きすぎ対策
        if rare_id in [130, 9, 3, 136, 4, 112]:
            if random.randint(1, 13) != 2:
                return normarise()

        # ベトベトン沸きすぎ対策2
        if rare_id in [89, 134, 59, 3]:
            if random.randint(1, 4) != 2:
                return normarise()

        return random.choice(rare_ids)
    if z >= 92:
        # noraml
        if random.randint(1, 2) == 1:
            return normarise()
        return random.choice(normal_ids)
    return 0


def normarise():
    l = [
        (1,0,136),
        (4,137,321),
        (10,322,524),
        (13,525,909),
        (16,910,1302),
        (19,1303,1665),
        (60,1666,1837),
        (84,1838,2703),
        (118,2704,2868),
        (127,2869,3041),
    ]
    f = random.randint(0, 3041)
    for pokemon_id, _min, _max in l:
        if _min <= f <= _max:
            return pokemon_id
    return 127
