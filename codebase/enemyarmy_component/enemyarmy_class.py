from enemyconfiglibrary_subcomponent import enemyconfiglibrary_module as EnemyConfigurationLibrary
from enemyunit_subcomponent import enemyunit_module as EnemyUnit



class DefineEnemyArmy:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self):

		# Collection of enemies
		self.units = []

		# Currently attacked enemy - Points to one of the enemy collection
		self.currenttargetunit = None

		# Name of enemy army for current wave - Used only on next wave plaque
		self.enemyname = ""

		# Initial healthpoints - Used only on next wave plaque
		self.initialhealth = -999

		# Store all the enemy configurations
		self.configlibrary = EnemyConfigurationLibrary.createconfig()
		
		

	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Reduce the enemy's health, if any is a target
	# -------------------------------------------------------------------

	def takehit(self, defenderunit, defenderarmy):

		# Only perform the hit if there is an enemy object under attack by a defender
		# The enemy object is already determined and stored in the CurrentTargetUnit pointer
		if self.currenttargetunit is None:
			outcome = 1 / 0

		# If the defender has a non-zero collateral radius, it can damage multiple enemies in one hit
		# Perform hits on all enemy objects in the collateral radius and retrieves coins if any deaths
		if defenderunit.getcollateralradius() > 0:
			outcome = self.takecollateralhit(defenderunit, defenderarmy)

		# If the defender has a zero collateral radius, it can damage only the target enemy in one hit
		# Perform the hit on the individual enemy object and retrieve the coins if the enemy dies
		else:
			outcome = self.currenttargetunit.takehit(defenderunit, defenderarmy)

		# Returns the total number of coins retrieved from enemies who have died
		return outcome



	# -------------------------------------------------------------------
	# Reduce multiple enemies' health, if any is in collateral range
	# -------------------------------------------------------------------

	def takecollateralhit(self, defenderunit, defenderarmy):

		# Keeps a count of how any coins are retrieved if an enemy dies
		outcome = 0

		# Loop over all enemy objects in collection
		for enemyunit in self.units:

			# Determine if the individual enemy and defender are in collateral distance of each other
			if enemyunit.isinrange(defenderunit.getcurrentcoordinates(), defenderunit.getcollateralradius()) == True:

				# Perform the hit on the individual enemy object
				# And retrieve the coins if the enemy dies
				outcome = outcome + enemyunit.takehit(defenderunit, defenderarmy)

		# Returns the total number of coins retrieved from enemies who have died
		return outcome



	# -------------------------------------------------------------------
	# Wipe all enemies from the army (ready for the next wave)
	# -------------------------------------------------------------------

	def wipearmy(self):

		# Delete all enemy objects in the collection
		del self.units[:]



	# -------------------------------------------------------------------
	# Populate the army for the current wave
	# -------------------------------------------------------------------

	def populatearmy(self, game, field):

		# Delete all enemy objects in the collection
		self.wipearmy()

		# Retrieve the configuration of the enemies and army for the specified wave
		config = self.configlibrary.getenemyconfig(game.getwave())

		# Create as many enemy objects in the collection as specified in the configuration
		for enemyunit in range(0, config.number):

			# Calculate the starting position along the path for the current enemy object
			startposition = int(field.getstartingposition() - (enemyunit * config.spacing))

			# Create an enemy object with the correct configuration
			self.units.append(EnemyUnit.createconfig(startposition, config.health, config.speed,
													config.coinvalue, field.getselectionsize(), config.physical,
													config.magical, config.flies, config.crystalvalue, config.name))

		# Set enemy army name
		self.enemyname = config.name

		# Set enemy unit initial health
		self.initialhealth = config.health



	# -------------------------------------------------------------------
	# Determine the enemy which is closest to the end of the path, for
	# enemies within a given radius of the specified defender object
	# -------------------------------------------------------------------

	def identifytargetenemy(self, defenderunit):

		# Default to there being no target enemy
		selectedunit = None

		# Loop over all enemy units in the collection
		for enemyunit in self.units:

			# Only evaluate enemy if it walks (with any kind of defender)
			# OR the defender fights with projectiles (with any kind of enemy)
			if enemyunit.isvisibletodefender(defenderunit) == True:

				# Only evaluate enemy if it is within battle radius of the defender object's base coordinates
				if enemyunit.isinrange(defenderunit.getbasecoordinates(), defenderunit.getbattleradius()) == True:

					# If this is the first enemy within the battleradius, make it the selected unit
					# If this isn't the first enemy within the battleradius, only make it the selected
					# unit if it is further along the path than the existing selected unit
					selectedunit = self.getlatestunit(selectedunit, enemyunit)

		# Set the Army's CurrentTargetUnit to be the selected unit
		self.currenttargetunit = selectedunit



	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Return the enemy which is closest to a point, for enemies
	# within a given radius of that point
	# -------------------------------------------------------------------

	def gettargetenemy(self):

		return self.currenttargetunit



	# -------------------------------------------------------------------
	# Return whether there are any enemy units still in play
	# -------------------------------------------------------------------

	def isanyonealive(self):

		outcome = False
		for enemyunit in self.units:
			if enemyunit.getinplaystatus() == True:
				outcome = True

		return outcome



	# -------------------------------------------------------------------
	# Return the name of the enemy
	# -------------------------------------------------------------------

	def getname(self):

		return self.enemyname



	# -------------------------------------------------------------------
	# Return the initial health of the enemy
	# -------------------------------------------------------------------

	def getinitialhealth(self):

		return "HP: " + str(self.initialhealth)



	# -------------------------------------------------------------------
	# Gets unit which is closer to end of path / goal
	# -------------------------------------------------------------------

	def getlatestunit(self, unitone, unittwo):

		if unitone is None:
			outcome = unittwo
		elif unittwo is None:
			outcome = unitone
		else:
			if unitone.getposition() > unittwo.getposition():
				outcome = unitone
			else:
				outcome = unittwo

		return outcome

