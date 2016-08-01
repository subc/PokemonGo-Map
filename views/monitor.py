# -*- coding: utf-8 -*-
import json

import flask
from flask import Blueprint

from example import get_pokemarkers
from module.account_monitor import get_all_login_failed
from points import get_near_point, POINTS
from example import get_google_map_api, render_template, get_map, get_rare_markers
from command.check_worker import CheckWorker
from kvs import get_pokemon_count
from views.decorator import credential

app = Blueprint("monitor",
                __name__,
                url_prefix='/<user_url_slug>')


@app.route('/')
@credential
def monitor():
    # acc wrong password
    all_login_failed = get_all_login_failed()

    # redis
    result = []
    total = 0
    for x in xrange(len(POINTS)):
        value = get_pokemon_count(x)
        if value and "," in value:
            _ = str(value).split(str(","))
            result.append((x, int(_[0]), _[1]))
            total += int(_[0])
        else:
            result.append((x, None, value))

    return render_template(
        'monitor.html',
        all_login_failed=all_login_failed.items(),
        redis_data=result,
        total=total
    )
