class DefineVector:

	# ---------------------------------------------
	# Vectors are defined from a pair of values
	# ---------------------------------------------

	def __init__(self):
		self.x = 0
		self.y = 0



	# ---------------------------------------------
	# Vector can be reset as "blank"
	# ---------------------------------------------

	def setblank(self):
		self.x = -999
		self.y = -999



	# ---------------------------------------------
	# Vector can be set to the origin
	# ---------------------------------------------

	def setorigin(self):
		self.x = 0
		self.y = 0



	# ---------------------------------------------
	# Vectors can be redefined from a pair of values
	# ---------------------------------------------

	def setfromvalues(self, xval, yval):
		self.x = xval
		self.y = yval



	# ---------------------------------------------
	# Vectors can be redefined from a tuplet
	# ---------------------------------------------

	def setfrompair(self, pair):
		self.x, self.y = pair



	# ---------------------------------------------
	# Vectors can be redefined from another Vector
	# ---------------------------------------------

	def setfromvector(self, vector):
		self.x = vector.x
		self.y = vector.y



	# ---------------------------------------------
	# Sets the x coordinate value
	# ---------------------------------------------

	def setx(self, xval):
		self.x = xval



	# ---------------------------------------------
	# Sets the y coordinate value
	# ---------------------------------------------

	def sety(self, yval):
		self.y = yval



	# ---------------------------------------------
	# Gets the area of the Vector
	# ---------------------------------------------

	def getarea(self):
		return self.x * self.y



	# ---------------------------------------------
	# Gets the length of the Vector
	# ---------------------------------------------

	def getlength(self):
		return ((self.x ** 2.0) + (self.y ** 2.0)) ** 0.5



	# ---------------------------------------------
	# Gets the coordinates of the Vector as a pair
	# ---------------------------------------------

	def getcoordinates(self):
		return self.x, self.y



	# ---------------------------------------------
	# Gets the x coordinate value
	# ---------------------------------------------

	def getx(self):
		return self.x



	# ---------------------------------------------
	# Gets the y coordinate value
	# ---------------------------------------------

	def gety(self):
		return self.y



	# ---------------------------------------------
	# Returns a Vector which is the inverse,
	# or polar opposite of the input Vector
	# ---------------------------------------------

	def getinverted(self):
		outcome = DefineVector()
		outcome.setfromvalues(-self.x, -self.y)
		return outcome



	# ---------------------------------------------
	# Returns a Vector which has the x & y
	# co-ordinates of the input Vector
	# ---------------------------------------------

	def getswapped(self):
		outcome = DefineVector()
		outcome.setfromvalues(self.y, self.x)
		return outcome



	# ---------------------------------------------
	# Returns a Vector with integer coordinates
	# ---------------------------------------------

	def getint(self):
		outcome = DefineVector()
		outcome.setfromvalues(int(self.x), int(self.y))
		return outcome



	# ---------------------------------------------
	# Returns a Vector with floating coordinates
	# ---------------------------------------------

	def getfloat(self):
		outcome = DefineVector()
		outcome.setfromvalues(float(self.x), float(self.y))
		return outcome



	# ---------------------------------------------
	# Returns a Vector by rotating the input Vector
	# 90 degrees counter clockwise
	# ---------------------------------------------

	def getrotated(self):
		outcome = DefineVector()
		outcome.setfromvalues(0 - self.y, self.x)
		return outcome



	# ---------------------------------------------
	# Returns a scalar signifying "perimeter"
	# Adding the input Vector coordinates together
	# ---------------------------------------------

	def getperimeter(self):
		return self.x + self.y



	# ---------------------------------------------
	# Returns a Vector, scaling the input Vector BY A MULTIPLE
	# Each coordinate is formed by multiplying the equivalent
	# coordinate of the input Vector by the input scalar
	# ---------------------------------------------

	def getscaled(self, factor):
		outcome = DefineVector()
		outcome.setfromvalues(self.x * factor, self.y * factor)
		return outcome



	# ---------------------------------------------
	# Returns a Vector, scaling the input Vector TO A LENGTH
	# Each coordinate is formed by multiplying the equivalent
	# coordinate of the input Vector by a scalar such that
	# the output Vector has length equal to the input scalar
	# ---------------------------------------------

	def getfitted(self, finallength):
		if self.getlength() == 0:
			scalar = 0
		else:
			scalar = finallength / self.getlength()
		return self.getscaled(scalar)



	# ---------------------------------------------
	# Returns a string, signifying non-zero
	# projections on N/S & E/W axes
	# ---------------------------------------------

	def getprojection(self):

		if self.x > 0.000001:
			ns = "S"
		elif self.x < -0.000001:
			ns = "N"
		else:
			ns = ""

		if self.y > 0.000001:
			ew = "E"
		elif self.y < -0.000001:
			ew = "W"
		else:
			ew = ""

		outcome = ns + ew

		return outcome



	# ---------------------------------------------
	# Builds a string, signifying 1 or 2 digit
	# compass points, based on equal angle partitions
	# ---------------------------------------------

	def getcompass(self, points):
		# points can be 1 or 2

		projection = self.getprojection()

		if len(projection) == 2:
			if points == 2:
				majorside = float(max(abs(self.x), abs(self.y)))
				minorside = float(min(abs(self.x), abs(self.y)))
				if (majorside / minorside) < 2.3:
					pointsmode = "Keep"  # both letters
				else:
					pointsmode = "Reduce"  # to dominant letter
			else:
				pointsmode = "Reduce"  # to dominant letter
		else:
			pointsmode = "Keep"  # original projection, which is 1 or 0 letters

		if pointsmode == "Keep":
			outcome = projection
		else:
			if abs(self.x) > abs(self.y):
				outcome = projection[0]
			else:
				outcome = projection[1]

		return outcome

