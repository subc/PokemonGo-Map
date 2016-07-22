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
        pass

    def _run(self, point):
        update_map(point)
