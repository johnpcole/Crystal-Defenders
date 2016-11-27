from enemyconfig_subcomponent import enemyconfig_module as EnemyConfiguration
from ...common_components.fileprocessing_framework import fileprocessing_module as File

class DefineEnemyConfigurationLibrary:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self):

		self.enemyitem = []
		self.populatelibrary()


	def populatelibrary(self):

		# Read in the data from a file into a simple string list
		rawconfigs = File.readfromdisk(File.concatenatepaths("configs", "Enemies.txt"))
		
		# Loop over all lines of data
		for configitem in rawconfigs:

			# Create a new enemy configuration object
			newenemyconfig = EnemyConfiguration.createconfig()

			# Get the tabulated data
			tabulatedlist = File.extracttabulateddata(configitem)
			
			# Loop over the tabulated pairs
			for tabulateditem in tabulatedlist:
			
				# Extract the first data field name and the rest of the line
				fieldname, fieldvalue = File.extractdatapair(tabulateditem)

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
		