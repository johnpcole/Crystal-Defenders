from ..common_components.fileprocessing_framework import fileprocessing_module as File

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
		section = File.extracttabulateddata(dataline)
		sectioncount = len(section)

		if (sectioncount == 2) or (sectioncount == 3):
			subfolder = section[0]
			prefix = section[1]
			if sectioncount == 2:
				imagename = prefix
				outcome.append(subfolder + "\t" + imagename)
			else:
				iterations = File.extractcommadata(section[2])
				for iteration in iterations:
					imagename = prefix + " - " + iteration
					outcome.append(subfolder + "\t" + imagename)
		else:
			print "Invalid image data - ", dataline

	return outcome



# -------------------------------------------------------------------
# Returns the plaque animation frame, either 1 or 2 AS A STRING
# -------------------------------------------------------------------

def getplaqueanimationframe(animationclock):

	# Return modulo so that half the time the clock returns 1, the other half 2
	return str(1 + (animationclock.getpartition(10) % 2))



# -------------------------------------------------------------------
# Returns the coin animation frame, 0-9 AS A STRING
# -------------------------------------------------------------------

def getcoinanimationframe(animationclock, game):

	if game.getcoingainstatus() == True:
		outcome = "10"
	else:
		outcome = str(10 - min(10, animationclock.getpartition(200)))

	return outcome



# -------------------------------------------------------------------
# Returns the crystal animation frame, 0-7 AS A STRING
# -------------------------------------------------------------------

def getcrystalanimationframe(animationclock, game):

	if game.getcrystallossstatus() == True:
		outcome = "8"
	else:
		outcome = str(min(7, 50 - animationclock.getpartition(50)))

	return outcome


# -------------------------------------------------------------------
# Returns the name of the field selection overlay image name
# -------------------------------------------------------------------

def getfieldoverlayimagename(displaymode):

	if displaymode == "Add":
		outcome = "Highlight - Field Allowed"
	elif displaymode == "Upgrade":
		outcome = "Highlight - Defender Base"
	elif displaymode == "Disabled":
		outcome = "Highlight - Field Disallowed"
	else:
		outcome = "???"
		assert displaymode == "Add", "Invalid Field Selection Image"

	return outcome

