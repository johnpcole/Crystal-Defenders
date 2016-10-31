from defenderconfiglibrary_subcomponent import DefineDefenderConfigurationLibrary
from defenderunit_subcomponent import DefineDefenderUnit
from ..common_components import Vector



class DefineDefenderArmy:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self, field):

		# Collection of Defenders
		self.units = []

		# Currently selected Defender, used for upgrading
		self.selecteddefender = None

		# Standard defender footprint size on field (in pixels)
		self.defendergroundsize = field.getselectionsize()

		# Store all the defender configurations
		self.configlibrary = DefineDefenderConfigurationLibrary()
		


	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================


	# -------------------------------------------------------------------
	# Add a new defender to the army, or upgrade an existing defender
	# If adding, flag this in the outcome so the defender can also
	# be added to the field
	# -------------------------------------------------------------------

	def addorupgradedefender(self, controls):

		outcome = False

		if controls.getaddorupgradedefenderaction()[:3] == "Add":
			# Add new defender object to collection
			self.adddefendertoarmy(controls)

			# Set the outcome to true so the defender can also be added to the field
			outcome = True

		elif controls.getaddorupgradedefenderaction() == "Upgrade Defender":
			# Upgrade the existing defender
			self.upgradeexistingdefender()

		return outcome



	# -------------------------------------------------------------------
	# Add a new defender to the field
	# -------------------------------------------------------------------

	def upgradeexistingdefender(self):

		# Retrieve the existing level of the defender
		newlevel = self.selecteddefender.getlevel() + 1

		# Retrieve the standard configuration for a level x defender of the required type
		newconfig = self.configlibrary.getdefenderconfig(self.selecteddefender.gettype(), newlevel)

		# Update the existing defender with the new stats
		self.selecteddefender.updatestats(newlevel, newconfig.strength, newconfig.engageradius)



	# -------------------------------------------------------------------
	# Add a new defender to the field
	# -------------------------------------------------------------------

	def adddefendertoarmy(self, controls):

		# Retrieve the defender type requested by user, stored in the control object
		newdefendertype = controls.getaddorupgradedefenderaction()[6:]

		# Retrieve the standard configuration for a level 1 defender of the required type
		config = self.configlibrary.getdefenderconfig(newdefendertype, 1)

		# Add the new defender, using all the configuration parameters
		self.units.append(DefineDefenderUnit(controls.getfieldselectionlocation(), config.movespeed,
												config.combatspeed, config.strength, config.engageradius,
												newdefendertype, self.defendergroundsize, config.strikeradius,
												config.collateralradius, config.realm, config.ammo))



	# -------------------------------------------------------------------
	# Clear the field of all defenders
	# -------------------------------------------------------------------

	def wipearmy(self):

		# Delete all defenders in the collection
		del self.units[:]



	# -------------------------------------------------------------------
	# Determine the defender positioned exactly at the field selection
	# point, if there is one. Used to determine whether user can upgrade
	# -------------------------------------------------------------------

	def updateselection(self, control):

		# Default to there being no target enemy
		selectedunit = None

		# Retrieve the location of the defender requested by user, stored in the control object
		groundposition = control.getfieldselectionlocation()

		# Loop over all enemy units in the collection
		for defenderunit in self.units:

			if Vector.compare(groundposition, defenderunit.getbasecoordinates()) == True:
				selectedunit = defenderunit

		# Set the Army's SelectedDefender to be the selected unit
		self.selecteddefender = selectedunit



	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Return whether there are any defenders away from base
	# -------------------------------------------------------------------

	def isanyoneawayfrombase(self):

		outcome = False

		# Loop over all defenders in the colection
		for defenderunit in self.units:

			# Determine if the defender is NOT back at base
			if defenderunit.isdefenderatbase() != True:
				outcome = True

		# If at least one defender is NOT at base, return True
		return outcome



	# -------------------------------------------------------------------
	# Return whether there are any theives near location
	# -------------------------------------------------------------------

	def istheifnearby(self, location):

		outcome = False

		# Loop over all defenders in the colection
		for defenderunit in self.units:

			# Is defender a theif
			if defenderunit.getrealm() == "Theiving":

				# Is the theif within the collateral radius of the specified location
				if Vector.ispointinradius(location, defenderunit.getcurrentcoordinates(),
																	defenderunit.getcollateralradius()) == True:

					outcome = True

		# If at least one theif is close enough, return True
		return outcome



	# -------------------------------------------------------------------
	# Returns the cost of a new defender
	# -------------------------------------------------------------------

	def getnewdefendercost(self, defendertype):

		# Retrieve the standard configuration for a level 1 defender of the required type
		config = self.configlibrary.getdefenderconfig(defendertype, 1)

		# Returns the coin cost of a level 1 defender of requested type
		return config.cost



	# -------------------------------------------------------------------
	# Returns the cost of a defender upgrade for selected defender
	# -------------------------------------------------------------------

	def getdefenderupgradecost(self):

		# Retrieve the standard configuration for a level 1 defender of the required type
		newconfig = self.configlibrary.getdefenderconfig(self.selecteddefender.gettype(),
																	self.selecteddefender.getlevel() + 1)

		# Returns the coin cost of leveling up the defender
		return newconfig.cost



	# -------------------------------------------------------------------
	# Returns the currently selected defender, if there is one
	# -------------------------------------------------------------------

	def getselecteddefender(self):

		# Returns the currently selected defender, or None
		return self.selecteddefender

