class DefineDefenderConfiguration:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self):

		# Defender Type
		self.defendertype = "-999"

		# Speed of defender movement - Maximum Vector length of coordinate change per cycle
		self.movespeed = -999.999

		# Radius from baseposition in which a defender will engage an enemy
		self.engageradius = -999

		# Radius from currentposition in which a defender will strike an enemy
		self.strikeradius = -999

		# Radius from currentposition, when a stike is made to a target enemy,
		# in which other enemies also take a hit
		self.collateralradius = -999

		# Speed of defender combat - The number of cycles between enemy hits from defender
		self.combatspeed = -999

		# Strength of defender - number of hit points each strike makes
		self.strength = -999

		# Cost to buy defender
		self.cost = -999

		# Level of defender
		self.level = -999

		# Whether defender can be upgraded
		#self.upgradeable = True
		
		# Whether the hit type is Magical or Physical
		self.realm = "-999"

		# The name of the ammo, if a projectile
		self.ammo = "-999"

		

	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	def copypartialconfig(self, existingdefender):
	
		self.defendertype = existingdefender.defendertype
		self.movespeed = existingdefender.movespeed
		self.strikeradius = existingdefender.strikeradius
		self.collateralradius = existingdefender.collateralradius
		self.combatspeed = existingdefender.combatspeed
		self.realm = existingdefender.realm
		self.ammo = existingdefender.ammo
		self.defendertype = existingdefender.defendertype



	def setdata(self, fieldname, rawfieldvalue):

		if rawfieldvalue == "None":
			fieldvalue = ""
		else:
			fieldvalue = rawfieldvalue
	
		if fieldname == "Defender Type":
			self.defendertype = fieldvalue
		elif fieldname == "Move Speed":
			self.movespeed = float(fieldvalue)
		elif fieldname == "Combat Strike Radius":
			self.strikeradius = int(fieldvalue)
		elif fieldname == "Combat Speed":
			self.combatspeed = int(fieldvalue)
		elif fieldname == "Combat Realm":
			self.realm = fieldvalue
		elif fieldname == "Combat Collateral Radius":
			self.collateralradius = int(fieldvalue)
		elif fieldname == "Combat Ammo":
			self.ammo = fieldvalue

		elif fieldname == "Level":
			self.level = int(fieldvalue)
		elif fieldname == "Engage Radius":
			self.engageradius = int(fieldvalue)
		elif fieldname == "Combat Strength":
			self.strength = int(fieldvalue)
		elif fieldname == "Cost":
			self.cost = int(fieldvalue)
		else:
			print "Invalid Defender Config Data - ", fieldname, fieldvalue



	# ==========================================================================================
	# Get Information
	# ==========================================================================================

# Getters are not used for this class, because the class's sole object instance is a grandchild of
# of another object, and the grandparent is the only thing which interacts with this object

	def validateconfig(self):
	
		outcome = True
		if self.defendertype == "-999":
			outcome = False
		if self.movespeed == -999.999:
			outcome = False
		if self.strikeradius == -999:
			outcome = False
		if self.collateralradius == -999:
			outcome = False
		if self.combatspeed == -999:
			outcome = False
		if self.realm == "-999":
			outcome = False
		if self.ammo == "-999":
			outcome = False
		if self.defendertype == "-999":
			outcome = False
		if self.level == -999:
			outcome = False
		if self.engageradius == -999:
			outcome = False
		if self.strength == -999:
			outcome = False
		if self.cost == -999:
			outcome = False

		return outcome
