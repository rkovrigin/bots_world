from collections import namedtuple
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


class Bot(BotRepresentation):
    __slots__ = ["_mutant", "_energy", "_size", "_commands", "_age", "_is_alive", "_move_cost", "_day_cost",
                 "_current_command", "_max_age", "_kind", "_sun_rate", "_map", "_bite_mineral",
                 "_bitmap", "_jump_cost", "_copy_cost", "_die_from_age", "_color"]

    def __init__(self, map, energy=100, mutant=False, copy_commands=None):
        self._mutant = mutant
        self._energy = energy
        self._size = 64
        self._commands = [0] * self.size
        self._age = 0
        self._is_alive = True
        self._move_cost = randrange(1, 5)
        self._jump_cost = randrange(6, 12)
        self._current_command = 0
        self._max_age = randrange(70, 300)
        self._kind = 0
        self._map = map
        self._bitmap = 0
        self._day_cost = randrange(1, 2)
        self._bite_mineral = randrange(20, 40)
        self._sun_rate = randrange(1, 40)
        self._copy_cost = 150
        self._die_from_age = False
        self._color = Representation(0, 0, 0)

        if copy_commands is None:
            for i in range(self._size):
                self._commands[i] = choice((0, GET_ENERGY_FROM_SUN, CREATE_COPY, EAT_ANOTHER_BOT, EAT_MINERAL))
            # for i in range(self._size):
            #     self._commands[i] = randrange(0, self._size)
            # self._commands[0] = GET_ENERGY_FROM_SUN
            # self._commands[2] = GET_ENERGY_FROM_SUN
            # self._commands[3] = GET_ENERGY_FROM_SUN
            # self._commands[4] = GET_ENERGY_FROM_SUN
            #
            # self._commands[-1] = CREATE_COPY
        else:
            self._commands = copy_commands[:]

        if mutant:
            self._mutate()

        self._set_kind()

    def _mutate(self):
        rand_nmb = randint(0, self.size - 1)
        cmd = self._commands[rand_nmb]
        new_cmd_nmb = self._invert_bit(cmd, randint(0, 5))
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
    def _invert_bit(nmb, bit_to_change):
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
        if self._energy < MAX_ENERGY:
            return

        for coord_x, coord_y in get_cells_around_list:
            # coord_x, coord_y = self._find_direction_cell(x, y, pointer_step=i)
            if self._map.is_bot_at(x + coord_x, y + coord_y) is None:
                break
        else:
            self.die("Can't create copy")
            return False

        self._change_energy(-self._copy_cost)
        child = Bot(self._map, energy=50, mutant=mutate, copy_commands=self._commands)
        self._map.add_member_in_pos(child, coord_x + x, coord_y + y)
        child._move_cost = max(1, self._move_cost + randrange(-1, 2))
        child._max_age = max(1, self._max_age + randrange(-1, 2))
        child._sun_rate = max(1, self._sun_rate + randrange(-1, 2))
        child._bite_mineral = max(1, self._bite_mineral + randrange(-1, 2))
        child._jump_cost = max(1, self._jump_cost + randrange(-1, 2))
        child._day_cost = max(1, self._day_cost + randrange(-1, 2))
        child._copy_cost = max(50, self._copy_cost + randrange(-1, 2))
        child._color = self._color

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
        # energy = min(self._sun_rate, sun_rate)
        energy = sun_rate

        if self._kind == BOT_VEGAN_KIND:
            self._change_energy(energy*2)
        else:
            self._change_energy(energy)

        self._color.increaseGreen()

        # if sun_rate//2 > self._sun_rate:
        #     self.die("Sun burned me")
        # else:
        #     energy = min(self._sun_rate, sun_rate)
        #     self._change_energy(energy)

    def eat_mineral(self, x, y):
        # for i in range(1, 5):
        #     coord_x, coord_y = self._find_direction_cell(x, y, pointer_step=i, cells=get_cells_around_list_plus_self)
        #     potential_mineral = self._map.is_mineral_at(coord_x, coord_y)
        #     if isinstance(potential_mineral, Bot):
        #         break
        # else:
        #     return False

        for _x, _y in get_cells_around_list_plus_self:
            potential_mineral = self._map.is_mineral_at(x + _x, y + _y)
            if isinstance(potential_mineral, Mineral):
                break
        else:
            return False

        if self._kind == BOT_MINERAL_KIND:
            bite_mineral_rating = self._bite_mineral*2
        else:
            bite_mineral_rating = self._bite_mineral

        bite = potential_mineral.bite_piece(bite_mineral_rating)
        self._change_energy(bite)
        # print("Have bitten %d size piece at [%d:%d]" % (bite, coord_x, coord_y))

        self._color.increaseBlue()
        return True

    def look_around(self):
        pass

    def eat_another_bot(self, x, y):
        for i in range(1, 9):
            coord_x, coord_y = self._find_direction_cell(x, y, pointer_step=i)
            possible_victim = self._map.is_bot_at(coord_x, coord_y)

            # if self._bitmap == BOT_PREDATOR_KIND:
            #     if possible_victim is not None and isinstance(possible_victim, Bot) and possible_victim._bitmap != BOT_PREDATOR_KIND:
            #         break
            # elif self._bitmap & BOT_PREDATOR_KIND:
            #     if possible_victim is not None and isinstance(possible_victim, Bot) and (possible_victim._bitmap & BOT_PREDATOR_KIND) == 0:
            #         break
            if isinstance(possible_victim, Bot) and not self.is_same_kind(possible_victim):
                break
        else:
            return False

        # if isinstance(possible_victim, Bot):
        #     if possible_victim._kind == BOT_PREDATOR_KIND:
        #         return False

        # # TODO: Find out correct rule for that
        # if self._energy < possible_victim._energy/4:
        #     return False

            # if self._energy < possible_victim._energy/10 or self._age < possible_victim._age:
            #     return False

        self._change_energy(possible_victim._energy)
        possible_victim.die("EATEN BY PREDATOR REASON")

        self._color.increaseRed()
        return True

    def die(self, reason):
        self._is_alive = False
        # self._energy = 0
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
            # self._current_command = cmd
            self._current_command = self._next_command_pointer(min(1, cmd))
            self._change_energy(-self._day_cost)
            # self._current_command = self._next_command_pointer()

    def share_energy_with_same_kind(self, x, y):
        for i in range(1, 2):
            coord_x, coord_y = self._find_direction_cell(x, y, pointer_step=i)
            possible_mate = self._map.is_bot_at(coord_x, coord_y)
            if isinstance(possible_mate, Bot):
                if self.is_same_kind(possible_mate):
                    break
            # if isinstance(possible_mate, Bot) and possible_mate._bitmap == self._bitmap:
            #     break
        else:
            return False

        # assert self._bitmap == possible_mate._bitmap

        if self._energy//3 >= possible_mate._energy:
            one_third = self._energy//3
            self._change_energy(-one_third)
            possible_mate._change_energy(one_third)

            return True

        return False

    def jump_with_spin(self, x, y):
        coord_x, coord_y = self._find_direction_cell_jump(x, y)

        if self._energy <= self._move_cost or self._map.is_bot_at(coord_x, coord_y) is not None:
            return False

        self._map.move_bot(x, y, coord_x, coord_y)
        self._change_energy(-self._jump_cost)
        return True

    def is_same_kind(self, member):
        for i in range(self._size):
            if self._commands[i] != member._commands[i]:
                return False
        return True
