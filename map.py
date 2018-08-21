from collections import defaultdict
from random import randint, randrange
from bot import Bot

class OutsideOfMap(object):
    pass

outside_map = OutsideOfMap()

class Map(object):
    __slots__ = ["_x", "_y", "_map", "_plt", "_sun_rate", "_wrapper"]
    outside_map = OutsideOfMap()

    def __init__(self, x, y, wrapper=True):
        self._x = x
        self._y = y
        self._wrapper = wrapper
        #self._map = defaultdict(lambda: None)
        self._map = {}

    @property
    def sun_rate(self):
        return self._sun_rate

    @sun_rate.setter
    def sun_rate(self, sun_rate):
        self._sun_rate = sun_rate

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def is_empty(self, x, y):
        return self.at(x, y) is None

    def add_member_in_pos(self, member, x, y):
        if self._wrapper:
            x %= self.x
            y %= self.y
        self._map[(x, y)] = member
        return True

    def add_member_in_rand(self, member, x=None, y=None):
        if x is None:
            x = randrange(0, self.x)
        if y is None:
            y = randrange(0, self.y)

        if self.is_empty(x, y):
            return self.add_member_in_pos(member, x, y)
        else:
            return False

    def move(self, x, y, new_x, new_y):
        if self._wrapper:
            x %= self.x
            y %= self.y
            new_x %= self.x
            new_y %= self.y
        self._map[(new_x, new_y)] = self._map[(x, y)]
        del self._map[(x, y)]

    def remove_bot(self, x, y):
        if self._wrapper:
            x %= self.x
            y %= self.y
        if (x, y) in self._map:
            del self._map[(x, y)]

    def print_2d(self):
        print(self._map)

    def print_manual(self):
        for i in range(self.x):
            for j in range(self.y):
                print("%d" % self._map[i][j], )
            print('')

    def at(self, x, y):
        if self._wrapper:
            x %= self.x
            y %= self.y

            if (x, y) in self._map:
                return self._map[(x, y)]
            else:
                return None
        elif 0 <= x < self.x or 0 <= y < self.y:
            if (x, y) in self._map:
                return self._map[(x, y)]
            else:
                return None
        else:
            return outside_map

    def get_bots_amount(self):
        return len(self._map)

    def cycle(self):
        for member, x, y in self.iterate_members(Bot):
            member.execute_command(x, y)
            if not member.is_alive:
                del self._map[(x, y)]

    #TODO: Save snapshots of actions
    def iterate_members(self, member_kind=None):
        for x, y in list(self._map.keys()):
            member = self._map[(x, y)]
            if member_kind is None or isinstance(member, member_kind):
                yield member, x, y
        #return None
