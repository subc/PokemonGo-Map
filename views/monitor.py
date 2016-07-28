# -*- coding: utf-8 -*-
import json

import flask
from flask import Blueprint

from example import get_pokemarkers
from module.account_monitor import get_all_login_failed
from points import get_near_point
from example import get_google_map_api, render_template, get_map, get_rare_markers
from command.check_worker import CheckWorker

app = Blueprint("monitor",
                __name__,
                url_prefix='/<user_url_slug>')


@app.route('/')
def monitor():
    # acc wrong password
    all_login_failed = get_all_login_failed()

    # redis
    ok_group, warning_group, ng_group = CheckWorker()._run(cut=True)

    return render_template(
        'monitor.html',
        all_login_failed=all_login_failed.items(),
        ok_group=ok_group,
        warning_group=warning_group,
        ng_group=ng_group,
    )
