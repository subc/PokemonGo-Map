# -*- coding: utf-8 -*-
from flask import Blueprint
from views.decorator import err, credential
from kvs import set_profiler_account_level, get_profiler_account_level


app = Blueprint("account",
                __name__,
                url_prefix='/<user_url_slug>')


@app.route('/', methods=['GET'])
@err
@credential
def account():
    """
    Gets worker account
    """
    import random
    import uuid
    username = str(uuid.uuid4())
    username = "e3a69e62-9cc9-4846-9f08-58efcc598ae8"
    level = random.randint(1, 10)
    set_profiler_account_level(username, level)
    return "ok:{}".format(str(get_profiler_account_level()))
