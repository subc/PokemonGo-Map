# -*- coding: utf-8 -*-
import json
import random
import flask
from flask import Blueprint
import threading
from example import get_pokemarkers
from kvs import incr_point_access
from module.tls_property import cached_tls_random
from points import get_near_point
from views.decorator import err

app = Blueprint("date",
                __name__,
                url_prefix='/<user_url_slug>')

tls = threading.local()


@app.route('/', methods=['GET'])
@err
def data():
    """
    Gets all the PokeMarkers via REST
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

    # profile
    if random.randint(1, 20) == 1:
        incr_point_access(ct)

    return json.dumps(A.get_marker(ct, first_time))


class A(object):
    @classmethod
    @cached_tls_random
    def get_marker(cls, point, first_time):
        return get_pokemarkers(point=point, first_time=first_time, enable_gym=False)
