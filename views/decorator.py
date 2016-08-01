# -*- coding: utf-8 -*-
import logging
import traceback
from functools import wraps
import datetime
import flask


IGNORE_NAMES = [
    "favicon.ico",
    "robots.txt",
    "apple-touch-icon.png",
    "apple-touch-icon-precomposed.png",
    "mstile-144x144.png",
    "browserconfig.xml",
]


def app_log(log_level, msg):
    prefix = '[{}] '.format(str(datetime.datetime.now()))
    msg = prefix + msg

    from app import create_app
    _l = create_app().logger
    if log_level >= 50:
        _l.critical(msg)
    elif log_level >= 40:
        _l.error(msg)
    elif log_level >= 20:
        _l.debug(msg)


def err(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        エラーをログファイルに記録する
        """
        try:
            r = f(*args, **kwargs)
            return r
        except Exception as e:
            from app import create_app
            app_log(logging.ERROR, str(datetime.datetime.now()))
            app_log(logging.ERROR, traceback.format_exc())
            raise e
    return decorated_function


def credential(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        Viewにアクセス制限を掛けるデコレータ
        """
        if "credential" not in flask.request.url:
            return "Required Credential"

        from app import conf
        if conf()['CREDENTIAL'] not in flask.request.url:
            return "Wrong Credential Code"
        r = f(*args, **kwargs)
        return r
    return decorated_function
