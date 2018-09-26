from collections import defaultdict
from random import randint, randrange

from bot import Bot


def my_mod(a, n):
    while a >= n:
        a -= n
    while a < 0:
        a += n
    return a


class OutsideOfMap(object):
    pass

outside_map = OutsideOfMap()

class Map(object):
    __slots__ = ["_x", "_y", "_map", "_plt", "_sun_rate", "_wrapper_x", "_wrapper_y", "_outside_map"]
    outside_map = OutsideOfMap()

    def __init__(self, x, y, wrapper_x=True, wrapper_y=True):
        self._x = x
        self._y = y
        self._wrapper_x = wrapper_x
        self._wrapper_y = wrapper_y
        self._map = {}
        self._outside_map = outside_map

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
        if self._wrapper_x:
            x = my_mod(x, self.x)

        if self._wrapper_y:
            y = my_mod(y, self.y)

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
        if self._wrapper_x:
            x = my_mod(x, self.x)
            new_x = my_mod(new_x, self.x)

        if self._wrapper_y:
            y = my_mod(y, self.y)
            new_y = my_mod(new_y, self.y)

        self._map[(new_x, new_y)] = self._map[(x, y)]
        del self._map[(x, y)]

    def remove_bot(self, x, y):
        if self._wrapper_x:
            x = my_mod(x, self.x)
        if self._wrapper_y:
            y = my_mod(y, self.y)

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
        if self._wrapper_x:
            x = my_mod(x, self.x)
        if self._wrapper_y:
            y = my_mod(y, self.y)

        if x < 0 or x >= self.x:
            return outside_map

        if y < 0 or y >= self.y:
            return self._outside_map

        if (x, y) in self._map:
            return self._map[(x, y)]
        else:
            return None

    def get_members_amount(self, member_kind=None):
        if member_kind is None:
            return len(self._map)
        else:
            return sum(1 for _ in self.iterate_members(member_kind=member_kind))

    def cycle(self):
        for member, x, y in self.iterate_members():
            member.execute_command(x, y)
            if not member.is_alive:
                self.remove_bot(x, y)
                # del self._map[(x, y)]

        #for member, x, y in self.iterate_members(Mineral):
        #    member.grow()
        #    if not member._is_active:
        #        del self._map[x, y]

    #TODO: Save snapshots of actions
    def iterate_members(self, member_kind=None):
        for x, y in list(self._map.keys()):
            member = self._map[(x, y)]
            if member_kind is None or isinstance(member, member_kind):
                yield member, x, y

    def create_representation_snapshot(self):
        return [[member.print_style(), x, y, member.energy, member._commands] for (x, y), member in self._map.items()]


class Map2(object):
    __slots__ = ["_x", "_y", "_map", "_plt", "_sun_rate", "_wrapper_x", "_wrapper_y", "_outside_map"]
    outside_map = OutsideOfMap()

    def __init__(self, x, y, wrapper_x=True, wrapper_y=True):
        self._x = x
        self._y = y
        self._wrapper_x = wrapper_x
        self._wrapper_y = wrapper_y
        self._map = [None] * self.x * self.y
        self._outside_map = outside_map

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
        if self._wrapper_x:
            x = my_mod(x, self.x)
        if self._wrapper_y:
            y = my_mod(y, self.y)

        self._map[x + y*self.y] = member
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
        if self._wrapper_x:
            x = my_mod(x, self.x)
            new_x = my_mod(new_x, self.x)

        if self._wrapper_y:
            y = my_mod(y, self.y)
            new_y = my_mod(new_y, self.y)

        self._map[new_x + new_y*self.y] = self._map[x + y*self.y]
        self._map[x + y*self.y] = None

    def remove_bot(self, x, y):
        if self._wrapper_x:
            x = my_mod(x, self.x)
        if self._wrapper_y:
            y = my_mod(y, self.y)

        self._map[x+y*self.y] = None

    def print_2d(self):
        print(self._map)

    def print_manual(self):
        for i in range(self.x):
            for j in range(self.y):
                print("%d" % self._map[i][j], )
            print('')

    def at(self, x, y):
        if self._wrapper_x:
            x = my_mod(x, self.x)
        if self._wrapper_y:
            y = my_mod(y, self.y)

        if x < 0 or x >= self.x:
            return outside_map

        if y < 0 or y >= self.y:
            return self._outside_map

        return self._map[x+y*self.y]

    def get_members_amount(self, member_kind=None):
        #if member_kind is None:
        #    return len(self._map)
        #else:
        return sum(1 for _ in self.iterate_members(member_kind=member_kind))

    def cycle(self):
        for member, x, y in self.iterate_members():
            member.execute_command(x, y)
            if not member.is_alive:
                self._map[x+y*self.y] = None

        #for member, x, y in self.iterate_members(Mineral):
        #    member.grow()
        #    if not member._is_active:
        #        del self._map[x, y]

    #TODO: Save snapshots of actions
    def iterate_members(self, member_kind=None):
        if member_kind is None:
            for idx_x in range(self.x):
                for idx_y in range(self.y):
                    if self._map[idx_x + idx_y * self.y] is not None:
                        yield self._map[idx_x + idx_y * self.y], idx_x, idx_y
        else:
            for idx_x in range(self.x):
                for idx_y in range(self.y):
                    if isinstance(self._map[idx_x + idx_y*self.y], member_kind):
                        yield self._map[idx_x + idx_y*self.y], idx_x, idx_y

    def create_representation_snapshot(self):
        return [[m, x, y, 0, []] for m, x, y in self.iterate_members()]
