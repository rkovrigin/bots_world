from collections import defaultdict
from itertools import chain
from random import randint, randrange

import config
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
        self._sun_map = SunMap(x, y, 30, 4)
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
                    pass
                    #mineral.energy += min(member.energy + mineral.energy, mineral._max_energy)
                else:
                    pass
                    # self._map_minerals.add_in_pos(Mineral(self, 10), x, y)
                    #self._map_minerals.add_in_pos(Mineral(self, member.energy), x, y)

                self._map_bots.remove(x, y)
            else:
                self._map_bots.remove(x, y)
        elif isinstance(member, Mineral):
            self._map_minerals.remove(x, y)

    def is_mineral_at(self, x, y):
        return self._map_minerals.at(x, y)

    def is_bot_at(self, x, y):
        return self._map_bots.at(x, y)

    def get_minerals_amount(self):
        return len(self._map_minerals)

    def get_bots_amount(self):
        return len(self._map_bots)

    def cycle(self):
        for member, x, y in chain(self._map_bots.iterate_members(), self._map_minerals.iterate_members()):
            member.execute_command(x, y)
            if not member.is_alive:
                self.remove_member(member, x, y)

    def create_representation_snapshot(self):
        config.BOTS = len(self._map_bots)
        return [member.represent_itself(x, y)
                for (x, y), member in chain(self._map_minerals._map_items.items(), self._map_bots._map_items.items())]
