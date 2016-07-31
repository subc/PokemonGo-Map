# -*- coding: utf-8 -*-
import json

import flask
from flask import Blueprint

from example import get_pokemarkers
from points import get_near_point
from views.decorator import err

app = Blueprint("date",
                __name__,
                url_prefix='/<user_url_slug>')


@app.route('/', methods=['GET'])
@err
def data():
    """
    Gets all the PokeMarkers via REST
    :param position: str
    """
    first_time = "FirstTime" in flask.request.url
    enable_gym = "gym" in flask.request.url
    x, y = flask.request.url.split("?")[-1].split("&")[0].split(",")

    point_x, point_y = get_near_point(float(x), float(y))

    # debug
    from points import POINTS
    # print len(POINTS)
    ct = 0
    for _x, _y, _ in POINTS:
        if point_x == _x and point_y == _y:
            # print "No.is...{}".format(ct)
            break
        ct += 1

    return json.dumps(get_pokemarkers(point=ct, first_time=first_time, enable_gym=enable_gym))
