from random import randrange
from map import Map
from bot import Bot

M = 100
N = 100
X = 200

class World(object):
	_bots = None
	_map = None

	def __init__(self):
		self._map = Map(N, M)
		self._bots = []

		for i in range(X):
			x = randrange(0, N)
			y = randrange(0, M)
			if self._map.is_empty(x, y):
				self._map.addBot(x, y)
				bot = Bot(x, y)
				self._bots.append(bot)