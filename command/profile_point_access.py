# -*- coding: utf-8 -*-
from flask_script import Command
from kvs import get_all_point_access


class ProfilePointAccess(Command):
    """
    point毎のアクセス数を表示
    """

    def run(self):
        self.init()
        self._run()
        print("finish")

    def init(self):
        pass

    def _run(self, cut=False):
        for key, count in get_all_point_access():
            print(key, count)
