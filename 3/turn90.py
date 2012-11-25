#!/usr/bin/env python

# check for python 3!
import sys
if sys.version_info[0] < 3:
	print("This program needs at least Python 3 to run.")
del sys


# actual program
import re
import time
import tkinter
import turtle

from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Rect = namedtuple('Rect', ['left', 'top', 'right', 'bottom'])

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

def solve(room):
	def goto_dir(p, dir_):
		DIRECTIONS = (Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0))
		direction = DIRECTIONS[dir_ % len(DIRECTIONS)]
		p = Point(*p)
		return Point(p.x + direction.x, p.y + direction.y)

	path = Path(room.pos)
	dir_ = 0
	while not room.is_exit(path.pos):
		curpos = path.pos
		frontpos = goto_dir(curpos, dir_)
		leftpos = goto_dir(curpos, dir_ + 1)
		front = not room.is_collision(frontpos)
		left = not room.is_collision(leftpos)

		newpos = None

		if dir_ == 0:
			if front:
				newpos = frontpos
			else:
				newpos = curpos
				dir_ -= 1
		else:
			if left:
				newpos = leftpos
				dir_ += 1
			elif front:
				newpos = frontpos
			else:
				newpos = curpos
				dir_ -= 1

		path.goto(newpos)

	return path

if __name__ == '__main__':
	f = open('raum0_beispiel.txt', 'r')
	#f = open('raum1.txt', 'r')
	#f = open('raum2.txt', 'r')
	#f = open('raum3.txt', 'r')
	room = Room(f)
	f.close()

	grid_canvas = GridCanvas(room.dimension, 10)
	room.paint(grid_canvas)

	path = solve(room)
	path.paint(grid_canvas)

	grid_canvas.mainloop()

