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
                print "[+]ok({}) point:{}".format(num, x)
            else:
                print "[-]NGNGNG({}) point:{}".format(num, x)
                ng_group.append((num, x))

        print("++++++++++++++++++++++++++++++++++++")
        print("ERRORS")
        print("++++++++++++++++++++++++++++++++++++")
        for num, x in ng_group:
            print "[-]NG({}) point:{}".format(num, x)
        print("++++++++++++++++++++++++++++++++++++")
