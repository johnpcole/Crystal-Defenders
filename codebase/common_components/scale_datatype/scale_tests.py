from . import scale_module as Scale


# ====================================================================================
# scale_module
# ====================================================================================

def test_create_full():
	testscale = Scale.createfull(10)
	assert testscale.getvalue() == 10
	
	
def test_create_empty():
	testscale = Scale.createempty(10)
	assert testscale.getvalue() == 0
	
	
def test_partition():
	for testmax in [10, 33, 88, 1000]:
		for testblocks in [1, 2, 3, 4, 5, 10]:
			boundary = int(float(testmax) / float(testblocks))
			for testvalue in range(0, testmax + 1):
				testpartition = int(float(testvalue) / int(testmax))
				assert Scale.partitionintobuckets(testmax, testblocks, testvalue) == testpartition

				
def test_rangeoverhang():
	print "??????????????????????????????????????????????????????????????"

	
	
	

# ====================================================================================
# scale_class
# ====================================================================================

def test_deplete():
	for testmax in [33, 88, 1000]:
		testscale = Scale.createfull(testmax)
		tracker = testmax
		for delta in [3, 0, 5, 20]:
			tracker = tracker - delta
			outcome = testscale.deplete(delta)
			assert testscale.getvalue() == tracker
			assert outcome == False
		#--------------------------------------------------
		testscale.recharge()
		outcome = testscale.deplete(testmax - 1)
		assert testscale.getvalue() == 1
		assert outcome == False
		#--------------------------------------------------
		testscale.recharge()
		outcome = testscale.deplete(testmax)
		assert testscale.getvalue() == 0
		assert outcome == True
		#--------------------------------------------------
		testscale.recharge()
		outcome = testscale.deplete(2 + (testmax / 2))
		assert testscale.getvalue() > 0
		assert outcome == False
		outcome = testscale.deplete(2 + (testmax / 2))
		assert testscale.getvalue() == 0
		assert outcome == True
		#--------------------------------------------------
		testscale.recharge()
		outcome = testscale.deplete(testmax)
		assert testscale.getvalue() == 0
		assert outcome == True
		#--------------------------------------------------
		testscale.recharge()
		outcome = testscale.deplete(testmax + 1)
		assert testscale.getvalue() == 0
		assert outcome == True


def test_restore():
	for testmax in [33, 88, 1000]:
		testscale = Scale.createempty(testmax)
		tracker = 0
		for delta in [3, 0, 5, 20]:
			tracker = tracker + delta
			outcome = testscale.restore(delta)
			assert testscale.getvalue() == tracker
			assert outcome == False
		#--------------------------------------------------
		testscale.discharge()
		outcome = testscale.restore(testmax - 1)
		assert testscale.getvalue() == testmax - 1
		assert outcome == False
		#--------------------------------------------------
		testscale.discharge()
		outcome = testscale.restore(testmax)
		assert testscale.getvalue() == testmax
		assert outcome == True
		#--------------------------------------------------
		testscale.discharge()
		outcome = testscale.restore(2 + (testmax / 2))
		assert testscale.getvalue() < testmax
		assert outcome == False
		outcome = testscale.restore(2 + (testmax / 2))
		assert testscale.getvalue() == testmax
		assert outcome == True
		#--------------------------------------------------
		testscale.discharge()
		outcome = testscale.restore(testmax)
		assert testscale.getvalue() == testmax
		assert outcome == True
		#--------------------------------------------------
		testscale.discharge()
		outcome = testscale.restore(testmax + 1)
		assert testscale.getvalue() == testmax
		assert outcome == True

		

def test_get_percentage():
	for testmax in [33, 88, 1000]:
		testscale = Scale.createfull(testmax)
		for testvalue in range(0, testmax + 1, 9):
			testpercentage = int((100 * testvalue) / testmax)
			testscale.setvalue(testvalue)
			assert testscale.getpercentage() == testpercentage

			
def test_get_fraction():
	for testmax in [33, 88, 1000]:
		testscale = Scale.createfull(testmax)
		for denominator in [2, 3, 5, 10]:
			for testvalue in range(0, testmax + 1, 9):
				testfraction = int((denominator * testvalue) / testmax)
				testscale.setvalue(testvalue)
				assert testscale.getfraction(denominator) == testfraction

			
def test_get_partition():
	print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
			
			
			
			






def test_recharge():
	for testmax in [4, 10, 33, 88, 1000]:
		testscale = Scale.createempty(testmax)
			for testvalue in range(0, testmax, int(testmax / 7)):
				testscale.setvalue(testvalue)
				testscale.recharge()
				assert testscale.getvalue() == testmax
				
def test_discharge():
	for testmax in [4, 10, 33, 88, 1000]:
		testscale = Scale.createfull(testmax)
			for testvalue in range(0, testmax, int(testmax / 7)):
				testscale.setvalue(testvalue)
				testscale.discharge()
				assert testscale.getvalue() == 0
				
				
def test_is_empty():
	for testmax in [4, 10, 33, 88, 1000]:
		testscale = Scale.createfull(testmax)
		testscale.setvalue(1)
		assert testscale.isempty() == False
		testscale.setvalue(0)
		assert testscale.isempty() == True
		testscale.setvalue(testmax)
		assert testscale.isempty() == False

				
def test_is_full():
	for testmax in [4, 10, 33, 88, 1000]:
		testscale = Scale.createempty(testmax)
		testscale.setvalue(testmax - 1)
		assert testscale.isfull() == False
		testscale.setvalue(testmax)
		assert testscale.isempty() == True
		testscale.setvalue(0)
		assert testscale.isempty() == False
		

def test_get_value():
	for testmax in [4, 10, 33, 88, 1000]:
		testscale = Scale.createfull(testmax)
		for testvalue in range(0, testmax + 1, 4):
			testscale.val = testvalue
			assert testscale.getvalue() == testvalue
			

def test_set_value():
	for testmax in [4, 10, 33, 88, 1000]:
		testscale = Scale.createfull(testmax)
		for testvalue in range(0, testmax + 1, 4):
			testscale.setvalue(testvalue)
			assert testscale.getvalue() == testvalue
			