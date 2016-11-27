from ....common_components import GUI



class DefineImageLibrary:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self):

		self.key = {}
		self.key['Text'] = None



	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Reads images in from disk, applying transparency where required
	# -------------------------------------------------------------------

	def add(self, imagelabel, subfolder, filename, transparency):

		if subfolder is None:
			fullpath = "graphics\\" + filename + ".png"
		else:
			fullpath = "graphics\\" + subfolder + "\\" + filename + ".png"

		if transparency == True:
			self.key[imagelabel] = GUI.image.load(fullpath).convert_alpha()
		else:
			self.key[imagelabel] = GUI.image.load(fullpath).convert()



	# -------------------------------------------------------------------
	# Sets the text image to be the image object passed in
	# -------------------------------------------------------------------

	def settext(self, imageobject):
		self.key['Text'] = imageobject



	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Returns the specified image object
	# -------------------------------------------------------------------

	def get(self, imagename):
		return self.key[imagename]
