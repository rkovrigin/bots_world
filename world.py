from copy import copy, deepcopy
from random import randrange
from threading import Thread, Event
from time import sleep, time

from Wall import Wall
from map import Map
import timing
from bot import Bot
from mineral import Mineral
from parent_map import ParentMap
from collections import namedtuple
import config

SUN_RATE = 10
DAYS_IN_MONTH = 30
MONTHS = 12

sun_rates = [8, 8, 10, 12, 14, 16, 18, 14, 12, 8, 10, 6, 4]

Data = namedtuple("Data", ["cycle", "day", "population", "sun_rate"])

seasons = [1, 2, 3, 4, 5, 4, 3, 2, 1]


class World(Thread):
    def __init__(self, animate_handle, x, y, init_bot_amount=100, init_mineral_amount=100):
        Thread.__init__(self)
        self._map = ParentMap(x, y, wrapper_x=True, wrapper_y=False)
        self._date = 0
        self._cycle = 0
        self._init_bot_amount = init_bot_amount
        self._init_mineral_amount = init_mineral_amount
        self.animate_handle = animate_handle
        self.representation_no = 0

        self._run = Event()

        # for i in range(30):
        #     for j in range(30):
        #         self._map.add_in_pos(Wall(), i+10, j+10)
        #
        # for i in range(28):
        #     for j in range(28):
        #         del self._map._map_items[(i+11, j+11)]

        self._set_bots_randomly(init_bot_amount)
        self._set_minerals_randomly(init_mineral_amount)

    def _set_bots_randomly(self, bot_amount):
        for _ in range(bot_amount):
            self._map.add_in_rand(Bot(self._map), y=randrange(0, self._map._y))

    def _set_minerals_randomly(self, mineral_amount):
        for _ in range(mineral_amount):
            self._map.add_in_rand(Mineral(self._map, energy=30000), y=randrange(self._map.y-15, self._map.y))
            # self._map.add_member_in_rand(Mineral(self._map, energy=30000), y=randrange(0, self._map.y))

    def finish_him(self):
        self._run.set()

    def run(self):
        start_time = time()
        iteration_no = 0
        q = 0

        while not self._run.is_set():
            iteration_no += 1

            if iteration_no % 100 == 0:
                end_time = time()
                print("Iteration %d %f (fields occupied: %d)" % (iteration_no, end_time - start_time, self._map.members_amount()))
                start_time = time()
                self._map.set_sun_rate_division(seasons[q % len(seasons)])
                q += 1

            if self._map.members_amount(Bot) == 0:
                self._set_bots_randomly(self._init_bot_amount)
            if self._map.members_amount(Mineral) < 0:  # self._init_mineral_amount//2:
                self._set_minerals_randomly(self._init_mineral_amount//2)

            # sun_rate = sun_rates[self._date//DAYS_IN_MONTH]
            # self._map.sun_rate = sun_rate

            self._map.cycle()

            if self._date > 360:
                self._date = 0
            else:
                self._date += 1

            self._cycle += 1

            # passed_time = self._cycle / (time() - start_time)
            # print(self._cycle, passed_time)

            self.animate_handle(self._map.create_representation_snapshot(self.representation_no))
            # self.animate_handle(None)

            config.DAY += 1
