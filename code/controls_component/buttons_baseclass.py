from ..common_components.appinput_framework import appinput_module as AppInput
from ..common_components.vector_datatype import vector_module as Vector



class DefineButtons:

	# ==========================================================================================
	# Object Setup
	# ==========================================================================================


	def __init__(self, field):

		# Initialises the pygame input controller
		self.inputobject = AppInput.createappinput()

		# Sets up the buttons
		self.setupbuttons(field)



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
	# Update Add/Upgrade/Cancel buttons
	# -------------------------------------------------------------------

	def updatemanagedefenderbuttons(self, managemode, game, defenderarmy):

		# Add Defender Buttons
		if managemode == "Add":
			for defendertype in ["Soldier", "Archer", "Wizard", "Theif"]:
				if defenderarmy.getnewdefendercost(defendertype) > game.getcoincount():
					self.inputobject.setareastate("Add - " + defendertype, "Disabled")
				else:
					self.inputobject.setareastate("Add - " + defendertype, "Enabled")

		# Upgrade Defender Buttons
		elif managemode == "Upgrade":
			if defenderarmy.getdefenderupgradecost() > game.getcoincount():
				self.inputobject.setareastate("Upgrade Defender", "Disabled")
			else:
				self.inputobject.setareastate("Upgrade Defender", "Enabled")

		else:
			assert managemode == "Upgrade", "Unrecognised field-hover-mode"

		self.inputobject.setareastate("Cancel", "Enabled")


	# -------------------------------------------------------------------
	# Update buttons
	# -------------------------------------------------------------------

	def updatebutton(self, buttonname, buttonstate):

		self.inputobject.setareastate(buttonname, buttonstate)




	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Returns the hover state of the button
	# -------------------------------------------------------------------

	def getbuttonhoverstate(self, buttonname):

		if buttonname == self.inputobject.getcurrentmousearea():
			outcome = True
		else:
			outcome = False

		return outcome



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

