# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import datetime
from collections import defaultdict

from kvs import set_monitor_account, \
    get_all_monitor_account, get_monitor_account, get_monitor_account_key


def login_failed(username, point):
    now = datetime.datetime.now()
    data = {
        'username': username,
        'point': int(point),
        'created_at': str(now),
    }

    # timeout 3600 * 72 で保存
    set_monitor_account(data)
    return


def get_all_login_failed():
    accounts = get_all_monitor_account()
    result = defaultdict(list)
    for acc in accounts:
        for login_error in acc:
            l = LoginError(login_error)
            result[l.username] += [l]
    return result


def get_login_failed_count(username):
    """
    :param username: utf8 or str
    :rtype : int
    """
    key = get_monitor_account_key(username)
    return len(get_monitor_account(key))


class LoginError(object):
    def __init__(self, data):
        self._rep = data

    def __repr__(self):
        return "{}[{}] - {}".format(self.username, self.point, str(self.created_at))

    @property
    def username(self):
        return self._rep['username']

    @property
    def created_at(self):
        s_time = self._rep['created_at']
        return datetime.datetime.strptime(s_time, '%Y-%m-%d %H:%M:%S.%f')

    @property
    def time(self):
        s_time = self._rep['created_at']
        return datetime.datetime.strptime(s_time, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')

    @property
    def point(self):
        return int(self._rep['point'])
