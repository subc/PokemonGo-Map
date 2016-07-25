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
        for x in xrange((len(POINTS))):
            num = len(get_all_pokemon(point=x))
            if num > 5:
                print "[+]ok({0:04d}) point:{0:04d}".format(num, x)
            else:
                print "[-]NGNGNG({0:04d}) point:{0:04d}".format(num, x)
                ng_group.append((num, x))

        if ng_group:
            print("++++++++++++++++++++++++++++++++++++")
            print("ERRORS")
            print("++++++++++++++++++++++++++++++++++++")
            for num, x in ng_group:
                print "[-]NG({0:04d}) point:{0:04d}".format(num, x)
            print("++++++++++++++++++++++++++++++++++++")
        else:
            print("")
            print("ok.")
            print("")
