# encoding=utf8

import tkinter

from natives import Point, Rect

class GridCanvas:
	def __init__(self, name, dimension, scale):
		dimension = Point(*dimension)
		# Initialisierung der Zeichenoberfläche
		self.tk = tkinter.Tk()
		self.name = name
		self.tk.title(name)
		self.canvas = tkinter.Canvas(
			self.tk,
			width=dimension.x*scale,
			height=dimension.y*scale
		)
		self.canvas.pack()
		self.scale = scale

	def draw_rect(self, rect, color='red', fill=True):
		rect = Rect(*rect)

		# Ohne Füllung => vier gefüllte Rechtecke für die Linien
		if not fill:
			l, t, r, b = rect  # split coordinates

			self.draw_rect((l, t, r, t), color) # top line
			self.draw_rect((l, b, r, b), color) # bottom line
			self.draw_rect((l, t, l, b), color) # left line
			self.draw_rect((r, t, r, b), color) # right line
			return

		# Berechnen der Fensterkoordinaten
		world_rect = [self.scale * x for x in rect]
		world_rect[2] += self.scale - 1
		world_rect[3] += self.scale - 1

		# Zeichnen
		self.canvas.create_rectangle(
			world_rect,
			fill=color,
			outline=color,
			activefill='black',
			width=0
		)

	def dump(self, filename):
		# Ausgabe in Datei
		self.canvas.update()
		self.canvas.postscript(file=filename)

	def mainloop(self):
		self.tk.mainloop()

