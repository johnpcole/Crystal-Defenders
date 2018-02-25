from . import appdisplay_class as AppWindowClass
from ..vector_datatype import vector_module as Vector


# ---------------------------------------------
# Builds a Display window
# ---------------------------------------------

def createwindow(windowsize, windowtitle):
	return AppWindowClass.DefineApplicationWindow(windowsize, windowtitle)



def createfullscreendisplay(windowtitle):
	return AppWindowClass.DefineApplicationWindow(Vector.createorigin(), windowtitle)
