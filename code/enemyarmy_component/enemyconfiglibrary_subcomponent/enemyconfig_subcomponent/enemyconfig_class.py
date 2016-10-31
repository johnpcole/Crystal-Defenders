class DefineEnemyConfiguration:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self):

		self.wave = -999
	
		# Number of enemy units in army for wave
		self.number = 30

		# Integer scalar specifying how far along a path the enemy is initially
		self.spacing = 500

		# Starting health
		self.health = -999

		# The speed of the enemy along the path
		self.speed = 2

		# The coin value of an enemy when it dies
		self.coinvalue = 1

		# The name of the enemy
		self.name = "-999"

		# If the enemy flies rather than walks
		self.flies = False

		# Susceptability to physical attacks (Percentage)
		self.physical = 100

		# Suseptability to magical attacks (Percentage)
		self.magical = 100

		# How many crystals enemy unit steals if reaches the end of the path
		self.crystalvalue = 1

		

	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	def setdata(self, fieldname, rawfieldvalue):

		if rawfieldvalue == "None":
			fieldvalue = ""
		else:
			fieldvalue = rawfieldvalue
	
		if fieldname == "Wave":
			self.wave = int(fieldvalue)
		elif fieldname == "Name":
			self.name = fieldvalue
		elif fieldname == "Health":
			self.health = int(fieldvalue)
		elif fieldname == "Speed":
			self.setspeed(fieldvalue)
		elif fieldname == "Coin":
			self.coinvalue = int(fieldvalue)
		elif fieldname == "Crystal":
			self.crystalvalue = int(fieldvalue)
		elif fieldname == "Number":
			self.number = int(fieldvalue)
		elif fieldname == "Spacing":
			self.spacing = int(fieldvalue)
		elif fieldname == "Move":
			self.setmove(fieldvalue)
		elif fieldname == "Resist-Magical":
			self.resistmagical(fieldvalue)
		elif fieldname == "Resist-Physical":
			self.resistphysical(fieldvalue)
		else:
			print "Invalid Enemy Config Data - ", fieldname, fieldvalue

			
			

	def resistphysical(self, level):

		if level == "1":
			self.physical = 90 # Percent
		elif level == "2":
			self.physical = 70 # Percent
		elif level == "3":
			self.physical = 40 # Percent
		elif level == "4":
			self.physical = 0 # Percent
		else:
			print "Invalid Enemy Physical Resistance - ", level



	def resistmagical(self, level):

		if level == "1":
			self.magical = 90 # Percent
		elif level == "2":
			self.magical = 70 # Percent
		elif level == "3":
			self.magical = 40 # Percent
		elif level == "4":
			self.magical = 0 # Percent
		else:
			print "Invalid Enemy Magical Resistance - ", level


			
			
			
	
	def setspeed(self, speedlabel):

		if speedlabel == "Fast":
			self.speed = 5
		else:
			print "Invalid Enemy Speed - ", speedlabel
	
	
	
	def setmove(self, movelabel):

		if movelabel == "Fly":
			self.flies = True
		else:
			print "Invalid Enemy Move Type - ", movelabel
	
	
	
	
	# ==========================================================================================
	# Get Information
	# ==========================================================================================

# Getters are not used for this class, because the class's sole object instance is a grandchild of
# of another object, and the grandparent is the only thing which interacts with this object

	def validateconfig(self):
	
		outcome = True
		if self.name == "-999":
			outcome = False
		if self.health == -999:
			outcome = False
		if self.wave == -999:
			outcome = False
	
		return outcome
