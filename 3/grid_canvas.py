
import tkinter

from types import Point, Rect

class GridCanvas:
	def __init__(self, dimension, scale):
		dimension = Point(*dimension)
		self.tk = tkinter.Tk()
		self.canvas = tkinter.Canvas(self.tk, width=(dimension.x)*scale, height=(dimension.y)*scale)
		self.canvas.pack()
		self.scale = scale

	def draw_rect(self, rect, color='red', fill=True):
		rect = Rect(*rect)
		if not fill:
			l, t, r, b = rect  # split coordinates

			self.draw_rect((l, t, r, t), color) # top line
			self.draw_rect((l, b, r, b), color) # bottom line
			self.draw_rect((l, t, l, b), color) # left line
			self.draw_rect((r, t, r, b), color) # right line
			return

		world_rect = [self.scale * x for x in rect]
		world_rect[2] += self.scale - 1
		world_rect[3] += self.scale - 1

		self.canvas.create_rectangle(world_rect, fill=color, outline=color, activefill='black', width=0)

	def mainloop(self):
		self.tk.mainloop()

