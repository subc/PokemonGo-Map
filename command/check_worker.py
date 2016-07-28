# -*- coding: utf-8 -*-
from flask_script import Command, Option
from points import POINTS
from kvs import get_all_pokemon
from datetime import datetime
from kvs import get_all_pokemon


class CheckWorker(Command):
    """
    redis確認する
    """

    def run(self):
        self.init()
        self._run()
        print("finish")

    def init(self):
        pass

    def _run(self):
        ng_group = []
        warning_group = []
        for point in xrange((len(POINTS))):
            num = get_pokemon_count(point)
            if num > 5:
                print "[-]OK({0:04d})".format(num) + " point:{0:04d}".format(point)
                if num <= 40:
                    warning_group.append((num, point))
            else:
                print "[-]NGNGNG({0:04d})".format(num) + " point:{0:04d}".format(point)
                ng_group.append((num, point))

        if warning_group:
            print("++++++++++++++++++++++++++++++++++++")
            print("WARNING")
            print("++++++++++++++++++++++++++++++++++++")
            for num, point in warning_group:
                print "[-]WARNING({0:04d})".format(num) + " point:{0:04d}".format(point)
            print("++++++++++++++++++++++++++++++++++++")

        if ng_group:
            print("++++++++++++++++++++++++++++++++++++")
            print("ERRORS")
            print("++++++++++++++++++++++++++++++++++++")
            for num, point in ng_group:
                print "[-]NGNGNG({0:04d})".format(num) + " point:{0:04d}".format(point)
            print("++++++++++++++++++++++++++++++++++++")

        print("")
        print("ok.")
        print("")


def get_pokemon_count(point):
    count = 0
    pokemons = get_all_pokemon(point)
    for p in pokemons:
        if not p:
            continue
        diff = datetime.fromtimestamp(p['disappear_time']) - datetime.now()
        sec = diff.seconds
        if 1 <= sec <= 900:
            count += 1
    return count
