from random import randrange
from map import EMPTY, BOT

EAT_MINERAL = 10
GET_ENERGY = 23
CREATE_COPY = 55
LOOK_AROUND = 29
MOVE = 31
EAT_ANOTHER_BOT = 63

__evolution_probability__ = 4
__life_length__ = 100

MASK = 0b111111

def get_cells_around(x, y): # TODO: Don't need to get every cell, need only to check one depending on spin
    crds = []
    crds.append((x - 1, y - 1))
    crds.append((x + 1, y + 1))
    crds.append((x + 1, y - 1))
    crds.append((x - 1, y + 1))
    crds.append((x - 1, y))
    crds.append((x + 1, y))
    crds.append((x, y - 1))
    crds.append((x, y + 1))
    return crds

#TODO: Implement sharing of energy with kind. Same kind - similar except 1 bit or 1 command
class Bot(object):
    def __init__(self, x, y, energy=10, mutate=False, copy_commands=None, predator=False):
        self.x = x
        self.y = y
        self.energy = energy
        self._size = 64
        self.commands = [0] * self.size
        self.age = 0
        self._is_alife = True
        self.move_cost = randrange(1, 5)
        self.current_command = 0
        self._max_age = randrange(40, 70)
        self._predator = predator
        if self._predator:
            self.sun_rate = 0
        else:
            self.sun_rate = randrange(5, 11) / 10.0

        if copy_commands is None:  #TODO: add random numbers
            for i in range(self._size):
                r = randrange(0,3)
                if r == 0:
                    self.commands[i] = GET_ENERGY
                elif r == 1:
                    self.commands[i] = randrange(0, 64)
                else:
                    if randrange(0, 2) == 0:
                        self.commands[i] = CREATE_COPY
                    else:
                        self.commands[i] = MOVE
        else:
            self.commands = copy_commands[:]

        self.current_command = 0
        self._is_alife = True

        if mutate:
            self._mutate()

    def _next_command_pointer(self):
        return (self.current_command + 1) % self.size

    @property
    def size(self):
        return self._size

    @staticmethod
    def _invert_bit(nmb, bit_to_change):
        nmb ^= 1 << bit_to_change
        return nmb

    def create_copy(self, map, mutate=False):
        crds = self.find_grids_around(map)
        if self.energy >= 70 and len(crds) > 0:
            self.energy -= 30
            crd = crds[randrange(0, len(crds))]
            child = Bot(crd[0], crd[1], energy=10, mutate=mutate, copy_commands=self.commands, predator=self._predator)

            map._map[child.x][child.y] = BOT
            return child
            # TODO: create bot with probability of evolution is 25% and add it to the map
            # if randrange(0, __evolution_probability__) == 0:
        return None

    def _check_cell(self, map, x, y, look_for=EMPTY):
        crd = {'x': None, 'y': None}
        if x < 0 or y < 0:
            return None
        if x >= map._N or y >= map._M:
            return None

        if map.at(x, y) == look_for:
            crd['x'] = x
            crd['y'] = y
            return crd

    def find_grids_around(self, map):
        crds = []

        if self._check_cell(map, self.x - 1, self.y - 1):
            crds.append([self.x - 1, self.y - 1])
        if self._check_cell(map, self.x + 1, self.y + 1):
            crds.append([self.x + 1, self.y + 1])
        if self._check_cell(map, self.x + 1, self.y - 1):
            crds.append([self.x + 1, self.y - 1])
        if self._check_cell(map, self.x - 1, self.y + 1):
            crds.append([self.x - 1, self.y + 1])
        if self._check_cell(map, self.x - 1, self.y):
            crds.append([self.x - 1, self.y])
        if self._check_cell(map, self.x + 1, self.y):
            crds.append([self.x + 1, self.y])
        if self._check_cell(map, self.x, self.y - 1):
            crds.append([self.x, self.y - 1])
        if self._check_cell(map, self.x, self.y + 1):
            crds.append([self.x, self.y + 1])

        if len(crds) > 0:
            return crds
        return []

    def move_random_direction(self, map):
        paths = self.find_grids_around(map)

        if self.energy <= self.move_cost or len(paths) <= 0:
            return

        loc = paths[randrange(len(paths))]
        _x = loc['x']
        _y = loc['y']

        map._map[self.x][self.y] = EMPTY
        map._map[_x][_y] = BOT
        self.x = _x
        self.y = _y

        self.energy -= self.move_cost

    def _find_direction_cell(self, map, look_for=EMPTY):
        next_cp = self._next_command_pointer()
        spin = self.commands[next_cp] % 8
        coords = get_cells_around(self.x, self.y)
        new_coord = coords[spin]
        loc = self._check_cell(map, new_coord[0], new_coord[1], look_for)
        return loc

    def move_with_spin(self, map):
        loc = self._find_direction_cell(map)

        if self.energy <= self.move_cost or loc is None:
            return

        # loc = paths[randrange(len(paths))]
        _x = loc['x']
        _y = loc['y']

        map._map[self.x][self.y] = EMPTY
        map._map[_x][_y] = BOT
        self.x = _x
        self.y = _y

        self.energy -= self.move_cost

    def receive_energy(self, sun_rate):
        if sun_rate > 20:
            self.die("SUN RATE REASON")
            return self
        else:
            self.energy += sun_rate * self.sun_rate

    def eat_meneral(self):
        pass

    def look_around(self):
        pass

    def eat_another_bot(self, map, bots): #TODO: takes 73% of time, save bots in map
        cell = self._find_direction_cell(map, BOT)
        victim = None

        if cell is None:
            return

        for v in bots:
            if cell['x'] == v.x and cell['y'] == v.y:
                victim = v
                break

        if victim._predator == True:
            return

        if self.energy <= 40 and self.energy <= victim.energy:
            return

        self.energy += victim.energy
        victim.die("EATEN BY PREDATOR REASON")

        return victim

    def die(self, reason):
        self._is_alife = False
        self.energy = 0
        # print(reason)

    def execute_command(self, sun_rate, map, bots):

        if self.energy <= 0:
            self.die("ENERGY = 0 RESON")
            return self

        if self.age >= self._max_age:
            self.die("AGE REASON")
            return self

        # self._max_age -= 1
        self.age += 1

        self.current_command = self._next_command_pointer()
        cmd = self.commands[self.current_command]

        if cmd == GET_ENERGY:
            self.receive_energy(sun_rate)
        elif cmd == CREATE_COPY:
            mutate = False
            if randrange(0,4) == 0:
                mutate = True
            child = self.create_copy(map, mutate=mutate)
            return child
        elif cmd == EAT_MINERAL:
            self.eat_meneral()
        elif cmd == LOOK_AROUND:
            self.look_around()
        elif cmd == MOVE:
            self.move_with_spin(map)
        elif cmd == EAT_ANOTHER_BOT:
            victim = self.eat_another_bot(map, bots)
            return victim
        else:
            self.current_command = cmd

    def _mutate(self):
        rand_nmb = randrange(0, self.size)
        cmd = self.commands[rand_nmb]
        new_cmd_nmb = self._invert_bit(cmd, randrange(0, 6))
        self.commands[rand_nmb] = new_cmd_nmb
        for i in self.commands:
            if self.commands[i] == EAT_ANOTHER_BOT:
                self._predator = True

