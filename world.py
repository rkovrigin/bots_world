from random import randrange
from map import Map
from bot import Bot

M = 100
N = 100
X = 200
SUN_RATE = 10
DAYS_IN_MONTH = 30
MONTHS = 12

_DATE_ = 0
_CYCLE_ = 0

class World(object):
    _bots = None
    _map = None
    _M = None
    _N = None
    _B = None

    def __init__(self, n=N, m=M, b=100):
        self._N = n
        self._M = m
        self._B = b
        self._map = Map(n, m)
        self._bots = []

        for i in range(self._B):
            x = randrange(0, self._map._N)
            y = randrange(0, self._map._M)
            if self._map.is_empty(x, y):
                self._map.addBot(x, y)
                bot = Bot(x, y)
                self._bots.append(bot)

    def show(self):
        self._map.showBots(self._bots)

    def diag_shake(self):
        for bot in self._bots:
            bot.x = (bot.x+1) % self._N
            bot.y = (bot.y + 1) % self._M

    def cycle(self):
        global _DATE_
        global _CYCLE_
        bots_to_remove = []
        for bot in self._bots:
            ret = None
            if bot._is_alife:
                sun_rate = 0
                if _DATE_ in range(0, DAYS_IN_MONTH*3):
                    sun_rate = SUN_RATE / 4
                elif _DATE_ in range(DAYS_IN_MONTH*3, DAYS_IN_MONTH*6):
                    sun_rate = SUN_RATE / 2
                elif _DATE_ in range(DAYS_IN_MONTH*6, DAYS_IN_MONTH*9):
                    sun_rate = SUN_RATE
                elif _DATE_ in range(DAYS_IN_MONTH*9, DAYS_IN_MONTH*12):
                    sun_rate = SUN_RATE / 2

                ret = bot.execute_command(sun_rate, self._map, self._bots)

            if isinstance(ret, Bot):
                self._bots.append(ret)

            if bot._is_alife is False:
                bots_to_remove.append(bot)

        for rbot in bots_to_remove:
            self._bots.remove(rbot)
            self._map.removeBot(rbot.x, rbot.y)
        bots_to_remove.clear()

        _DATE_ = (_DATE_ + 1) % (DAYS_IN_MONTH * MONTHS)
        _CYCLE_ += 1
        print("Cycle: %d; Day: %d; Population: %d" % (_CYCLE_, _DATE_, len(self._bots)))
        self.print_bots()

    def print_bots(self):
        pass
        # for bot in self._bots:
        #     print(bot.energy,)
        # print('')
