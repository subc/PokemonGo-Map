# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from threading import local
cache = {}
import numpy


def get_near_point(x, y):
    key = "{}:{}".format(x, y)
    if key in cache:
        return cache[key]

    near = None
    for point_x, point_y, _ in POINTS:
        if near is None:
            near = (point_x, point_y, _distance(x, y, point_x, point_y))
            continue
        di = _distance(x, y, point_x, point_y)
        if di < near[2]:
            near = (point_x, point_y, di)
    return near[0], near[1]


def _distance(x1, y1, x2, y2):
    a = numpy.array([x1, y1])
    b = numpy.array([x2, y2])
    u = b - a
    return numpy.linalg.norm(u)


def main():
    from flavor import get_flavor_text
    base_x, base_y = (48.1404235, 11.5631706)
    step = 1
    step_base = 0.0025
    for x in xrange(-1 * step, step + 1):
        for y in xrange(-1 * step, step + 1):
            _x = base_x + x * step_base * 9
            _y = base_y + y * step_base * 9
            print("({}, {}, '{}'),".format(_x, _y, get_flavor_text()))

if __name__ == '__main__':
    main()


POINTS = [
    (48.1179235, 11.5406706, '不幸の波を生成しています'),
    (48.1179235, 11.5631706, '滞在しています'),
    (48.1179235, 11.5856706, 'ラクダ:迷子になっています'),
    (48.1404235, 11.5406706, '猫:えさ場No.8'),
    (48.1404235, 11.5631706, 'グラフィックスを引き締めています'),
    (48.1404235, 11.5856706, 'ユニットをスナップ撮影しています'),
    (48.1629235, 11.5406706, 'CONTROLNET送信装置を調整中'),
    (48.1629235, 11.5631706, '濡れた砂をアニメートしています'),
    (48.1629235, 11.5856706, '下水を浄化中'),
]
