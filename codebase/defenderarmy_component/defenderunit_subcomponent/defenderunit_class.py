from ...common_components.vector_datatype import vector_module as Vector
from ...common_components.scale_datatype import scale_module as Scale
from ...common_components.enumeration_datatype import enumeration_module as Enumeration



class DefineDefenderUnit:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self, baseposition, movespeed, combatspeed, combatstrength, battleradius, defendertype, groundsize,
																strikeradius, collateralradius, realm, ammunition):

		# Level of Defender
		self.level = 1

		# Pixel location of defender base on field
		self.basecoordinates = baseposition

		# Pixel location of actual defender on field
		self.currentcoordinates = Vector.createfromvector(self.basecoordinates)

		# Pixel dimensions of the defender - The whole game requires actor/selection sizes to be 64x64
		self.groundsize = groundsize

		# Speed of defender movement - Maximum Vector length of coordinate change per cycle
		self.speed = movespeed

		# Radius from baseposition in which a defender will engage an enemy
		self.battleradius = battleradius

		# Radius from currentposition in which a defender will strike an enemy
		self.strikeradius = strikeradius

		# Radius from currentposition in which a defender will damage nearby enemies
		self.collateralradius = collateralradius

		# Speed of defender combat - The number of cycles between enemy hits from defender
		self.readytostrike = Scale.createfull(combatspeed)

		# Strength of defender - number of hit points each strike makes
		self.strength = combatstrength

		# Defender Type: Soldier, Archer, Wizard, Theif, Mage
		self.defendertype = Enumeration.createenum(["Soldier", "Archer", "Wizard", "Theif"], defendertype)

		# Ammo - If blank, contact combat type, if not blank, projectile combat type
		self.ammotype = Enumeration.createenum(["None", "Magic", "Arrow"], ammunition)

		# Direction of travel
		self.direction = Vector.createorigin()

		# Hit Type: Magical, Physical, Theif
		self.realm = Enumeration.createenum(["Magical", "Physical", "Theif"], realm)

		# Distance Odometer - For display purposes
		self.odometerdistance = Scale.createfull(100)

		# Combat Odometer - For display purposes
		self.odometercombat = Scale.createempty(20)

		# Display image offset - For display purposes
		self.displayoffset = Vector.createfromvalues(-16, -40)

		# Display image size - For display purposes
		self.displaysize = Vector.createfromvalues(64, 64)

		# Ammo display image offset - For display purposes
		self.ammodisplayoffset = Vector.createfromvalues(0, -16)

		# Ammo display image size - For display purposes
		self.ammodisplaysize = Vector.createfromvalues(32, 32)

		# Logs if a projectile defender's current coordinates should be reset back to base
		# next time the defender moves
		self.jumptobasenextmove = False



	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Upgrade defender with new stats
	# -------------------------------------------------------------------

	def updatestats(self, level, combatstrength, battleradius):

		# Level of Defender
		self.level = level

		# Radius from baseposition in which a defender will engage an enemy
		self.battleradius = battleradius

		# Strength of defender - number of hit points each strike makes
		self.strength = combatstrength



	# -------------------------------------------------------------------
	# Move the defender, either towards enemy if there is an enemy in
	# range, or back to base if there is no enemy in range
	# Ensure the defender stays on the field
	# -------------------------------------------------------------------

	def move(self, field, enemyarmy):

		# If the defender strikes via projectile, and they performed a strike on
		# the last move, immediately move the projectile back to base in one move
		if self.jumptobasenextmove == True:
			self.jumptobase()

		# Retrieve the enemy object in the collection which is in the defender battle radius
		# This has already been calculated and the result is stored on the parent army object
		detectedenemy = enemyarmy.gettargetenemy()

		# If there is no enemy object in the defender battle radius, move the defender/projectile back to base
		if detectedenemy is None:
			self.movetowardsbase(field)

		# If there is an enemy object in the defender battle radius, move the defender/projectile towards enemy
		else:
			self.movetowardsenemy(field, detectedenemy)



	# -------------------------------------------------------------------
	# Move the defender towards enemy
	# -------------------------------------------------------------------

	def movetowardsenemy(self, field, detectedenemy):

		# Only move the defender/projectile if the defender walks OR the projectile is ready to strike
		if (self.getcombatmethod() == "Contact") or (self.readytostrike.isfull() == True):

			# Restore combat odometer for display purposes, If it's a projectile based defender
			# who is only just starting to fire their projectile
			self.rechargeodometercombat("Move towards enemy")

			# Move the defender/projectile towards the coordinates of the enemy object
			self.movesmoothly(field, detectedenemy.getcoordinates())



	# -------------------------------------------------------------------
	# Move the defender towards base
	# -------------------------------------------------------------------

	def movetowardsbase(self, field):

		# If the defender fights by contact, walk slowly back to base coordinates
		if self.getcombatmethod() == "Contact":
			self.movesmoothly(field, self.basecoordinates)

		# If the defender fights by projectile, just reset the projectile back to base in one step
		else:
			self.jumptobase()



	# -------------------------------------------------------------------
	# Move the defender, towards a target co-ordinate
	# Ensure the defender stays on the field
	# -------------------------------------------------------------------

	def movesmoothly(self, field, targetlocation):

		# Calculate the Vector required to move the defender towards the target coordinates
		# The direction value is also used to determine which sprite is used to display the defender/projectile
		self.setspeedlimiteddirection(targetlocation)

		# Update the odometer for display purposes
		self.updateodometer()

		# Determine the new preferred location of the defender, based on the move Vector above
		preferredlocation = Vector.add(self.currentcoordinates, self.direction)

		# Move the defender to the new coordinates, ensuring it doesn't leave the field
		self.currentcoordinates = field.keepitemonfield(preferredlocation, self.groundsize)



	# -------------------------------------------------------------------
	# Set the movement displacement Vector, for one cycle,
	# based on a target and the defender's speed
	# -------------------------------------------------------------------

	def setspeedlimiteddirection(self, targetlocation):
		# Calculate the Vector required to move the defender towards the target coordinates
		# The direction value is also used to determine which sprite is used to display the defender/projectile
		gaptoclose = Vector.subtract(targetlocation, self.currentcoordinates)

		# Calculate the Vector used to move the defender
		# The same as above but limited in length by the speed of the defender
		self.direction = gaptoclose.getfitted(min(self.speed, gaptoclose.getlength()))



	# -------------------------------------------------------------------
	# Updates the movement odometer, purely for display purposes
	# -------------------------------------------------------------------

	def updateodometer(self):

		# Only update if the defender has moved a significant amount
		if self.direction.getlength() > 0.01:

			# Update the odometer counter
			if self.odometerdistance.restore(1) == True:

				# If the counter is full, reset to zero
				self.odometerdistance.discharge()



	# -------------------------------------------------------------------
	# Move the defender back to base immediately
	# -------------------------------------------------------------------

	def jumptobase(self):

		# Moves the defender/projectile back to base coordinates in one jump
		self.currentcoordinates = Vector.createfromvector(self.basecoordinates)

		# Ensure the defender's return to base flag is reset
		self.jumptobasenextmove = False
		
		# Set Direction
		self.direction.setorigin()



	# -------------------------------------------------------------------
	# Strikes the enemy, if the defender is completely recharged
	# and the enemy is on top of the defender
	# If Archer or Wizard, reset location back to base
	# -------------------------------------------------------------------

	def combatenemy(self, enemyarmy):

		# Default to NOT striking an enemy
		outcome = False

		# Update combat odometer for display purposes
		self.odometercombat.deplete(1)

		# Don't perform combat if the realm is Theif
		if self.realm != "Theiving":
		
			# Update the ReadyToStrike counter, recharging the defender's ability to strike enemies
			# Then only continue if the the defender is fully recharged to strike
			if self.readytostrike.restore(1) == True:

				# Retrieve the enemy object in the collection which is in the defender battle radius
				# This has already been calculated and the result is stored on the parent army object
				detectedenemy = enemyarmy.gettargetenemy()

				# Only continue if there is an enemy in the defender battle radius
				if self.canperformstrike(detectedenemy) == True:

					# Discharge the ReadyToStrike counter
					self.performstrike()

					# Set the outcome to successfully strike
					outcome = True

		# Return if a strike has successfully been made
		return outcome



	# -------------------------------------------------------------------
	# Perform the strike
	# -------------------------------------------------------------------

	def performstrike(self):

		# Discharge the ReadyToStrike counter
		self.readytostrike.discharge()

		# Restore combat odometer for display purposes, IF it's a combat based defender
		self.rechargeodometercombat("Perform Strike")

		# If the defender strikes via projectile, immediately move the
		# projectile back to base in one move, on the next move
		if self.getcombatmethod() == "Projectile":
			self.jumptobasenextmove = True



	# -------------------------------------------------------------------
	# Recharge the combat-odometer for display purposes
	# -------------------------------------------------------------------

	def rechargeodometercombat(self, action):

		if action == "Perform Strike":
			if self.getcombatmethod() == "Contact":
				self.odometercombat.recharge()

		elif action == "Move towards enemy":
			if self.getcombatmethod() == "Projectile":
				if self.isdefenderatbase() == True:
					self.odometercombat.recharge()

		else:
			print "Unknown Combat-Odometer Action"
			x = 1/0



	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Is enemy strikeable
	# -------------------------------------------------------------------

	def canperformstrike(self, detectedenemy):

		# By default, cannot perform strike
		outcome = False

		# Only continue if there is an enemy in the defender battle radius
		if detectedenemy is not None:

			# Only continue if the the defender is close enough to the enemy object's coordinates
			# At this point the defender successfully lands a strike on the enemy object
			if detectedenemy.isinrange(self.currentcoordinates, self.strikeradius) == True:
				outcome = True

		# Return whether defender can perform strike
		return outcome



	# -------------------------------------------------------------------
	# Return whether defender is back at base
	# -------------------------------------------------------------------

	def isdefenderatbase(self):

		if self.getdistancefrombase() < 0.1:
			outcome = True
		else:
			outcome = False
		return outcome



	# -------------------------------------------------------------------
	# Return defender's pixel position on field
	# -------------------------------------------------------------------

	def getcurrentcoordinates(self):

		return self.currentcoordinates



	# -------------------------------------------------------------------
	# Return defender's base pixel position on field
	# -------------------------------------------------------------------

	def getbasecoordinates(self):

		return self.basecoordinates



	# -------------------------------------------------------------------
	# Return defender's distance from base
	# -------------------------------------------------------------------

	def getdistancefrombase(self):

		return Vector.gap(self.basecoordinates, self.currentcoordinates)



	# -------------------------------------------------------------------
	# Return defender's battle radius
	# -------------------------------------------------------------------

	def getbattleradius(self):

		return self.battleradius



#	# -------------------------------------------------------------------
#	# Return defender's strike radius
#	# -------------------------------------------------------------------
#
#	def getstrikeradius(self):
#
#		return self.strikeradius



	# -------------------------------------------------------------------
	# Return defender's collateral radius
	# -------------------------------------------------------------------

	def getcollateralradius(self):

		return self.collateralradius



	# -------------------------------------------------------------------
	# Return defender's ground size in pixels
	# -------------------------------------------------------------------

	def getsize(self):

		return self.groundsize



	# -------------------------------------------------------------------
	# Return defender's hit type: Magical, Physical, Theif
	# -------------------------------------------------------------------

	def getrealm(self):

		return self.realm.displaycurrent()



	# -------------------------------------------------------------------
	# Return defender's hit strength
	# -------------------------------------------------------------------

	def getstrength(self):

		return self.strength



	# -------------------------------------------------------------------
	# Return defender's type: Soldier, Archer, Wizard, Theif, Mage
	# -------------------------------------------------------------------

	def gettype(self):

		return self.defendertype.displaycurrent()



	# -------------------------------------------------------------------
	# Return defender's combat method: Projectile or Contact
	# -------------------------------------------------------------------

	def getcombatmethod(self):

		if self.ammotype.get("None") == True:
			outcome = "Contact"
		else:
			outcome = "Projectile"

		return outcome



	# -------------------------------------------------------------------
	# Return defender's direction & frame label - for display purposes only
	# -------------------------------------------------------------------

	def getdisplayframereference(self):

		# Get the compass label of the direction of travel
		compasslabel = self.direction.getswapped().getcompass(1)

		# If there is no direction, set it to south anyway
		if compasslabel == "":
			compasslabel = "S"

		# Determine the display frame based on whether the defender has recently performed a strike
		if self.odometercombat.getpercentage() > 0:
			frame = 3
		else:
			frame = self.odometerdistance.getpartition(2)

		# Return a composite string containing the name, compass label and frame number
		return self.defendertype.displaycurrent() + " - " + compasslabel + str(frame)



	# -------------------------------------------------------------------
	# Return defender's display location
	# -------------------------------------------------------------------

	def getdisplaylocation(self):

		# If the defender is a soldier or theif, display actor at current location
		# If the defender is an archer or wizard display actor at base location

		# Offset the pixel location to ensure the ground is in the right place
		return Vector.add(self.getcoordinates().getint(), self.displayoffset)



	# -------------------------------------------------------------------
	# Return defender's display size
	# -------------------------------------------------------------------

	def getdisplaysize(self):

		# pixel size of display image, for erase purposes
		return self.displaysize



	# -------------------------------------------------------------------
	# Return ammos's direction & frame label - for display purposes only
	# -------------------------------------------------------------------

	def getammodisplayframereference(self):

		# For magic, frame depends on distance from defender base
		if self.realm.get("Magical") == True:
			# Return a composite string containing the name and frame number
			suffix = str(Scale.partitionintobuckets(self.battleradius, 8, self.getdistancefrombase()) % 4)

		# For arrows, frame depends on direction
		else:
			# Return a composite string containing the name and compass label
			suffix = self.getcompassdirection()

		return self.ammotype.displaycurrent() + " - " + suffix



	# -------------------------------------------------------------------
	# Return ammos's direction compass label
	# -------------------------------------------------------------------

	def getcompassdirection(self):

		# Get the compass label of the direction of travel
		compasslabel = self.direction.getswapped().getcompass(2)

		# If there is no direction, set it to south anyway
		if compasslabel == "":
			compasslabel = "S"

		# Return compass label
		return compasslabel



	# -------------------------------------------------------------------
	# Return ammo's display location
	# -------------------------------------------------------------------

	def getammodisplaylocation(self):

		# Offset the pixel location to ensure the ground is in the right place
		return Vector.add(self.currentcoordinates.getint(), self.ammodisplayoffset)



	# -------------------------------------------------------------------
	# Return ammos's display size
	# -------------------------------------------------------------------

	def getammodisplaysize(self):

		# pixel size of display image, for erase purposes
		return self.ammodisplaysize



	# -------------------------------------------------------------------
	# Return ammos's display status
	# -------------------------------------------------------------------

	def getammodisplaystatus(self):

		outcome = False
		if self.getcombatmethod() == "Projectile":
			if self.isdefenderatbase() == False:
				outcome = True

		return outcome



	# -------------------------------------------------------------------
	# Return defender's display z-order
	# -------------------------------------------------------------------

	def getdisplayzorder(self):

		# If the defender is a soldier or theif, display actor at current location
		# If the defender is an archer or wizard, display actor at base location

		return 9999 + (10000 * int(self.getcoordinates().gety()))


	# -------------------------------------------------------------------
	# Return ammo's display z-order
	# -------------------------------------------------------------------

	def getammodisplayzorder(self):

		return 9999 + (10000 * int(self.currentcoordinates.gety()))



	# -------------------------------------------------------------------
	# Return defender actors actual coordinates
	# -------------------------------------------------------------------

	def getcoordinates(self):

		# If the defender is a soldier or theif, current location
		if self.getcombatmethod() == "Contact":
			actuallocation = self.currentcoordinates

		# If the defender is an archer or wizard, base location
		else:
			actuallocation = self.basecoordinates

		return actuallocation



	# -------------------------------------------------------------------
	# Return defender actors actual coordinates
	# -------------------------------------------------------------------

	def getlevel(self):

		return self.level
