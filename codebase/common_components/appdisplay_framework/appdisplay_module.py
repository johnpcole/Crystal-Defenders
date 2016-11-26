from . import appdisplay_class as AppWindowClass



# ---------------------------------------------
# Builds a Display window
# ---------------------------------------------

def createwindow(windowsize, windowtitle):
	return AppWindowClass.DefineApplicationWindow(windowsize, windowtitle)

