from ..common_components import Scale



class DefineGame:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self):

		# Defines the game clock, which increments every cycle;
		# When the player selects fast mode, display only refreshes when the scale full cycles
		self.displayclock = Scale.createfull(200)

		# Defines the current wave, or level
		self.currentwave = -999

		# Defines the number of coins the player has
		self.coins = -999

		# Defines the number of crystals the player has
		self.crystals = -999

		# Sets up the crystal loss clock
		self.crystallossclock = Scale.createempty(100)

		# Sets up the coin gain clock
		self.coingainclock = Scale.createempty(100)

		# Populate all values with defaults for when a new game starts
		self.initialisegame()



	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Populate all game values with defaults for when a new game starts
	# -------------------------------------------------------------------

	def initialisegame(self):

		# Current wave is set to 0; will be incremented to 1 later
		self.currentwave = 0

		# Initial number of coins
		self.coins = 50

		# Initial number of crystals
		self.crystals = 20



	# -------------------------------------------------------------------
	# Reduce number of crystals; Used when an enemy reaches the end of a path
	# -------------------------------------------------------------------

	def losecrystals(self, crystalcount):

		if crystalcount > 0:

			# Lose Crystals
			self.crystals = max(self.crystals - crystalcount, 0)

			# Set Crystal Loss Clock
			self.crystallossclock.recharge()



	# -------------------------------------------------------------------
	# Determines whether the display should be refreshed,
	# based on game speed setting and clock counter
	# -------------------------------------------------------------------

	def cycledisplay(self, controls):

		# Update crystallossclock & coingainclock
		self.updatecoinandcrystalclocks()

		# Update the displayclock, by amount determined by the game speed
		# If the clock completes a full cycle, update the display
		if self.displayclock.deplete(self.getclockspeed(controls.getdisplayallframes())) == True:
			self.displayclock.recharge()
			outcome = True
		else:
			outcome = False

		# Return whether to update display or not
		return outcome



	# -------------------------------------------------------------------
	# Updates the coin/crystal clocks
	# -------------------------------------------------------------------

	def updatecoinandcrystalclocks(self):

		# Update crystallossclock
		self.crystallossclock.deplete(1)

		# Update coingainclock
		self.coingainclock.deplete(1)



	# -------------------------------------------------------------------
	# Increases the level count
	# -------------------------------------------------------------------

	def startnextlevel(self):

		# Increase wave count
		self.currentwave = self.currentwave + 1



	# -------------------------------------------------------------------
	# Spends coins, if possible
	# -------------------------------------------------------------------

	def spendcoins(self, cost):

		# Reduce coin count
		self.coins = self.coins - cost

		if self.coins < 0:
			print "Overspend"
			x = 1/0



	# -------------------------------------------------------------------
	# Adds coins to player's tally
	# -------------------------------------------------------------------

	def gaincoins(self, amount):

		if amount > 0:

			# Gain Coins
			self.coins = self.coins + amount

			# Set Coin Gain Clock
			self.coingainclock.recharge()



	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Gets the current wave, or level
	# -------------------------------------------------------------------

	def getwave(self):

		return self.currentwave



	# -------------------------------------------------------------------
	# Gets the coin count
	# -------------------------------------------------------------------

	def getcoincount(self):

		return self.coins



	# -------------------------------------------------------------------
	# Gets the crystal count
	# -------------------------------------------------------------------

	def getcrystalcount(self):

		return self.crystals



	# -------------------------------------------------------------------
	# Gets the crystallosscountstatus
	# -------------------------------------------------------------------

	def getcrystallossstatus(self):

		return not(self.crystallossclock.isempty())



	# -------------------------------------------------------------------
	# Gets the coingaincountstatus
	# -------------------------------------------------------------------

	def getcoingainstatus(self):

		return not(self.coingainclock.isempty())




	# -------------------------------------------------------------------
	# Gets the number of clock ticks based on the game speed
	# -------------------------------------------------------------------

	def getclockspeed(self, goslowflag):

		# If game is set to slow speed, return true for every fourth frame
		if goslowflag == True:
			depletionrate = 50

		# If game is set to fast speed, update the clock counter, and if it has
		# fully cycled, only then return true (because only occasional frames are displayed)
		else:
			depletionrate = 1

		return depletionrate



	# -------------------------------------------------------------------
	# Determines if the game is over
	# -------------------------------------------------------------------

	def isgameover(self):

		# If all crystals have gone, return true
		if self.crystals <= 0:
			outcome = True

		# If there is at least one crystal, return false
		else:
			outcome = False

		return outcome



	# -------------------------------------------------------------------
	# Determines if the player has enough coins to make a purchase
	# -------------------------------------------------------------------

	# def canspendcoins(self, cost):
	#
	# 	# If there are enough coins, return true
	# 	if self.coins >= cost:
	# 		outcome = True
	#
	# 	# If there are not enough coins, return false
	# 	else:
	# 		outcome = False
	#
	# 	return outcome


