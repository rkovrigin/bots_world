from copy import copy, deepcopy
from random import randrange
from threading import Thread, Event
from time import sleep, time

from map import Map
from bot import Bot
from mineral import Mineral
from collections import namedtuple

SUN_RATE = 10
DAYS_IN_MONTH = 30
MONTHS = 12

sun_rates = [8, 8, 10, 12, 14, 16, 18, 14, 12, 8, 10, 6, 4]

Data = namedtuple("Data", ["cycle", "day", "population", "sun_rate"])


class World(Thread):
    def __init__(self, queue, x, y, init_bot_amount=100, init_mineral_amount=400, event=Event()):
        Thread.__init__(self)
        self._map = Map(x, y, wrapper=True)
        self._date = 0
        self._cycle = 0
        self._init_bot_amount = init_bot_amount
        self._init_mineral_amount = init_mineral_amount
        self._set_bots_randomly(init_bot_amount)
        self._set_minerals_randomly(init_mineral_amount)
        self.queue = queue

        self._run = event

    def _set_bots_randomly(self, bot_amount):
        for _ in range(bot_amount):
            self._map.add_member_in_rand(Bot(self._map))

    def _set_minerals_randomly(self, mineral_amount):
        for _ in range(mineral_amount):
            self._map.add_member_in_rand(Mineral(self._map), y=randrange(self._map.y-15,self._map.y))

    def run(self):
        while not self._run.is_set():
            if self._map.get_members_amount(Bot) == 0:
                self._set_bots_randomly(self._init_bot_amount)

            sun_rate = sun_rates[self._date//DAYS_IN_MONTH]
            self._map.sun_rate = sun_rate

            start_time = time()
            self._map.cycle()
            last_time = time()
            passed_time = last_time - start_time

            if self._date > 360:
                self._date = 0
            else:
                self._date += 1

            self._cycle += 1

            self.queue.put([[member.print_style(0), x, y] for member, x, y in self._map.iterate_members()])
