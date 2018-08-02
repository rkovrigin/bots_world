EAT_MINERAL = 10
GET_ENERGY = 23
CREATE_COPY = 55
LOOK_AROUND = 29
MOVE = 31
EAT_MINERAL = 63

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
	
	@property
	def size(self):
		return self._size

	# @size.setter
	# def size(self, x):
	# 	self._size = self._size

	def create_copy(self, mutate = False):
		pass

	def is_there_palce_around(self):
		pass

	def move(self):
		pass

	def execute_command(self):
		self.currenc_command = (self.currenc_command + 1) / self.size

		if self.currenc_command == GET_ENERGY:
			self.energy += 1
		else if self.currenc_command == CREATE_COPY:
			if self.energy >= 100 and self.is_there_palce_around():
				self.create_copy()
				self.energy -= 50
		else if self.currenc_command == 
