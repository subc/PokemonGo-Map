# -*- coding: utf-8 -*-
from flask import render_template, Blueprint
from datetime import datetime

app = Blueprint("sitemap",
                __name__,
                url_prefix='/<user_url_slug>')


@app.route("/sitemap.xml")
def sitemap():
    """
    googleクローラー用のsitemap.xml
    """
    return render_template('sitemap/sitemap.html', now=datetime.now())
