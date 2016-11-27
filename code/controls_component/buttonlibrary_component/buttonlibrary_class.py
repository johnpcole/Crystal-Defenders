from button_subcomponent import DefineButton
from ...common_components import Vector



class DefineButtonLibrary:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self, field, defenderarmy):

		fieldsize = field.getsize()
		self.area = {}
		self.createbutton("Start Wave",          287, 380, 30, 30,                       0)
		self.createbutton("Speed - Stop",        625, 400, 30, 30,                       0)
		self.createbutton("Speed - Slow",   625 + 40, 400, 30, 30,                       0)
		self.createbutton("Speed - Fast",   625 + 80, 400, 30, 30,                       0)
		self.createbutton("Field",                 0,   0, fieldsize.getx(), fieldsize.gety(),     0)
		self.createbutton("Add - Soldier",       625, 450, 30, 30,        defenderarmy.getnewdefendercost("Soldier"))
		self.createbutton("Add - Archer",   625 + 40, 450, 30, 30,        defenderarmy.getnewdefendercost("Archer"))
		self.createbutton("Add - Wizard",   625 + 80, 450, 30, 30,        defenderarmy.getnewdefendercost("Wizard"))
		self.createbutton("Cancel",        625 + 120, 450, 30, 30,                       0)
		self.createbutton("Upgrade Defender",    625, 450, 30, 30,                       0)



	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	def createbutton(self, buttonname, buttonpositionx, buttonpositiony, buttondimensionsx, buttondimensionsy,
																										buttoncost):

		self.area[buttonname] = DefineButton(Vector.createfromvalues(buttonpositionx, buttonpositiony),
											Vector.createfromvalues(buttondimensionsx, buttondimensionsy), buttoncost)



	# -------------------------------------------------------------------
	# Sets button to Disabled, but Visible state
	# -------------------------------------------------------------------

	def disablebutton(self, buttonname):
		self.area[buttonname].state = "Disabled"



	# -------------------------------------------------------------------
	# Sets button to Enabled, and Visible state
	# -------------------------------------------------------------------

	def enablebutton(self, buttonname):
		self.area[buttonname].state = "Enabled"



	# -------------------------------------------------------------------
	# Sets button to Enabled or Disabled, depending on whether
	# user has enough coins
	# -------------------------------------------------------------------

	def conditionallyenablebutton(self, buttonname, coincount):
		if coincount >= self.area[buttonname].cost:
			self.area[buttonname].state = "Enabled"
		else:
			self.area[buttonname].state = "Disabled"



	# -------------------------------------------------------------------
	# Sets button to Hidden (and Disabled) state
	# -------------------------------------------------------------------

	def hidebutton(self, buttonname):
		self.area[buttonname].state = "Hidden"



	# -------------------------------------------------------------------
	# Sets the speed button group to desired state
	# -------------------------------------------------------------------

	def setspeedgroup(self, groupmode):

		for buttonname in ["Speed - Stop", "Speed - Fast", "Speed - Slow"]:
			if (groupmode == buttonname) or (groupmode == "Disabled"):
				self.disablebutton(buttonname)
			else:
				self.enablebutton(buttonname)



	# -------------------------------------------------------------------
	# Sets the add defender button group to desired state
	# -------------------------------------------------------------------

	def setadddefendergroup(self, groupmode, coins):

		for buttonname in ["Add - Soldier", "Add - Archer", "Add - Wizard", "Cancel"]:
			if groupmode == "Enable":
				self.conditionallyenablebutton(buttonname, coins)
			elif groupmode == "Disable":
				self.disablebutton(buttonname)
			else:
				self.hidebutton(buttonname)



	# -------------------------------------------------------------------
	# Sets the upgrade defender button group to desired state
	# -------------------------------------------------------------------

	def setupgradedefendergroup(self, groupmode, coins):

		for buttonname in ["Upgrade Defender", "Cancel"]:
			if groupmode == "Enable":
				self.conditionallyenablebutton(buttonname, coins)
			elif groupmode == "Disable":
				self.disablebutton(buttonname)
			else:
				self.hidebutton(buttonname)



	# -------------------------------------------------------------------
	# Sets the upgrade cost for the current defencer
	# -------------------------------------------------------------------

	def setupgradecost(self, coins):

		self.area["Upgrade Defender"].cost = coins




	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Returns actioned (click or hover) button label based
	# on mouse pixel co-ordinates and button states
	# -------------------------------------------------------------------

	def gethoveringbutton(self, mouselocation):
		# Defaults to return NO button has been clicked / hovered over
		outcome = ""

		# Loop over all buttons
		for currentbutton, currentdefinition in self.area.items():

			# Only process if the current button is enabled
			if currentdefinition.state == "Enabled":

				# Only process if the mouse pointer is within the boundaries of the current button
				if Vector.ispointinarea(mouselocation, currentdefinition.position, currentdefinition.dimensions):
					# Set the outcome to return the name of the button
					outcome = currentbutton

		# Return the name of the button (and role), if any, that is clicked / hovered
		return outcome



	# -------------------------------------------------------------------
	# Returns the State of the button
	# -------------------------------------------------------------------

	def getbuttonstate(self, buttonname):
		# The current state of the specified button
		return self.area[buttonname].state


	# -------------------------------------------------------------------
	# Returns the pixel co-ordinates of the button location on screen
	# -------------------------------------------------------------------

	def getbuttonlocation(self, buttonname):
		# The pixel location of the specified button
		return self.area[buttonname].position



	# -------------------------------------------------------------------
	# Returns the pixel dimensions of the button location on screen
	# -------------------------------------------------------------------

	def getbuttonsize(self, buttonname):
		# The pixel size of the specified button
		return self.area[buttonname].dimensions



	# -------------------------------------------------------------------
	# Returns the cost of the button
	# -------------------------------------------------------------------

	def getbuttoncost(self, buttonname):
		# The current state of the specified button
		return self.area[buttonname].cost



	# -------------------------------------------------------------------
	# Returns the list of "real" button names
	# -------------------------------------------------------------------

	def getbuttonlist(self):

		outcome = []
		for buttonname in self.area:
			if buttonname != "Field":
				outcome.append(buttonname)

		return outcome


