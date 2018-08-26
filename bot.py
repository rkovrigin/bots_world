from collections import namedtuple
from random import randrange, randint, choice

EAT_MINERAL = 00
SHARE_ENERGY = 1
GET_ENERGY = 11
CREATE_COPY = 22
LOOK_AROUND = 33
MOVE = 44
EAT_ANOTHER_BOT = 55

__evolution_probability__ = 4
__life_length__ = 100

MASK = 0b111111

get_cells_around_list = ((-1, -1), (1, 1), (1, -1), (-1, 1), (-1, 0), (1, 0), (0, -1), (0, 1))

sun_rates_diff = list((i/100 for i in range(-10, 11)))

Bot_short_info = namedtuple("Bot_short_info", ["x", "y", "predator", "energy", "age"])

# TODO: Implement sharing of energy with kind. Same kind - similar except 1 bit or 1 command
# TODO: Remember the best bots depending on these values:
"""
_max_age
max amount of saved energy
max sun_rate
how many children gave a birth
max distance passed
how many bots has eaten
"""
# TODO: After that generate new generation with the best bots


class Bot(object):
    __slots__ = ["_mutant", "_energy", "_size", "_commands", "_age", "_is_alive", "_move_cost", "_current_command",
                 "_max_age", "_predator", "sun_rate", "_map"]

    def __init__(self, map, energy=10, mutant=False, copy_commands=None, predator=False):
        self._mutant = mutant
        self._energy = energy
        self._size = 64
        self._commands = [0] * self.size
        self._age = 0
        self._is_alive = True
        self._move_cost = randrange(1, 5)
        self._current_command = 0
        self._max_age = randrange(40, 70)
        self._predator = predator
        self._map = map
        if self._predator:
            self.sun_rate = 0
        else:
            self.sun_rate = choice((0.9, 1.0))

        if copy_commands is None:  # TODO: add random numbers
            for i in range(self._size):
                r = randrange(0, 3)
                if r == 0:
                    self._commands[i] = GET_ENERGY
                elif r == 1:
                    self._commands[i] = randrange(0, 64)
                else:
                    if randrange(0, 2) == 0:
                        self._commands[i] = CREATE_COPY
                    else:
                        self._commands[i] = MOVE
        else:
            self._commands = copy_commands[:]

        self._current_command = 0

        if mutant:
            self._mutate()

    @property
    def size(self):
        return self._size

    @property
    def predator(self):
        return self._predator

    @property
    def is_alive(self):
        return self._is_alive

    @property
    def age(self):
        return self._age

    @property
    def energy(self):
        return self._energy

    @staticmethod
    def _invert_bit(nmb, bit_to_change):
        nmb ^= 1 << bit_to_change
        return nmb

    def _next_command_pointer(self, step=1):
        next_cmd = self._current_command + step
        if next_cmd >= self._size:
            return next_cmd - self._size
        return next_cmd

    def create_copy(self, x, y, mutate=False):
        # if self._map.get_bots_amount() >= 5000:
        #     return

        for i in range(1, 5):
            coord_x, coord_y = self._find_direction_cell(x, y, pointer_step=i)
            if self._map.at(coord_x, coord_y) is None:
                break
        else:
            return False

        if self._energy >= 70:
            self._energy -= 30
            child = Bot(self._map, energy=10, mutant=mutate, copy_commands=self._commands, predator=self._predator)
            self._map.add_member_in_pos(child, coord_x, coord_y)
            if self._predator:
                child._predator = True
                child.sun_rate = 0.4
            else:
                child.sun_rate += choice(sun_rates_diff)
            child._move_cost = self._move_cost
            child._max_age = self._max_age
            return True
        return False

    def _find_direction_cell(self, x, y, pointer_step=1):
        next_cp = self._next_command_pointer(pointer_step)
        spin = self._commands[next_cp] % 8
        new_coord_x, new_coord_y = get_cells_around_list[spin]
        return x + new_coord_x, y + new_coord_y

    def _find_direction(self, pointer_step=1):
        next_cp = self._next_command_pointer(pointer_step)
        direction = self._commands[next_cp] % len(get_cells_around_list)
        return direction

    def move_with_spin(self, x, y):
        coord_x, coord_y = self._find_direction_cell(x, y)

        if self._energy <= self._move_cost or self._map.at(coord_x, coord_y) is not None:
            return False

        self._map.move(x, y, coord_x, coord_y)
        self._energy -= self._move_cost
        return True

    def receive_energy(self, sun_rate):
        if sun_rate > 20:
            self.die("SUN RATE REASON")
        else:
            self._energy += sun_rate * self.sun_rate

    def eat_mineral(self):
        pass

    def look_around(self):
        pass

    def eat_another_bot(self, x, y):  # TODO: takes 73% of time, save bots in map
        coord_x, coord_y = self._find_direction_cell(x, y)

        possible_victim = self._map.at(coord_x, coord_y)
        if isinstance(possible_victim, Bot):
            if possible_victim._predator:
                return False

            if self._energy <= 40 and self._energy <= possible_victim._energy:
                return False

            self._energy += possible_victim._energy
            possible_victim.die("EATEN BY PREDATOR REASON")
            return True

        return False

    def die(self, reason):
        self._is_alive = False
        self._energy = 0
        # print(reason)

    def execute_command(self, x, y):
        if self._energy <= 0:
            self.die("ENERGY = 0 REASON")
            return

        if self._age >= self._max_age:
            self.die("AGE REASON")
            return

        self._age += 1

        self._current_command = self._next_command_pointer()
        cmd = self._commands[self._current_command]

        if cmd == GET_ENERGY:
            self.receive_energy(self._map.sun_rate)
        elif cmd == CREATE_COPY:
            mutate = False
            if randint(0, 3) == 0:
                mutate = True
            self.create_copy(x, y, mutate=mutate)
        elif cmd == EAT_MINERAL:
            self.eat_mineral()
        elif cmd == LOOK_AROUND:
            self.look_around()
        elif cmd == MOVE:
            self.move_with_spin(x, y)
        elif cmd == EAT_ANOTHER_BOT:
            self.eat_another_bot(x, y)
        elif cmd == SHARE_ENERGY:
            self.share_energy_with_same_kind(x, y)
        else:
            self._current_command = cmd
            self._energy -= 1
            # TODO: spend energy even if did nothing

    def _mutate(self):
        rand_nmb = randint(0, self.size - 1)
        cmd = self._commands[rand_nmb]
        new_cmd_nmb = self._invert_bit(cmd, randint(0, 5))
        self._commands[rand_nmb] = new_cmd_nmb
        for i in self._commands:
            if self._commands[i] == EAT_ANOTHER_BOT:
                self._predator = True

    def share_energy_with_same_kind(self, x, y):
        possible_mate = None
        for i in range(1, 5):
            coord_x, coord_y = self._find_direction_cell(x, y, pointer_step=i)
            possible_mate = self._map.at(coord_x, coord_y)
            if isinstance(possible_mate, Bot) and possible_mate._predator == self._predator:
                break
        else:
            return False

        assert self._predator == possible_mate._predator

        if self._energy/3 >= possible_mate._energy:
            one_third = self._energy/3
            self._energy -= one_third
            possible_mate._energy += one_third
            return True

        return False

# TODO: Implement running out of predators
# TODO: Implement following the victim
# TODO: Share energy with same kind