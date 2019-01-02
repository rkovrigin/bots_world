from random import randrange, randint, choice
from mineral import Mineral
from representation import *

SHARE_ENERGY          = 1
EAT_MINERAL           = 2
GET_ENERGY_FROM_SUN   = 4
EAT_ANOTHER_BOT       = 8
RUNAWAY_FROM_PREDATOR = 12
CREATE_COPY           = 22
LOOK_AROUND           = 33
MOVE                  = 44
JUMP                  = 45
CHOCKING              = 55
FALLOW_VICTIM         = 56

__evolution_probability__ = 4
__life_length__ = 100

legal_commands = [SHARE_ENERGY, EAT_MINERAL, GET_ENERGY_FROM_SUN, EAT_ANOTHER_BOT, CREATE_COPY, MOVE, JUMP]

"""
TODO: MAKE COMAND OF GETTING ENERGY; and with this command it can get energy only from one source!
"""

MASK = 0b111111

MAX_ENERGY = 255
BIRTH_COST = 50

get_cells_around_list = ((-1, -1), (1, 1), (1, -1), (-1, 1), (-1, 0), (1, 0), (0, -1), (0, 1))
get_cells_around_list_plus_self = ((0, 0), (-1, -1), (1, 1), (1, -1), (-1, 1), (-1, 0), (1, 0), (0, -1), (0, 1))
get_cells_to_jump_list = ((-2, 2), (-1, 2), (0, 2), (1, 2),
                          (2, 2), (2, 1), (2, 0), (2, -1),
                          (2, -2), (1, -2), (0, -2), (-1, -2),
                          (-2, -2), (-2, -1), (-2, 0), (-2, 1))

sun_rates_diff = list((i/100 for i in range(-10, 11)))

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
# TODO: Implement running out of predators
# TODO: Implement following the victim
# TODO: Create weight of action, eat/move/stay


class Bot(object):
    __slots__ = ["_mutant", "_energy", "_size", "_commands", "_age", "_is_alive", "_move_cost", "_day_cost",
                 "_current_command", "_max_age", "_kind", "_sun_rate", "_map", "_bite_mineral",
                 "_bitmap", "_jump_cost", "_copy_cost", "_die_from_age", "_color", "_attempts",
                 "_r", "_g", "_b"]

    def __init__(self, map, energy=100, mutant=False, copy_commands=None):
        self._mutant = mutant
        self._energy = energy
        self._size = 64
        self._commands = [0] * self.size
        self._age = 0
        self._is_alive = True
        self._current_command = 0
        self._kind = 0
        self._map = map
        self._bitmap = 0
        self._copy_cost = 150
        self._die_from_age = False
        self._color = Representation(0, 0, 0)
        self._attempts = 5

        if copy_commands is None:
            self._move_cost = randrange(1, 5)
            self._jump_cost = randrange(6, 12)
            self._max_age = randrange(70, 300)
            self._day_cost = randrange(1, 2)
            self._bite_mineral = randrange(20, 40)
            self._sun_rate = randrange(1, 40)
            for i in range(self._size):
                self._commands[i] = choice((GET_ENERGY_FROM_SUN, CREATE_COPY, EAT_ANOTHER_BOT, EAT_MINERAL, MOVE, JUMP, randrange(0, self._size)))
                self._commands[i] = randrange(0, self._size)
        else:
            self._commands = copy_commands[:]

        if mutant:
            self._mutate()

        self._set_kind()

    def _mutate(self):
        rand_nmb = randint(0, self.size - 1)
        cmd = self._commands[rand_nmb]
        new_cmd_nmb = self._invert_bit(cmd)
        self._commands[rand_nmb] = new_cmd_nmb

    def _set_kind(self):
        for command in self._commands:
            if command == EAT_ANOTHER_BOT:
                self._kind = BOT_PREDATOR_KIND
                self._bitmap |= BOT_PREDATOR_KIND
            elif command == EAT_MINERAL:
                self._kind = BOT_MINERAL_KIND
                self._bitmap |= BOT_MINERAL_KIND
            elif command == GET_ENERGY_FROM_SUN:
                self._kind = BOT_VEGAN_KIND
                self._bitmap |= BOT_VEGAN_KIND

    def _change_energy(self, energy):
        self._energy = min(self.energy + energy, MAX_ENERGY)
        if self.energy < 0:
            self.die("Energy level: %d" % self.energy)

    @property
    def size(self):
        return self._size

    @property
    def kind(self):
        return self._kind

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
    def _invert_bit(nmb):
        bit_to_change = randint(0, 5)
        nmb ^= 1 << bit_to_change
        return nmb

    @property
    def bitmap(self):
        return self._bitmap

    def _next_command_pointer(self, step=1):
        next_cmd = self._current_command + step
        if next_cmd >= self._size:
            return next_cmd - self._size
        return next_cmd

    def create_copy(self, x, y, mutate=False):
        if self._energy < MAX_ENERGY-55:
            return

        for i in range(self._attempts):
            _x, _y = self._find_direction_cell(x=x, y=y, pointer_step=i+1)
            if self._map.is_bot_at(_x, _y) is None:
                break
        else:
            self.die("Can't create copy")
            return False

        self._change_energy(-self._copy_cost)
        child = Bot(self._map, energy=50, mutant=mutate, copy_commands=self._commands)
        self._map.add_member_in_pos(child, _x, _y)

        if mutate:
            modifier = randrange(-1, 2)
            child._move_cost = max(1, self._move_cost + modifier)
            child._max_age = max(1, self._max_age + modifier)
            child._sun_rate = max(1, self._sun_rate + modifier)
            child._bite_mineral = max(1, self._bite_mineral + modifier)
            child._jump_cost = max(1, self._jump_cost + modifier)
            child._day_cost = max(1, self._day_cost + modifier)
            child._copy_cost = max(50, self._copy_cost + modifier)
        else:
            child._move_cost = self._move_cost
            child._max_age = self._max_age
            child._sun_rate = self._sun_rate
            child._bite_mineral = self._bite_mineral
            child._jump_cost = self._jump_cost
            child._day_cost = self._day_cost
            child._copy_cost = self._copy_cost

        return True

    def _find_direction_cell(self, x, y, pointer_step=1, cells=get_cells_around_list):
        next_cp = self._next_command_pointer(pointer_step)
        spin = self._commands[next_cp] % 8
        new_coord_x, new_coord_y = cells[spin]
        return x + new_coord_x, y + new_coord_y

    def _find_direction_cell_jump(self, x, y, pointer_step=1):
        next_cp = self._next_command_pointer(pointer_step)
        spin = self._commands[next_cp] % 4
        next_cp2 = self._next_command_pointer(pointer_step+1)
        spin2 = self._commands[next_cp2] % 4
        new_coord_x, new_coord_y = get_cells_to_jump_list[spin*4 + spin2]
        return x + new_coord_x, y + new_coord_y

    def _find_direction(self, pointer_step=1):
        next_cp = self._next_command_pointer(pointer_step)
        direction = self._commands[next_cp] % len(get_cells_around_list)
        return direction

    def move_with_spin(self, x, y):
        coord_x, coord_y = self._find_direction_cell(x, y)

        if self.energy >= self._move_cost and self._map.is_bot_at(coord_x, coord_y) is None:
            self._map.move_bot(x, y, coord_x, coord_y)
            self._change_energy(-self._move_cost)
            return True

        return False

    def die_of_choking(self, x, y):
        pass
        n = 0
        for _x, _y in get_cells_around_list:
            if self._map.is_bot_at(x + _x, y + _y) and self._map.is_bot_at(x + _x, y + _y) is not self._map._outside_map:
                n += 1
        if n == 7:
            self.die("choking")

    def receive_energy(self, sun_rate):
        self._change_energy(sun_rate)
        if sun_rate > 0:
            self._color.increaseGreen(sun_rate)

    def eat_mineral(self, x, y):
        for i in range(self._attempts):
            _x, _y = self._find_direction_cell(x=x, y=y, pointer_step=i+1, cells=get_cells_around_list_plus_self)
            potential_mineral = self._map.is_mineral_at(_x, _y)
            if isinstance(potential_mineral, Mineral):
                break
        else:
            return False

        bite = potential_mineral.bite_piece(self._bite_mineral)
        if bite > 0:
            self._change_energy(bite)
            self._color.increaseBlue(bite)
        else:
            print("No mineral to bite %d" % int(bite))

        return True

    def look_around(self):
        pass

    def eat_another_bot(self, x, y):
        for i in range(self._attempts):
            _x, _y = self._find_direction_cell(x=x, y=y, pointer_step=i+1)
            possible_victim = self._map.is_bot_at(_x, _y)
            if isinstance(possible_victim, Bot) and not self.is_same_kind(possible_victim):
                break
        else:
            return False

        self._change_energy(possible_victim._energy)
        self._color.increaseRed()
        # possible_victim._change_energy(-possible_victim._energy)

        possible_victim.die("EATEN BY PREDATOR REASON")
        return True

    def die(self, reason):
        self._is_alive = False
        self._energy = 0
        # print(reason)

    def execute_command(self, x, y):
        if not self.is_alive:
            return

        if self.energy <= 0:
            self.die("ENERGY = 0 REASON")
            return

        if self._die_from_age and self._age >= self._max_age:
            self.die("AGE REASON")
            return

        self._age += 1

        self._current_command = self._next_command_pointer()
        cmd = self._commands[self._current_command]

        if cmd == GET_ENERGY_FROM_SUN:
            self.receive_energy(self._map.sun_rate(x, y))
        elif cmd == CREATE_COPY:
            mutate = False
            if randint(0, 3) == 0:
                mutate = True
            self.create_copy(x, y, mutate=mutate)
        elif cmd == EAT_MINERAL:
            self.eat_mineral(x, y)
        elif cmd == LOOK_AROUND:
            self.look_around()
        elif cmd == MOVE:
            self.move_with_spin(x, y)
        elif cmd == JUMP:
            self.jump_with_spin(x, y)
        elif cmd == EAT_ANOTHER_BOT:
            self.eat_another_bot(x, y)
        elif cmd == SHARE_ENERGY:
            self.share_energy_with_same_kind(x, y)
        elif cmd == CHOCKING:
            self.die_of_choking(x, y)
        else:
            next_command = self._next_command_pointer(1)
            self._current_command = self._commands[next_command]
            self._change_energy(-self._day_cost)

    def share_energy_with_same_kind(self, x, y):
        if self._energy < 200:
            return

        for i in range(self._attempts):
            coord_x, coord_y = self._find_direction_cell(x, y, pointer_step=i+1)
            possible_mate = self._map.is_bot_at(coord_x, coord_y)
            if isinstance(possible_mate, Bot) and self.is_same_kind(possible_mate) and possible_mate._energy < 50:
                break
        else:
            return False

        # new_energy = (self._energy + possible_mate._energy) / 2
        # self._energy = new_energy
        # possible_mate._energy = new_energy
        # return True

        self._change_energy(-50)
        possible_mate._change_energy(+50)
        return True

    def jump_with_spin(self, x, y):
        coord_x, coord_y = self._find_direction_cell_jump(x, y)

        if self._energy <= self._move_cost or self._map.is_bot_at(coord_x, coord_y) is not None:
            return False

        self._map.move_bot(x, y, coord_x, coord_y)
        self._change_energy(-self._jump_cost)
        return True

    def is_same_kind(self, member):
        bit = 0
        for i in range(self._size):
            bit += bin(self._commands[i] ^ member._commands[i]).count('1')
            if bit > 1:
                return False
        return True

    def represent_itself(self):
        return Cell(self._color.r, self._color.g, self._color.b, self._energy, 'bot')

    def repr(self):
        return self._color