class DefineScale:

	def __init__(self, maximumvalue):
		self.maxval = maximumvalue
		self.val = maximumvalue



	def deplete(self, redval):
		self.val = max(self.val - redval, 0)
		if self.val == 0:
			outcome = True
		else:
			outcome = False
		return outcome



	def restore(self, incval):
		self.val = min(self.val + incval, self.maxval)
		if self.val == self.maxval:
			outcome = True
		else:
			outcome = False
		return outcome



	def getpercentage(self):
		return self.getfraction(100)



	def getfraction(self, denominator):
		return int(denominator * self.val / self.maxval)



	def getpartition(self, buckets):
		return 1 + int(buckets * self.val / (self.maxval + 1))



	def recharge(self):
		self.val = self.maxval



	def discharge(self):
		self.val = 0



	def isempty(self):
		if self.val == 0:
			outcome = True
		else:
			outcome = False
		return outcome



	def isfull(self):
		if self.val == self.maxval:
			outcome = True
		else:
			outcome = False
		return outcome

