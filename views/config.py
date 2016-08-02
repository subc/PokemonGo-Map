# -*- coding: utf-8 -*-
import json

import flask
from flask import Blueprint


app = Blueprint("config",
                __name__,
                url_prefix='/<user_url_slug>')


@app.route('/')
def config():
    """ Gets the settings for the Google Maps via REST"""
    from app import conf
    config = conf()
    origin_lat = conf().get('LAT')
    origin_lon = conf().get('LON')
    zoom = conf().get('ZOOM')
    center = {
        'lat': origin_lat,
        'lng': origin_lon,
        'zoom': zoom,
        'identifier': "fullmap"
    }
    return json.dumps(center)


@app.route('/c')
def configc():
    """
    Gets the settings for the Google Maps via REST
    """
    from app import conf
    config = conf()
    zoom = conf().get('ZOOM')

    p = flask.request.url.split("?")[1].replace("p=", "").split(",")
    if len(p) == 2:
        x, y = p
    elif len(p) == 3:
        x, y, zoom = p

        # 古いver対応
        if "z" in zoom:
            zoom = 18
    else:
        x = config.get('LAT')
        y = config.get('LON')

    center = {
        'lat': x,
        'lng': y,
        'zoom': int(zoom),
        'identifier': "fullmap"
    }
    return json.dumps(center)
