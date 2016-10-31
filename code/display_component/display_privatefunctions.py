from ..common_components import File

# -------------------------------------------------------------------
# Returns the colour of text for crystal count
# -------------------------------------------------------------------

def getcrystalcountcolour(game):
	if game.getcrystallossstatus() == True:
		outcome = "Red"
	else:
		outcome = "Cyan"

	return outcome



# -------------------------------------------------------------------
# Returns the colour of text for coin count
# -------------------------------------------------------------------

def getcoincountcolour(game):
	if game.getcoingainstatus() == True:
		outcome = "Blue"
	else:
		outcome = "Yellow"

	return outcome



# -------------------------------------------------------------------
# Adds images
# -------------------------------------------------------------------

def getimagedata(filenameandpath):

	outcome = []
	rawdata = File.readfromdisk(filenameandpath)

	for dataline in rawdata:
		section = File.tabulateddata(dataline)
		sectioncount = len(section)

		if (sectioncount == 2) or (sectioncount == 3):
			subfolder = section[0]
			prefix = section[1]
			if sectioncount == 2:
				imagename = prefix
				outcome.append(subfolder + "\t" + imagename)
			else:
				iterations = File.commadata(section[2])
				for iteration in iterations:
					imagename = prefix + " - " + iteration
					outcome.append(subfolder + "\t" + imagename)
		else:
			print "Invalid image data - ", dataline

	return outcome
