from collections import defaultdict
from itertools import chain
from random import randint, randrange

from mineral import Mineral
from parent_map import ParentMap, outside_map, my_mod
from sun_map import SunMap

from bot import Bot

class Map(object):
    __slots__ = ["_x", "_y", "_map_bots", "_map_minerals", "_sun_rate", "_wrapper_x", "_wrapper_y", "_outside_map", "_sun_map"]

    def __init__(self, x, y, wrapper_x=True, wrapper_y=True):
        self._x = x
        self._y = y
        self._wrapper_x = wrapper_x
        self._wrapper_y = wrapper_y
        self._map_bots = ParentMap(x, y, wrapper_x, wrapper_y)
        self._map_minerals = ParentMap(x, y, wrapper_x, wrapper_y)
        self._sun_map = SunMap(x, y, 10, 0)
        self._outside_map = outside_map

    def sun_rate(self, x, y):
        return self._sun_map.sun_rate_at(x, y)

    # # TODO: create a map for sun
    # @sun_rate.setter
    # def sun_rate(self, sun_rate):
    #     self._sun_rate = sun_rate
    #     # self._sun_rate = self._sun_map.sun_rate_at(x, y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def is_empty_from_bot(self, x, y):
        return self._map_bots.is_empty(x, y)

    def add_member_in_pos(self, member, x, y):
        if isinstance(member, Bot):
            return self._map_bots.add_in_pos(member, x, y)
        elif isinstance(member, Mineral):
            return self._map_minerals.add_in_pos(member, x, y)
        else:
            raise Exception("No such kind")

    def add_member_in_rand(self, member, x=None, y=None):
        if isinstance(member, Bot):
            return self._map_bots.add_in_rand(member, x, y)
        elif isinstance(member, Mineral):
            return self._map_minerals.add_in_rand(member, x, y)
        else:
            raise Exception("No such kind")

    def move_bot(self, x, y, new_x, new_y):
        self._map_bots.move(x, y, new_x, new_y)

    def move_mineral(self, x, y, new_x, new_y):
        current_position = self._map_minerals.at(x, y)
        new_position = self._map_minerals.at(new_x, new_y)

        if new_position is None:
            return self._map_minerals.move(x, y, new_x, new_y)
        elif isinstance(new_position, Mineral):

            sum_energy = current_position.energy + new_position.energy
            new_position.energy = min(sum_energy, current_position._max_energy)
            current_position.energy = max(0, sum_energy - new_position.energy)
            if current_position.energy == 0:
                current_position.die()

    def remove_member(self, member, x, y):
        mineral = self._map_minerals.at(x, y)

        if isinstance(member, Bot):
            if member.energy > 0:
                if isinstance(mineral, Mineral):
                    mineral.energy += min(member.energy + mineral.energy, mineral._max_energy)
                else:
                    # self._map_minerals.add_in_pos(Mineral(self, 10), x, y)
                    self._map_minerals.add_in_pos(Mineral(self, member.energy), x, y)

                self._map_bots.remove(x, y)
            else:
                self._map_bots.remove(x, y)
        elif isinstance(member, Mineral):
            self._map_minerals.remove(x, y)

    def is_mineral_at(self, x, y):
        return self._map_minerals.at(x, y)

    def is_bot_at(self, x, y):
        return self._map_bots.at(x, y)

    def get_minerals_amount(self, x, y):
        return len(self._map_minerals)

    def get_bots_amount(self):
        return len(self._map_bots)

    def cycle(self):
        for member, x, y in chain(self._map_bots.iterate_members(), self._map_minerals.iterate_members()):
            member.execute_command(x, y)
            if not member.is_alive:
                self.remove_member(member, x, y)

    def create_representation_snapshot(self):
        return [[member.print_style(), x, y, member.energy]
                for (x, y), member in chain(self._map_minerals._map_items.items(), self._map_bots._map_items.items())]


class Map2(object):
    __slots__ = ["_x", "_y", "_map", "_plt", "_sun_rate", "_wrapper_x", "_wrapper_y", "_outside_map"]

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
