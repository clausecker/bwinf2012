
import xml.sax

from xml_writer import XMLWriter

class SVGProcessor(xml.sax.ContentHandler):
	# this class is to be inherited by one that defines onElement and
	# does something with it, afterwards calling writeElement
	def __init__(self, in_file, out_file):
		super().__init__()
		self.writer = XMLWriter(out_file)
		self.writer.startDocument()
		self.in_file = in_file
		self.encountered_root = False

	def start(self):
		xml.sax.parse(self.in_file, self)

	def startElement(self, name, attributes):
		if name == "svg":
			assert(not self.encountered_root)
			self.writer.startElement(name, attributes)
			self.encountered_root = True
			return
		self.onElement(name, attributes)

	def endElement(self, name):
		pass

	def writeElement(self, name, attributes):
		self.writer.startElement(name, attributes)
		self.writer.endElement(name)

	def endDocument(self):
		self.writer.endElement("svg")
		self.writer.endDocument()


