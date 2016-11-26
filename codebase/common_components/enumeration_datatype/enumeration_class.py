class DefineEnumeration:

	def __init__(self, valuelist, initialvalue):

		self.valuelist = []

		for valueitem in valuelist:
			if valueitem not in self.valuelist:
				self.valuelist.append(valueitem)

		self.currentvalue = ""
		self.set(initialvalue)



	def set(self, valuelabel):

		self.validatevalue(valuelabel)

		if valuelabel in self.valuelist:
			self.currentvalue = valuelabel



	def displaycurrent(self):

		return self.currentvalue



	def displaylist(self):

		return self.valuelist



	def checkexists(self, valuelabel):

		if valuelabel in self.valuelist:
			outcome = True
		else:
			outcome = False

		return outcome



	def get(self, valuelabel):

		self.validatevalue(valuelabel)

		if valuelabel == self.currentvalue:
			outcome = True
		else:
			outcome = False

		return outcome



	def validatevalue(self, valuelabel):

		if valuelabel not in self.valuelist:
			outputline = "Value <" + valuelabel + "> does not exist in list |"
			for itemname in self.valuelist:
				outputline = outputline + itemname + "|"
				assert valuelabel in self.valuelist, outputline + "."
