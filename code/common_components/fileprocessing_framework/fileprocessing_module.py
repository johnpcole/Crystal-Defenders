def readfromdisk(filename):

	newfilelist = []

	try:
		# Open the file for the duration of this process
		with open(filename) as fileobject:

			# Loop over all lines in the file
			for fileline in fileobject.readlines():

				# Only process if the line isn't blank
				if fileline != "":
					newfilelist.append(fileline.rstrip('\r\n'))

	except:
		# Print an error if the file cannot be read
		print "Cannot read file - Configs/Field.txt"

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
