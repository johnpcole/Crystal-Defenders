class DefineButton:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self, buttonposition, buttondimensions, buttoncost):

		# pixel location of button
		self.position = buttonposition

		# pixel size of button
		self.dimensions = buttondimensions

		# state of button - Can be Hidden, Disabled, or Enabled
		self.state = "Hidden"

		# cost of button, only relevent for add and upgrade defenders
		self.cost = buttoncost



	# ==========================================================================================
	# Get Information
	# ==========================================================================================

# Getters are not used for this class, because the class's sole object instance is a child of
# of another object, and the parent is the only thing which interacts with this object
