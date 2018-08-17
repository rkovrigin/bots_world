from random import randint, randrange
from bot import Bot

class OutsideOfMap(object):
    pass

class Map(object):
    __slots__ = ["_x", "_y", "_map", "_plt"]
    _wrapper = True

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._map = []
        for _ in range(self._x):
            self._map.append([None] * self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def is_empty(self, x, y):
        return self.at(x, y) is None

    def add_member(self, member, x=None, y=None):
        if x is None:
            x = randrange(0, self.x)
        if y is None:
            y = randrange(0, self.y)

        if self.is_empty(x, y):
            if self._wrapper:
                x %= self.x
                y %= self.y
            self._map[x][y] = member
            return True
        else:
            return False

    def move(self, x, y, new_x, new_y):
        if self._wrapper:
            x %= self.x
            y %= self.y
            new_x %= self.x
            new_y %= self.y
        self._map[new_x][new_y] = self._map[x][y]
        self._map[x][y] = None

    def remove_bot(self, x, y):
        if self._wrapper:
            x %= self.x
            y %= self.y
        self._map[x][y] = None

    def print_2d(self):
        print(self._map)

    def print_manual(self):
        for i in range(self.x):
            for j in range(self.y):
                print("%d" % self._map[i][j], )
            print('')

    def at(self, x, y):
        if self._wrapper:
            return self._map[x % self.x][y % self.y]
        elif 0 <= x < self.x or 0 <= y < self.y:
            return self._map[x][y]
        else:
            return OutsideOfMap()

    def get_bots_amount(self):
        #return Bot.amount_of_bots
        amount = 0
        for i in self.iterate_members(Bot):
            amount += 1
        return amount, Bot.amount_of_bots

    def cycle(self, sun_rate, cycle):
        for member, x, y in self.iterate_members(Bot):
            member.execute_command(sun_rate, x, y, cycle)
            if not member.is_alive:
                self._map[x][y] = None

    def iterate_members(self, member_kind=None):
        for x in range(self.x):
            for y in range(self.y):
                member = self._map[x][y]
                if member is not None:
                    if member_kind is None or isinstance(member, member_kind):
                        yield member, x, y
        return None
