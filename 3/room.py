
from types import Point, Rect

class Room:
	def __init__(self, input_file):
		def read():
			return [int(x) for x in input_file.readline().split()]

		self.dimension = Point(*read())
		self.pos = Point(*read())
		self.exit = Rect(*read())
		num_rects = read()[0]
		self.rects = []
		for i in range(num_rects):
			self.rects.append(Rect(*read()))

	@staticmethod
	def _in_rect(point, rect):
		return ((rect.left <= point.x <= rect.right
			or rect.right <= point.x <= rect.left)
			and (rect.top <= point.y <= rect.bottom
			or rect.bottom <= point.y <= rect.top))

	def is_collision(self, point):
		point = Point(*point)
		if self._in_rect(point, self.exit):
			return False
		if (point.x <= 0 or point.y <= 0
			or point.x >= self.dimension.x - 1
			or point.y >= self.dimension.y - 1):
			return True
		for wall in self.rects:
			if self._in_rect(point, wall):
				return True
		return False

	def is_exit(self, point):
		return self._in_rect(Point(*point), self.exit)

	def paint(self, canvas):
		for r in self.rects:
			canvas.draw_rect(r)
		canvas.draw_rect((0, 0, self.dimension.x - 1, self.dimension.y- 1), fill=False)
		canvas.draw_rect(self.exit, color='white')

