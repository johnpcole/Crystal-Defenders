from enemyconfig_subcomponent import DefineEnemyConfiguration
from ...common_components import File

class DefineEnemyConfigurationLibrary:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self):

		self.enemyitem = []
		self.populatelibrary()


	def populatelibrary(self):

		# Read in the data from a file into a simple string list
		rawconfigs = File.readfromdisk("configs/Enemies.txt")
		
		# Loop over all lines of data
		for configitem in rawconfigs:

			# Create a new enemy configuration object
			newenemyconfig = DefineEnemyConfiguration()

			# Get the tabulated data
			tabulatedlist = File.tabulateddata(configitem)
			
			# Loop over the tabulated pairs
			for tabulateditem in tabulatedlist:
			
				# Extract the first data field name and the rest of the line
				fieldname, fieldvalue = File.datapair(tabulateditem)

				# Set the defender level type specific data
				newenemyconfig.setdata(fieldname, fieldvalue)

			# Add this configuration if all values have been set
			if newenemyconfig.validateconfig() == True:
				self.enemyitem.append(newenemyconfig)
			else:
				print "Incomplete Enemy Configuration"
				
						

	# ==========================================================================================
	# Get Information
	# ==========================================================================================

	def getenemyconfig(self, wavenumber):
	
		outcome = None
	
		for configitem in self.enemyitem:
			if configitem.wave == wavenumber:
				outcome = configitem

		print "Inappropriate Enemy Wave - ", wavenumber

		return outcome
		