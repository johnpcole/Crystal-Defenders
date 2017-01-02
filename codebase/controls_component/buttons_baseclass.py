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
		self.area = {}
		self.setupbuttons(field)

		# Manage Defender Overlay position
		self.managedefenderoverlayposition = Vector.createblank()



	def setupbuttons(self, field):

		fieldsize = field.getsize()
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

		self.inputobject.createarea(buttonname, Vector.createfromvalues(along, down),
															Vector.createfromvalues(width, height), groupmembership)





	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Update Manage Defender Overlay fauxbutton
	# -------------------------------------------------------------------

	def updatemanagedefenderoverlaylocation(self, newlocation):

		self.managedefenderoverlayposition.setfromvector(newlocation)



	# -------------------------------------------------------------------
	# Update Add/Upgrade/Cancel buttons
	# -------------------------------------------------------------------

	def updatemanagedefenderbuttons(self, managemode, game, defenderarmy):

		if managemode == "Add":
			buttonlist = ["Soldier", "Archer", "Wizard", "Cancel"]
		elif managemode == "Upgrade":
			buttonlist = ["Upgrade", "Cancel"]
		else:
			buttonlist = ["Cancel"]
			assert managemode == "Upgrade", "Unrecognised field-hover-mode"

		buttonoffset = -30

		for buttontype in buttonlist:

			if buttontype == "Cancel":
				buttonname = buttontype
				buttoncost = -999
			elif buttontype == "Upgrade":
				buttonname = "Upgrade Defender"
				buttoncost = defenderarmy.getdefenderupgradecost()
			else:
				buttonname = "Add - " + buttontype
				buttoncost = defenderarmy.getnewdefendercost(buttontype)

			buttonoffset = buttonoffset + 40
			self.updatemanagebuttonlocation(buttonname, buttonoffset)

			if buttoncost > game.getcoincount():
				newstate = "Disabled"
			else:
				newstate = "Enabled"
			self.inputobject.setareastate(buttonname, newstate)



	# -------------------------------------------------------------------
	# Update button states
	# -------------------------------------------------------------------

	def updatebutton(self, buttonname, buttonstate):

		self.inputobject.setareastate(buttonname, buttonstate)



	# -------------------------------------------------------------------
	# Update button positions
	# -------------------------------------------------------------------

	def updatemanagebuttonlocation(self, buttonname, offsetvalue):

		newbuttonlocation = Vector.createfromvalues(self.managedefenderoverlayposition.getx() + offsetvalue,
													self.managedefenderoverlayposition.gety() + 160)
		self.inputobject.setareadimensions(buttonname, newbuttonlocation,
																		self.inputobject.getareadimensions(buttonname))



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



	# -------------------------------------------------------------------
	# Returns the manage defender overlay position
	# -------------------------------------------------------------------

	def getmanagedefenderoverlayposition(self):

		return self.managedefenderoverlayposition

