from colours_subcomponent import DefineColourLibrary
from images_subcomponent import DefineImageLibrary
from text_subcomponent import DefineTextGenerator
from ...common_components import Vector
from ...common_components import GUI



class DefineApplicationWindow:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self, windowsize, windowtitle):


		# Defines the size of the application window
		self.screensize = Vector.createfromvector(windowsize)

		# Creates the application window object
		self.windowobject = GUI.display.set_mode((self.screensize.getcoordinates()))

		# Defines the application window title
		GUI.display.set_caption(windowtitle)

		# Loads image library
		self.imagelibrary = DefineImageLibrary()

		# Loads text generator
		self.textgenerator = DefineTextGenerator()

		# Loads colour library
		self.colourlibrary = DefineColourLibrary()



	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Adds a colour to the colour library
	# -------------------------------------------------------------------

	def addcolour(self, colourlabel, redvalue, greenvalue, bluevalue):

		self.colourlibrary.add(colourlabel, redvalue, greenvalue, bluevalue)



	# -------------------------------------------------------------------
	# Adds an image to the image library
	# -------------------------------------------------------------------

	def addimage(self, imagelabel, subfolder, filename, transparency):

		self.imagelibrary.add(imagelabel, subfolder, filename, transparency)



	# -------------------------------------------------------------------
	# Adds a font to the font library
	# -------------------------------------------------------------------

	def addfont(self, fontname, fontfile, fontsize):

		self.textgenerator.addfont(fontname, fontfile, fontsize)



	# -------------------------------------------------------------------
	# Prints image / text to screen
	# -------------------------------------------------------------------

	def drawimage(self, picture, position):

		self.windowobject.blit(self.imagelibrary.get(picture), (position.getcoordinates()))



	# -------------------------------------------------------------------
	# Flips the display
	# -------------------------------------------------------------------

	def updatescreen(self):

		GUI.display.flip()



	# -------------------------------------------------------------------
	# Draws a rectangle
	# -------------------------------------------------------------------

	def drawbox(self, topleft, rectanglesize, colour):

		GUI.draw.rect(self.windowobject, self.colourlibrary.get(colour),
														(topleft.getcoordinates(), rectanglesize.getcoordinates()), 0)



	# -------------------------------------------------------------------
	# Draws a circle
	# -------------------------------------------------------------------

	def drawcircle(self, centre, radius, colour):

		GUI.draw.circle(self.windowobject, self.colourlibrary.get(colour),
																				(centre.getcoordinates()), radius, 0)



	# -------------------------------------------------------------------
	# Writes text
	# -------------------------------------------------------------------

	def drawtext(self, outputtext, textposition, alignment, colour, fontname):

		textwidth = Vector.createfrompair(self.textgenerator.gettextwidth(outputtext, fontname)).getx()

		if alignment == "Left":
			margin = Vector.createorigin()
		elif alignment == "Right":
			margin = Vector.createfromvalues(textwidth, 0)
		elif alignment == "Centre":
			margin = Vector.createfromvalues(int(textwidth / 2), 0)
		else:
			margin = 1/0

		actualposition = Vector.subtract(textposition, margin)

		self.imagelibrary.settext(self.textgenerator.gettextimage(outputtext, self.colourlibrary.get(colour), fontname))
		self.drawimage("Text", actualposition)



	# ==========================================================================================
	# Get Information
	# ==========================================================================================

	def getscreensize(self):
		return self.screensize

