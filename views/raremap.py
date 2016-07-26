# -*- coding: utf-8 -*-
import json

import flask
from flask import Blueprint

from example import get_pokemarkers
from points import get_near_point
from example import get_google_map_api, render_template, get_map, get_rare_markers

app = Blueprint("raremap",
                __name__,
                url_prefix='/<user_url_slug>')

@app.route('/')
def raremap():
    # clear_stale_pokemons()
    from app import conf
    key = get_google_map_api(conf())
    fullmap, fullmap_js = get_map()
    config = conf()
    zoom = conf().get('ZOOM')
    return render_template(
            'rare_fullmap.html',
            key=key,
            zoom=zoom,
            GOOGLEMAPS_KEY=key,
            fullmap=fullmap,
            fullmap_js=fullmap_js,
            auto_refresh=conf().get('AUTO_REFRESH'))


@app.route('/data/', methods=['GET'])
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
    ct = 0
    for _x, _y, _ in POINTS:
        if point_x == _x and point_y == _y:
            # print "No.is...{}".format(ct)
            break
        ct += 1

    return json.dumps(get_rare_markers())
