# -*- coding: utf-8 -*-
from flask_script import Command, Option
from points import POINTS
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
        for point in xrange((len(POINTS))):
            num = len(get_all_pokemon(point=point))
            if num > 5:
                print "[-]OK({0:04d})".format(num) + " point:{0:04d}".format(point)
            else:
                print "[-]NGNGNG({0:04d})".format(num) + " point:{0:04d}".format(point)
                ng_group.append((num, point))

        if ng_group:
            print("++++++++++++++++++++++++++++++++++++")
            print("ERRORS")
            print("++++++++++++++++++++++++++++++++++++")
            for num, point in ng_group:
                print "[-]NGNGNG({0:04d})".format(num) + " point:{0:04d}".format(point)
            print("++++++++++++++++++++++++++++++++++++")
        else:
            print("")
            print("ok.")
            print("")
