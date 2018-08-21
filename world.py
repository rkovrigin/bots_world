from random import randrange
from map import Map
from bot import Bot

#  TODO: create map as a tor, bots from the right side appear on the left side and vice versa
SUN_RATE = 10
DAYS_IN_MONTH = 30
MONTHS = 12

sun_rates = [4,4,5,6,7,8,9,7,6,4,5,3,2]

class World(object):
    def __init__(self, x, y, init_bot_amount=100):
        self._map = Map(x, y, wrapper=True)
        self._date = 0
        self._cycle = 0
        self._init_bot_amount = init_bot_amount
        self._set_bots_randomly(init_bot_amount)

    def _set_bots_randomly(self, b):
        for i in range(b):
            self._map.add_member(Bot(self._map))

    def cycle(self):
        if self._map.get_bots_amount() == 0:
            self._set_bots_randomly(self._init_bot_amount)

        # sun_rate = SUN_RATE
        # if self._date in range(0, DAYS_IN_MONTH*3):
        #     sun_rate = SUN_RATE / 4
        # elif self._date in range(DAYS_IN_MONTH*3, DAYS_IN_MONTH*6):
        #     sun_rate = SUN_RATE / 2
        # elif self._date in range(DAYS_IN_MONTH*6, DAYS_IN_MONTH*9):
        #     sun_rate = SUN_RATE
        # elif self._date in range(DAYS_IN_MONTH*9, DAYS_IN_MONTH*12):
        #     sun_rate = SUN_RATE / 2

        sun_rate = sun_rates[self._date//DAYS_IN_MONTH]
        self._map.sun_rate = sun_rate
        self._map.cycle()

        self._date = (self._date + 1) % (DAYS_IN_MONTH * MONTHS)
        self._cycle += 1
        loop = self._map.get_bots_amount()
        # print("Cycle: %d; Day: %d; Population: %s; Sun rate: %f" % (self._cycle, self._date, loop, sun_rate))
        return "Cycle: %d; Day: %d; Population: %s; Sun rate: %f" % (self._cycle, self._date, loop, sun_rate)
        # self.print_bots()

    def print_bots(self):
        pass
        # for bot in self._bots:
        #     print(bot.energy,)
        # print('')
