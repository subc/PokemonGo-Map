# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import datetime

from rarity import RARE_POKEMON
from slacker import Slacker
SLACK_TOKEN = "xoxp-13918973506-15373952882-61429408502-0de1196a97"
SLACK_CHANNEL = "pokemon-go"


def notify(pokemons):
    for pokemon in pokemons.values():
        execute(pokemon)


def execute(pokemon):
    # common pokemon dose not notify
    if pokemon["id"] not in RARE_POKEMON:
        return

    # notify
    n_pokemon = NotifyPokemon(pokemon)
    if n_pokemon.is_expired():
        # 通知済みのポケモンなら何もしない
        return

    print("notify:", n_pokemon.notify_message)
    _notify(n_pokemon)


def _notify(n_pokemon):
    # slack通知
    slack_client = Slacker(SLACK_TOKEN)
    slack_client.chat.post_message(SLACK_CHANNEL, n_pokemon.notify_message)

    # 通知済みと設定する
    n_pokemon.set_notified()


class NotifyPokemon(object):
    def __init__(self, pokemon):
        self.id = pokemon['id']
        self.name = pokemon['name']
        self.disappear_time = pokemon["disappear_time"]
        self.lat = pokemon["lat"]
        self.lng = pokemon["lng"]
        self._pokemon = pokemon

    def is_expired(self):
        if not self._pokemon:
            return True
        return "_notified" in self._pokemon

    def set_notified(self):
        _ = self._pokemon
        _["_notified"] = 1

    @property
    def disappear_time_formatted(self):
        datestr = datetime.fromtimestamp(self.disappear_time)
        return datestr.strftime("%H:%M:%S")

    @property
    def key(self):
        return ",".join([str(self.id),
                         self.disappear_time_formatted,
                         str(self.lat),
                         str(self.lng),
                         ])

    @property
    def notify_message(self):
        return "コイキング出現({})[id:{}] expired_at:{} \n".format(self.name, self.id, self.disappear_time_formatted) + self.google_map_url

    @property
    def google_map_url(self):
        """
        example:
        http://maps.googleapis.com/maps/api/staticmap?center=47.4908499,11.0983542&zoom=15&format=png&sensor=false&size=640x480&maptype=roadmap&markers=47.4908499,11.0983542
        """
        _base = "http://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom=15&format=png&sensor=false&size=640x480&maptype=roadmap&markers={lat},{lng}"
        return _base.format(lat=self.lat, lng=self.lng)
