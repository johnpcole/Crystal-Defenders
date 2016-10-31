from ....common_components import GUI



class DefineTextGenerator:

	def __init__(self):

		# Define the font library
		self.fontlibrary = {}



	def addfont(self, fontname, fontfile, fontsize):
		self.fontlibrary[fontname] = GUI.font.Font(fontfile, fontsize)



	def gettextwidth(self, textstring, fontname):
		return self.fontlibrary[fontname].size(textstring)



	def gettextimage(self, textstring, colourcode, fontname):
		return self.fontlibrary[fontname].render(textstring, True, colourcode)