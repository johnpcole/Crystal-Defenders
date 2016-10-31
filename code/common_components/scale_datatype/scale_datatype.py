from scale_class import DefineScale



def createfull(maxval):
	newscale = DefineScale(maxval)
	return newscale



def createempty(maxval):
	newscale = DefineScale(maxval)
	newscale.discharge()
	return newscale



def partitionintobuckets(rangemax, partitions, valuetobucket):
	partitionsize = (float(rangemax * 1.01) / float(partitions))
	return int(float(valuetobucket) / partitionsize)



def keepsubrangeinrange(rangestart, rangewidth, subrangestart, subrangewidth):
	if subrangestart < rangestart:
		finaldestination = rangestart
	elif (subrangestart + subrangewidth - 1) > (rangestart + rangewidth - 1):
		finaldestination = rangestart + rangewidth - subrangewidth
	else:
		finaldestination = subrangestart
	return finaldestination



def getrangeoverhang(rangestart, rangewidth, subrangestart, subrangewidth):
	overhangstart = subrangestart
	overhangwidth = subrangewidth
	if subrangestart < rangestart:
		overhangstart = subrangestart
		overhangwidth = min((rangestart + 1 - subrangestart), subrangewidth)
	elif subrangestart + subrangewidth > rangewidth:
		overhangstart = max(rangestart + rangewidth, subrangestart)
		overhangwidth = subrangewidth + min((subrangestart - (rangestart + rangewidth)), 0)
	return overhangstart, overhangwidth
