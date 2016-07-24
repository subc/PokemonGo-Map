# -*- coding: utf-8 -*-
from flask_script import Command, Option
from example import update_map


class MapUpdate(Command):
    """
    マップ更新
    """
    option_list = (
        Option('-p', '--point', default=None, required=True, help='update map in range point'),
    )

    def run(self, point):
        self.init()
        self._run(int(point))
        print("finish")

    def init(self):
        # setting test
        from app import conf
        config = conf()
        acc1 = config['ACCOUNTS']
        acc2 = config['ACCOUNTS2']

        # test
        from points import POINTS
        assert len(POINTS) <= len(acc1), "point:{} acc1:{}".format(len(POINTS), len(acc1))
        assert len(POINTS) <= len(acc2), "point:{} acc2:{}".format(len(POINTS), len(acc2))

        # printer
        print "POINT:{} ACC1:{} ACC2:{}".format(len(POINTS), len(acc1), len(acc2))


    def _run(self, point):
        update_map(point)
