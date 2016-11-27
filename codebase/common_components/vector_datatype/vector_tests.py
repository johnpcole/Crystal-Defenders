from . import vector_module as Vector


# ====================================================================================
# vector_module
# ====================================================================================


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
					testscalar = (firstxvalue * secondxvalue) + (firstyvalue * secondyvalue)
					assert Vector.dotproduct(firstvector, secondvector) == testscalar

# Angle between two vectors

def test_vectors_angle():
	for firstxvalue in [-10, 0, 20]:
		for firstyvalue in [-300, 0, 400]:
			firstvector = Vector.createfromvalues(firstxvalue, firstyvalue)
			for secondxvalue in [-5000, 0, 6000]:
				for secondyvalue in [-70000, 0, 80000]:
					secondvector = Vector.createfromvalues(secondxvalue, secondyvalue)
					firstlength = (((firstxvalue ** 2.0) + (firstyvalue ** 2.0))) ** 0.5
					secondlength = (((secondxvalue ** 2.0) + (secondyvalue ** 2.0))) ** 0.5
					dotproduct = (firstxvalue * secondxvalue) + (firstyvalue * secondyvalue)
					testscalar = dotproduct / (firstlength * secondlength)
					assert Vector.angle(firstvector, secondvector) == testscalar

# Gap between the ends of two vectors

def test_vectors_gap():
	for firstxvalue in [-10, 0, 20]:
		for firstyvalue in [-300, 0, 400]:
			firstvector = Vector.createfromvalues(firstxvalue, firstyvalue)
			for secondxvalue in [-5000, 0, 6000]:
				for secondyvalue in [-70000, 0, 80000]:
					secondvector = Vector.createfromvalues(secondxvalue, secondyvalue)
					xdiff = firstxvalue - secondxvalue
					ydiff = firstyvalue - secondyvalue
					difflength = (((xdiff ** 2.0) + (ydiff ** 2.0))) ** 0.5
					assert difflength == Vector.gap(firstvector, secondvector)
					
# If two vectors are equal
						
def test_vectors_equal():
	for firstxvalue in [-10, 0, 20]:
		for firstyvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			firstvector = Vector.createfromvalues(firstxvalue, firstyvalue)
			for secondxvalue in [-10, 0, 20]:
				for secondyvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
					secondvector = Vector.createfromvalues(secondxvalue, secondyvalue)
					equalflag = True
					if firstxvalue != secondxvalue:
						equalflag = False:
					if firstyvalue != secondyvalue:
						equalflag = False:
					assert equalflag == Vector.compare(firstvector, secondvector)
					
					


# ====================================================================================
# vector_class
# ====================================================================================

def test_set_blank():
	testvector = Vector.createorigin()
	testvector.setblank
	assert self.getx() == -999
	assert self.gety() == -999
	
	
def test_set_origin():
	testvector = Vector.createblank()
	testvector.setorigin
	assert self.getx() == 0
	assert self.gety() == 0
	
	
def test_set_values():
	testvector = Vector.createblank()
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			testvector.setfromvalues(xvalue, yvalue)
			assert self.getx() == xvalue
			assert self.gety() == yvalue

def test_set_pair():
	testvector = Vector.createblank()
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			testpair = (xvalue, yvalue)
			testvector.setfrompair(testpair)
			assert self.getx() == xvalue
			assert self.gety() == yvalue
	

def test_set_vector():
	testvector = Vector.createblank()
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			sourcevector = Vector.createfromvalues(xvalue, yvalue)
			testvector.setfromvector(sourcevector)
			assert self.getx() == xvalue
			assert self.gety() == yvalue
	

def test_set_x():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			testvector = Vector.createfromvalues(xvalue, yvalue)
			for newvalue in [-12, -11, -10, -9, -8, -2, -1, 0, 1, 2, 18, 19, 20, 21, 22]:
				testvector.setx(newvalue)
				assert self.getx() == newvalue
				assert self.gety() == yvalue
				
				
def test_set_y():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			testvector = Vector.createfromvalues(xvalue, yvalue)
			for newvalue in [-12, -11, -10, -9, -8, -2, -1, 0, 1, 2, 18, 19, 20, 21, 22]:
				testvector.sety(newvalue)
				assert self.getx() == xvalue
				assert self.gety() == newvalue
				
				
def test_get_area():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			testvector = Vector.createfromvalues(xvalue, yvalue)
			assert self.getarea() == xvalue * yvalue


def test_get_length():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			testvector = Vector.createfromvalues(xvalue, yvalue)
			testlength = ((xvalue ** 2.0) + (yvalue ** 2.0)) ** 0.5
				assert self.getlength() == testlength
				
				
def test_get_coordinates():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			testvector = Vector.createfromvalues(xvalue, yvalue)
			resultx, resulty = testvector.getcoordinates()
			assert resultx == xvalue
			assert resulty == yvalue
				
				
def test_get_x():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			testvector = Vector.createfromvalues(xvalue, yvalue)
			for newvalue in [-12, -11, -10, -9, -8, -2, -1, 0, 1, 2, 18, 19, 20, 21, 22]:
				testvector.x = newvalue
				assert self.getx() == newvalue
				assert self.gety() == yvalue
				
				
def test_get_y():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			testvector = Vector.createfromvalues(xvalue, yvalue)
			for newvalue in [-12, -11, -10, -9, -8, -2, -1, 0, 1, 2, 18, 19, 20, 21, 22]:
				testvector.y = newvalue
				assert self.getx() == xvalue
				assert self.gety() == newvalue

				
def test_get_inverted():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			sourcevector = Vector.createfromvalues(xvalue, yvalue)
			testvector = sourcevector.getinverted()
			assert testvector.getx() == -xvalue
			assert testvector.gety() == -yvalue
			testvector = testvector.getinverted()
			assert testvector.getx() == xvalue
			assert testvector.gety() == yvalue
			
			
def test_get_swapped():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			sourcevector = Vector.createfromvalues(xvalue, yvalue)
			testvector = Vector.getswapped()
			assert testvector.getx() == yvalue
			assert testvector.gety() == xvalue
			testvector = testvector.getinverted()
			assert testvector.getx() == xvalue
			assert testvector.gety() == yvalue

			
def test_get_int():
	for xvalue in [-10.1, 0.1, 20.1]:
		for yvalue in [-11.1, -10.5, -9.9, -1.1, 0.5, 1.9, 19.1, 20.5, 21.9]:
			sourcevector = Vector.createfromvalues(xvalue, yvalue)
			testvector = Vector.getint()
			assert testvector.getx() == int(xvalue)
			assert testvector.gety() == int(yvalue)


def test_get_float():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			sourcevector = Vector.createfromvalues(xvalue, yvalue)
			testvector = Vector.getfloat()
			assert testvector.getx() == float(xvalue)
			assert testvector.gety() == float(yvalue)

			
def test_get_rotated():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			sourcevector = Vector.createfromvalues(xvalue, yvalue)
			testvector = sourcevector.getrotated()
			assert testvector.getx() == -yvalue
			assert testvector.gety() == xvalue
			testvector = testvector.getrotated()
			assert testvector.getx() == -xvalue
			assert testvector.gety() == -yvalue
			testvector = sourcevector.getrotated()
			assert testvector.getx() == yvalue
			assert testvector.gety() == -xvalue
			testvector = sourcevector.getrotated()
			assert testvector.getx() == xvalue
			assert testvector.gety() == yvalue


def test_get_perimeter():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			testvector = Vector.createfromvalues(xvalue, yvalue)
			assert self.getperimeter() == xvalue + yvalue
			

def test_get_scaled():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			sourcevector = Vector.createfromvalues(xvalue, yvalue)
			for sfactor in [-3, 0, 4]:
				testvector = sourcevector.getscaled(sfactor)
				assert testvector.getx() == xvalue * sfactor
				assert testvector.gety() == yvalue * sfactor
				if sfactor != 0:
					dfactor = 1 / sfactor
					testvector = testvector.getscaled(dfactor)
					assert testvector.getx() == xvalue
					assert testvector.gety() == yvalue
				

def test_get_fitted():
	for xvalue in [-10, 0, 20]:
		for yvalue in [-11, -10, -9, -1, 0, 1, 19, 20, 21]:
			sourcevector = Vector.createfromvalues(xvalue, yvalue)
			for ffactor in [-18, -1, 0, 1, 4]:
				testvector = sourcevector.getfitted(sfactor)
				sfactor = ffactor / (((xvalue ** 2) + (yvalue ** 2)) ** 0.5)
				assert testvector.getx() == xvalue * sfactor
				assert testvector.gety() == yvalue * sfactor
				if sfactor != 0:
					dfactor = 1 / sfactor
					testvector = testvector.getscaled(dfactor)
					assert testvector.getx() == xvalue
					assert testvector.gety() == yvalue
				
	
def test_get_projection():
	testvector = sourcevector.setfromvalues(0.0, 0.0)
	assert testvector.getprojection() = ""
	
	testvector = sourcevector.setfromvalues(0.01, 0.0)
	assert testvector.getprojection() = "S"
	testvector = sourcevector.setfromvalues(-0.01, 0.0)
	assert testvector.getprojection() = "N"
	testvector = sourcevector.setfromvalues(0.0, 0.01)
	assert testvector.getprojection() = "E"
	testvector = sourcevector.setfromvalues(0.0, -0.01)
	assert testvector.getprojection() = "W"
	
	testvector = sourcevector.setfromvalues(0.01, -0.01)
	assert testvector.getprojection() = "SW"
	testvector = sourcevector.setfromvalues(-0.01, 0.01)
	assert testvector.getprojection() = "NE"
	testvector = sourcevector.setfromvalues(0.01, 0.01)
	assert testvector.getprojection() = "SE"
	testvector = sourcevector.setfromvalues(-0.01, -0.01)
	assert testvector.getprojection() = "NW"

	testvector = sourcevector.setfromvalues(0, 0)
	assert testvector.getprojection() = ""
	
	testvector = sourcevector.setfromvalues(1, 0)
	assert testvector.getprojection() = "S"
	testvector = sourcevector.setfromvalues(-1, 0)
	assert testvector.getprojection() = "N"
	testvector = sourcevector.setfromvalues(0, 1)
	assert testvector.getprojection() = "E"
	testvector = sourcevector.setfromvalues(0, -1)
	assert testvector.getprojection() = "W"
	
	testvector = sourcevector.setfromvalues(1, -1)
	assert testvector.getprojection() = "SW"
	testvector = sourcevector.setfromvalues(-1, 1)
	assert testvector.getprojection() = "NE"
	testvector = sourcevector.setfromvalues(1, 1)
	assert testvector.getprojection() = "SE"
	testvector = sourcevector.setfromvalues(-1, -1)
	assert testvector.getprojection() = "NW"

def test_get_compass_one():
	testvector = sourcevector.setfromvalues(0.0, 0.0)
	assert testvector.getcompass(1) = ""
	
	testvector = sourcevector.setfromvalues(0.01001, 0.0)
	assert testvector.getcompass(1) = "S"
	testvector = sourcevector.setfromvalues(0.01001, -0.01)
	assert testvector.getcompass(1) = "S"
	testvector = sourcevector.setfromvalues(0.01001, 0.01)
	assert testvector.getcompass(1) = "S"

	testvector = sourcevector.setfromvalues(-0.01001, 0.0)
	assert testvector.getcompass(1) = "N"
	testvector = sourcevector.setfromvalues(-0.01001, -0.01)
	assert testvector.getcompass(1) = "N"
	testvector = sourcevector.setfromvalues(-0.01001, 0.01)
	assert testvector.getcompass(1) = "N"

	testvector = sourcevector.setfromvalues(0.0, 0.01001)
	assert testvector.getcompass(1) = "E"
	testvector = sourcevector.setfromvalues(0.01, 0.01001)
	assert testvector.getcompass(1) = "E"
	testvector = sourcevector.setfromvalues(-0.01, 0.01001)
	assert testvector.getcompass(1) = "E"
	
	testvector = sourcevector.setfromvalues(0.0, -0.01001)
	assert testvector.getcompass(1) = "W"
	testvector = sourcevector.setfromvalues(0.01, -0.01001)
	assert testvector.getcompass(1) = "W"
	testvector = sourcevector.setfromvalues(-0.01, -0.01001)
	assert testvector.getcompass(1) = "W"
	

def test_get_compass_two():
	testvector = sourcevector.setfromvalues(0.0, 0.0)
	assert testvector.getcompass(2) = ""
	
	testvector = sourcevector.setfromvalues(-1.0, -2.3)
	assert testvector.getcompass(2) = "W"
	testvector = sourcevector.setfromvalues(0.0, -2.3)
	assert testvector.getcompass(2) = "W"
	testvector = sourcevector.setfromvalues(1.0, -2.3)
	assert testvector.getcompass(2) = "W"

	testvector = sourcevector.setfromvalues(1.0001, -2.3)
	assert testvector.getcompass(2) = "SW"
	testvector = sourcevector.setfromvalues(2.3, -2.3)
	assert testvector.getcompass(2) = "SW"
	testvector = sourcevector.setfromvalues(2.3, -1.0001)
	assert testvector.getcompass(2) = "SW"
	testvector = sourcevector.setfromvalues(2.3, -1.0)
	assert testvector.getcompass(2) = "S"
	testvector = sourcevector.setfromvalues(2.3, 0.0)
	assert testvector.getcompass(2) = "S"
	testvector = sourcevector.setfromvalues(2.3, 1.0)
	assert testvector.getcompass(2) = "S"
	testvector = sourcevector.setfromvalues(2.3, 1.0001)
	assert testvector.getcompass(2) = "SE"
	testvector = sourcevector.setfromvalues(2.3, 2.3)
	assert testvector.getcompass(2) = "SE"
	testvector = sourcevector.setfromvalues(1.0001, 2.3)
	assert testvector.getcompass(2) = "SE"

	testvector = sourcevector.setfromvalues(1.0, 2.3)
	assert testvector.getcompass(2) = "E"
	testvector = sourcevector.setfromvalues(0.0, 2.3)
	assert testvector.getcompass(2) = "E"
	testvector = sourcevector.setfromvalues(-1.0, 2.3)
	assert testvector.getcompass(2) = "E"

	testvector = sourcevector.setfromvalues(-1.0001, -2.3)
	assert testvector.getcompass(2) = "NW"
	testvector = sourcevector.setfromvalues(-2.3, -2.3)
	assert testvector.getcompass(2) = "NW"
	testvector = sourcevector.setfromvalues(-2.3, -1.0001)
	assert testvector.getcompass(2) = "NW"
	testvector = sourcevector.setfromvalues(-2.3, -1.0)
	assert testvector.getcompass(2) = "N"
	testvector = sourcevector.setfromvalues(-2.3, 0.0)
	assert testvector.getcompass(2) = "N"
	testvector = sourcevector.setfromvalues(-2.3, 1.0)
	assert testvector.getcompass(2) = "N"
	testvector = sourcevector.setfromvalues(-2.3, 1.0001)
	assert testvector.getcompass(2) = "NE"
	testvector = sourcevector.setfromvalues(-2.3, 2.3)
	assert testvector.getcompass(2) = "NE"
	testvector = sourcevector.setfromvalues(-1.0001, 2.3)
	assert testvector.getcompass(2) = "NE"
