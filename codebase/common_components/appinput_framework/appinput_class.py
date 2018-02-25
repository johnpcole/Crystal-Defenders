from button_subcomponent import button_module as Button
from ..vector_datatype import vector_module as Vector
from ..userinterface_framework import userinterface_module as GUI



class DefineApplicationInput:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self):

		self.buttons = {}

		self.quitstate = False

		# The location the mouse is positioned at
		# regardless of mouse click state
		self.mouselocation = Vector.createfromvalues(-999, -999)

		# The current button/area that the mouse location is positioned over
		# regardless of mouse click state - requires button to be enabled or disabled
		self.mousecurrentbutton = ""

		# Flag to indicate if rest of application needs to process changes
		# to the mouse
		self.mouseaction = False

		# Flag to indicate the current state of the mouse - 1) Press, -1) Release, 0) Drag & Move
		self.mouseclickaction = 0
		


	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Interprets input events for this cycle
	# -------------------------------------------------------------------

	def processinputs(self):

		# Default to there being no mouse actions in this cycle
		self.preparemouse()

		# Loop over all events logged in this cycle
		for event in GUI.event.get():

			# Set quit game status if user closes the application window
			self.processquit(event)

			# Process keyboard actions
			#self.processkey(event)

			# Process mouse actions
			self.processmouse(event)



		return 0



	# -------------------------------------------------------------------
	# Process quit
	# -------------------------------------------------------------------

	def processquit(self, event):

		# Set quit game status if user closes the application window
		if event.type == GUI.QUIT:
			self.quitstate = True



	# -------------------------------------------------------------------
	# Process keyboard
	# -------------------------------------------------------------------

	def processkey(self, event):

		if event.type == GUI.KEYDOWN:
			action = "Press"
		elif event.type == GUI.KEYUP:
			action = "Release"
		else:
			action = "None"

		if action != "None":
			keyname = event.key
			keylabel = keyname[2:]
			if keylabel[:2] == "KP":
				keylabel = keylabel[2:]
			if keylabel[:1] == "_":
				keylabel = keylabel[1:]
			keylabel.upper()

			#UNFINISHED!



	# -------------------------------------------------------------------
	# Prepare Mouse states for this cycle
	# -------------------------------------------------------------------

	def preparemouse(self):

		self.mouseaction = False
		self.mouseclickaction = 0



	# -------------------------------------------------------------------
	# Process mouse
	# -------------------------------------------------------------------

	def processmouse(self, event):

		# Determine what kind of mouse action has occurred
		if event.type == GUI.MOUSEMOTION:
			action = "Move"
		elif event.type == GUI.MOUSEBUTTONDOWN:
			action = "Press"
			self.mouseclickaction = +1
		elif event.type == GUI.MOUSEBUTTONUP:
			action = "Release"
			self.mouseclickaction = -1
		else:
			action = "None"

		if action != "None":
			self.updatemouseposition(event.pos)
			self.mouseaction = True



	# -------------------------------------------------------------------
	# Update mouse position and current hover button - INTERNAL FUNCTION ONLY
	# -------------------------------------------------------------------

	def updatemouseposition(self, locationpair):

		self.mouselocation = Vector.createfrompair(locationpair)
		self.mousecurrentbutton = self.calculatecurrentmousebutton()



	# -------------------------------------------------------------------
	# Set button or buttongroup state
	# -------------------------------------------------------------------

	def setareastate(self, buttonname, newstate):

		if newstate in ["Enabled", "Disabled", "Hidden"]:

			if buttonname in self.buttons:
				self.buttons[buttonname].changestate(newstate)
			else:
				for individualbuttonname in self.buttons.keys():
					self.buttons[individualbuttonname].changegroupstate(buttonname, newstate)

		else:

			print "Invalid button state - ", newstate


	# -------------------------------------------------------------------
	# Set button dimensions
	# -------------------------------------------------------------------

	def setareadimensions(self, buttonname, newposition, newdimensions):

		if buttonname in self.buttons:
			self.buttons[buttonname].changeboundary(newposition, newdimensions)
		else:
			print "Invalid button name - ", buttonname



	# -------------------------------------------------------------------
	# Add a button
	# -------------------------------------------------------------------

	def createarea(self, buttonname, buttonposition, buttondimensions, buttongroupmembership):

		if buttonname in self.buttons:
			print "Duplicate button name - ", buttonname
		else:
			self.buttons[buttonname] = Button.createbutton(buttonposition, buttondimensions, buttongroupmembership)



	# -------------------------------------------------------------------
	# Forces quit
	# -------------------------------------------------------------------

	def forcequit(self):

		self.quitstate = True



	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Returns whether the user has requested the application to end
	# -------------------------------------------------------------------

	def getquitstate(self):

		return self.quitstate



	# -------------------------------------------------------------------
	# Returns which button the mouse is currently over
	# -------------------------------------------------------------------

	def getcurrentmousearea(self):

		return self.mousecurrentbutton



	# -------------------------------------------------------------------
	# Returns the state of the button the mouse is currently over
	# -------------------------------------------------------------------

	def getcurrentmouseareastate(self):

		if self.mousecurrentbutton == "":
			outcome = ""
		else:
			outcome = self.buttons[self.mousecurrentbutton].getstate()
		
		return outcome



	# -------------------------------------------------------------------
	# Returns whether a mouse action has occurred
	# -------------------------------------------------------------------

	def getmouseaction(self):

		return self.mouseaction



	# -------------------------------------------------------------------
	# Returns what the current mouse state is
	# -------------------------------------------------------------------

	def getmouseclickaction(self):

		return self.mouseclickaction



	# -------------------------------------------------------------------
	# Returns the location of the mouse
	# -------------------------------------------------------------------

	def getmouselocation(self):

		return self.mouselocation



	# -------------------------------------------------------------------
	# Returns the current hovering button         - INTERNAL FUNCTION
	# But only if the button is NOT hidden
	# -------------------------------------------------------------------

	def calculatecurrentmousebutton(self):

		outcome = ""
		checkcount = 0
		for buttonname in self.buttons.keys():
			if self.buttons[buttonname].gethoverstate(self.mouselocation) != "":
				if self.buttons[buttonname].getstate() != "Hidden":
					outcome = buttonname
					checkcount = checkcount + 1
		if checkcount > 1:
			outcome = "! Multiple Buttons !"
			print "Multiple visible buttons present at hover location"
		return outcome



	# -------------------------------------------------------------------
	# Returns the set of buttons in a group
	# If nothing specified, all buttons are returned
	# -------------------------------------------------------------------

	def getbuttoncollection(self, groupname):

		outcome = []

		if groupname == "":
			for buttonname in self.buttons.keys():
				outcome.append(buttonname)

		else:
			for buttonname in self.buttons.keys():
				if self.buttons[buttonname].isingroup(groupname) == True:
					outcome.append(buttonname)

		return outcome



	# -------------------------------------------------------------------
	# Get button state
	# -------------------------------------------------------------------

	def getareastate(self, buttonname):

		outcome = ""
		if buttonname in self.buttons:
			outcome = self.buttons[buttonname].getstate()
		else:
			print "Invalid button name - ", buttonname

		return outcome



	# -------------------------------------------------------------------
	# Returns the position of the button
	# -------------------------------------------------------------------

	def getareaposition(self, buttonname):

		outcome = ""
		if buttonname in self.buttons:
			outcome = self.buttons[buttonname].getposition()
		else:
			print "Invalid button name - ", buttonname

		return outcome



	# -------------------------------------------------------------------
	# Returns the dimensions of the button
	# -------------------------------------------------------------------

	def getareadimensions(self, buttonname):

		outcome = ""
		if buttonname in self.buttons:
			outcome = self.buttons[buttonname].getdimensions()
		else:
			print "Invalid button name - ", buttonname

		return outcome

