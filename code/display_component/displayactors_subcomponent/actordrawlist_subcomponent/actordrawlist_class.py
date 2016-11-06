from ....common_components.vector_datatype import vector_module as Vector



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

