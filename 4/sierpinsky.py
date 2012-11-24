
import itertools

from svg_processor import SVGProcessor

class SierpinskyProcessor(SVGProcessor):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def onElement(self, name, attributes):
		assert(name == "rect")
		if attributes["fill"] == "white":
			width = float(attributes["width"]) / 3
			height = float(attributes["height"]) / 3
			x0 = float(attributes["x"])
			y0 = float(attributes["y"])
			for x, y in itertools.product(range(0, 2+1), range(0, 2+1)):
				fill = "white"
				if x == y == 1:
					fill = "black"
				self.writeElement("rect", {
					"x": str(x0 + x * width),
					"y": str(y0 + y * height),
					"width": str(width),
					"height": str(height),
					"fill": fill,
				})
		else:
			self.writeElement(name, attributes)

