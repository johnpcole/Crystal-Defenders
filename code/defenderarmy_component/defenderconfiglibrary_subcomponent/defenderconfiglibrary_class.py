from defenderconfig_subcomponent import DefineDefenderConfiguration
from ...common_components import File



class DefineDefenderConfigurationLibrary:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self):

		self.defenderitem = []
		self.populatelibrary()


	def populatelibrary(self):

		# Loop over all defender types
		for filename in ['Soldier', 'Archer', 'Wizard', 'Theif']:
	
			# Read in the data from a file into a simple string list
			rawconfigs = File.readfromdisk("configs/Defender_" + filename + ".txt")
			
			# Create a new defender configuration object
			newdefendertypeconfig = DefineDefenderConfiguration()

			# Loop over all lines of data
			for configitem in rawconfigs:

				# Extract the first data field name and the rest of the line
				fieldname, fieldvalue = File.datapair(configitem)
				
				if fieldname == "Level":

					# Create a new defender configuration object based on the partial one above
					newdefenderlevelconfig = DefineDefenderConfiguration()
					newdefenderlevelconfig.copypartialconfig(newdefendertypeconfig)

					# Get the tabulated data
					tabulatedlist = File.tabulateddata(configitem)
					
					# Loop over the tabulated pairs
					for tabulateditem in tabulatedlist:

						# Extract the nth data field name and the rest of the line
						fieldnametwo, fieldvaluetwo = File.datapair(tabulateditem)

						# Set the defender level type specific data
						newdefenderlevelconfig.setdata(fieldnametwo, fieldvaluetwo)

					# Add this configuration if all values have been set
					if newdefenderlevelconfig.validateconfig() == True:
						self.defenderitem.append(newdefenderlevelconfig)
					else:
						print "Incomplete Defender Configuration"
						x = 1/0
						
				else:
				
					# Set the defender type specific data
					newdefendertypeconfig.setdata(fieldname, fieldvalue)
						
						
						
						
						

	# ==========================================================================================
	# Get Information
	# ==========================================================================================

	def getdefenderconfig(self, defendertype, defenderlevel):
	
		outcome = None
	
		for configitem in self.defenderitem:
			if defendertype == configitem.defendertype:
				if defenderlevel == configitem.level:
					outcome = configitem

		if outcome is None:
			print "Inappropriate Defender Type/Level - ", defendertype, defenderlevel

		return outcome
		