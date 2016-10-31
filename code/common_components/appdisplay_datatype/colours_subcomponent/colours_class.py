class DefineColourLibrary:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self):

		self.key = {}
		# Primary & Secondary Colours
		self.key['Black'] = (0,0,0)
		self.key['Red'] = (255,0,0)
		self.key['Yellow'] = (255,255,0)
		self.key['Green'] = (0,255,0)
		self.key['Cyan'] = (0,255,255)
		self.key['Blue'] = (0,0,255)
		self.key['Magenta'] = (255,0,255)
		self.key['White'] = (255,255,255)
		# Tertiary Colours
		self.key['Orange'] = (255,128,0)
		self.key['Lime'] = (128,255,0)
		self.key['Pink'] = (255,0,128)
		self.key['Purple'] = (128,0,255)
		self.key['Light Blue'] = (0,128,255)
		self.key['Light Green'] = (0,255,128)
		# Faded Primaries & Secondaries
		self.key['Faded Red'] = (255,128,128)
		self.key['Faded Green'] = (128,255,128)
		self.key['Faded Blue'] = (128,128,255)
		self.key['Faded Yellow'] = (255,255,128)
		self.key['Faded Cyan'] = (128,255,255)
		self.key['Faded Magenta'] = (255,128,255)
		self.key['Grey'] = (128,128,128)



	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================

	def add(self, colourlabel, redvalue, greenvalue, bluevalue):
		self.key[colourlabel] = (redvalue, greenvalue, bluevalue)



	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	def get(self, colourlabel):
		return self.key[colourlabel]
