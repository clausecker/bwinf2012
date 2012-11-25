#!/usr/bin/env python

# check for python 3!
import sys
if sys.version_info[0] < 3:
	print("This program needs at least Python 3 to run.")
del sys


# actual program
from types import Point, Rect

from grid_canvas import GridCanvas
from room import Room
from path import Path

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

