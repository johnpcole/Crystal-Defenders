import math
from . import vector_module as Vector

# Create a blank vector

def test_create_blank():
	testvector = Vector.createblank()
	assert testvector.getx() == -999
	assert testvector.gety() == -999


def test_create_origin():
	testvector = Vector.createorigin()
	assert testvector.getx() == 0
	assert testvector.gety() == 0

# Create a vector from a tuplet

def test_create_from_pair():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-300, 0, 400]:
			testvector = Vector.createfrompair((xvalue, yvalue))
			assert testvector.getx() == xvalue
			assert testvector.gety() == yvalue

# Create a vector from two values

def test_create_from_values():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-300, 0, 400]:
			testvector = Vector.createfromvalues(xvalue, yvalue)
			assert testvector.getx() == xvalue
			assert testvector.gety() == yvalue



# Add two vectors

def test_add_vectors():
	for firstxvalue in [-10, 0, 20]:
		for firstyvalue in [-300, 0, 400]:
			firstvector = Vector.createfromvalues(firstxvalue, firstyvalue)
			for secondxvalue in [-5000, 0, 6000]:
				for secondyvalue in [-70000, 0, 80000]:
					secondvector = Vector.createfromvalues(secondxvalue, secondyvalue)
					testvector = Vector.add(firstvector, secondvector)
					assert testvector.getx() == firstxvalue + secondxvalue
					assert testvector.gety() == firstyvalue + secondyvalue

# Subtract two vectors

def test_subtract_vectors():
	for firstxvalue in [-10, 0, 20]:
		for firstyvalue in [-300, 0, 400]:
			firstvector = Vector.createfromvalues(firstxvalue, firstyvalue)
			for secondxvalue in [-5000, 0, 6000]:
				for secondyvalue in [-70000, 0, 80000]:
					secondvector = Vector.createfromvalues(secondxvalue, secondyvalue)
					testvector = Vector.subtract(firstvector, secondvector)
					assert testvector.getx() == firstxvalue - secondxvalue
					assert testvector.gety() == firstyvalue - secondyvalue


# Divides two vectors

def test_divide_vectors():
	for firstxvalue in [-10, 0, 20]:
		for firstyvalue in [-300, 0, 400]:
			firstvector = Vector.createfromvalues(firstxvalue, firstyvalue)
			for secondxvalue in [-5000, 6000]:
				for secondyvalue in [-70000, 80000]:
					secondvector = Vector.createfromvalues(secondxvalue, secondyvalue)
					testvector = Vector.divide(firstvector, secondvector)
					assert testvector.getx() == firstxvalue / secondxvalue
					assert testvector.gety() == firstyvalue / secondyvalue

# Multiplies two vectors

def test_multiply_vectors():
	for firstxvalue in [-10, 0, 20]:
		for firstyvalue in [-300, 0, 400]:
			firstvector = Vector.createfromvalues(firstxvalue, firstyvalue)
			for secondxvalue in [-5000, 0, 6000]:
				for secondyvalue in [-70000, 0, 80000]:
					secondvector = Vector.createfromvalues(secondxvalue, secondyvalue)
					testvector = Vector.multiply(firstvector, secondvector)
					assert testvector.getx() == firstxvalue * secondxvalue
					assert testvector.gety() == firstyvalue * secondyvalue

# Dot product of two vectors

def test_dot_product():
	for firstxvalue in [-10, 0, 20]:
		for firstyvalue in [-300, 0, 400]:
			firstvector = Vector.createfromvalues(firstxvalue, firstyvalue)
			for secondxvalue in [-5000, 0, 6000]:
				for secondyvalue in [-70000, 0, 80000]:
					secondvector = Vector.createfromvalues(secondxvalue, secondyvalue)
					testscalar = Vector.dotproduct(firstvector, secondvector)
					assert testscalar == (firstxvalue * secondxvalue) + (firstyvalue * secondyvalue)


# Angle between two vectors

def donttest_vectors_angle():
	for firstxvalue in [-10, 0, 20]:
		for firstyvalue in [-300, 0, 400]:
			firstvector = Vector.createfromvalues(firstxvalue, firstyvalue)
			for secondxvalue in [-5000, 0, 6000]:
				for secondyvalue in [-70000, 0, 80000]:
					secondvector = Vector.createfromvalues(secondxvalue, secondyvalue)
					testscalar = Vector.angle(firstvector, secondvector)
					firstlength = math.sqrt(((firstxvalue ^ 2) + (firstyvalue ^ 2)))
					secondlength = math.sqrt(((secondxvalue ^ 2) + (secondyvalue ^ 2)))
					dotproduct = (firstxvalue * secondxvalue) + (firstyvalue * secondyvalue)
					assert testscalar == dotproduct / (firstlength * secondlength)

