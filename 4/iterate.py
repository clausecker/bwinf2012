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

class XMLWriter(xml.sax.saxutils.XMLGenerator):
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

	def startElement(self, name, attributes):
		if name == "rect":
			if attributes["fill"] == "white":
				width = float(attributes["width"]) / 3
				height = float(attributes["height"]) / 3
				x0 = float(attributes["x"])
				y0 = float(attributes["y"])
				for x, y in itertools.product(range(0, 2+1), range(0, 2+1)):
					fill = "white"
					if x == y == 1:
						fill = "black"
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
		if name != "rect": # rects are already ended in 'startElement'
			self.writer.endElement(name)

	def endDocument(self):
#		print("end_document")
		self.writer.endDocument()

def iterate(in_file, out_file):
	xml.sax.parse(in_file, SierpinskiIterator(out_file))

if __name__ == '__main__':
	import argparse
	import sys
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

