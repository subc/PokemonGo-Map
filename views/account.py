# -*- coding: utf-8 -*-
import json

import flask
from flask import Blueprint

from example import get_pokemarkers
from points import get_near_point
from views.decorator import err, credential

app = Blueprint("date",
                __name__,
                url_prefix='/<user_url_slug>')


@app.route('/', methods=['GET'])
@err
@credential
def account():
    """
    Gets worker account
    """
    return ok
