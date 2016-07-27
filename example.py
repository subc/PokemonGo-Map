#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import flask
from flask import render_template, Blueprint
from flask import Flask, render_template
from flask_googlemaps import Map, DEFAULT_ICON, icons, Markup
import random
import os
import re
import sys
import struct
import json
import requests
import argparse
import getpass
import threading
import werkzeug.serving
import pokemon_pb2
import time
from google.protobuf.internal import encoder
from google.protobuf.message import DecodeError
from s2sphere import *
from gpsoauth import perform_master_login, perform_oauth
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.adapters import ConnectionError
from requests.models import InvalidURL

from constants.dictionary import POKEMON_JAPANESE_NAME
from constants.cp import POKEMON_MAX_CP
from constants.rarity import RARE_POKEMON
from points import POINTS, get_near_point
from transform import *
from kvs import *
from threading import local

from views.decorator import err

app = Blueprint("example",
                __name__,
                url_prefix='/<user_url_slug>')


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

API_URL = 'https://pgorelease.nianticlabs.com/plfe/rpc'
LOGIN_URL = \
    'https://sso.pokemon.com/sso/login?service=https://sso.pokemon.com/sso/oauth2.0/callbackAuthorize'
LOGIN_OAUTH = 'https://sso.pokemon.com/sso/oauth2.0/accessToken'
APP = 'com.nianticlabs.pokemongo'

with open('credentials.json') as file:
	credentials = json.load(file)

PTC_CLIENT_SECRET = credentials.get('ptc_client_secret', None)
ANDROID_ID = credentials.get('android_id', None)
SERVICE = credentials.get('service', None)
CLIENT_SIG = credentials.get('client_sig', None)
# GOOGLEMAPS_KEY = credentials.get('gmaps_key', None)

SESSION = requests.session()
SESSION.headers.update({'User-Agent': 'Niantic App'})
SESSION.verify = False

global_password = None
global_token = None
access_token = None
DEBUG = True
VERBOSE_DEBUG = False  # if you want to write raw request/response to the console
COORDS_LATITUDE = 0
COORDS_LONGITUDE = 0
COORDS_ALTITUDE = 0
FLOAT_LAT = 0
FLOAT_LONG = 0
NEXT_LAT = 0
NEXT_LONG = 0
auto_refresh = 0
default_step = 0.001
api_endpoint = None
pokestops = {}
numbertoteam = {  # At least I'm pretty sure that's it. I could be wrong and then I'd be displaying the wrong owner team of gyms.
    0: 'Gym',
    1: 'Mystic',
    2: 'Valor',
    3: 'Instinct',
}
origin_lat, origin_lon = None, None
is_ampm_clock = False
tls = local()

# stuff for in-background search thread

search_thread = None

def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer

def parse_unicode(bytestring):
    decoded_string = bytestring.decode(sys.getfilesystemencoding())
    return decoded_string


def debug(message):
    if DEBUG:
        print '[-] {}'.format(message)


def time_left(ms):
    s = ms / 1000
    (m, s) = divmod(s, 60)
    (h, m) = divmod(m, 60)
    return (h, m, s)


def encode(cellid):
    output = []
    encoder._VarintEncoder()(output.append, cellid)
    return b''.join(output)


def getNeighbors():
    origin = CellId.from_lat_lng(LatLng.from_degrees(FLOAT_LAT,
                                                     FLOAT_LONG)).parent(15)
    walk = [origin.id()]

    # 10 before and 10 after

    next = origin.next()
    prev = origin.prev()
    for i in range(10):
        walk.append(prev.id())
        walk.append(next.id())
        next = next.next()
        prev = prev.prev()
    return walk


def f2i(float):
    return struct.unpack('<Q', struct.pack('<d', float))[0]


def f2h(float):
    return hex(struct.unpack('<Q', struct.pack('<d', float))[0])


def h2f(hex):
    return struct.unpack('<d', struct.pack('<Q', int(hex, 16)))[0]


def retrying_set_location(location_name):
    """
    Continue trying to get co-ords from Google Location until we have them
    :param location_name: string to pass to Location API
    :return: None
    """

    while True:
        try:
            set_location(location_name)
            return
        except (GeocoderTimedOut, GeocoderServiceError), e:
            debug(
                'retrying_set_location: geocoder exception ({}), retrying'.format(
                    str(e)))
        time.sleep(1.25)


def set_location(location_name):
    global origin_lat
    global origin_lon
    s = location_name.split(" ")
    local_lat = float(s[0])
    local_lng = float(s[1])
    origin_lat, origin_lon = local_lat, local_lng
    alt = 0.0
    print('[!] lat/long/alt: {} {} {}'.format(local_lat, local_lng, alt))
    set_location_coords(local_lat, local_lng, alt)


def set_location_coords(lat, long, alt):
    global COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE
    global FLOAT_LAT, FLOAT_LONG
    FLOAT_LAT = lat
    FLOAT_LONG = long
    COORDS_LATITUDE = f2i(lat)  # 0x4042bd7c00000000 # f2i(lat)
    COORDS_LONGITUDE = f2i(long)  # 0xc05e8aae40000000 #f2i(long)
    COORDS_ALTITUDE = f2i(alt)


def get_location_coords():
    return (COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE)


def retrying_api_req(service, api_endpoint, access_token, *args, **kwargs):
    while True:
        try:
            response = api_req(service, api_endpoint, access_token, *args,
                               **kwargs)
            if response:
                return response
            debug('retrying_api_req: api_req returned None, retrying')
        except (InvalidURL, ConnectionError, DecodeError), e:
            debug('retrying_api_req: request error ({}), retrying'.format(
                str(e)))
        time.sleep(1)


def api_req(service, api_endpoint, access_token, *args, **kwargs):
    p_req = pokemon_pb2.RequestEnvelop()
    p_req.rpc_id = 1469378659230941192

    p_req.unknown1 = 2

    (p_req.latitude, p_req.longitude, p_req.altitude) = \
        get_location_coords()

    p_req.unknown12 = 989

    if 'useauth' not in kwargs or not kwargs['useauth']:
        p_req.auth.provider = service
        p_req.auth.token.contents = access_token
        p_req.auth.token.unknown13 = 14
    else:
        p_req.unknown11.unknown71 = kwargs['useauth'].unknown71
        p_req.unknown11.unknown72 = kwargs['useauth'].unknown72
        p_req.unknown11.unknown73 = kwargs['useauth'].unknown73

    for arg in args:
        p_req.MergeFrom(arg)

    protobuf = p_req.SerializeToString()

    r = SESSION.post(api_endpoint, data=protobuf, verify=False)

    p_ret = pokemon_pb2.ResponseEnvelop()
    p_ret.ParseFromString(r.content)

    if VERBOSE_DEBUG:
        print 'REQUEST:'
        print p_req
        print 'Response:'
        print p_ret
        print '''

'''
    time.sleep(0.01)
    return p_ret


def get_api_endpoint(service, access_token, api=API_URL):
    profile_response = None
    while not profile_response:
        profile_response = retrying_get_profile(service, access_token, api,
                                                None)
        if not hasattr(profile_response, 'api_url'):
            debug(
                'retrying_get_profile: get_profile returned no api_url, retrying')
            profile_response = None
            continue
        if not len(profile_response.api_url):
            debug(
                'get_api_endpoint: retrying_get_profile returned no-len api_url, retrying')
            profile_response = None

    return 'https://%s/rpc' % profile_response.api_url


def retrying_get_profile(service, access_token, api, useauth, *reqq):
    profile_response = None
    ct = 0
    while not profile_response:
        profile_response = get_profile(service, access_token, api, useauth,
                                       *reqq)
        if not hasattr(profile_response, 'payload'):
            debug(
                'retrying_get_profile: get_profile returned no payload, retrying')
            profile_response = None
            continue
        if not profile_response.payload:
            debug(
                'retrying_get_profile: get_profile returned no-len payload, retrying')
            profile_response = None

        # 遅延
        if ct > 10:
            print("[-]start sleep... {}sec".format(100))
            time.sleep(10)
            raise ValueError, "[-]cannot login"
        ct += 1

    return profile_response

def get_profile(service, access_token, api, useauth, *reqq):
    req = pokemon_pb2.RequestEnvelop()
    req1 = req.requests.add()
    req1.type = 2
    if len(reqq) >= 1:
        req1.MergeFrom(reqq[0])

    req2 = req.requests.add()
    req2.type = 126
    if len(reqq) >= 2:
        req2.MergeFrom(reqq[1])

    req3 = req.requests.add()
    req3.type = 4
    if len(reqq) >= 3:
        req3.MergeFrom(reqq[2])

    req4 = req.requests.add()
    req4.type = 129
    if len(reqq) >= 4:
        req4.MergeFrom(reqq[3])

    req5 = req.requests.add()
    req5.type = 5
    if len(reqq) >= 5:
        req5.MergeFrom(reqq[4])
    return retrying_api_req(service, api, access_token, req, useauth=useauth)

def login_google(username, password):
    print '[!] Google login for: {}'.format(username)
    r1 = perform_master_login(username, password, ANDROID_ID)
    r2 = perform_oauth(username,
                       r1.get('Token', ''),
                       ANDROID_ID,
                       SERVICE,
                       APP,
                       CLIENT_SIG, )
    return r2.get('Auth')


def login_ptc(username, password):
    print '[!] PTC login for: {}'.format(username)
    head = {'User-Agent': 'Niantic App'}
    r = SESSION.get(LOGIN_URL, headers=head)
    if r is None:
        return render_template('nope.html', fullmap=fullmap)

    try:
        jdata = json.loads(r.content)
    except ValueError, e:
        debug('login_ptc: could not decode JSON from')
        # debug(b"".format(r.content))
        return None

    # Maximum password length is 15 (sign in page enforces this limit, API does not)

    if len(password) > 15:
        print '[!] Trimming password to 15 characters'
        password = password[:15]

    data = {
        'lt': jdata['lt'],
        'execution': jdata['execution'],
        '_eventId': 'submit',
        'username': username,
        'password': password,
    }
    r1 = SESSION.post(LOGIN_URL, data=data, headers=head)

    ticket = None
    try:
        ticket = re.sub('.*ticket=', '', r1.history[0].headers['Location'])
    except Exception, e:
        if DEBUG:
            print r1.json()['errors'][0]
        return None

    data1 = {
        'client_id': 'mobile-app_pokemon-go',
        'redirect_uri': 'https://www.nianticlabs.com/pokemongo/error',
        'client_secret': PTC_CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'code': ticket,
    }
    r2 = SESSION.post(LOGIN_OAUTH, data=data1)
    access_token = re.sub('&expires.*', '', r2.content)
    access_token = re.sub('.*access_token=', '', access_token)

    return access_token


def get_heartbeat(service,
                  api_endpoint,
                  access_token,
                  response, ):
    m4 = pokemon_pb2.RequestEnvelop.Requests()
    m = pokemon_pb2.RequestEnvelop.MessageSingleInt()
    m.f1 = int(time.time() * 1000)
    m4.message = m.SerializeToString()
    m5 = pokemon_pb2.RequestEnvelop.Requests()
    m = pokemon_pb2.RequestEnvelop.MessageSingleString()
    m.bytes = str('05daf51635c82611d1aac95c0b051d3ec088a930')
    m5.message = m.SerializeToString()
    walk = sorted(getNeighbors())
    m1 = pokemon_pb2.RequestEnvelop.Requests()
    m1.type = 106
    m = pokemon_pb2.RequestEnvelop.MessageQuad()
    m.f1 = b''.join(map(encode, walk))
    m.f2 = \
        b"\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"
    m.lat = COORDS_LATITUDE
    m.long = COORDS_LONGITUDE
    m1.message = m.SerializeToString()
    response = get_profile(service,
                           access_token,
                           api_endpoint,
                           response.unknown7,
                           m1,
                           pokemon_pb2.RequestEnvelop.Requests(),
                           m4,
                           pokemon_pb2.RequestEnvelop.Requests(),
                           m5, )

    try:
        payload = response.payload[0]
    except (AttributeError, IndexError):
        return

    heartbeat = pokemon_pb2.ResponseEnvelop.HeartbeatPayload()
    heartbeat.ParseFromString(payload)
    return heartbeat

def get_token(service, username, password):
    """
    Get token if it's not None
    :return:
    :rtype:
    """

    global global_token
    if global_token is None:
        if service == 'ptc':
            global_token = login_ptc(username, password)
        else:
            global_token = login_google(username, password)
        return global_token
    else:
        return global_token


def get_args(worker=False):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', '--auth_service',     help='Auth Service', default='ptc')
    parser.add_argument('-u', '--username', help='Username', required=False)
    parser.add_argument('-p', '--password', help='Password', required=False)
    parser.add_argument(
        '-l', '--location', type=parse_unicode, help='Location', required=False)
    parser.add_argument('-st', '--step-limit', help='Steps', required=False)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '-i', '--ignore', help='Comma-separated list of Pokémon names or IDs to ignore')
    group.add_argument(
        '-o', '--only', help='Comma-separated list of Pokémon names or IDs to search')
    parser.add_argument(
        "-ar",
        "--auto_refresh",
        help="Enables an autorefresh that behaves the same as a page reload. " +
             "Needs an integer value for the amount of seconds")
    parser.add_argument(
        '-dp',
        '--display-pokestop',
        help='Display pokéstop',
        action='store_true',
        default=False)
    parser.add_argument(
        '-dg',
        '--display-gym',
        help='Display Gym',
        action='store_true',
        default=False)
    parser.add_argument(
        '-H',
        '--host',
        help='Set web server listening host',
        default='127.0.0.1')
    parser.add_argument(
        '-P',
        '--port',
        type=int,
        help='Set web server listening port',
        default=5000)
    parser.add_argument(
        '-rH',
        '--redishost',
        help='Set redis server host',
        default='127.0.0.1')
    parser.add_argument(
        '-rP',
        '--redisport',
        type=int,
        help='Set redis server port',
        default=6379)
    parser.add_argument(
        "-L",
        "--locale",
        help="Locale for Pokemon names: default en, check locale folder for more options",
        default="en")
    parser.add_argument(
        "-ol",
        "--onlylure",
        help='Display only lured pokéstop',
        action='store_true')
    parser.add_argument(
        '-c',
        '--china',
        help='Coordinates transformer for China',
        action='store_true')
    parser.add_argument(
        '-stop',
        '--stopupdate',
        help='stop update bg',
        action='store_true',
        default=False)
    parser.add_argument(
        "-dpoint",
        "--diffpoint",
        type=int,
        help="偏差",
        default=0)
    parser.add_argument(
    	"-pm",
    	"--ampm_clock",
    	help="Toggles the AM/PM clock for Pokemon timers",
    	action='store_true',
    	default=False)
    parser.add_argument(
        '-d', '--debug', help='Debug Mode', action='store_true')
    parser.set_defaults(DEBUG=True)
    args = parser.parse_args()

    # 差分を入れる
    if int(args.diffpoint):
        from points import POINTS
        _ = POINTS[int(args.diffpoint)]
        args.location = "{} {}".format(_[0], _[1])
        print("_/_/_/_/_/_/_/_/_/_/_/_/_/_/")
        print("set point:{}".format(args.diffpoint))
        print("_/_/_/_/_/_/_/_/_/_/_/_/_/_/")
    elif(worker):
        from points import POINTS
        _ = POINTS[0]
        args.location = "{} {}".format(_[0], _[1])
        print("_/_/_/_/_/_/_/_/_/_/_/_/_/_/")
        print("set point:{}".format(0))
        print("_/_/_/_/_/_/_/_/_/_/_/_/_/_/")

    return args


def get_user_and_password(config, point):
    use_sub_account = get_acc_version(point)

    if config["IS_PRODUCTION"]:
        if use_sub_account:
            return config['ACCOUNTS2'][point]
        return config['ACCOUNTS'][point]
    else:
        return config['USERNAME'], config['PASSWORD']

@memoize
def login(config, point):
    global global_password
    auth_service = "google"
    username, global_password = get_user_and_password(config, point)

    access_token = get_token(auth_service, username, global_password)
    print(access_token)

    if access_token is None:
        time.sleep(5)
        raise Exception('[-] Wrong username/password')

    print '[+] RPC Session Token: {} ...'.format(access_token[:25])

    api_endpoint = get_api_endpoint(auth_service, access_token)
    if api_endpoint is None:
        raise Exception('[-] RPC server offline')

    print '[+][+][+][+][+][+][+][+][+][+][+][+]'
    print '[+] Received API endpoint: {}'.format(api_endpoint)

    profile_response = retrying_get_profile(auth_service, access_token,
                                            api_endpoint, None)
    if profile_response is None or not profile_response.payload:
        raise Exception('Could not get profile')
    #
    print '[+] Login successful'
    #
    # payload = profile_response.payload[0]
    # profile = pokemon_pb2.ResponseEnvelop.ProfilePayload()
    # profile.ParseFromString(payload)
    # print '[+] Username: {}'.format(profile.profile.username)
    #
    # creation_time = \
    #     datetime.fromtimestamp(int(profile.profile.creation_time)
    #                            / 1000)
    # print '[+] You started playing Pokemon Go on: {}'.format(
    #     creation_time.strftime('%Y-%m-%d %H:%M:%S'))
    #
    # for curr in profile.profile.currency:
    #     print '[+] {}: {}'.format(curr.type, curr.amount)

    return api_endpoint, access_token, profile_response


def update_map(point):
    full_path = os.path.realpath(__file__)
    (path, filename) = os.path.split(full_path)
    from app import conf
    config = conf()
    lat, lon, message = POINTS[point]
    # PokemonGo-Map/locales/pokemon.en.json, maybe en
    locale = config.get("LOCALE")
    location = "{} {}".format(lat, lon)
    step_limit = config["STEP_LIMIT"]

    print('[+] Locale is ' + locale)
    pokemonsJSON = json.load(
        open(path + '/locales/pokemon.' + locale + '.json'))

    global DEBUG
    DEBUG = True
    print '[!] DEBUG mode on'

    # only get location for first run
    print('[+] Getting initial location')
    print(location)
    retrying_set_location(location)

    api_endpoint, access_token, profile_response = login(config, point)

    # 10000回繰り返す
    for x in xrange(5):
        if x > 2:
            time.sleep(20)

        # clear_stale_pokemons()

        ignore = []
        only = []

        pos = 1
        x = 0
        y = 0
        dx = 0
        dy = -1
        steplimit2 = step_limit**2
        for step in range(steplimit2):
            debug('looping: step {} of {}'.format((step+1), step_limit**2))
            # debug('steplimit: {} x: {} y: {} pos: {} dx: {} dy {}'.format(steplimit2, x, y, pos, dx, dy))
            # Scan location math
            if -steplimit2 / 2 < x <= steplimit2 / 2 and -steplimit2 / 2 < y <= steplimit2 / 2:
                set_location_coords(x * 0.0025 + lat, y * 0.0025 + lon, 0)
            if x == y or x < 0 and x == -y or x > 0 and x == 1 - y:
                (dx, dy) = (-dy, dx)

            (x, y) = (x + dx, y + dy)

            process_step(config, api_endpoint, access_token, profile_response,
                         pokemonsJSON, ignore, only, point)

            print('Completed: ' + str(
                ((step+1) + pos * .25 - .25) / steplimit2 * 100) + '%')

        global NEXT_LAT, NEXT_LONG
        if (NEXT_LAT and NEXT_LONG and
                (NEXT_LAT != FLOAT_LAT or NEXT_LONG != FLOAT_LONG)):
            print('Update to next location %f, %f' % (NEXT_LAT, NEXT_LONG))
            set_location_coords(NEXT_LAT, NEXT_LONG, 0)
            NEXT_LAT = 0
            NEXT_LONG = 0
        else:
            set_location_coords(origin_lat, origin_lon, 0)



def main():
    full_path = os.path.realpath(__file__)
    (path, filename) = os.path.split(full_path)

    args = get_args(worker=True)
    locale = conf()

    print('[+] Locale is ' + args.locale)
    pokemonsJSON = json.load(
        open(path + '/locales/pokemon.' + args.locale + '.json'))

    if args.debug:
        global DEBUG
        DEBUG = True
        print '[!] DEBUG mode on'

    # only get location for first run
    if not (FLOAT_LAT and FLOAT_LONG):
        print('[+] Getting initial location')
        print(args.location)
        retrying_set_location(args.location)

    if args.auto_refresh:
        global auto_refresh
        auto_refresh = int(args.auto_refresh) * 1000

    if args.ampm_clock:
    	global is_ampm_clock
    	is_ampm_clock = True

    api_endpoint, access_token, profile_response = login(args)

    clear_stale_pokemons()

    steplimit = int(args.step_limit)

    ignore = []
    only = []
    if args.ignore:
        ignore = [i.lower().strip() for i in args.ignore.split(',')]
    elif args.only:
        only = [i.lower().strip() for i in args.only.split(',')]

    pos = 1
    x = 0
    y = 0
    dx = 0
    dy = -1
    steplimit2 = steplimit**2
    for step in range(steplimit2):
        #starting at 0 index
        debug('looping: step {} of {}'.format((step+1), steplimit**2))
        #debug('steplimit: {} x: {} y: {} pos: {} dx: {} dy {}'.format(steplimit2, x, y, pos, dx, dy))
        # Scan location math
        if -steplimit2 / 2 < x <= steplimit2 / 2 and -steplimit2 / 2 < y <= steplimit2 / 2:
            set_location_coords(x * 0.0025 + origin_lat, y * 0.0025 + origin_lon, 0)
        if x == y or x < 0 and x == -y or x > 0 and x == 1 - y:
            (dx, dy) = (-dy, dx)

        (x, y) = (x + dx, y + dy)

        process_step(args, api_endpoint, access_token, profile_response,
                     pokemonsJSON, ignore, only)

        print('Completed: ' + str(
            ((step+1) + pos * .25 - .25) / (steplimit2) * 100) + '%')

    global NEXT_LAT, NEXT_LONG
    if (NEXT_LAT and NEXT_LONG and
            (NEXT_LAT != FLOAT_LAT or NEXT_LONG != FLOAT_LONG)):
        print('Update to next location %f, %f' % (NEXT_LAT, NEXT_LONG))
        set_location_coords(NEXT_LAT, NEXT_LONG, 0)
        NEXT_LAT = 0
        NEXT_LONG = 0
    else:
        set_location_coords(origin_lat, origin_lon, 0)

    # register_background_thread()


def process_step(config, api_endpoint, access_token, profile_response,
                 pokemonsJSON, ignore, only, point):
    print('[+] Searching for Pokemon at location {} {}'.format(FLOAT_LAT, FLOAT_LONG))
    origin = LatLng.from_degrees(FLOAT_LAT, FLOAT_LONG)
    step_lat = FLOAT_LAT
    step_long = FLOAT_LONG
    parent = CellId.from_lat_lng(LatLng.from_degrees(FLOAT_LAT,
                                                     FLOAT_LONG)).parent(15)
    china = False
    display_gym = config['DISPLAY_GYM']
    display_pokestop = config['DISPLAY_POKE_STOP']
    auth_service = "ptc"
    h = get_heartbeat(auth_service, api_endpoint, access_token,
                      profile_response)
    hs = [h]
    seen = {}

    for child in parent.children():
        latlng = LatLng.from_point(Cell(child).get_center())
        set_location_coords(latlng.lat().degrees, latlng.lng().degrees, 0)
        hs.append(
            get_heartbeat(auth_service, api_endpoint, access_token,
                          profile_response))
    set_location_coords(step_lat, step_long, 0)
    visible = []
    wild_pokemon_ct = 0
    for hh in hs:
        try:
            for cell in hh.cells:
                for wild in cell.WildPokemon:
                    hash = wild.SpawnPointId
                    if hash not in seen.keys() or (seen[hash].TimeTillHiddenMs <= wild.TimeTillHiddenMs):
                        wild_pokemon_ct += 1
                        visible.append(wild)
                    seen[hash] = wild.TimeTillHiddenMs
                if cell.Fort:
                    for Fort in cell.Fort:
                        if Fort.Enabled == True:
                            if china:
                                (Fort.Latitude, Fort.Longitude) = \
transform_from_wgs_to_gcj(Location(Fort.Latitude, Fort.Longitude))
                            if Fort.GymPoints and display_gym:
                                set_gym(Fort.FortId, [Fort.Team, Fort.Latitude,
                                                      Fort.Longitude, Fort.GymPoints], point)

                            elif Fort.FortType \
                                and display_pokestop:
                                expire_time = 0
                                if Fort.LureInfo.LureExpiresTimestampMs:
                                    expire_time = datetime\
                                        .fromtimestamp(Fort.LureInfo.LureExpiresTimestampMs / 1000.0)\
                                        .strftime("%H:%M:%S")
                                if (expire_time != 0):
                                    pokestops[Fort.FortId] = [Fort.Latitude,
                                                              Fort.Longitude, expire_time]
        except AttributeError:
            break
    print("[+]pokemon count:{}".format(wild_pokemon_ct))

    for poke in visible:
        pokeid = str(poke.pokemon.PokemonId)
        pokename = pokemonsJSON[pokeid]

        disappear_timestamp = time.time() + poke.TimeTillHiddenMs \
            / 1000

        if china:
            (poke.Latitude, poke.Longitude) = \
                transform_from_wgs_to_gcj(Location(poke.Latitude,
                    poke.Longitude))

        set_pokemon(poke.SpawnPointId, {
                        "lat": poke.Latitude,
                        "lng": poke.Longitude,
                        "disappear_time": disappear_timestamp,
                        "id": poke.pokemon.PokemonId,
                        "name": pokename
                        },
                    point=point
                    )


def clear_stale_pokemons():
    current_time = time.time()

    for pokemon_key in get_pokemon_keys():
        pokemon = get_pokemon(pokemon_key)
        if pokemon and current_time > pokemon['disappear_time']:
            print "[+] removing stale pokemon %s at %f, %f from list" % (
                pokemon['name'], pokemon['lat'], pokemon['lng'])
            # delete_pokemon(pokemon_key, point=int(args.diffpoint))


def register_background_thread(initial_registration=False):
    """
    Start a background thread to search for Pokemon
    while Flask is still able to serve requests for the map
    :param initial_registration: True if first registration and thread should start immediately, False if it's being called by the finishing thread to schedule a refresh
    :return: None
    """

    debug('register_background_thread called')
    global search_thread

    if initial_registration:
        if not werkzeug.serving.is_running_from_reloader():
            debug(
                'register_background_thread: not running inside Flask so not starting thread')
            return
        if search_thread:
            debug(
                'register_background_thread: initial registration requested but thread already running')
            return

        debug('register_background_thread: initial registration')
        search_thread = threading.Thread(target=main)

    else:
        debug('register_background_thread: queueing')
        search_thread = threading.Timer(30, main)  # delay, in seconds

    search_thread.daemon = True
    search_thread.name = 'search_thread'
    search_thread.start()


# @app.route('/data', methods=['GET'])
# def data():
#     """
#     Gets all the PokeMarkers via REST
#     :param position: str
#     """
#     # notify(pokemons)
#     first_time = "FirstTime" in flask.request.url
#     x, y = flask.request.url.split("?")[-1].split("&")[0].split(",")
#     point_x, point_y = get_near_point(float(x), float(y))
#     print(point_x, point_y)
#
#     # debug
#     from points import POINTS
#     ct = 0
#     for _x, _y, _ in POINTS:
#         if point_x == _x and point_y == _y:
#             print "No.is...{}".format(ct)
#             break
#         ct += 1
#
#     return json.dumps(get_pokemarkers(point=ct, first_time=first_time))


# @app.route('/raw_data')
# def raw_data():
#     """ Gets raw data for pokemons/gyms/pokestops via REST """
#     return flask.jsonify(pokemons=get_all_pokemon(), gyms=get_all_gym(), pokestops=pokestops)
#
#
# @app.route('/config')
# def config():
#     """ Gets the settings for the Google Maps via REST"""
#     center = {
#         'lat': FLOAT_LAT,
#         'lng': FLOAT_LONG,
#         'zoom': 15,
#         'identifier': "fullmap"
#     }
#     return json.dumps(center)
#
#
# @app.route('/configc')
# def configc():
#     """
#     Gets the settings for the Google Maps via REST
#     """
#     x, y = flask.request.url.split("?")[1].replace("p=", "").split(",")
#     center = {
#         'lat': x,
#         'lng': y,
#         'zoom': 15,
#         'identifier': "fullmap"
#     }
#     return json.dumps(center)


@app.route('/')
@err
def fullmap():
    # clear_stale_pokemons()
    from app import conf
    key = get_google_map_api(conf())
    fullmap, fullmap_js = get_map()
    config = conf()
    zoom = conf().get('ZOOM')
    is_maintenance = conf().get('IS_MAINTENANCE')
    return render_template(
            'example_fullmap.html',
            key=key,
            zoom=zoom,
            GOOGLEMAPS_KEY=key,
            is_maintenance=is_maintenance,
            fullmap=fullmap,
            fullmap_js=fullmap_js,
            auto_refresh=conf().get('AUTO_REFRESH'))


@app.route('/next_loc')
def next_loc():
    global NEXT_LAT, NEXT_LONG

    lat = flask.request.args.get('lat', '')
    lon = flask.request.args.get('lon', '')
    if not (lat and lon):
        print('[-] Invalid next location: %s,%s' % (lat, lon))
    else:
        print('[+] Saved next location as %s,%s' % (lat, lon))
        NEXT_LAT = float(lat)
        NEXT_LONG = float(lon)
        return 'ok'


def get_marker_for_debug(point):
    """
    デバッグ用、探索範囲をpointする
    """
    r = []
    ct = -1
    from app import conf
    # step = conf().get("STEP_LIMIT")
    for _x, _y, flavor_text in POINTS:
        ct += 1

        # red
        red_marker = {
            'icon': icons.dots.red,
            'lat': _x,
            'lng': _y,
            'infobox': "{} position:{},{} No:{}".format(flavor_text, _x, _y, ct),
            'type': 'custom',
            'key': 'start-position:{}:{}'.format(_x, _y),
            'disappear_time': -1
        }
        r.append(red_marker)

        # blue 超重い
        # d = (step - 1) / 2
        # for y in [-1 * d, d]:
        #     for x in [-1 * d, d]:
        #         if x == y == 0:
        #             continue
        #         __x = _x + 0.0025 * x
        #         __y = _y + 0.0025 * y
        #         r.append({
        #             'type': 'custom',
        #             'key': 'options-position:{}:{}'.format(str(__x), str(__y)),
        #             'disappear_time': -1,
        #             'icon': icons.dots.blue,
        #             'lat': __x,
        #             'lng': __y,
        #             'infobox': "edge:{}:{}".format(str(__x), str(__y))
        #         })
    return r


def is_rare_pokemon(pokemon_id):
    # max_cp が2000以上
    max_cp = POKEMON_MAX_CP[pokemon_id]
    if max_cp <= 2500:
        return False

    # 特定ポケモン除外
    ignore_id = [
        55,  # ゴルダック
        127,  # カイロス
    ]
    if pokemon_id in ignore_id:
        return False

    return True


def get_rare_markers():
    """
    first_timeはhtmlのjs側で制御してる。
    :param point:
    :param first_time:
    :param enable_gym:
    """
    pokeMarkers = []
    for point in range(len(POINTS)):
        if random.randint(1, 10) != 3:
            continue

        for pokemon_key in get_pokemon_keys(point=point):
            pokemon = get_pokemon(pokemon_key, point=point)
            if not pokemon:
                continue
            datestr = datetime.fromtimestamp(pokemon[
                'disappear_time'])
            dateoutput = datestr.strftime("%H:%M:%S")
            if is_ampm_clock:
                dateoutput = datestr.strftime("%I:%M%p").lstrip('0')
            pokemon['disappear_time_formatted'] = dateoutput
            pokemon['jpn_name'] = POKEMON_JAPANESE_NAME.get(pokemon['id'])

            # check rare pokemon
            if not is_rare_pokemon(pokemon['id']):
                continue

            if pokemon['id'] in POKEMON_MAX_CP:
                pokemon['max_cp'] = int(POKEMON_MAX_CP[pokemon['id']])

                LABEL_TMPL = u'''
<div><b>{jpn_name}</b><span> </span><small><a href='http://pokemongo.gamepress.gg/pokemon/{id}' target='_blank' title='View in Pokedex'>#{id}</a> MaxCP: {max_cp}</small></div>
<div>逃走まであと - {disappear_time_formatted} <span class='label-countdown' disappears-at='{disappear_time}'></span></div>
'''
            else:
                LABEL_TMPL = u'''
<div><b>{jpn_name}</b><span> - </span><small><a href='http://pokemongo.gamepress.gg/pokemon/{id}' target='_blank' title='View in Pokedex'>#{id}</a></small></div>
<div>逃走まであと - {disappear_time_formatted} <span class='label-countdown' disappears-at='{disappear_time}'></span></div>
'''

            label = LABEL_TMPL.format(**pokemon)
            #  NOTE: `infobox` field doesn't render multiple line string in frontend
            label = label.replace('\n', '')
            large_icon = int(pokemon["id"]) in RARE_POKEMON
            icon = '../static/{}/{}.png'.format("larger-icons" if large_icon else "icons", pokemon["id"])
            pokeMarkers.append({
                'type': 'pokemon',
                'key': pokemon_key,
                'disappear_time': pokemon['disappear_time'],
                'icon': icon,
                'lat': pokemon["lat"],
                'lng': pokemon["lng"],
                'infobox': label
            })

    return pokeMarkers


def get_pokemarkers(point=0, first_time=False, enable_gym=False):
    """
    first_timeはhtmlのjs側で制御してる。
    :param point:
    :param first_time:
    :param enable_gym:
    """
    # 範囲通知用のマーカー
    if first_time:
        pokeMarkers = get_marker_for_debug(point)
    else:
        pokeMarkers = []

    for pokemon_key in get_pokemon_keys(point=point):
        pokemon = get_pokemon(pokemon_key, point=point)
        if not pokemon:
            continue
        datestr = datetime.fromtimestamp(pokemon[
            'disappear_time'])
        dateoutput = datestr.strftime("%H:%M:%S")
        if is_ampm_clock:
        	dateoutput = datestr.strftime("%I:%M%p").lstrip('0')
        pokemon['disappear_time_formatted'] = dateoutput
        pokemon['jpn_name'] = POKEMON_JAPANESE_NAME.get(pokemon['id'])

        if pokemon['id'] in POKEMON_MAX_CP:
            pokemon['max_cp'] = int(POKEMON_MAX_CP[pokemon['id']])
            LABEL_TMPL = u'''
<div><b>{jpn_name}</b><span> </span><small><a href='http://pokemongo.gamepress.gg/pokemon/{id}' target='_blank' title='View in Pokedex'>#{id}</a> MaxCP: {max_cp}</small></div>
<div>逃走まであと - {disappear_time_formatted} <span class='label-countdown' disappears-at='{disappear_time}'></span></div>
'''
        else:
            LABEL_TMPL = u'''
<div><b>{jpn_name}</b><span> - </span><small><a href='http://pokemongo.gamepress.gg/pokemon/{id}' target='_blank' title='View in Pokedex'>#{id}</a></small></div>
<div>逃走まであと - {disappear_time_formatted} <span class='label-countdown' disappears-at='{disappear_time}'></span></div>
'''

        label = LABEL_TMPL.format(**pokemon)
        #  NOTE: `infobox` field doesn't render multiple line string in frontend
        label = label.replace('\n', '')
        large_icon = int(pokemon["id"]) in RARE_POKEMON
        icon = 'static/{}/{}.png'.format("larger-icons" if large_icon else "icons", pokemon["id"])
        pokeMarkers.append({
            'type': 'pokemon',
            'key': pokemon_key,
            'disappear_time': pokemon['disappear_time'],
            'icon': icon,
            'lat': pokemon["lat"],
            'lng': pokemon["lng"],
            'infobox': label
        })

    if not enable_gym:
        return pokeMarkers

    for gym_key in get_gym_keys(point):
        gym = get_gym(gym_key, point)
        if gym[0] == 0:
            color = "rgba(0,0,0,.4)"
        if gym[0] == 1:
            color = "rgba(74, 138, 202, .6)"
        if gym[0] == 2:
            color = "rgba(240, 68, 58, .6)"
        if gym[0] == 3:
            color = "rgba(254, 217, 40, .6)"

        icon = 'static/forts/'+numbertoteam[gym[0]]+'_large.png'
        pokeMarkers.append({
            'icon': 'static/forts/' + numbertoteam[gym[0]] + '.png',
            'type': 'gym',
            'key': gym_key,
            'disappear_time': -1,
            'lat': gym[1],
            'lng': gym[2],
            'infobox': "<div><center><b style='color:" + color + "'>Team " + numbertoteam[gym[0]] + "</b><br><img id='" + numbertoteam[gym[0]] + "' height='100px' src='"+icon+"'><br>Prestige: " + str(gym[3]) + "</center>"
        })
    for stop_key in pokestops:
        stop = pokestops[stop_key]
        if stop[2] > 0:
            pokeMarkers.append({
                'type': 'lured_stop',
                'key': stop_key,
                'disappear_time': -1,
                'icon': 'static/forts/PstopLured.png',
                'lat': stop[0],
                'lng': stop[1],
                'infobox': 'Lured Pokestop, expires at ' + stop[2],
            })
        else:
            pokeMarkers.append({
                'type': 'stop',
                'key': stop_key,
                'disappear_time': -1,
                'icon': 'static/forts/Pstop.png',
                'lat': stop[0],
                'lng': stop[1],
                'infobox': 'Pokestop',
            })
    return pokeMarkers


def get_google_map_api(config):
    keys = config.get('GOOGLEMAPS_KEYS')
    return random.choice(keys)


def get_map():
    from app import conf
    config = conf()
    origin_lat = config.get('LAT')
    origin_lon = config.get('LON')
    key = get_google_map_api(config)
    fullmap = Map(
        identifier="fullmap2",
        style='height:100%;width:100%;top:0;left:0;position:absolute;z-index:200;',
        lat=origin_lat,
        lng=origin_lon,
        markers=get_pokemarkers(),
        zoom='20')
    fullmap_js = Markup(
            fullmap.render(
                    'googlemaps/gmapjs.html',
                    gmap=fullmap,
                    DEFAULT_ICON=DEFAULT_ICON,
                    GOOGLEMAPS_KEY=key
            )
    )
    return fullmap, fullmap_js


def start(debug, threaded, host, port):
    app.run(debug=True, threaded=True, host=host, port=port)


def start_production():
    app.run(debug=True)

if __name__ == '__main__':
    args = get_args()
    if not args.stopupdate:
        register_background_thread(initial_registration=True)
    else:
        # スタンドアローン
        retrying_set_location(args.location)
        if args.auto_refresh:
            auto_refresh = int(args.auto_refresh) * 1000
    start(debug=True, threaded=True, host=args.host, port=args.port)
    # app.run(debug=True, threaded=True, host=args.host, port=args.port)
