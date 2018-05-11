# -*- coding: utf-8 -*-
from datetime import datetime

import logging


logger = logging.getLogger('Render Timer')
profiling_info = {}


def profile_time_set(key):
    global profiling_info
    profiling_info[key] = datetime.now()


def profile_time_print(key, msg=None):
    global profiling_info
    startt = profiling_info.get(key, None)
    if startt is None:
        return
    duration = (datetime.now() - startt).total_seconds()
    msg = msg + ' ' if msg else ''
    logger.info(msg + 'processing time for %s: %10.8fs' % (key, duration))
    try:
        del profiling_info[key]
    except KeyError:
        pass


def tilerender_before(event):
    profile_time_set('%s %s' % (event.tile_href, id(event.tile_node)))


def tilerender_after(event):
    profile_time_print('%s %s' % (event.tile_href, id(event.tile_node)), 'Tile')  # noqa


def transforms_before(event):
    profile_time_set('alltransforms')


def transforms_after(event):
    profile_time_print('alltransforms', 'All transforms')


def transformsingle_before(event):
    profile_time_set('%s %s' % (event.name, id(event.handler)))


def transformsingle_after(event):
    profile_time_print('%s %s' % (event.name, id(event.handler)), 'Transform')
