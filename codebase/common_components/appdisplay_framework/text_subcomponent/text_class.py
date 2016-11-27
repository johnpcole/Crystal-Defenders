from ....common_components.userinterface_framework import userinterface_module as GUI
from ....common_components.fileprocessing_framework import fileprocessing_module as File



class DefineTextGenerator:

	def __init__(self):

		# Define the font library
		self.fontlibrary = {}



	def addfont(self, fontname, subfolder, fontfile, fontsize):

		if subfolder is None:
			fullpath = File.concatenatepaths("graphics", fontfile + ".ttf")
		else:
			fullpath = File.concatenatepaths(File.concatenatepaths("graphics", subfolder), fontfile + ".ttf")

		self.fontlibrary[fontname] = GUI.font.Font(fullpath, fontsize)



	def gettextsize(self, textstring, fontname):
		return self.fontlibrary[fontname].size(textstring)



	def gettextimage(self, textstring, colourcode, fontname):
		return self.fontlibrary[fontname].render(textstring, True, colourcode)
