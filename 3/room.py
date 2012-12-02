# encoding=utf8

from natives import Point, Rect

class Room:
	def __init__(self, input_file):
		def read():
			# Funktion liefert die nächstgelesene Zeile als Liste
			# von Ganzzahlen zurück ("1 2 3" => [1, 2, 3])
			return [int(x) for x in input_file.readline().split()]

		# Lesen der Datei nach dem spezifizierten Format
		self.dimension = Point(*read())
		self.pos = Point(*read())
		self.exit = Rect(*read())
		num_rects = read()[0]
		self.rects = []
		for i in range(num_rects):
			self.rects.append(Rect(*read()))

	@staticmethod
	def _in_rect(point, rect):
		# Funktion zum Überprüfen, ob ein Punkt in einem Rechteck liegt
		# Da oberer und untere bzw. linke und rechte Grenze vertauscht
		# vorliegen können, werden beide Varianten geprüft.
		return ((rect.left <= point.x <= rect.right
			or rect.right <= point.x <= rect.left)
			and (rect.top <= point.y <= rect.bottom
			or rect.bottom <= point.y <= rect.top))

	def is_collision(self, point):
		# Funktion gibt zurück, ob am gegebenen Punkt eine Wand ist
		point = Point(*point)

		# Im Falle des Ausgangs liegt per Definition keine Wand vor
		if self._in_rect(point, self.exit):
			return False

		# Der restliche Rand ist Wand
		if (point.x <= 0 or point.y <= 0
			or point.x >= self.dimension.x - 1
			or point.y >= self.dimension.y - 1):
			return True

		# Ansonsten alle Wandrechtecke durchgehen und auf 'Im-Rechteck-
		# Liegen' prüfen
		for wall in self.rects:
			if self._in_rect(point, wall):
				return True

		# Falls es innerhalb von keinem Hindernis ist, so liegt ein
		# frei begehbares Feld vor
		return False

	def is_exit(self, point):
		# Gibt zurück, ob der vorliegende Punkt ein Ausgang ist
		return self._in_rect(Point(*point), self.exit)

	def paint(self, canvas):
		# Zeichnet den Raum mit den Hindernissen
		for r in self.rects:
			canvas.draw_rect(r)

		# Außenbegrenzung
		canvas.draw_rect((0, 0, self.dimension.x - 1,
			self.dimension.y - 1), fill=False)

		# Ausgang
		canvas.draw_rect(self.exit, color='white')

