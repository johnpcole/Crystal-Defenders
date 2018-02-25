

# ---------------------------------------------
# Returns a list of strings, extracted from a
# single string of tab separated substrings
# ---------------------------------------------

def extracttabulateddata(fileline):

	splitdata = fileline.split("\t")
	return splitdata



# ---------------------------------------------
# Returns a list of strings, extracted from a
# single string of comma-space separated substrings
# ---------------------------------------------

def extractcommadata(fileline):

	splitdata = fileline.split(", ")
	return splitdata



# ---------------------------------------------
# Returns a list of two strings, extracted from a
# single string of space-equals-space separated substrings
# ---------------------------------------------

def extractdatapair(dataitem):

	splitdata = dataitem.split(" = ")
	return splitdata[0], splitdata[1]



