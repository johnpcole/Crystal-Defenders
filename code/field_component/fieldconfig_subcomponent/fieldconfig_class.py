from ...common_components import Vector
from ...common_components import File



class DefineFieldConfiguration:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self):

		# Field layout showing path layout and border
		self.layout = self.readlayoutfromdisk()

		# Size of the field
		self.blocksize = Vector.createfromvalues(len(self.layout[0]), len(self.layout))

		# Block Position of the enemy path Start point
		self.startblock = self.findpathendblock("S")

		# Block Position of the enemy path End point
		self.endblock = self.findpathendblock("E")

		# Crop width of field
		self.blockcrop = Vector.createfromvalues(2, 2)



	def readlayoutfromdisk(self):

		templayout = File.readfromdisk("configs/Field.txt")
		outcome = []

		for templine in templayout:
			outcome.append(list(templine))

		return outcome




	def findnextpathblock(self, pos):

		# Default next block to be dummy location
		outcome = Vector.createblank()

		# If block is not on edge of screen, check the neighbouring block
		if pos.getx() > 0:

			# If neighbouring block is path (or end), return this neighbouring block location
			if self.isblockonpath(pos.getx() - 1, pos.gety()) == True:
				outcome.setfromvalues(pos.getx() - 1, pos.gety())

		# If block is not on edge of screen, check the neighbouring block
		if pos.getx() < self.blocksize.getx():
			# If neighbouring block is path (or end), return this neighbouring block location
			if self.isblockonpath(pos.getx() + 1, pos.gety()) == True:
				outcome.setfromvalues(pos.getx() + 1, pos.gety())

		# If block is not on edge of screen, check the neighbouring block
		if pos.gety() > 0:
			# If neighbouring block is path (or end), return this neighbouring block location
			if self.isblockonpath(pos.getx(), pos.gety() - 1) == True:
				outcome.setfromvalues(pos.getx(), pos.gety() - 1)

		# If block is not on edge of screen, check the neighbouring block
		if pos.gety() < self.blocksize.gety():
			# If neighbouring block is path (or end), return this neighbouring block location
			if self.isblockonpath(pos.getx(), pos.gety() + 1) == True:
				outcome.setfromvalues(pos.getx(), pos.gety() + 1)

		# Return location of neighbouring block which is marked as a path
		return outcome



	def isblockonpath(self, x, y):

		# Default outcome to NOT on path
		outcome = False

		# Return the type of block on the layout map
		blocktype = self.getblock(Vector.createfromvalues(x, y))

		# If the block is a path or end, then outcome to IS on path
		if (blocktype == "#") or (blocktype == "E"):
			outcome = True

		# Returns whether block is on path or not
		return outcome



	def findpathendblock(self, whichend):

		# Default outcome to dummy location off field
		outcome = Vector.createblank()

		# Loop over all blocks
		block = Vector.createblank()
		for x in range(0, self.blocksize.getx()):
			for y in range(0, self.blocksize.gety()):
				block.setfromvalues(x, y)

				# If current block is specified path end, set outcome to be block coordinates
				if self.getblock(block) == whichend:
					outcome.setfromvector(block)

		# Return block coordinates of specified path end
		return outcome



	def markpathdone(self, currentblockposition):

		# Set the block value of the layout plan to be NOT a path, so it isn't processed again
		self.layout[currentblockposition.gety()][currentblockposition.getx()] = "O"






	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	def getsize(self):

		return Vector.subtract(self.blocksize, self.blockcrop.getscaled(2))



	def getblock(self, location):

		return self.layout[location.gety()][location.getx()]



	def getterraintype(self, location):

		terrain = self.getblock(Vector.add(location, self.blockcrop))
		if terrain == "~":
			outcome = "Border"
		else:
			outcome = "Grass"
		return outcome



	def getenemypath(self, pixelblockratio, characterblocksize):

		# How many path movements per screen pixel
		pathblockratio = 10 * max(pixelblockratio.getx(), pixelblockratio.gety())

		# How far to shift the path coordinates to accont for the actor size
		actorsizeshift = Vector.subtract(characterblocksize,Vector.createfromvalues(1,1)).getscaled(0.5)

		# How far in pixels to shift the path coordinates to account for cropping AND actor size
		pixelshift = Vector.multiply(pixelblockratio, Vector.add(actorsizeshift, self.blockcrop))

		# Collection of points along the path
		pathdefinition = {}

		# Current point along path
		currentpathposition = 0

		# Pixel coordinates of current point along path
		currentpathblock = Vector.createfromvector(self.startblock)

		# Keep looping until the end block of the layout map is reached
		keepmapping = True
		while keepmapping == True:

			# Identify the next block in the path (the only block adjacent to the current block which is
			# marked on the layout map as path)
			nextpathblock = self.findnextpathblock(currentpathblock)

			# Get floating point coordinate versions of the current and next blocks
			initial = currentpathblock.getfloat()
			final = nextpathblock.getfloat()

			# Interpolate points along the path between the top left corners of the current and next blocks
			for offset in range(0, pathblockratio):

				# Increment current path position counter
				currentpathposition = currentpathposition + 1

				# Calculate interpolation factors
				forwardoffset = float(offset) / float(pathblockratio)
				reverseoffset = 1.0 - forwardoffset

				# Calculate floating point / fractional block coordinates of path position
				blockcoords = Vector.add(final.getscaled(forwardoffset), initial.getscaled(reverseoffset))

				# Calculate floating point / fractional pixel coordinates of path position
				pixelcoords = Vector.multiply(blockcoords, pixelblockratio)

				# Add pixel coordinate to path definition collection, shifting by crop & enemy size offsets
				pathdefinition[currentpathposition] = Vector.subtract(pixelcoords, pixelshift)

				# If current block is the end block, stop looping
				if self.getblock(currentpathblock) == "E":
					keepmapping = False

				# If current block is NOT end block, mark current block as processed
				# and replace current block with next block
				else:
					self.markpathdone(currentpathblock)
					currentpathblock.setfromvector(nextpathblock)

		# Return the collection of path definition points
		return pathdefinition