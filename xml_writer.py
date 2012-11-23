
import xml.sax.saxutils

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
