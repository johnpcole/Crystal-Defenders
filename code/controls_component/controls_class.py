from ..common_components.appinput_framework import appinput_module as AppInput
from ..common_components.vector_datatype import vector_module as Vector
from ..common_components.enumeration_datatype import enumeration_module as Enumeration


class DefineController:

	# ==========================================================================================
	# Object Setup
	# ==========================================================================================


	def __init__(self, field):

		# Initialises the pygame input controller
		self.inputobject = AppInput.createappinput()

		# Sets up the buttons
		self.setupbuttons(field)

		# Specifies whether the game should "run" - enemies walk and defenders walk/combat, in this cycle
		self.runstate = True

		# Specifies whether the user has requested to close the application in this cycle
		self.quitstate = False

		# Game speed
		self.gamefast = False

		# Specifies whether the game is "between waves" mode
		self.betweenwavesmode = False

		# Specifies whether the field or add/upgrade defender buttons have been clicked in this cycle
		self.managedefenderaction = Enumeration.createenum(["None", "Select Field Location", "Upgrade Defender",
															"Add Soldier", "Add Archer", "Add Wizard"], "None")

		# Specifies whether the game is in "select location", "add defender" or "upgrade defender" mode
		self.managedefendermode = Enumeration.createenum(["None", "Select", "Add", "Upgrade"], "None")

		# Specifies what would happen if the user clicked at the current field hover location
		self.managedefenderavailability = Enumeration.createenum(["Disabled", "Add", "Upgrade"], "Disabled")

		# Initialise game
		self.startnextlevel()

		# Hover overlay offset & size - For display purpose only
		self.selectiondisplaysize = Vector.createfromvalues(64, 72)
		self.selectiondisplayoffset = Vector.createfromvalues(-16, -40)

		# Granularised hover location of the mouse on the field
		self.fieldhoverlocation = Vector.createblank()



	def setupbuttons(self, field):

#----------------------------------------------------------------------------------------------------------

		fieldsize = field.getsize()
		self.area = {}
		self.definebutton("Start Wave",          287, 380, 30, 30, [])
		self.definebutton("Speed - Stop",        625, 400, 30, 30, ["Speed", "Non-Slow", "Non-Fast"])
		self.definebutton("Speed - Slow",   625 + 40, 400, 30, 30, ["Speed", "Non-Stop", "Non-Fast"])
		self.definebutton("Speed - Fast",   625 + 80, 400, 30, 30, ["Speed", "Non-Slow", "Non-Stop"])
		self.definebutton("Field",                 0,   0, fieldsize.getx(), fieldsize.gety(), [])
		self.definebutton("Add - Soldier",       625, 450, 30, 30, ["Add-Defender"])
		self.definebutton("Add - Archer",   625 + 40, 450, 30, 30, ["Add-Defender"])
		self.definebutton("Add - Wizard",   625 + 80, 450, 30, 30, ["Add-Defender"])
		self.definebutton("Cancel",        625 + 120, 450, 30, 30, ["Add-Defender", "Upgrade-Defender"])
		self.definebutton("Upgrade Defender",    625, 450, 30, 30, ["Upgrade-Defender"])

#----------------------------------------------------------------------------------------------------------



	def definebutton(self, buttonname, along, down, width, height, groupmembership):

		self.inputobject.createarea(buttonname, Vector.createfromvalues(along, down), Vector.createfromvalues(width, height), groupmembership)





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
		self.managedefenderaction.set("None")

		# Loop over all events logged in this cycle and update all mouse properties
		self.inputobject.processinputs()

		# If the user releases the mouse button, process click actions
		coinstolose = self.processbuttonclicks()

		# for event in GUI.event.get():
		#
		# 	# Set quit game status if user closes the application window
		# 	if event.type == GUI.QUIT:
		# 		self.quitstate = True
		#
		# 	# Only process if the user releases the mouse button, or moves the mouse cursor
		# 	elif (event.type == GUI.MOUSEBUTTONUP) or (event.type == GUI.MOUSEMOTION):
		#
		# 		# Get pixel coordinates of mouse cursor, and button name of hover location (if any)
		# 		self.updatecurrentmouselocation(GUI.mouse.get_pos())
		#
		# 		# Mouse Click only events
		# 		if event.type == GUI.MOUSEBUTTONUP:
		# 			coinstolose = self.processbuttonclicks()
		#
		# 		# Mouse Click OR Movement events, only apply when in field select mode
		# 		if self.shouldfieldselectionbeupdated() == True:
		# 			self.updatefieldselectionlocation(field)
		#
		# 	else:
		# 		pass
		# 	# print "Unknown Event"

		return coinstolose



	# -------------------------------------------------------------------
	# Process button clicks, return any cost
	# -------------------------------------------------------------------

	def processbuttonclicks(self):

		coinstolose = 0

		if self.inputobject.getmouseaction() == True:
			if self.inputobject.getmouseclickaction() == -1:
				if self.inputobject.getcurrentmouseareastate() == "Enabled":
					clickedbutton = self.inputobject.getcurrentmousearea()

					# If StartWave button is pressed, clear the between waves state
					if clickedbutton == "Start Wave":
						self.playnextlevel()

					# If Fast button is pressed, set game state to run in fast mode
					# If Slow button is pressed, set game state to run in slow mode
					# If Stop button is pressed, set game state to paused
					elif clickedbutton[:8] == "Speed - ":
						self.setgamespeed(clickedbutton[8:])

					# If Add Soldier/Archer button is pressed, complete the add defender action
					elif (clickedbutton[:6] == "Add - ") or (clickedbutton == "Upgrade Defender"):
						coinstolose = self.completemanagedefender()

					# If Cancel Soldier/Archer button is pressed, cancel defender add state
					elif clickedbutton == "Cancel":
						self.cancelmanagedefender()

					# If the field is clicked, invoke field click
					elif clickedbutton == "Field":
						self.clickfieldlocation()

		return coinstolose



	# -------------------------------------------------------------------
	# Sets game to fast or slow or stop mode
	# -------------------------------------------------------------------

	def setgamespeed(self, speedlabel):

		if speedlabel == "Stop":
			self.runstate = False
			self.changefieldselectionmode("Enable")
		elif speedlabel == "Disable":
			self.inputobject.setareastate("Speed", "Disabled")
		else:
			self.runstate = True
			self.changefieldselectionmode("Disable")
			if speedlabel == "Fast":
				self.gamefast = True
			else:
				self.gamefast = False

		# Update Go/Stop button states
		self.inputobject.setareastate("Speed - " + speedlabel, "Disabled")
		self.inputobject.setareastate("Non-" + speedlabel, "Enabled")



	# -------------------------------------------------------------------
	# When user has clicked field, determine whether it should be add
	# or upgrade defender, and invoke the correct mode
	# -------------------------------------------------------------------

	def invokemanagedefender(self, game, defenderarmy):

		if self.managedefenderaction.get("Select Field Location") == True:

			# If it's possible to add a defender, put the game into add defender mode
			if (self.managedefenderavailability.get("Add") == True) or (self.managedefenderavailability.get("Upgrade") == True):

				# Cancel Field selection mode
				self.changefieldselectionmode("Disable")

				# Disable play
				self.setgamespeed("Disable")

				# Put the game into upgrade or add mode
				self.managedefendermode.set(self.managedefenderavailability.displaycurrent())

				# Update button states
			# self.buttons.setadddefendergroup("Enable", userscoins) !!!!!!!
					# OR
			# self.buttons.setupgradecost(upgradecost) !!!!!!!!!!
			# self.buttons.setupgradedefendergroup("Enable", usercoins) !!!!!!!!!!!!!



	# -------------------------------------------------------------------
	# Completes Add Defender Mode, when a defender type is chosen
	# by the user. Returns the cost of adding the defender
	# -------------------------------------------------------------------

	def completemanagedefender(self):

		# Set "Add DefenderType" or "Upgrade Defender" outcome
		self.managedefenderaction.set(self.inputobject.getcurrentmousearea())

		# Cancel Add/Upgrade defender mode and update button states
		self.cancelmanagedefender()

		# Return the cost of adding the defender
		#return self.buttons.getbuttoncost(self.currenthoverbutton) !!!!!!!




	# -------------------------------------------------------------------
	# Resets Add/Upgrade Defender Mode
	# -------------------------------------------------------------------

	def cancelmanagedefender(self):

		# Clear add/upgrade mode
		self.managedefendermode.set("None")

		# Update button states
		self.setgamespeed("Stop")
		#self.buttons.setadddefendergroup("Hide", -999) !!!!!!!!!!!!!!!!!
		#self.buttons.setupgradedefendergroup("Hide", -999) !!!!!!!!!!!!!



	# -------------------------------------------------------------------
	# Select field location to add or upgrade new defender
	# -------------------------------------------------------------------

	def clickfieldlocation(self):

		# Set "User Selected point on Field" outcome
		self.managedefenderaction.set("Select Field Location")



	# -------------------------------------------------------------------
	# Sets the game to "between waves" mode, and pauses the game
	# -------------------------------------------------------------------

	def startnextlevel(self):

		# Stop the game (moving enemies and defenders)
		self.runstate = False

		# Start inbetween wave mode
		self.betweenwavesmode = True

		# Disable play
		self.setgamespeed("Disable")

		# Update button states
		self.inputobject.setareastate("Start Wave", "Enabled")



	# -------------------------------------------------------------------
	# Exits "between waves" mode
	# -------------------------------------------------------------------

	def playnextlevel(self):

		# Finish inbetween wave mode
		self.betweenwavesmode = False

		# Update button states and game run mode
		self.setgamespeed("Stop")

		# Update button states
		self.inputobject.setareastate("Start Wave", "Hidden")



	# -------------------------------------------------------------------
	# When user has is hovering, determine whether
	# the hover should be add or upgrade defender
	# -------------------------------------------------------------------

	def updateselectiontype(self, field, defenderarmy):

		# If it's possible to add a defender
		if field.isselectionvalidtoadddefender() == True:
			self.managedefenderavailability.set("Add")

		# If the current selection properly overlaps an existing defender
		elif defenderarmy.getselecteddefender() is not None:
			self.managedefenderavailability.set("Upgrade")

		# None mode
		else:
			self.managedefenderavailability.set("Disabled")



	# -------------------------------------------------------------------
	# In the correct mode, user should be able to hover and select
	# on the game field
	# -------------------------------------------------------------------

	def changefieldselectionmode(self, modelabel):

		# Turn on field button-area
		self.inputobject.setareastate("Field", modelabel + "d")

		# Set field selection mode
		if modelabel == "Enable":
			self.managedefendermode.set("Select")
		else:
			self.managedefendermode.set("None")



	# -------------------------------------------------------------------
	# Returns whether the field selection should be updated
	# on the field and defender objects
	# -------------------------------------------------------------------

	def updatefieldselection(self, field):

		# If the game is in select mode, and the user hasn't just clicked add/upgrade
		if (self.managedefendermode.get("Select") == True) and (self.managedefenderaction.get("None") == True):
			outcome = True

			# If mouse is in field area, set fieldblocklocation to be granularised pixel location
			if self.inputobject.getcurrentmousearea() == "Field":
				self.fieldhoverlocation = field.calculatefieldselectionlocation(self.inputobject.getmouselocation())

			# If mouse is outside field area, set fieldhoverlocation to be dummy off field location
			else:
				self.fieldhoverlocation = Vector.createblank()

		else:
			outcome = False

		return outcome


	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Returns the State of the button
	# -------------------------------------------------------------------

	def getbuttonhoverstate(self, buttonname):

		if buttonname == self.inputobject.getcurrentmousearea():
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

	def getmanagedefenderaction(self):

		return self.managedefenderaction.displaycurrent()



	# -------------------------------------------------------------------
	# Returns whether the field hover overlay should be
	# Add, Upgrade or Disabled (or None)
	# -------------------------------------------------------------------

	def getfieldselectionoverlay(self):

		hoverlocation = self.inputobject.getmouselocation()
		if hoverlocation.getx() < -1:
			outcome = ""
		else:
			outcome = self.managedefenderavailability.displaycurrent()

		return outcome



	# -------------------------------------------------------------------
	# Returns what mode the mouse is in
	# -------------------------------------------------------------------

	def getcurrentaddorupgrademode(self):

		return self.managedefendermode.displaycurrent()

	#	# -------------------------------------------------------------------
	#	# Returns what the outcome of pressing the
	#	# current add or upgrade button would be
	#	# -------------------------------------------------------------------
	#
	#	def getcurrenthoverdefenderbutton(self):
	#
	#		outcome = ""
	#		if self.managedefendermode.get("Add") == True:
	#			if self.currenthoverbutton[:3] == "Add":
	#				outcome = self.currenthoverbutton
	#		elif self.managedefendermode.get("Upgrade") == True:
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



	# -------------------------------------------------------------------
	# Returns whether the user has requested the application to end
	# -------------------------------------------------------------------

	def getquitstate(self):

		return self.inputobject.getquitstate()



	# -------------------------------------------------------------------
	# Returns the set of buttons in a group
	# -------------------------------------------------------------------

	def getbuttoncollection(self, groupname):

		return self.inputobject.getbuttoncollection(groupname)



	# -------------------------------------------------------------------
	# Returns the actual button object for the specified button name
	# -------------------------------------------------------------------

	def getbuttonobject(self, buttonname):

		return self.inputobject.getbuttonobject(buttonname)
