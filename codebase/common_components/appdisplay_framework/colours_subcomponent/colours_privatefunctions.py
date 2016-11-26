def getrgbtriplet(tripletstring):
	outcome = (int(tripletstring[0:3]), int(tripletstring[4:7]), int(tripletstring[8:11]))
	return outcome


def getcolourmixvalues(mixturestring):
	mixture = mixturestring.split("/")
	colourone = mixture[0]
	colourtwo = mixture[2]
	mixpercent = float(mixture[1])
	return colourone, colourtwo, mixpercent


def getmixturetriplet(tripletone, triplettwo, fraction):
	onered, onegreen, oneblue = tripletone
	twored, twogreen, twoblue = triplettwo
	mixred = (onered * fraction) + (twored * (1.0 - fraction))
	mixgreen = (onegreen * fraction) + (twogreen * (1.0 - fraction))
	mixblue = (oneblue * fraction) + (twoblue * (1.0 - fraction))
	mix = (int(mixred), int(mixgreen), int(mixblue))
	return mix


#def gettransparentquadlet(tripletone, fraction):
#	onered, onegreen, oneblue = tripletone
#	onealpha = 255.0 * fraction
#	mix = (int(onered), int(onegreen), int(oneblue), int(onealpha))
#	return mix