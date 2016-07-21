# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from points import get_near_point


def test_get_near_point():
    x = 47.4458499
    y = 11.0533542
    print get_near_point(x, y)
    assert get_near_point(x, y)[0] == x
    assert get_near_point(x, y)[1] == y

    x = 47.5358499
    y = 11.0983542
    print get_near_point(x, y)
    assert get_near_point(x, y)[0] == x
    assert get_near_point(x, y)[1] == y

    x = 147.5358499
    y = -11.0983542
    get_near_point(x, y)

    x = -147.5358499
    y = -11.0983542
    get_near_point(x, y)
