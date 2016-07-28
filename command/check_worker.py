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

    def _run(self, cut=False):
        ok_group = []
        ng_group = []
        warning_group = []
        for point in xrange((len(POINTS))):
            num = get_pokemon_count(point, cut=cut)
            if num > 5:
                print "[-]OK({0:04d})".format(num) + " point:{0:04d}".format(point)
                if num <= 20:
                    warning_group.append((num, point))
                else:
                    ok_group.append((num, point))
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
        return ok_group, warning_group, ng_group


def get_pokemon_count(point, cut=False):
    count = 0
    pokemons = get_all_pokemon(point)
    for p in pokemons:
        if not p:
            continue
        diff = datetime.fromtimestamp(p['disappear_time']) - datetime.now()
        sec = diff.seconds
        if 1 <= sec <= 900:
            count += 1

        if cut and count >= 21:
            return 100
    return count
