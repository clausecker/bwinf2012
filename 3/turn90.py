#!/usr/bin/env python
# encoding=utf8

# check for python 3!
import sys
if sys.version_info[0] < 3:
	print("This program needs at least Python 3 to run.")
del sys


# actual program

from natives import Point, Rect

from grid_canvas import GridCanvas
from room import Room
from path import Path

def solve(room):
	def goto_dir(p, dir_):
		DIRECTIONS = (Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0))
		direction = DIRECTIONS[dir_ % len(DIRECTIONS)]
		p = Point(*p)
		return Point(p.x + direction.x, p.y + direction.y)

	# path speichert den zurückgelegten Weg
	path = Path(room.pos)

	# dir_ speichert die aktuelle Richtung
	dir_ = 0

	# Nach jedem Schritt überprüfen, ob bereits am Ende angekommen
	while not room.is_exit(path.pos):

		# Setzen einiger Variablen:
		# curpos: aktuelle Position
		# frontpos: Position vor dem Roboter
		# leftpos: Position links von dem Roboter
		# front bzw. left speichern, ob das Feld vor bzw. links vom
		#   Roboter frei sind
		curpos = path.pos
		frontpos = goto_dir(curpos, dir_)
		leftpos = goto_dir(curpos, dir_ + 1)
		front = not room.is_collision(frontpos)
		left = not room.is_collision(leftpos)

		# newpos wird in jedem Fall auf die Position gesetzt, auf die
		#   der Roboter sich bewegen wird.
		newpos = None

		# Pledge-Algorithmus
		if dir_ == 0:
			# Ursprünglicher Richtung:
			#   geradeaus gehen, falls möglich
			#   sonst der Wand folgen
			if front:
				newpos = frontpos
			else:
				# stehen bleiben und nach rechts drehen
				newpos = curpos
				dir_ -= 1
		else:
			# Wandfolgen
			if left:
				# falls links frei ist, dorthin drehen und
				# hinlaufen
				dir_ += 1
				newpos = leftpos
			elif front:
				# ansonsten falls möglich geradeaus der Wand
				# folgen
				newpos = frontpos
			else:
				# ansonsten nach rechts drehen
				newpos = curpos
				dir_ -= 1

		# Wenn sich die Position geändert hat, zur Ergebnisvariable
		# path hinzufügen
		if newpos != curpos:
			path.goto(newpos)

	return path

if __name__ == '__main__':
	import argparse
	import sys

	# Initialisierung der Parameterübergabe
	p = argparse.ArgumentParser()
	p.add_argument('input', help="file to use as input")
		# for format documentation, see
		#http://www.bundeswettbewerb-informatik.de/index.php?id=1168 (german)
	p.add_argument('-s', '--scale', type=int, default=10,
		help="pixels per grid point")
	p.add_argument('-o', '--output', type=str, default=None,
		help="file to output the result to")
	p.add_argument('-q', '--no-interactive', action="store_true",
		help="deactivate interactive window output")
	p.add_argument('-w', '--wall-color', type=str, default='red',
		help="color for the walls")
	p.add_argument('-p', '--path-color', type=str, default='green',
		help="color for the path")
	args = p.parse_args()

	in_file = sys.stdin

	if args.input != '-':
		in_file = open(args.input, 'r')

	# Raum aus Datei auslesen
	room = Room(in_file)

	if in_file != sys.stdin:
		in_file.close()

	# Zeichenoberfläche vorbereiten
	grid_canvas = GridCanvas("Turn90", room.dimension, args.scale)

	# Raum einzeichnen
	room.paint(grid_canvas, color=args.wall_color)

	# Weg berechnen und einzeichnen
	path = solve(room)
	path.paint(grid_canvas, color=args.path_color)

	# Ausgabe
	if args.output:
		grid_canvas.dump(args.output)
	if not args.no_interactive:
		grid_canvas.mainloop()

