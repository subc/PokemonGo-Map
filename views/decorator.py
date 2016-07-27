# -*- coding: utf-8 -*-
import logging
import traceback
from functools import wraps
from flask import redirect, url_for
import datetime


IGNORE_NAMES = [
    "favicon.ico",
    "robots.txt",
    "apple-touch-icon.png",
    "apple-touch-icon-precomposed.png",
    "mstile-144x144.png",
    "browserconfig.xml",
]


def app_log(log_level, msg):
    prefix = '[{}] '.format(datetime.datetime.now())
    msg = prefix + msg

    from app import create_app
    _l = create_app().logger
    if log_level >= 50:
        _l.critical(msg)
    elif log_level >= 40:
        _l.error(msg)
    elif log_level >= 20:
        _l.debug(msg)


def requires_site_title(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        site_title = kwargs.pop('site_title')

        if site_title == "example":
            return "HelloWorld"

        if site_title in IGNORE_NAMES:
            # faviconやrobots.txtにアクセスされた場合
            app_log(logging.ERROR, "File does not exist :{}".format(site_title))
            return "File does not exist"
        try:
            site = Site.get_title(site_title)
        except IndexError:
            # サイトトップにリダイレクト
            app_log(logging.ERROR, "Site title does not exist :{}".format(site_title))
            return redirect(url_for('site_top.index'))
        return f(site, **kwargs)
    return decorated_function


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
            now = datetime.datetime.now()
            create_app().logger.critical(datetime.datetime.now())
            create_app().logger.critical("{}\n{}".format(str(now), traceback.format_exc()))
            raise e
    return decorated_function
