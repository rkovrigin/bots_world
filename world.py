import copy
from random import randrange
from threading import Thread
from time import sleep

from map import Map
from bot import Bot, Bot_short_info
from map import Map
from bot import Bot
from collections import namedtuple

#  TODO: create map as a tor, bots from the right side appear on the left side and vice versa
SUN_RATE = 10
DAYS_IN_MONTH = 30
MONTHS = 12

sun_rates = [4, 4, 5, 6, 7, 8, 9, 7, 6, 4, 5, 3, 2]

Data = namedtuple("Data", ["cycle", "day", "population", "sun_rate"])


class World(Thread):
    def __init__(self, queue, x, y, init_bot_amount=100):
        Thread.__init__(self)
        self._map = Map(x, y, wrapper=True)
        self._date = 0
        self._cycle = 0
        self._init_bot_amount = init_bot_amount
        self._set_bots_randomly(init_bot_amount)
        self.queue = queue

        self._run = True

    def _set_bots_randomly(self, bot_amount):
        for i in range(bot_amount):
            self._map.add_member_in_rand(Bot(self._map))

    def run(self):
        while self._run:
            if self._map.get_bots_amount() == 0:
                self._set_bots_randomly(self._init_bot_amount)

            sun_rate = sun_rates[self._date//DAYS_IN_MONTH]
            self._map.sun_rate = sun_rate
            self._map.cycle()

            if self._date > 360:
                self._date = 0
            else:
                self._date += 1

            self._cycle += 1

            bots_list = []
            for bot, x, y in self._map.iterate_members():
                bot_info = Bot_short_info(x, y, bot._predator, bot.energy, bot.age)
                bots_list.append(bot_info)

            self.queue.put(bots_list)

