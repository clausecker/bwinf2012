
from types import Point, Rect

class Path:
	def __init__(self, pos):
		pos = Point(*pos)
		self.pos = pos
		self.path = [pos]

	def goto(self, newpos):
		newpos = Point(*newpos)
		if newpos.x != self.pos.x and newpos.y != self.pos.y:
			raise TypeError()
		self.pos = newpos
		self.path.append(newpos)

	def paint(self, canvas):
		for pos in self.path:
			canvas.draw_rect((pos + pos), color='green')

