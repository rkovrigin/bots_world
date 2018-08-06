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


class Bot(object):
    x = 0
    y = 0
    _size = 0
    commands = []
    energy = 0
    current_command = 0
    _is_alife = None
    age = None

    def __init__(self, x, y, energy=10, mutate=False, copy_commands = None):
        self.x = x
        self.y = y
        self.energy = energy
        self._size = 64
        self.commands = [0] * self.size
        self.age = 0
        self._is_alife = True

        for i in range(self._size):
            if copy_commands is None:
                if randrange(0,2) == 0:
                    self.commands[i] = GET_ENERGY
                else:
                    self.commands[i] = CREATE_COPY
            else:
                self.commands[i] = copy_commands[i]

        self.current_command = 0
        self._is_alife = True

        if mutate:
            command = randrange(0, self.size)
            cmd_nmb = self.commands[command]
            new_cmd_nmb = self._invert_bit(cmd_nmb, randrange(0, 6))
            self.commands[command] = new_cmd_nmb

    @property
    def size(self):
        return self._size

    @staticmethod
    def _invert_bit(nmb, bit_to_change):
        nmb ^= 1 << bit_to_change
        return nmb

    def create_copy(self, map, mutate=False):
        crds = self.find_grids_around(map)
        if self.energy > 10:
            print ">10"
        if self.energy >= 100 and len(crds) > 0:
            self.energy -= 50
            crd = crds[randrange(0, len(crds))]
            child = Bot(crd[0], crd[1], 10, mutate)

            map._map[child.x][child.y] = BOT
            return child
            # TODO: create bot with probability of evolution is 25% and add it to the map
            # if randrange(0, __evolution_probability__) == 0:
        return None

    def _check_cell(self, map, x, y):
        crd = {'x': None, 'y': None}
        try:
            if map.at(x, y) == EMPTY:
                crd['x'] = self.x
                crd['y'] = self.y
                return crd
            else:
                return None
        except:
            return None

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

    def move(self):
        pass

    def receive_energy(self, sun_rate):
        if sun_rate > 20:
            self.die()
        else:
            self.energy += sun_rate

    def eat_meneral(self):
        pass

    def look_around(self):
        pass

    def eat_another_bot(self):
        pass

    def die(self):
        self._is_alife = False
        self.energy = 0

    def execute_command(self, sun_rate, map):

        if self.energy <= 0 or self.age > 100:
            self.die()
            return

        self.age += 1

        self.current_command = (self.current_command + 1) % self.size
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
            self.move()
        elif cmd == EAT_ANOTHER_BOT:
            self.eat_another_bot()
