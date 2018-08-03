EMPTY = 0
BOT = 1

class Map(object):
	_N = None
	_M = None
	_map = None

	def __init__(self, n, m):
		self._N = n
		self._M = m
		self._map = [[EMPTY]*self._M]*self._N

	def is_empty(self, x, y): 
		if self._map[x][y] == EMPTY:
			return True

	def addBot(self, x, y):
		self._map[x][y] = BOT