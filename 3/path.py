# encoding=utf8

from natives import Point, Rect

class Path:
	def __init__(self, pos):
		pos = Point(*pos)
		self.pos = pos
		self.path = [pos]

	def goto(self, newpos):
		# Registrierung einer neuen Position
		newpos = Point(*newpos)

		# Überprüfen auf Plausiblität, nur rechtwinklige
		# Ortsänderungen erlaubt
		if newpos.x != self.pos.x and newpos.y != self.pos.y:
			raise TypeError()

		self.pos = newpos
		self.path.append(newpos)

	def paint(self, canvas):
		for pos in self.path:
			canvas.draw_rect((pos + pos), color='green')

