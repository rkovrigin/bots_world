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
        bots_to_remove = []
        for bot in self._bots:
            ret = None
            if bot._is_alife:
                # print bot, bot.energy, bot.current_command
                if _DATE_ in range(0, DAYS_IN_MONTH*3):
                    ret = bot.execute_command(SUN_RATE/4, self._map)
                elif _DATE_ in range(DAYS_IN_MONTH*3, DAYS_IN_MONTH*6):
                    ret = bot.execute_command(SUN_RATE/2, self._map)
                elif _DATE_ in range(DAYS_IN_MONTH*6, DAYS_IN_MONTH*9):
                    ret = bot.execute_command(SUN_RATE, self._map)
                elif _DATE_ in range(DAYS_IN_MONTH*9, DAYS_IN_MONTH*12):
                    ret = bot.execute_command(SUN_RATE/2, self._map)

            if isinstance(ret, Bot):
                self._bots.append(ret)

            if bot._is_alife is False:
                bots_to_remove.append(bot)

        for rbot in bots_to_remove:
            self._bots.remove(rbot)
            self._map.removeBot(rbot.x, rbot.y)
        bots_to_remove.clear()

        _DATE_ = (_DATE_ + 1) % (DAYS_IN_MONTH * MONTHS)
        print("Day: %d; Population: %d" % (_DATE_, len(self._bots)))
        self.print_bots()

    def print_bots(self):
        pass
        # for bot in self._bots:
        #     print(bot.energy,)
        # print('')
