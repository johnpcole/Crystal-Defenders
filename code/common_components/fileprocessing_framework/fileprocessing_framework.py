def readfromdisk(filename):

	try:
		# Open the file for the duration of this process
		with open(filename) as fileobject:

			# Capture the number of lines read in from the file
			numberoflines = 0

			# Loop over all lines in the file
			for fileline in fileobject.readlines():

				# Only process if the line isn't blank
				if fileline != "":

					# Increment the number of lines
					numberoflines = numberoflines + 1

					# Create the new list
					if numberoflines == 1:
						newfilelist = [fileline.rstrip('\r\n')]

					# Or, append to the existing list
					else:
						newfilelist.append(fileline.rstrip('\r\n'))

	except:
		# Print an error if the file cannot be read
		print "Cannot read file - Configs/Field.txt"

	# If the file is empty, return a single line
	if numberoflines == 0:
		newfilelist = ["!!! Empty File !!!"]
		
	return newfilelist

	
	
def tabulateddata(fileline):

	splitdata = fileline.split("\t")
	return splitdata



def commadata(fileline):
	splitdata = fileline.split(", ")
	return splitdata



def datapair(dataitem):

	splitdata = dataitem.split(" = ")
	return splitdata[0], splitdata[1]
