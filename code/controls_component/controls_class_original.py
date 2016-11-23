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

		# Initialise game
		self.startnextlevel()

		# Hover overlay offset & size - For display purpose only
		self.selectiondisplaysize = Vector.createfromvalues(64, 72)
		self.selectiondisplayoffset = Vector.createfromvalues(-16, -40)

		# Granularised hover location of the mouse on the field
		self.fieldhoverlocation = Vector.createblank()

		# Specifies what would happen if the user clicked at the current field hover location
		self.fieldhovermode = Enumeration.createenum(["Disabled", "Add", "Upgrade", "Unknown"], "Disabled")

		# Specifies what the user has done this cycle
		self.useraction = Enumeration.createenum(["None", "Click Field", "Upgrade Defender",
														"Add - Soldier", "Add - Archer", "Add - Wizard"], "None")



	def setupbuttons(self, field):

		fieldsize = field.getsize()
		self.area = {}
		self.definebutton("Start Wave",          287, 380, 30, 30, [])
		self.definebutton("Speed - Stop",        625, 400, 30, 30, ["Speed", "Non-Slow", "Non-Fast"])
		self.definebutton("Speed - Slow",   625 + 40, 400, 30, 30, ["Speed", "Non-Stop", "Non-Fast"])
		self.definebutton("Speed - Fast",   625 + 80, 400, 30, 30, ["Speed", "Non-Slow", "Non-Stop"])
		self.definebutton("Field",                 0,   0, fieldsize.getx(), fieldsize.gety(), [])
		self.definebutton("Add - Soldier",       625, 450, 30, 30, ["Manage-Defender"])
		self.definebutton("Add - Archer",   625 + 40, 450, 30, 30, ["Manage-Defender"])
		self.definebutton("Add - Wizard",   625 + 80, 450, 30, 30, ["Manage-Defender"])
		self.definebutton("Cancel",        625 + 120, 450, 30, 30, ["Manage-Defender"])
		self.definebutton("Upgrade Defender",    625, 450, 30, 30, ["Manage-Defender"])



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

	def processinput(self):

		# Loop over all events logged in this cycle and update all mouse properties
		self.inputobject.processinputs()

		# Default to no user action being specified
		self.useraction.set("None")

		if self.inputobject.getmouseaction() == True:
			if self.inputobject.getmouseclickaction() == -1:
				if self.inputobject.getcurrentmouseareastate() == "Enabled":
					clickedbutton = self.inputobject.getcurrentmousearea()

					# If StartWave button is pressed, clear the between waves state
					if clickedbutton == "Start Wave":
						self.playnextlevel()

					# If Fast/Slow/Stop button is pressed, set game state
					elif clickedbutton[:8] == "Speed - ":
						self.setgamespeed(clickedbutton[8:])

					# If Add Soldier/Archer button is pressed, complete the add defender action
					elif (clickedbutton[:6] == "Add - ") or (clickedbutton == "Upgrade Defender"):
						self.useraction.set(clickedbutton)

					# If Cancel Soldier/Archer button is pressed, cancel defender add state
					elif clickedbutton == "Cancel":
						self.cancelmanagedefender()

					# If the field is clicked, invoke field click
					elif clickedbutton == "Field":
						self.useraction.set("Click Field")



	# -------------------------------------------------------------------
	# Sets game to fast or slow or stop mode
	# -------------------------------------------------------------------

	def setgamespeed(self, speedlabel):

		if speedlabel == "Stop":
			self.runstate = False
			self.inputobject.setareastate("Field", "Enabled")
		elif speedlabel == "Disable":
			self.inputobject.setareastate("Speed", "Disabled")
		else:
			self.runstate = True
			self.inputobject.setareastate("Field", "Hidden")
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

		if self.useraction.get("Click Field") == True:

			# If it's possible to add a defender, put the game into add defender mode
			if (self.fieldhovermode.get("Add") == True) or (self.fieldhovermode.get("Upgrade") == True):

				# Disable play
				self.setgamespeed("Disable")

				# Disable Field selection
				self.inputobject.setareastate("Field", "Hidden")

				# Update button states
				self.showmanagebuttons(game, defenderarmy)



	# -------------------------------------------------------------------
	# Completes Add Defender Mode, when a defender type is chosen
	# by the user. Returns the cost of adding the defender
	# -------------------------------------------------------------------

	def showmanagebuttons(self, game, defenderarmy):

		# Add Defender Buttons
		if self.fieldhovermode.get("Add") == True:
			for defendertype in ["Soldier", "Archer", "Wizard", "Theif"]:
				if defenderarmy.getnewdefendercost(defendertype) > game.getcoincount():
					self.inputobject.setareastate("Add - " + defendertype, "Disabled")
				else:
					self.inputobject.setareastate("Add - " + defendertype, "Enabled")

		# Upgrade Defender Buttons
		elif self.fieldhovermode.get("Upgrade") == True:
			if defenderarmy.getdefenderupgradecost() > game.getcoincount():
				self.inputobject.setareastate("Upgrade Defender", "Disabled")
			else:
				self.inputobject.setareastate("Upgrade Defender", "Enabled")

		else:
			x = 1/0

		self.inputobject.setareastate("Cancel", "Enabled")



	# -------------------------------------------------------------------
	# Resets Add/Upgrade Defender Mode
	# -------------------------------------------------------------------

	def cancelmanagedefender(self):

		# Update button states
		self.setgamespeed("Stop")

		# Reset buttons to Hidden
		self.inputobject.setareastate("Manage-Defender", "Hidden")

		# Restores field selection mode
		self.inputobject.setareastate("Field", "Enabled")



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
	# Returns whether the field selection should be updated
	# on the field and defender objects
	# -------------------------------------------------------------------

	def updatefieldselectionlocation(self, field):

		# If the field is enabled
		if self.inputobject.getareastate("Field") == "Enabled":
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



	# -------------------------------------------------------------------
	# When user has is hovering, determine whether
	# the hover should be add or upgrade defender
	# -------------------------------------------------------------------

	def updatefieldselectionmode(self, field, defenderarmy):

		# If it's possible to add a defender
		if field.isselectionvalidtoadddefender() == True:
			self.fieldhovermode.set("Add")

		# If the current selection properly overlaps an existing defender
		elif defenderarmy.getselecteddefender() is not None:
			self.fieldhovermode.set("Upgrade")

		# None mode
		else:
			self.fieldhovermode.set("Disabled")



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

		return self.useraction.displaycurrent()



	# -------------------------------------------------------------------
	# Returns whether the field hover overlay should be
	# Add, Upgrade or Disabled (or None)
	# -------------------------------------------------------------------

	def getfieldselectionoverlay(self):

		if self.inputobject.getcurrentmousearea() == "Field":
			outcome = self.fieldhovermode.displaycurrent()
		else:
			outcome = ""

		return outcome



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
	# Returns the button's state
	# -------------------------------------------------------------------

	def getbuttonstate(self, buttonname):

		return self.inputobject.getareastate(buttonname)



	# -------------------------------------------------------------------
	# Returns the button's position
	# -------------------------------------------------------------------

	def getbuttonposition(self, buttonname):
		return self.inputobject.getareaposition(buttonname)



	# -------------------------------------------------------------------
	# Returns the button's size
	# -------------------------------------------------------------------

	def getbuttonsize(self, buttonname):

		return self.inputobject.getareadimensions(buttonname)

