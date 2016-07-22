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
    center = {
        'lat': origin_lat,
        'lng': origin_lon,
        'zoom': 15,
        'identifier': "fullmap"
    }
    return json.dumps(center)


@app.route('/c')
def configc():
    """
    Gets the settings for the Google Maps via REST
    """
    x, y = flask.request.url.split("?")[1].replace("p=", "").split(",")
    center = {
        'lat': x,
        'lng': y,
        'zoom': 15,
        'identifier': "fullmap"
    }
    return json.dumps(center)
