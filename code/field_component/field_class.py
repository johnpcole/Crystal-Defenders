from fieldconfig_subcomponent import fieldconfig_module as FieldConfiguration
from ..common_components.vector_datatype import vector_module as Vector
from ..common_components.scale_datatype import scale_module as Scale



class DefineField:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self):

		# Gets the field layout, from which the board and enemy path are built
		layoutplan = FieldConfiguration.createfieldconfig()

		# Size of the field in blocks - units that determine granularity of defender base positioning
		# and actor size
		self.blocksize = layoutplan.getsize()

		# Grid array of all block locations in the field, defining the terrain type which
		# can be Grass, Border, Path, or Defender
		self.board = [["Grass" for y in range(0, self.blocksize.gety())] for x in range(0, self.blocksize.getx())]

		# Defines the pixel size of each block
		self.pixelblockratio = Vector.createfromvalues(16, 16)

		# Size of the field in pixels - Can be calculated on the fly but easier to store
		self.pixelsize = self.convertblocksizetopixelsize()

		# Current block coordinates of the mouse cursor on the field
		self.currentblockselection = Vector.createblank()

		# Defines the size of the cursor selection of the field & actors, in block units
		self.selectionblocksize = Vector.createfromvalues(2, 2)

		# Defines the perimeter around the edge of the field (in block coordinates)
		self.setupfieldperimeter(layoutplan)

		# Defines the pixel & block coordinates of each position along the enemy's path
		self.enemypath = layoutplan.getenemypath(self.pixelblockratio, self.selectionblocksize)
		self.minpos = 1
		self.maxpos = len(self.enemypath)
		self.pathblockwidth = 3
		self.setupenemypath()
		self.tidyenemypath()



	# -------------------------------------------------------------------
	# Draws a block perimeter around the edge of the field
	# -------------------------------------------------------------------

	def setupfieldperimeter(self, layoutplan):

		block = Vector.createblank()
		for x in range(0, self.blocksize.getx()):
			for y in range(0, self.blocksize.gety()):
				block.setfromvalues(x, y)
				if layoutplan.getterraintype(block) == "Border":
					self.setgroundtype(block, "Border")



	# -------------------------------------------------------------------
	# Sets up the enemy path on board
	# - Based on path definition, NOT layout
	# -------------------------------------------------------------------

	def setupenemypath(self):

		oldblock = Vector.createblank()
		looper = Vector.createblank()

		# Loop over all positions along the path
		for pathposition in range(self.minpos, self.maxpos + 1):

			# Get block coordinates of path position
			block = self.convertpixeltoblock(self.enemypath[pathposition].getint())

			# Only process the block if it hasn't already been processed
			if Vector.compare(block, oldblock) == False:
				oldblock.setfromvector(block)

				# Loop over blocks surrounding the current block
				for x in range(0, self.pathblockwidth):
					for y in range(0, self.pathblockwidth):
						looper.setfromvalues(x, y)
						marker = Vector.add(block, looper)

						# Only process surrounding block if it's on the field
						if self.issingleblockonboard(marker) == True:

							# Mark the block as Path
							self.setgroundtype(marker, "Path")



	# -------------------------------------------------------------------
	# Tidyup Enemy Path for display purposes
	# -------------------------------------------------------------------

	def tidyenemypath(self):

		# Loop over all blocks on the board
		block = Vector.createblank()
		for x in range(0, self.blocksize.getx()):
			for y in range(0, self.blocksize.gety()):
				block.setfromvalues(x, y)

				# Only process path blocks
				if self.getgroundtype(block) == "Path":

					# Determine search limits, ensuring seached blocks are kept on the field
					if x == 0:
						eastlimit = x
					else:
						eastlimit = x - 1
					if x == self.blocksize.getx() - 1:
						westlimit = x
					else:
						westlimit = x + 1
					if y == 0:
						northlimit = y
					else:
						northlimit = y - 1
					if y == self.blocksize.gety() - 1:
						southlimit = y
					else:
						southlimit = y + 1

					# Keeps track of which neighbouring blocks are NOT path blocks
					nonpathcount = ""

					if self.board[x][northlimit][:4] != "Path":
						nonpathcount = nonpathcount + "S"
					if self.board[x][southlimit][:4] != "Path":
						nonpathcount = nonpathcount + "N"
					if self.board[eastlimit][y][:4] != "Path":
						nonpathcount = nonpathcount + "W"
					if self.board[westlimit][y][:4] != "Path":
						nonpathcount = nonpathcount + "E"

					# If NESW neighbouring blocks are all Path, check diagnoally surrounding
					# blocks to determine if it's an internal corner path block
					if len(nonpathcount) == 0:
						if self.board[westlimit][northlimit][:4] != "Path":
							self.setgroundtype(block, "Path - Internal NW")
						elif self.board[westlimit][southlimit][:4] != "Path":
							self.setgroundtype(block, "Path - Internal SW")
						elif self.board[eastlimit][northlimit][:4] != "Path":
							self.setgroundtype(block, "Path - Internal NE")
						elif self.board[eastlimit][southlimit][:4] != "Path":
							self.setgroundtype(block, "Path - Internal SE")
						else:
							self.setgroundtype(block, "Path - Full")

					# If two NESW neighbouring blocks are not path, it's an external corner path block
					elif len(nonpathcount) == 2:
						self.setgroundtype(block, "Path - External " + nonpathcount)

					# If one NESW block is not path, it's an edge path block
					elif len(nonpathcount) == 1:
						self.setgroundtype(block, "Path - " + nonpathcount)

					# If three NESW blocks are not path, something has gone wrong
					else:
						x = 1/0


	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Updates the selected block-selection on the field
	# -------------------------------------------------------------------

	def updateselection(self, controls):

		# Update field selection value with dummy location if selection is off the field
		self.currentblockselection.setblank()

		# Get pixel coordinates of mouse cursor
		sanitisedmouseposition = controls.getfieldselectionlocation()

		# Only process if the mouse cursor is on the field
		if Vector.ispointinarea(sanitisedmouseposition, Vector.createorigin(), self.pixelsize) == True:

			# Get block coordinates of mouse cursor
			blockposition = self.convertpixeltoblock(sanitisedmouseposition)

			# Update field selection value with actual location if selection is on the field
			if self.isblockonboard(blockposition, self.selectionblocksize) == True:
				self.currentblockselection = blockposition



	# -------------------------------------------------------------------
	# Add a defender to the field (assumes terrain permits)
	# -------------------------------------------------------------------

	def adddefendertofield(self):

		# Only process if the selection is valid - It's not overlapping path or another defender
		if self.isselectionvalidtoadddefender() == True:

			# Loops over all blocks that the new defender is based on
			origin = self.currentblockselection
			offset = Vector.createblank()
			for offsetx in range(0, self.selectionblocksize.getx()):
				for offsety in range(0, self.selectionblocksize.gety()):
					offset.setfromvalues(offsetx, offsety)
					block = Vector.add(offset, origin)

					# Set field block value to Defender
					self.setgroundtype(block, "Defender")

		else:
			print "Attempted to add a defender to field at invalid selection point"
			print self.currentblockselection.getx(), self.currentblockselection.gety()
			x = 1/0



	# -------------------------------------------------------------------
	# Wipes all defenders from field
	# -------------------------------------------------------------------

	def wipedefendersfromfield(self):

		# Loop over all blocks on the field
		offset = Vector.createblank()
		for offsetx in range(0, self.blocksize.getx()):
			for offsety in range(0, self.blocksize.gety()):
				offset.setfromvalues(offsetx, offsety)

				# Only process if the current block is marked as a Defender
				if self.getgroundtype(offset) == "Defender":

					# Set the field's block back to Grass
					self.setgroundtype(offset, "Grass")



	# -------------------------------------------------------------------
	# Sets the field terrain of block on field
	# -------------------------------------------------------------------

	def setgroundtype(self, position, terrain):

		self.board[position.getx()][position.gety()] = terrain



	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Returns pixel co-ordinates of point along enemy path
	# -------------------------------------------------------------------

	def getpathcoordinates(self, position):

		# Default location is dummt location, off the field
		outcome = Vector.createblank()

		# Only return a real location if the position is within the path boundaries
		if position >= self.minpos:
			if position <= self.maxpos:
				outcome = self.enemypath[position]

		# Return the pixel co-ordinates of the path position
		return outcome



	# -------------------------------------------------------------------
	# Returns field terrain of block on field
	# -------------------------------------------------------------------

	def getgroundtype(self, position):

		return self.board[position.getx()][position.gety()]



	# -------------------------------------------------------------------
	# Returns pixel dimensions of field
	# -------------------------------------------------------------------

	def getsize(self):

		return self.pixelsize



	# -------------------------------------------------------------------
	# Returns pixel dimensions of selection on field
	# -------------------------------------------------------------------

	def getselectionsize(self):

		return Vector.multiply(self.selectionblocksize, self.pixelblockratio)



#	# -------------------------------------------------------------------
#	# Returns pixel co-ordinates of current field selection
#	# -------------------------------------------------------------------

#	def getcurrentselection(self):

#		return multiplyvectors(self.currentblockselection, self.pixelblockratio)



	# -------------------------------------------------------------------
	# Returns block dimensions of field
	# -------------------------------------------------------------------

	def getblocksize(self):

		return self.blocksize



	# -------------------------------------------------------------------
	# Ensures tentative co-ordinates are kept within the field boundary
	# If tentative co-ordinates are outside boundary, they are adjusted
	# to be as close to desired as possible but within field
	# Returns pixel co-ordinates
	# -------------------------------------------------------------------

	def keepitemonfield(self, tentativedestination, itemdimensions):

		finaldestination = Vector.createblank()

		finaldestination.setx(Scale.keepsubrangeinrange(0, self.pixelsize.getx(), tentativedestination.getx(),
																							itemdimensions.getx()))
		finaldestination.sety(Scale.keepsubrangeinrange(0, self.pixelsize.gety(), tentativedestination.gety(),
																							itemdimensions.gety()))

		return finaldestination



	# -------------------------------------------------------------------
	# Returns pixel location and dimensions of item overhang/off field
	# NOTE This assumes the overhang is only off one edge of the field,
	# 										NOT a corner
	# -------------------------------------------------------------------

	def getoverhang(self, itemlocation, itemdimensions):

		# If item is completely on field, return original coordinates
		overhanglocation = Vector.createfromvector(itemlocation)
		overhangdimensions = Vector.createfromvector(itemdimensions)

		# If item is partially or fully off field, calculate off field oblong
		if self.isitemonfield(itemlocation, itemdimensions) == False:

			ol, od = Scale.getrangeoverhang(0, self.pixelsize.getx(), itemlocation.getx(), itemdimensions.getx())
			overhanglocation.setx(ol)
			overhangdimensions.setx(od)

			ol, od = Scale.getrangeoverhang(0, self.pixelsize.gety(), itemlocation.gety(), itemdimensions.gety())
			overhanglocation.sety(ol)
			overhangdimensions.sety(od)

		return overhanglocation, overhangdimensions



	# -------------------------------------------------------------------
	# Returns whether a pixel-defined oblong is within the boundary of the field
	# -------------------------------------------------------------------

	def isitemonfield(self, itemlocation, itemdimensions):

		return Vector.isoblonginarea(itemlocation, itemdimensions, Vector.createorigin(), self.pixelsize)



	# -------------------------------------------------------------------
	# Returns whether a block-defined oblong is within the boundary of the field
	# -------------------------------------------------------------------

	def isblockonboard(self, blocklocation, blockdimensions):

		return Vector.isoblonginarea(blocklocation, blockdimensions, Vector.createorigin(), self.blocksize)



	# -------------------------------------------------------------------
	# Returns whether a single-block location is within the boundary of the field
	# -------------------------------------------------------------------

	def issingleblockonboard(self, blocklocation):

		return Vector.ispointinarea(blocklocation, Vector.createorigin(), self.blocksize)



	# -------------------------------------------------------------------
	# Returns the final position of the enemy along the path
	# -------------------------------------------------------------------

	def getfinalposition(self):

		return self.maxpos



	# -------------------------------------------------------------------
	# Returns the starting position of the first enemy along the path
	# -------------------------------------------------------------------

	def getstartingposition(self):

		return self.minpos



	# -------------------------------------------------------------------
	# Returns block co-ordinates for any given pixel co-ordinates
	# -------------------------------------------------------------------

	def convertpixeltoblock(self, vector):

		outcome = (Vector.divide(vector, self.pixelblockratio)).getint()
		if vector.getx() < 0:
			outcome.setx(outcome.getx() - 1)
		if vector.gety() < 0:
			outcome.sety(outcome.gety() - 1)
		return outcome



	# -------------------------------------------------------------------
	# Returns pixel co-ordinates for any given block co-ordinates
	# -------------------------------------------------------------------

	def convertblocktopixel(self, vector):

		return Vector.multiply(vector, self.pixelblockratio)



	# -------------------------------------------------------------------
	# Returns pixel co-ordinates for any given block co-ordinates
	# -------------------------------------------------------------------

	def getpixelblockratio(self):

		return self.pixelblockratio



	# -------------------------------------------------------------------
	# Returns pixel dimensions for any given block dimensions
	# -------------------------------------------------------------------

	def convertblocksizetopixelsize(self):

		return Vector.multiply(self.blocksize, self.pixelblockratio)



	# -------------------------------------------------------------------
	# Returns whether a defender could be added to the field
	# with the specified block co-ordinates
	# -------------------------------------------------------------------

	def isselectionvalidtoadddefender(self):

		# Default to ALLOW defender to be added to field at selection location
		outcome = True

		# Loop over all blocks in selection area
		offset = Vector.createblank()
		for offsetx in range(0, self.selectionblocksize.getx()):
			for offsety in range(0, self.selectionblocksize.gety()):
				offset.setfromvalues(offsetx, offsety)
				block = Vector.add(offset, self.currentblockselection)

				# Only test block if it is on the field
				if self.issingleblockonboard(block) == True:

					# If the block is NOT grass, then set outcome to NOT ALLOW defender to be addded
					if self.getgroundtype(block) != "Grass":
						outcome = False

				# If block is not on the field, then set outcome to NOT ALLOW defender to be addded
				else:
					outcome = False

		# Return whether a defender could be added in this position
		return outcome



	# -------------------------------------------------------------------
	# Converts a mouse pixel location to a field selection location
	# -------------------------------------------------------------------

	def calculatefieldselectionlocation(self, mouseposition):
		# Update field selection value with dummy location if selection is off the field
		outcome = Vector.createblank()

		# Only process if the mouse cursor is on the field
		if Vector.ispointinarea(mouseposition, Vector.createorigin(), self.pixelsize) == True:

			# Get block coordinates of mouse cursor
			rawmouseblockposition = self.convertpixeltoblock(mouseposition)

			# Get pixel offset of mouse cursor from top left of block
			mousepositionwithinblock = Vector.subtract(mouseposition, self.convertblocktopixel(rawmouseblockposition))

			# Determine which block is deemed selected based on the mouse cursor position within the hovered block
			selectionoffset = Vector.createblank()
			selectionoffset.setx(Scale.partitionintobuckets(self.pixelblockratio.getx() - 1, 2,
																			mousepositionwithinblock.getx()) - 1)
			selectionoffset.sety(Scale.partitionintobuckets(self.pixelblockratio.gety() - 1, 2,
																			mousepositionwithinblock.gety()) - 1)
			mouseblockposition = Vector.add(rawmouseblockposition, selectionoffset)

			# Update field selection value with actual location if selection is on the field
			if self.isblockonboard(mouseblockposition, self.selectionblocksize) == True:
				outcome = self.convertblocktopixel(mouseblockposition)

		return outcome


