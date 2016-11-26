from . import actordrawlist_class as ActorDrawItemClass

def createdrawitem(imagelocation, imagedimensions, imagename, imagezorder, imagehealth):
	return ActorDrawItemClass.DefineDisplayActor(imagelocation, imagedimensions, imagename, imagezorder, imagehealth)

