from random import randrange

from sun_map import SunMap


class OutsideOfMap(object):
    pass

outside_map = OutsideOfMap()


def my_mod(a, n):
    while a >= n:
        a -= n
    while a < 0:
        a += n
    return a


class ParentMap(object):
    __slots__ = ["_x", "_y", "_map_items", "_sun_map", "_sun_rate_division", "_wrapper_x", "_wrapper_y", "_outside_map"]

    def __init__(self, x, y, wrapper_x=True, wrapper_y=True):
        self._x = x
        self._y = y
        self._map_items = {}
        self._wrapper_x = wrapper_x
        self._wrapper_y = wrapper_y
        self._outside_map = outside_map
        self._sun_map = SunMap(x, y, 20, 0)
        self._sun_rate_division = 1

    def sun_rate(self, x, y):
        return self._sun_map.sun_rate_at(x, y) // self._sun_rate_division

    def set_sun_rate_division(self, division):
        self._sun_rate_division = division

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def is_empty(self, x, y):
        return self.at(x, y) is None

    def add_in_pos(self, member, x, y):
        if self._wrapper_x:
            x = my_mod(x, self.x)

        if self._wrapper_y:
            y = my_mod(y, self.y)

        if (x, y) in self._map_items:
            if isinstance(self._map_items[(x, y)], set):
                self._map_items[(x, y)].add(member)
            else:
                self._map_items[(x, y)] = {self._map_items[(x, y)], member}
        else:
            self._map_items[(x, y)] = member
        return True

    def add_in_rand(self, member, x=None, y=None):
        if x is None:
            x = randrange(0, self.x)
        if y is None:
            y = randrange(0, self.y)

        if self.is_empty(x, y):
            return self.add_in_pos(member, x, y)
        else:
            return False

    def move(self, x, y, new_x, new_y):
        if self._wrapper_x:
            x = my_mod(x, self.x)
            new_x = my_mod(new_x, self.x)

        if self._wrapper_y:
            y = my_mod(y, self.y)
            new_y = my_mod(new_y, self.y)

        if self.at(new_x, new_y) is outside_map:
            return

        self._map_items[(new_x, new_y)] = self._map_items[(x, y)]
        del self._map_items[(x, y)]

    def remove(self, x, y):
        if self._wrapper_x:
            x = my_mod(x, self.x)
        if self._wrapper_y:
            y = my_mod(y, self.y)

        if (x, y) in self._map_items:
            del self._map_items[(x, y)]

    def at(self, x, y):
        if self._wrapper_x:
            x = my_mod(x, self.x)
        if self._wrapper_y:
            y = my_mod(y, self.y)

        if x < 0 or x >= self.x:
            return outside_map

        if y < 0 or y >= self.y:
            return self._outside_map

        if (x, y) in self._map_items:
            return self._map_items[(x, y)]
        else:
            return None

    def remove_candidate(self, x, y, candidate):
        if self._wrapper_x:
            x = my_mod(x, self.x)
        if self._wrapper_y:
            y = my_mod(y, self.y)

        if (x, y) in self._map_items:
            if isinstance(self._map_items[(x, y)], set):
                self._map_items[(x, y)].remove(candidate)
            elif self._map_items[(x, y)] is candidate:
                del self._map_items[(x, y)]

    def member_at(self, x, y, member):
        if self._wrapper_x:
            x = my_mod(x, self.x)
        if self._wrapper_y:
            y = my_mod(y, self.y)

        if x < 0 or x >= self.x:
            return outside_map

        if y < 0 or y >= self.y:
            return self._outside_map

        if (x, y) in self._map_items:
            if isinstance(self._map_items[(x, y)], member):
                return self._map_items[(x, y)]
            elif isinstance(self._map_items[(x, y)], Container):
                return self._map_items[(x, y)].return_member(member)
        else:
            return None

    def cycle(self):
        for member, x, y in self.iterate_members():
            member.execute_command(x, y)
            if not member.is_alive:
                self.remove(x, y)

    #TODO: Save snapshots of actions
    def iterate_members(self, member_kind=None):
        for x, y in list(self._map_items.keys()):
            member = self._map_items[(x, y)]
            if member_kind is None or isinstance(member, member_kind):
                yield member, x, y

    def members_amount(self, member_kind=None):
        if member_kind is None:
            return len(self._map_items)
        amount = 0
        for x, y in list(self._map_items.keys()):
            member = self._map_items[(x, y)]
            if isinstance(member, member_kind):
                amount += 1
        return amount

    def create_representation_snapshot(self):
        return [[member.represent_itself(), x, y] for (x, y), member in self._map_items.items()]
