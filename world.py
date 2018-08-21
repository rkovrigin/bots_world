from random import randrange
from map import Map
from bot import Bot

#  TODO: create map as a tor, bots from the right side appear on the left side and vice versa
SUN_RATE = 10
DAYS_IN_MONTH = 30
MONTHS = 12

sun_rates = [4, 4, 5, 6, 7, 8, 9, 7, 6, 4, 5, 3, 2]


class World(object):
    def __init__(self, x, y, init_bot_amount=100):
        self._map = Map(x, y, wrapper=True)
        self._date = 0
        self._cycle = 0
        self._init_bot_amount = init_bot_amount
        self._set_bots_randomly(init_bot_amount)

    def _set_bots_randomly(self, b):
        for i in range(b):
            self._map.add_member_in_rand(Bot(self._map))

    def cycle(self):
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
        loop = self._map.get_bots_amount()
        return "Cycle: %d; Day: %d; Population: %s; Sun rate: %f" % (self._cycle, self._date, loop, sun_rate)

    def print_bots(self):
        pass
        # for bot in self._bots:
        #     print(bot.energy,)
        # print('')
