from random import randrange

EAT_MINERAL = 10
GET_ENERGY = 23
CREATE_COPY = 55
LOOK_AROUND = 29
MOVE = 31
EAT_ANOTHER_BOT = 63

__evolution_probability__ = 4

MASK = 0b111111

class Bot(object):
	x = 0
	y = 0
	_size = 0
	commands = []
	energy = 0
	currenc_command = 0

	def __init__(self, x, y, energy=10, evolve=False):
		self.x = x
		self.y = y
		self.energy = energy
		self._size = 64
		self.commands = [0]*self.size
		self.currenc_command = -1

		if evolve:
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

	def create_copy(self, mutate = False):
		if self.energy >= 100 and self.is_there_palce_around():
			self.energy -= 50
			#TODO: create bot with probability of evolution is 25% and add it to the map
			# if randrange(0, __evolution_probability__) == 0:

	def is_there_palce_around(self):
		pass

	def move(self):
		pass

	def get_energy(self):
		self.energy += 10

	def eat_meneral():
		pass

	def look_around():
		pass

	def eat_another_bot():
		pass

	def die():
		pass

	def execute_command(self):

		if self.energy == 0:
			self.die()
			return

		self.currenc_command = (self.currenc_command + 1) / self.size

		if self.currenc_command == GET_ENERGY:
			self.get_energy()
		elif self.currenc_command == CREATE_COPY:
			self.create_copy()
		elif self.currenc_command == EAT_MINERAL:
			self.eat_meneral()
		elif self.currenc_command == LOOK_AROUND:
			self.look_around()
		elif self.currenc_command == MOVE:
			self.move()
		elif self.currenc_command == EAT_ANOTHER_BOT:
			self.eat_another_bot()
