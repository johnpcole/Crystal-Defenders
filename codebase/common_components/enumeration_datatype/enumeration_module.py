from . import enumeration_class as EnumerationClass



def createenum(valuelist, initialvalue):
	newenum = EnumerationClass.DefineEnumeration(valuelist, initialvalue)
	return newenum



def copyexisting(existingobject):
	newenum = EnumerationClass.DefineEnumeration(existingobject.displaylist(), existingobject.displaycurrent())
	return newenum
