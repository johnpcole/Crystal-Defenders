from colours_subcomponent import colours_module as ColourLibrary
from images_subcomponent import images_module as ImageLibrary
from text_subcomponent import text_module as TextGenerator
from ..vector_datatype import vector_module as Vector
from ..userinterface_framework import userinterface_module as GUI



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
		self.imagelibrary = ImageLibrary.createlibrary()

		# Loads text generator
		self.textgenerator = TextGenerator.creategenerator()

		# Loads colour library
		self.colourlibrary = ColourLibrary.createlibrary()



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
	# Draws a rectangle outline
	# -------------------------------------------------------------------

	def drawboxoutline(self, topleft, rectanglesize, colour, thickness):

		GUI.draw.rect(self.windowobject, self.colourlibrary.get(colour),
												(topleft.getcoordinates(), rectanglesize.getcoordinates()), thickness)



	# -------------------------------------------------------------------
	# Draws a circle
	# -------------------------------------------------------------------

	def drawcircle(self, centre, radius, colour):

		GUI.draw.circle(self.windowobject, self.colourlibrary.get(colour), (centre.getcoordinates()), radius, 0)



	# -------------------------------------------------------------------
	# Draws a circle outline
	# -------------------------------------------------------------------

	def drawcircleoutline(self, centre, radius, colour, thickness):

		GUI.draw.circle(self.windowobject, self.colourlibrary.get(colour),
																		(centre.getcoordinates()), radius, thickness)



	# -------------------------------------------------------------------
	# Writes text
	# -------------------------------------------------------------------

	def drawtext(self, outputtext, textposition, alignment, colour, fontname):

		textwidth = (self.gettextsize(outputtext, fontname)).getx()

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

	# -------------------------------------------------------------------
	# Returns the screensize
	# -------------------------------------------------------------------

	def getscreensize(self):
		return self.screensize



	# -------------------------------------------------------------------
	# Returns the size of a block of a text
	# -------------------------------------------------------------------

	def gettextsize(self, outputtext, fontname):
		return Vector.createfrompair(self.textgenerator.gettextsize(outputtext, fontname))
