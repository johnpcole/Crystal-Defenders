from vector_class import DefineVector



# ---------------------------------------------
# Builds a Vector that's not initialised
# ---------------------------------------------

def createblank():
	return DefineVector(-999, -999)



# ---------------------------------------------
# Builds a Vector that's at the origin
# ---------------------------------------------

def createorigin():
	return DefineVector(0, 0)



# ---------------------------------------------
# Builds a Vector from a pair of values
# ---------------------------------------------

def createfromvalues(xval, yval):
	return DefineVector(xval, yval)



# ---------------------------------------------
# Builds a Vector from a tuplet
# ---------------------------------------------

def createfrompair(pair):
	xval, yval = pair
	outcome = DefineVector(xval, yval)
	return outcome



# ---------------------------------------------
# Builds a Vector from another Vector
# ---------------------------------------------

def createfromvector(inputvector):
	return DefineVector(inputvector.getx(), inputvector.gety())




# ---------------------------------------------
# Builds a Vector, summing two input vectors
# Each coordinate is formed by adding the
# equivalent coordinate of the two input vectors
# ---------------------------------------------

def add(first, second):
	return DefineVector(first.getx() + second.getx(), first.gety() + second.gety())



# ---------------------------------------------
# Builds a Vector, subtracting two input vectors
# Each coordinate is formed by subtracting the
# equivalent coordinate of the two input vectors
# ---------------------------------------------

def subtract(first, second):
	return DefineVector(first.getx() - second.getx(), first.gety() - second.gety())



# ---------------------------------------------
# Builds a Vector, "dividing" two input vectors
# Each coordinate is formed by dividing the
# equivalent coordinate of the two input vectors
# ---------------------------------------------

def divide(first, second):
	return DefineVector(first.getx() / second.getx(), first.gety() / second.gety())



# ---------------------------------------------
# Builds a Vector, "multiplying" two input vectors
# Each coordinate is formed by multiplying the
# equivalent coordinate of the two input vectors
# ---------------------------------------------

def multiply(first, second):
	return DefineVector(first.getx() * second.getx(), first.gety() * second.gety())



# ---------------------------------------------
# Builds a Vector, "multiplying" two input vectors
# Using formal dot product formula
# ---------------------------------------------

def dotproduct(first, second):
	multiplied = multiply(first, second)
	return multiplied.getperimeter()


# ---------------------------------------------
# Builds a scalar, signifying the cosine of the angle
# between two origin based vectors
# ---------------------------------------------

def angle(first, second):
	return dotproduct(first, second) / (first.getlength() * second.getlength())



# ---------------------------------------------
# Builds a scalar signifying distance between
# the end points of two origin based vectors
# ---------------------------------------------

def gap(first, second):
	difference = subtract(first, second)
	return difference.getlength()



# ---------------------------------------------
# Builds a boolean signifying equality
# between two input vectors
# ---------------------------------------------

def compare(first, second):
	outcome = False
	if first.getx() == second.getx():
		if first.gety() == second.gety():
			outcome = True
	return outcome








# ---------------------------------------------
# Builds a boolen, signifying whether two
# locations are within a specified distance apart
# ---------------------------------------------

def ispointinradius(objectposition, centreposition, thresholdradius):
	if gap(centreposition, objectposition) > thresholdradius:
		outcome = False
	else:
		outcome = True
	return outcome



# ---------------------------------------------
# Builds a boolen, signifying whether a location
# is within a specified rectangular area
# ---------------------------------------------

def ispointinarea(objectposition, areaposition, areadimensions):
	outcome = False
	if objectposition.getx() >= areaposition.getx():
		if objectposition.getx() <= (areaposition.getx() + areadimensions.getx() - 1):
			if objectposition.gety() >= areaposition.gety():
				if objectposition.gety() <= (areaposition.gety() + areadimensions.gety() - 1):
					outcome = True
	return outcome



# ---------------------------------------------
# Builds a boolen, signifying whether a rectangle
# is within a specified rectangular area
# ---------------------------------------------

def isoblonginarea(oblongposition, oblongdimensions, areaposition, areadimensions):
	outcome = False
	if oblongposition.getx() >= areaposition.getx():
		if (oblongposition.getx() + oblongdimensions.getx() - 1) <= (areaposition.getx() + areadimensions.getx() - 1):
			if oblongposition.gety() >= areaposition.gety():
				if (oblongposition.gety() + oblongdimensions.gety() - 1) <= (areaposition.gety() +
																							areadimensions.gety() - 1):
					outcome = True
	return outcome


