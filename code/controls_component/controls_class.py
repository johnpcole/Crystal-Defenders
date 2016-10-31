from buttonlibrary_component import DefineButtonLibrary
from ..common_components import Vector
from ..common_components import GUI



class DefineController:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self, field, defenderarmy):

		# Store all button definitions, including field selection area
		self.buttons = DefineButtonLibrary(field, defenderarmy)

		# Specifies whether the game should "run" - enemies walk and defenders walk/combat, in this cycle
		self.runstate = True

		# Specifies whether the user has requested to close the application in this cycle
		self.quitstate = False

		# Game speed
		self.gamefast = False

		# Specifies whether the game is "between waves" mode
		self.betweenwavesmode = False

		# Specifies where the field selection location is
		self.fieldhoverlocation = Vector.createblank()

		# Specifies where the mouse location is
		self.mousehoverlocation = Vector.createblank()

		# Specifies which enabled button, if any, the current mouse position is
		self.currenthoverbutton = ""

		# Specifies whether the field or add/upgrade defender buttons have been clicked in this cycle
		self.addorupgradedefenderaction = "" # Select Field Location, Upgrade Defender, Add Soldier, Add Archer etc

		# Specifies whether the game is in "select location", "add defender" or "upgrade defender" mode
		self.addorupgradedefendermode = "" # Select, Add, Upgrade

		# Specifies what would happen if the user clicked at the current field hover location
		self.addorupgradedefenderavailability = "Disabled" # Disabled, Add, Upgrade

		# Initialise game
		self.initialisegame()

		# Hover overlay offset & size - For display purpose only
		self.selectiondisplaysize = Vector.createfromvalues(64, 72)
		self.selectiondisplayoffset = Vector.createfromvalues(-16, -40)



	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Interprets input events for this cycle, setting flags that will
	# be read and interpreted by other methods later in the same cycle
	# Returns number of coins to spend, for any costly actions performed
	# -------------------------------------------------------------------

	def processinput(self, field):

		# Default the current cycle to NOT attempt to add/upgrade a defender to the field
		self.addorupgradedefenderaction = ""

		# By default, there ar eno coins to spend
		coinstolose = 0

		# Loop over all events logged in this cycle
		for event in GUI.event.get():

			# Set quit game status if user closes the application window
			if event.type == GUI.QUIT:
				self.quitstate = True

			# Only process if the user releases the mouse button, or moves the mouse cursor
			elif (event.type == GUI.MOUSEBUTTONUP) or (event.type == GUI.MOUSEMOTION):

				# Get pixel coordinates of mouse cursor, and button name of hover location (if any)
				self.updatecurrentmouselocation(GUI.mouse.get_pos())

				# Mouse Click only events
				if event.type == GUI.MOUSEBUTTONUP:
					coinstolose = self.processbuttonclicks()

				# Mouse Click OR Movement events, only apply when in field select mode
				if self.shouldfieldselectionbeupdated() == True:
					self.updatefieldselectionlocation(field)

			else:
				pass
			# print "Unknown Event"

		return coinstolose


	# -------------------------------------------------------------------
	# Process button clicks, return any cost
	# -------------------------------------------------------------------

	def processbuttonclicks(self):

		coinstolose = 0

		# If StartWave button is pressed, clear the between waves state
		if self.currenthoverbutton == "Start Wave":
			self.playnextlevel()

		# If Fast button is pressed, set game state to run in fast mode
		elif self.currenthoverbutton == "Speed - Fast":
			self.gofast()

		# If Slow button is pressed, set game state to run in slow mode
		elif self.currenthoverbutton == "Speed - Slow":
			self.goslow()

		# If Stop button is pressed, set game state to paused
		elif self.currenthoverbutton == "Speed - Stop":
			self.pauselevel()

		# If Add Soldier/Archer button is pressed, complete the add defender action
		elif (self.currenthoverbutton[:6] == "Add - ") or (self.currenthoverbutton == "Upgrade Defender"):
			coinstolose = self.completeaddorupgradedefender()

		# If Cancel Soldier/Archer button is pressed, cancel defender add state
		elif self.currenthoverbutton == "Cancel":
			self.canceladdorupgradedefender()

		# If the field is clicked, invoke field click
		elif self.currenthoverbutton == "Field":
			self.clickfieldlocation()

		return coinstolose


	# -------------------------------------------------------------------
	# Updates the mouse position
	# -------------------------------------------------------------------

	def updatecurrentmouselocation(self, mouselocationpair):

		# Get pixel coordinates of mouse cursor
		self.mousehoverlocation = Vector.createfrompair(mouselocationpair)

		# Get button label, if any, of current mouse cursor location
		self.currenthoverbutton = self.buttons.gethoveringbutton(self.mousehoverlocation)



	# -------------------------------------------------------------------
	# Updates the mouse field selection pixel co-ordinates
	# -------------------------------------------------------------------

	def updatefieldselectionlocation(self, field):

		# If mouse is moved or clicked in field area, set fieldhoverlocation to be pixel location
		if self.currenthoverbutton == "Field":
			self.fieldhoverlocation = field.calculatefieldselectionlocation(self.mousehoverlocation)

		# If mouse is moved or clicked outside field area, set fieldhoverlocation to be dummy off field location
		else:
			self.fieldhoverlocation = Vector.createblank()



	# -------------------------------------------------------------------
	# Sets game to slow mode
	# -------------------------------------------------------------------

	def goslow(self):

		# Sets game to slow
		self.gamefast = False

		# Start the game (moving enemies and defenders) and cancel field selection mode
		self.go()

		# Update Go/Stop button states
		self.buttons.setspeedgroup("Speed - Slow")



	# -------------------------------------------------------------------
	# Sets game to fast mode
	# -------------------------------------------------------------------

	def gofast(self):

		# Sets game to slow
		self.gamefast = True

		# Start the game (moving enemies and defenders) and cancel field selection mode
		self.go()

		# Update Go/Stop button states
		self.buttons.setspeedgroup("Speed - Fast")



	# -------------------------------------------------------------------
	# Sets game to go
	# -------------------------------------------------------------------

	def go(self):

		# Start the game (moving enemies and defenders)
		self.runstate = True

		# Cancel Field selection mode
		self.disablefieldselectionmode()



	# -------------------------------------------------------------------
	# Disable play
	# -------------------------------------------------------------------

	def disableplay(self):

		# Update button states
		self.buttons.setspeedgroup("Disabled")



	# -------------------------------------------------------------------
	# Sets Add Defender Mode
	# -------------------------------------------------------------------

	def invokeadddefender(self, userscoins):

		# Cancel Field selection mode
		self.disablefieldselectionmode()

		# Disable play
		self.disableplay()

		# Set Add defender mode
		self.addorupgradedefendermode = "Add"

		# Update button states
		self.buttons.setadddefendergroup("Enable", userscoins)



	# -------------------------------------------------------------------
	# Completes Add Defender Mode, when a defender type is chosen
	# by the user. Returns the cost of adding the defender
	# -------------------------------------------------------------------

	def completeaddorupgradedefender(self):

		# Set "Add DefenderType" or "Upgrade Defender" outcome
		self.addorupgradedefenderaction = self.currenthoverbutton

		# Cancel Add/Upgrade defender mode and update button states
		self.canceladdorupgradedefender()

		# Return the cost of adding the defender
		return self.buttons.getbuttoncost(self.currenthoverbutton)



	# -------------------------------------------------------------------
	# Sets Upgrade Defender Mode
	# -------------------------------------------------------------------

	def invokeupgradedefender(self, usercoins, upgradecost):

		# Cancel Field selection mode
		self.disablefieldselectionmode()

		# Disable play
		self.disableplay()

		# Set Upgrade defender mode
		self.addorupgradedefendermode = "Upgrade"

		# Update button states
		self.buttons.setupgradecost(upgradecost)
		self.buttons.setupgradedefendergroup("Enable", usercoins)



	# -------------------------------------------------------------------
	# Resets Add/Upgrade Defender Mode
	# -------------------------------------------------------------------

	def canceladdorupgradedefender(self):

		# Clear add/upgrade mode
		self.addorupgradedefendermode = ""

		# Update button states
		self.pauselevel()
		self.buttons.setadddefendergroup("Hide", -999)
		self.buttons.setupgradedefendergroup("Hide", -999)



	# -------------------------------------------------------------------
	# Select field location to add or upgrade new defender
	# -------------------------------------------------------------------

	def clickfieldlocation(self):

		# Set "User Selected point on Field" outcome
		self.addorupgradedefenderaction = "Select Field Location"



	# -------------------------------------------------------------------
	# Pauses the game
	# -------------------------------------------------------------------

	def pauselevel(self):

		# Stop the game (moving enemies and defenders)
		self.runstate = False

		# Turn on field selection mode
		self.enablefieldselectionmode()

		# Update button states
		self.buttons.setspeedgroup("Speed - Stop")



	# -------------------------------------------------------------------
	# Sets the game to "between waves" mode, and pauses the game
	# -------------------------------------------------------------------

	def startnextlevel(self):

		# Stop the game (moving enemies and defenders)
		self.runstate = False

		# Start inbetween wave mode
		self.betweenwavesmode = True

		# Disable play
		self.disableplay()

		# Update button states
		self.buttons.enablebutton("Start Wave")



	# -------------------------------------------------------------------
	# Exits "between waves" mode
	# -------------------------------------------------------------------

	def playnextlevel(self):

		# Finish inbetween wave mode
		self.betweenwavesmode = False

		# Update button states and game run mode
		self.pauselevel()

		# Update button states
		self.buttons.hidebutton("Start Wave")



	# -------------------------------------------------------------------
	# Initialise Controls for new game
	# -------------------------------------------------------------------

	def initialisegame(self):

		# Stop the game and start inbetween wave mode
		self.startnextlevel()



	# -------------------------------------------------------------------
	# When user has is hovering, determine whether
	# the hover should be add or upgrade defender
	# -------------------------------------------------------------------

	def updateselection(self, field, defenderarmy):

		# If it's possible to add a defender
		if field.isselectionvalidtoadddefender() == True:
			self.addorupgradedefenderavailability = "Add"

		# If the current selection properly overlaps an existing defender
		elif defenderarmy.getselecteddefender() is not None:
			self.addorupgradedefenderavailability = "Upgrade"

		# None mode
		else:
			self.addorupgradedefenderavailability = "Disabled"



	# -------------------------------------------------------------------
	# When user has clicked field, determine whether it should be add
	# or upgrade defender, and invoke the correct mode
	# -------------------------------------------------------------------

	def invokeaddorupgradedefender(self, game, defenderarmy):

		if self.addorupgradedefenderaction == "Select Field Location":

			# If it's possible to add a defender, put the game into add defender mode
			if self.addorupgradedefenderavailability == "Add":
				self.invokeadddefender(game.getcoincount())

			# If the current selection properly overlaps an existing defender, put the game into upgrade defender mode
			elif self.addorupgradedefenderavailability == "Upgrade":
				self.invokeupgradedefender(game.getcoincount(), defenderarmy.getdefenderupgradecost())



	# -------------------------------------------------------------------
	# In the correct mode, user should be able to hover and select
	# on the game field
	# -------------------------------------------------------------------

	def enablefieldselectionmode(self):

		# Turn on field button-area
		self.buttons.enablebutton("Field")

		# Set field selection mode
		self.addorupgradedefendermode = "Select"



	# -------------------------------------------------------------------
	# In the correct mode, user should NOT be able to hover and select
	# on the game field
	# -------------------------------------------------------------------

	def disablefieldselectionmode(self):

		# Turn on field button-area
		self.buttons.hidebutton("Field")

		# Set field selection mode
		self.addorupgradedefendermode = ""



	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Returns the State of the button
	# -------------------------------------------------------------------

	def getbuttonhoverstate(self, buttonname):

		if buttonname == self.currenthoverbutton:
			outcome = True
		else:
			outcome = False

		return outcome



	# -------------------------------------------------------------------
	# Returns the pixel co-ordinates of the cursor within the field
	# -------------------------------------------------------------------

	def getfieldselectionlocation(self):

		return self.fieldhoverlocation



	# -------------------------------------------------------------------
	# Returns the game speed
	# -------------------------------------------------------------------

	def getdisplayallframes(self):

		# Display all frames if the game is set to SLOW or the game is paused
		if (self.gamefast == False) or (self.runstate == False):
			outcome = True

		# Display only some frames if the game is set to FAST and the game is not paused
		else:
			outcome = False

		# Returns whether to display all frames or not
		return outcome



	# -------------------------------------------------------------------
	# Returns whether the wave should run (i.e. actors should animate)
	# -------------------------------------------------------------------

	def getprocesswavestate(self):

		return self.runstate



	# -------------------------------------------------------------------
	# Returns whether the game is between waves
	# -------------------------------------------------------------------

	def getbetweenwavestate(self):

		return self.betweenwavesmode



	# -------------------------------------------------------------------
	# Returns whether the user has requested to add or upgrade a defender
	# -------------------------------------------------------------------

	def getaddorupgradedefenderaction(self):

		return self.addorupgradedefenderaction



	# -------------------------------------------------------------------
	# Returns whether the field hover overlay should be
	# Add, Upgrade or Disabled (or None)
	# -------------------------------------------------------------------

	def getfieldselectionoverlay(self):

		if self.fieldhoverlocation.getx() < -1:
			outcome = ""
		else:
			outcome = self.addorupgradedefenderavailability

		return outcome



	# -------------------------------------------------------------------
	# Returns whether the user has requested the application to end
	# -------------------------------------------------------------------

	def getquitstate(self):

		return self.quitstate



	# -------------------------------------------------------------------
	# Returns whether the field selection should be updated
	# on the field and defender objects
	# -------------------------------------------------------------------

	def shouldfieldselectionbeupdated(self):

		# If the game is in select mode, and the user hasn't just clicked add/upgrade
		if (self.addorupgradedefendermode == "Select") and (self.addorupgradedefenderaction == ""):
			outcome = True
		else:
			outcome = False

		return outcome



	# -------------------------------------------------------------------
	# Returns what mode the mouse is in
	# -------------------------------------------------------------------

	def getcurrentaddorupgrademode(self):

		return self.addorupgradedefendermode



#	# -------------------------------------------------------------------
#	# Returns what the outcome of pressing the
#	# current add or upgrade button would be
#	# -------------------------------------------------------------------
#
#	def getcurrenthoverdefenderbutton(self):
#
#		outcome = ""
#		if self.addorupgradedefendermode == "Add":
#			if self.currenthoverbutton[:3] == "Add":
#				outcome = self.currenthoverbutton
#		elif self.addorupgradedefendermode == "Upgrade":
#			if self.currenthoverbutton == "Upgrade Defender":
#				outcome = "Upgrade"
#
#		return outcome



	# -------------------------------------------------------------------
	# Return field selection display location
	# -------------------------------------------------------------------

	def getselectiondisplaylocation(self):
		# Offset the pixel location to ensure the ground is in the right place
		return Vector.add(self.fieldhoverlocation, self.selectiondisplayoffset)



	# -------------------------------------------------------------------
	# Return field selection display size
	# -------------------------------------------------------------------

	def getselectiondisplaysize(self):
		# pixel size of display image, for erase purposes
		return self.selectiondisplaysize



