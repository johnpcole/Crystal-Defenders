from defenderconfig_subcomponent import defenderconfig_module as DefenderConfiguration
from ...common_components.fileprocessing_framework import fileprocessing_module as File



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
			newdefendertypeconfig = DefenderConfiguration.createconfig()

			# Loop over all lines of data
			for configitem in rawconfigs:

				# Extract the first data field name and the rest of the line
				fieldname, fieldvalue = File.datapair(configitem)
				
				if fieldname == "Level":

					# Create a new defender configuration object based on the partial one above
					newdefenderlevelconfig = DefenderConfiguration.createconfig()
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
					assert newdefenderlevelconfig.validateconfig() == True, "Incomplete Defender Configuration"
					self.defenderitem.append(newdefenderlevelconfig)

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
		