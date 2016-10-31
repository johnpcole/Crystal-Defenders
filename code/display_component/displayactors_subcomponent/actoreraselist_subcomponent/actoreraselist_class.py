from ....common_components import *



class DefineEraseBlock:



	def __init__(self, imagelocation, imagename):

		# image name
		self.blockname = imagename

		# Pixel location of image
		self.coordinates = Vector.createfromvector(imagelocation)


