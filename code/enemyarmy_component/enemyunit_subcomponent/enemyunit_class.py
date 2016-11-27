from ...common_components import Vector
from ...common_components import Scale



class DefineEnemyUnit:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self, startposition, health, speed, coinvalue, groundsize, physicalvulnerability,
				 													magicalvulnerability, flies, crystalvalue, name):

		# Integer scalar specifying how far along a path the enemy is
		self.position = int(startposition)

		# Vector indicating the specific pixel location of the enemy on the field
		# (Can be calculated on the fly from self.position, but is stored for convenience)
		self.coordinates = Vector.createblank()

		# Pixel dimensions of the enemy - The whole game requires actor/selection sizes to be 30x30
		self.groundsize = groundsize

		# Scale object, scalar integer with built in methods to handle health - Zero = dead
		self.health = Scale.createfull(health)

		# Determines whether the enemy is still alive and should therefore be processed
		# (Can be calculated on the fly from self.position, but is stored for convenience)
		self.isinplay = True

		# Determines whether the enemy is on the board, and can be attacked
		# (Can be calculated on the fly from self.position, but is stored for convenience)
		self.isonboard = False

		# Sets the speed of the enemy along the path
		self.speed = speed

		# Sets the coin value of the enemy when it dies
		self.coinvalue = coinvalue

		# Sets the name of the enemy
		self.name = name

		# Direction of travel - Used for display purposes
		self.direction = Vector.createorigin()

		# Sets the vulnerability of the enemy to physical attacks
		self.physical = physicalvulnerability

		# Sets the vulnerability of the enemy to magical attacks
		self.magical = magicalvulnerability

		# Sets whether the enemy flies or travels on land
		self.flies = flies

		# Sets how many crystals each enemy unit steals if they reach the goal
		self.crystalvalue = crystalvalue

		# Display image offset - For display purposes
		self.displayoffset = Vector.createfromvalues(-16, -36)

		# Display image size - For display purposes
		self.displaysize = Vector.createfromvalues(64, 64)



	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Move the enemy along the field's path if it's still in play (alive)
	# If the end of the path is reached, take out of play and register number
	# of crystals to lose. Also update whether the enemy is on the board
	# -------------------------------------------------------------------

	def move(self, field):

		# Keep track of how many crystals need to be deducted
		outcome = 0

		# Only process if the enemy object is still in play
		if self.isinplay == True:

			# Update enemy's position along the path
			if self.stepalongpath(field) == True:

			# If the end of the path is reached take the enemy object out of play and register crystal loss
				outcome = self.reachgoal()

			else:

			# If the end of the path is not reached, move the enemy object to new coordinates
				self.movetonewpathlocation(field)

		# Returns the number of crystals taken by the enemy
		return outcome



	# -------------------------------------------------------------------
	# Take step along path
	# -------------------------------------------------------------------

	def stepalongpath(self, field):

		# Update enemy's position along the path
		self.position = int(self.position + self.speed)

		# If the end of the path is reached mark as reached goal
		if self.position >= field.getfinalposition():
			outcome = True
		else:
			outcome = False

		# Return the goal situation
		return outcome



	# -------------------------------------------------------------------
	# Take step along path to new coordinates, and set direction
	# -------------------------------------------------------------------

	def movetonewpathlocation(self, field):

		# Determine the new location, using field information
		targetlocation = Vector.createfromvector(field.getpathcoordinates(self.position))

		# Set the direction of the enemy, used for display purposes
		self.direction = Vector.subtract(targetlocation, self.coordinates)

		# Move enemy to new coordinates
		self.coordinates = Vector.createfromvector(targetlocation)

		# Set the IsOnBoard status of the enemy object
		self.isonboard = field.isitemonfield(self.coordinates, self.groundsize)



	# -------------------------------------------------------------------
	# Reach goal, take out of play and reduce crystal count
	# -------------------------------------------------------------------

	def reachgoal(self):

		# Move enemy to off field, and take out of play
		self.removefromgame()

		# Returns the number of crystals taken by the enemy
		return self.crystalvalue



	# -------------------------------------------------------------------
	# Kill's the enemy, taking it out of play
	# -------------------------------------------------------------------

	def kill(self, defenderarmy):

		# If there is a theif nearby, multiply the coin count
		if defenderarmy.istheifnearby(self.coordinates) == True:
			multiplier = 2
		else:
			multiplier = 1

		# Take the enemy object out of play, off field
		self.removefromgame()

		# Returns the coin value of the enemy
		return multiplier * self.coinvalue



	# -------------------------------------------------------------------
	# Take the enemy object out of play, off field
	# -------------------------------------------------------------------

	def removefromgame(self):

		# Take the enemy object out of play
		self.isinplay = False

		# Move enemy to off field
		self.coordinates.setblank()

		# Set the IsOnBoard status of the enemy object
		self.isonboard = False



	# -------------------------------------------------------------------
	# Reduce the enemy's health - if it is zero, remove enemy from game
	# and return the number of coins it gives up
	# -------------------------------------------------------------------

	def takehit(self, defenderunit, defenderarmy):

		# Register no coin value return by default
		outcome = 0

		# Only evaluate enemy if it walks (with any kind of defender)
		# OR the defender fights with projectiles (with any kind of enemy)
		if self.isvisibletodefender(defenderunit) == True:

			# Reduce the enemy object health by the specified amount (depends on realm etc)
			# If there is no health remaining, take enemy off board and register coins gained
			if self.health.deplete(self.gethitpower(defenderunit)) == True:

				# Take the enemy object out of play & register the coin value of the enemy
				outcome = self.kill(defenderarmy)

		# Return the number of coins gained from the dead enemy
		return outcome



	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Return enemy's susceptability to being hit
	# -------------------------------------------------------------------

	def gethitpower(self, defenderunit):

		# Actual hitpower is a fraction of the defender's hit strength,
		# based on enemy's immunity to physical or magical attacks
		if defenderunit.getrealm() == "Physical":
			outcome = int(self.physical * defenderunit.getstrength() / 100)
		elif defenderunit.getrealm() == "Magical":
			outcome = int(self.magical * defenderunit.getstrength() / 100)
		else:
			outcome = 1/0

		return outcome



	# -------------------------------------------------------------------
	# Return enemy's pixel coordinates on field
	# -------------------------------------------------------------------

	def getcoordinates(self):

		return self.coordinates



	# -------------------------------------------------------------------
	# Return enemy's health as integer percentage
	# -------------------------------------------------------------------

	def gethealth(self):

		return int(self.health.getpercentage())



	# -------------------------------------------------------------------
	# Return enemy's on board status (is on the field)
	# -------------------------------------------------------------------

	def getonboardstatus(self):

		return self.isonboard



	# -------------------------------------------------------------------
	# Return enemy's in play status (has health and not yet reached goal)
	# -------------------------------------------------------------------

	def getinplaystatus(self):

		return self.isinplay



	# -------------------------------------------------------------------
	# Return enemy's ground size in pixels
	# -------------------------------------------------------------------

	def getsize(self):

		return self.groundsize



	# -------------------------------------------------------------------
	# Return enemy's integer progress along the path
	# -------------------------------------------------------------------

	def getposition(self):

		return self.position



	# -------------------------------------------------------------------
	# Return enemy's direction
	# -------------------------------------------------------------------

	def getdirection(self):

		return self.direction



	# -------------------------------------------------------------------
	# Return whether enemy flies
	# -------------------------------------------------------------------

	def doesfly(self):

		return self.flies



	# -------------------------------------------------------------------
	# Return enemy's direction & frame label - for display purposes only
	# -------------------------------------------------------------------

	def getdisplayframereference(self):

		# Determine the display frame based on the position on the path
		frame = 1 + (int(self.position / 40) % 2)

		# Return a composite string containing the name, compass label and frame number
		return self.name + " - " + self.getcompassdirection() + str(frame)



	# -------------------------------------------------------------------
	# Return enemy's direction compass label
	# -------------------------------------------------------------------

	def getcompassdirection(self):

		# Get the compass label of the direction of travel
		compasslabel = self.direction.getswapped().getcompass(1)

		# If there is no direction, set it to south anyway
		if compasslabel == "":
			compasslabel = "S"

		# Return the compass label
		return compasslabel



	# -------------------------------------------------------------------
	# Return whether an attacking thing is within attacking range of the enemy
	# Can be any set of coordinates, doesn't require actual defender object
	# -------------------------------------------------------------------

	def isinrange(self, defenderposition, radius):

		# Default to not engageable
		outcome = False

		# Is the enemy object located on the field
		if self.isonboard == True:

			# Is the enemy within the battle radius of the specified location
			if Vector.ispointinradius(self.coordinates, defenderposition, radius) == True:

				# Set the outcome to engageable
				outcome = True

		# Return the engageable value
		return outcome



	# -------------------------------------------------------------------
	# Return whether the eneny is even visible to the defender
	# -------------------------------------------------------------------

	def isvisibletodefender(self, defenderunit):

		# True only evaluate enemy if it walks (with any kind of defender)
		# OR the defender fights with projectiles (with any kind of enemy)
		if (self.flies == False) or (defenderunit.getcombatmethod() == "Projectile"):
			outcome = True
		else:
			outcome = False   # The defender is combat based and the enemy flies

		# Return the IsVisible value
		return outcome



	# -------------------------------------------------------------------
	# Return enemy's display location
	# -------------------------------------------------------------------

	def getdisplaylocation(self):
		# Offset the pixel location to ensure the ground is in the right place
		return Vector.add(self.displayoffset, self.coordinates.getint())



	# -------------------------------------------------------------------
	# Return enemy's display size
	# -------------------------------------------------------------------

	def getdisplaysize(self):
		# pixel size of display image, for erase purposes
		return self.displaysize



	# -------------------------------------------------------------------
	# Return enemy's display z-order
	# -------------------------------------------------------------------

	def getdisplayzorder(self):

		direction = self.getcompassdirection()
		if direction == "W":
			zorder = int(self.coordinates.getx())
		elif direction == "E":
			zorder = 9997 - int(self.coordinates.getx())
		else:
			zorder = 9998

		return zorder + (10000 * int(self.coordinates.gety()))
