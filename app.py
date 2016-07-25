# -*- coding: utf-8 -*-
import os
import threading
import logging
from logging.handlers import RotatingFileHandler
import example
from flask import Flask
from views import data
from views import config as c
from views import sitemap

tls = threading.local()


def create_app(config=None):
    app = Flask(__name__, static_url_path='/static')

    # configをtlsに保存して、2回目以降呼び出したときにもmanage.pyで指定したconfigにアクセスする
    if config:
        tls.config_path = config
    if hasattr(tls, "config_path"):
        config_path = tls.config_path
        config = os.path.join(app.root_path, config_path)

    # config未設定のときはdefault configを読む
    if config is None:
        config = os.path.join(app.root_path, 'config/local.py')
    app.config.from_pyfile(config)
    app.debug = app.config.get('debug')

    # 機能毎のURLを定義
    app.register_blueprint(example.app, url_prefix="/")
    app.register_blueprint(data.app, url_prefix="/data")
    app.register_blueprint(c.app, url_prefix="/config")
    app.register_blueprint(sitemap.app, url_prefix="/sitemap")

    # log
    handler = RotatingFileHandler('/tmp/error.log', maxBytes=1024 * 1024 * 10, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    return app


def conf():
    return create_app().config
