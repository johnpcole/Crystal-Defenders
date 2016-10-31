from ....common_components import *



class DefineDisplayActor:



	def __init__(self, imagelocation, imagedimensions, imagename, imagezorder, imagehealth):

		# image name
		self.actorname = imagename

		# Pixel location of image
		self.coordinates = Vector.createfromvector(imagelocation)

		# Pixel dimensions of image
		self.dimensions = Vector.createfromvector(imagedimensions)

		# health of image, if an enemy
		self.health = imagehealth

		# z-order of image
		self.zorder = imagezorder

