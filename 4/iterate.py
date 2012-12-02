#!/usr/bin/env python

# check for python 3!
import sys
if sys.version_info[0] < 3:
	print("This program needs at least Python 3 to run.")
	sys.exit(-1)
del sys


# actual program
import xml.sax
import xml.sax.saxutils
import itertools

# Klasse zum Schreiben von XML-Dokumenten
class XMLWriter(xml.sax.saxutils.XMLGenerator):

	# Decorator zum Schreiben des nötigen Whitespaces, letztendlich egal,
	# da es wirklich nur Whitespace schreibt
	def do_indentation(delta_ind=0):
		def decorator(func):
			def do_indentation_impl(self, *args, **kwargs):
				if delta_ind > 0 and self.newline:
					self.write("\n")
				if delta_ind < 0:
					self.ind += delta_ind
				if delta_ind >= 0 or not self.newline:
					self.write("\t" * self.ind)
				if delta_ind > 0:
					self.ind += delta_ind
				func(self, *args, **kwargs)
				if delta_ind <= 0:
					self.write("\n")
					self.newline = False
				else:
					self.newline = True
			return do_indentation_impl
		return decorator

	def __init__(self, out, encoding='UTF-8'):
		# Initialisierung der Basisklasse XMLGenerator
		super().__init__(out, encoding)
		self.out = out
		self.ind = 0 # indentation count
		self.newline = False

	def write(self, s):
		self.out.write(s)

	@do_indentation(delta_ind=1)
	def startElement(self, *args, **kwargs):
		super().startElement(*args, **kwargs)

	@do_indentation()
	def characters(self, chars):
		super().characters(chars)

	@do_indentation(delta_ind=-1)
	def endElement(self, *args, **kwargs):
		super().endElement(*args, **kwargs)

	del do_indentation

class SierpinskiIterator(xml.sax.ContentHandler):
	def __init__(self, out_file):
		super().__init__()
		self.writer = XMLWriter(out_file)
		self.writer.startDocument()

	# Wird aufgerufen, wenn ein XML-Element beginnt
	def startElement(self, name, attributes):
		if name == "rect":
			# Falls das Quadrat weiß ist, so wird es durch acht
			# weiße und ein schwarzes in der Mitte ersetzt
			if attributes["fill"] == "white":
				# Die neue Breite und Höhe muss ein Drittel
				# der alten sein, damit 3x3 Quadrate in das
				# alte Quadrat hineinpassen
				width = float(attributes["width"]) / 3
				height = float(attributes["height"]) / 3
				x0 = float(attributes["x"])
				y0 = float(attributes["y"])

				# Für x,y in jeglicher Kombination von (0,1,2)
				for x, y in itertools.product(range(0, 2+1),
						range(0, 2+1)):
					fill = "white"
					# Falls es das mittlere Quadrat ist,
					# schwarz füllen
					if x == y == 1:
						fill = "black"
					# Element schreiben
					self.writer.startElement("rect", {
						"x": str(x0 + x * width),
						"y": str(y0 + y * height),
						"width": str(width),
						"height": str(height),
						"fill": fill,
					})
					self.writer.endElement("rect")
			else:
				self.writer.startElement(name, attributes)
				self.writer.endElement(name)
			return

		self.writer.startElement(name, attributes)

	def endElement(self, name):
		if name != "rect":
			# Da Rechtecke schon in der Funktion startElement
			# (s. o.) beendet werden, müssen hier nur alle anderen
			# beendet werden
			self.writer.endElement(name)

	def endDocument(self):
		self.writer.endDocument()

def iterate(in_file, out_file):
	# Parsen der Datei mithilfe des Event-basierten Parser, der oben
	# definiert wurde
	xml.sax.parse(in_file, SierpinskiIterator(out_file))

if __name__ == '__main__':
	# Ausgeführt, wenn das Programm als Skript gestartet wurde
	import argparse
	import sys

	# Kommandozeilenschnittstelle
	p = argparse.ArgumentParser()
	p.add_argument('input', nargs='?', default='-',
		help="file to use as input (default: stdin)")
	p.add_argument('output', nargs='?', default='-',
		help="file to output to (default: stdout)")
	args = p.parse_args()

	in_file = sys.stdin
	out_file = sys.stdout

	if args.input != '-':
		in_file = open(args.input, 'r')
	if args.output != '-':
		out_file = open(args.output, 'w')

	iterate(in_file, out_file)

	in_file.close()
	out_file.close()

