from ..common_components.scale_datatype import scale_module as Scale
from ..common_components.vector_datatype import vector_module as Vector
from ..common_components.appdisplay_framework import appdisplay_module as AppDisplay
from displayactors_subcomponent import displayactors_module as DisplayActorList
from . import display_privatefunctions as DisplayFunction



class DefineDisplay:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self, field, control):

		# Sets up the application window size
		self.displaysize = Vector.add(field.getsize(), Vector.createfromvalues(200, 0))

		# Sets up pygame window related properties & methods and loads images, fonts & custom colours
		self.display = AppDisplay.createwindow(self.displaysize, "Crystal Defenders")
		self.display.addfont("20", "graphics/Font.ttf", 20)
		self.setupcustomcolours()
		self.setupimages()

		# Sets up animation clock for next wave plaque and coins & crystals
		self.miscanimationclock = Scale.createfull(1000)

		# Sets up the list of actors, for efficient painting of defenders, ammo and enemies
		self.actorlist = DisplayActorList.createlist()

		# Stores right-hand location of field for wiping overhang
		self.overhanglocation = Vector.createfromvalues(field.getsize().getx(), 0)
		self.overhangsize = Vector.createfromvalues(self.displaysize.getx() - field.getsize().getx(),
																								field.getsize().gety())

		# Stores the list of buttons to process
		self.buttonlist = control.getbuttoncollection("")
		self.buttonlist.remove("Field")



	# -------------------------------------------------------------------
	# Adds custom colours
	# -------------------------------------------------------------------
	def setupcustomcolours(self):
		self.display.addcolour("Dirty Red", 230, 0, 0)
		self.display.addcolour("Dirty Yellow", 230, 230, 0)
		self.display.addcolour("Dirty Purple", 25, 12, 61)



	# -------------------------------------------------------------------
	# Adds images
	# -------------------------------------------------------------------
	def setupimages(self):

		imagelist = DisplayFunction.getimagedata("graphics/ImageLibrary.txt")

		for imagedata in imagelist:
			imagesplit = imagedata.split("\t")
			self.display.addimage(imagesplit[1], imagesplit[0], imagesplit[1], True)



	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Updates all elements of the screen, flips the display, then
	# removes embellishments from the field ready for the next cycle
	# -------------------------------------------------------------------

	def refreshscreen(self, enemyarmy, defenderarmy, field, control, game):

		self.updatemiscanimation()

		if game.cycledisplay(control) == True:
			self.paintdefendersandenemies(defenderarmy, enemyarmy, field, control)
			self.paintstats(game)
			self.paintnewwaveplaque(enemyarmy, control)
			#self.paintaddorupgradedefenderplaque(control, defenderarmy)
			self.paintbuttons(control)
			#
			self.display.updatescreen()
			#
			self.erasebuttons(control)
			#self.eraseaddorupgradedefenderplaque(control)
			self.erasenewwaveplaque(control, field)
			self.erasestats()
			self.erasedefendersandenemies()



	# -------------------------------------------------------------------
	# Replaces image with field background
	# -------------------------------------------------------------------

	def erase(self, position, dimensions, field):

		origin = field.convertpixeltoblock(position)
		offsetrange = Vector.add(field.convertpixeltoblock(dimensions), Vector.createfromvalues(1, 1))
		offset = Vector.createblank()
		for offsetx in range(0, offsetrange.getx()):
			for offsety in range(0, offsetrange.gety()):
				offset.setfromvalues(offsetx, offsety)
				block = Vector.add(offset, origin)
				if field.issingleblockonboard(block) == True:
					self.display.drawimage(field.getgroundtype(block), field.convertblocktopixel(block))
				else:
					self.display.drawbox(field.convertblocktopixel(block), field.getpixelblockratio(), "Black")



	# -------------------------------------------------------------------
	# Draws the button groups
	# -------------------------------------------------------------------

	def paintbuttons(self, control):

		for buttonname in self.buttonlist:
			buttonobject = control.getbuttonobject(buttonname)
			buttonstate = buttonobject.getstate()

			if buttonstate != "Hidden":
				buttonlocation = buttonobject.getposition()
				self.display.drawimage(buttonname, buttonlocation)

				if buttonstate == "Disabled":
					self.display.drawimage("Overlay - Disabled", buttonlocation)

				else:
					if control.getbuttonhoverstate(buttonname) == True:
						self.display.drawimage("Overlay - Hover", buttonlocation)



	# -------------------------------------------------------------------
	# Erases the button groups
	# -------------------------------------------------------------------

	def erasebuttons(self, control):

		for buttonname in self.buttonlist:
			buttonobject = control.getbuttonobject(buttonname)
			if buttonobject.getstate() != "Hidden":
				self.display.drawrectangle(buttonobject.getposition(), buttonobject.getdimensions(), "Black", "", 0)



	# -------------------------------------------------------------------
	# Gets a list of all defenders and ammo to paint
	# -------------------------------------------------------------------

	def preparedefenders(self, defenderarmy, field):

		for defenderunit in defenderarmy.units:
			self.actorlist.additem(defenderunit.getdisplayframereference(), defenderunit.getdisplaylocation(),
											defenderunit.getdisplaysize(), defenderunit.getdisplayzorder(), -999, field)
			if defenderunit.getammodisplaystatus() == True:
				self.actorlist.additem(defenderunit.getammodisplayframereference(),
										defenderunit.getammodisplaylocation(), defenderunit.getammodisplaysize(),
										defenderunit.getammodisplayzorder(), -999, field)



	# -------------------------------------------------------------------
	# Prepares field selection overlay(s), if necessary
	# -------------------------------------------------------------------

	def preparefieldselection(self, control, field):

		displaymode = control.getfieldselectionoverlay()
		if displaymode != "":
			if displaymode == "Add":
				imagename = "Highlight - Field Allowed"
			elif displaymode == "Upgrade":
				imagename = "Highlight - Defender Base"
			elif displaymode == "Disabled":
				imagename = "Highlight - Field Disallowed"
			else:
				print "Invalid Selection Image"
				imagename = 1/0
			self.actorlist.additem(imagename, control.getselectiondisplaylocation(),
															control.getselectiondisplaysize(), 100000004, -999, field)



	# -------------------------------------------------------------------
	# Gets a list of all enemies to paint
	# -------------------------------------------------------------------

	def prepareenemies(self, enemyarmy, field):

		for enemyunit in enemyarmy.units:
			if enemyunit.getinplaystatus() == True:
				self.actorlist.additem(enemyunit.getdisplayframereference(), enemyunit.getdisplaylocation(),
								enemyunit.getdisplaysize(), enemyunit.getdisplayzorder(), enemyunit.gethealth(), field)



	# -------------------------------------------------------------------
	# Draws defender/ammo/enemy overlay for each actor in list
	# -------------------------------------------------------------------

	def paintactors(self):

		for actor in self.actorlist.actors:
			self.display.drawimage(actor.actorname, actor.coordinates)
			if actor.health > -1:
				self.drawenemyhealth(actor.coordinates, actor.dimensions, actor.health)



	# -------------------------------------------------------------------
	# Draws defender/ammo/enemy overlays
	# -------------------------------------------------------------------

	def paintdefendersandenemies(self, defenderarmy, enemyarmy, field, control):

		# Get list of enemies
		self.prepareenemies(enemyarmy, field)

		# Get list of defenders
		self.preparedefenders(defenderarmy, field)

		# Add selection overlays
		self.preparefieldselection(control, field)

		# Order defenders & enemies to give correct 3D view
		self.actorlist.orderactors()

		# Paint defenders & enemies
		self.paintactors()

		#Clear-up overhaging actors on the right of the screen
		self.display.drawrectangle(self.overhanglocation, self.overhangsize, "Black", "", 0)



	# -------------------------------------------------------------------
	# Erases defender/ammo/enemy overlays
	# -------------------------------------------------------------------

	def erasedefendersandenemies(self):

		# Erase from field
		self.eraseactors()

		# Clear list of defenders & enemies
		self.actorlist.clearlists()



	# -------------------------------------------------------------------
	# Overwrites defender/ammo/enemy sprite overlays with background
	# -------------------------------------------------------------------

	def eraseactors(self):

		for block in self.actorlist.blocks:
			self.display.drawimage(block.blockname, block.coordinates)



	# -------------------------------------------------------------------
	# Paints the enemy health bar at top of enemy sprite
	# -------------------------------------------------------------------

	def drawenemyhealth(self, topleft, dimensions, healthpercentage):

		# Full width of the health bar
		barfullwidth = 40

		# Top left position of the health bar
		topleftcorner = Vector.add(topleft, Vector.createfromvalues(int((dimensions.getx() - barfullwidth) / 2), 0))

		# Draw full width red bar
		self.display.drawrectangle(topleftcorner, Vector.createfromvalues(barfullwidth, 3), "Dirty Red", "", 0)

		# Draw proportional yellow bar
		self.display.drawrectangle(topleftcorner, Vector.createfromvalues(int(barfullwidth * healthpercentage / 100),
																							3), "Dirty Yellow", "", 0)



	# -------------------------------------------------------------------
	# Displays the game stats such as wave, coins and crystals
	# -------------------------------------------------------------------

	def paintstats(self, game):

		# Wave
		self.display.drawtext("Wave " + str(game.getwave()), Vector.createfromvalues(621, 52), "Left", "Yellow", "20")

		# Crystals
		self.display.drawimage("Crystal - " + self.getcrystalanimationframe(game), Vector.createfromvalues(621, 76))
		self.display.drawtext(str(game.getcrystalcount()), Vector.createfromvalues(654, 82), "Left",
																	DisplayFunction.getcrystalcountcolour(game), "20")

		# Coins
		self.display.drawimage("Coin - " + self.getcoinanimationframe(game), Vector.createfromvalues(621, 106))
		self.display.drawtext(str(game.getcoincount()), Vector.createfromvalues(654, 112), "Left",
																	DisplayFunction.getcoincountcolour(game), "20")



	# -------------------------------------------------------------------
	# Displays the game stats such as wave, coins and crystals
	# -------------------------------------------------------------------

	def erasestats(self):

		self.display.drawrectangle(Vector.createfromvalues(620, 50), Vector.createfromvalues(100, 100), "Black", "", 0)



	# -------------------------------------------------------------------
	# Displays the new wave plaque
	# -------------------------------------------------------------------

	def paintnewwaveplaque(self, enemyarmy, control):

		if control.getbetweenwavestate() == True:
			self.display.drawimage("Plaque", Vector.createfromvalues(203, 133))
			self.display.drawtext("Next Wave!", Vector.createfromvalues(303, 150), "Centre", "Yellow", "20")
			self.display.drawcircle(Vector.createfromvalues(303, 230), 46, "Dirty Purple", "", 0)
			self.display.drawimage(enemyarmy.getname() + " - S" + self.getplaqueanimationframe(),
																					Vector.createfromvalues(271, 199))
			self.display.drawtext(enemyarmy.getname(), Vector.createfromvalues(303, 295), "Centre", "Yellow", "20")
			self.display.drawtext(enemyarmy.getinitialhealth(), Vector.createfromvalues(303, 325), "Centre", "Yellow",
																												"20")



	# -------------------------------------------------------------------
	# Erases the new wave plaque
	# -------------------------------------------------------------------

	def erasenewwaveplaque(self, control, field):

		if control.getbetweenwavestate() == True:
			self.erase(Vector.createfromvalues(203, 133), Vector.createfromvalues(210, 310), field)



	# -------------------------------------------------------------------
	# Displays add or upgrade defender plaque
	# -------------------------------------------------------------------

	def paintaddorupgradedefenderplaque(self, control, defenderarmy):

		if control.getcurrentaddorupgrademode() == "Upgrade":
			self.display.drawimage("Plaque", Vector.createfromvalues(600, 200))
			self.display.drawimage("Coin - 0", Vector.createfromvalues(621, 210))
			self.display.drawtext(str(defenderarmy.getdefenderupgradecost()), Vector.createfromvalues(654, 210),
																								"Left", "Yellow", "20")

#			self.draw.text("Next Wave!", Vector.createfromvalues(303, 150), "Centre", "Yellow")
#			self.draw.circle(Vector.createfromvalues(303, 230), 46, "Dirty Purple")
#			self.draw.image(enemyarmy.getname() + " - S" + self.getplaqueanimationframe(), Vector.createfromvalues(271, 199))
#			self.draw.text(enemyarmy.getname(), Vector.createfromvalues(303, 295), "Centre", "Yellow")
#			self.draw.text(enemyarmy.getinitialhealth(), Vector.createfromvalues(303, 325), "Centre", "Yellow")



	# -------------------------------------------------------------------
	# Erases the add or upgrade defender plaque
	# -------------------------------------------------------------------

	def eraseaddorupgradedefenderplaque(self, control):

		if control.getcurrentaddorupgrademode() == "Upgrade":
			self.display.drawbox(Vector.createfromvalues(600, 200), Vector.createfromvalues(100, 100), "Black")



	# -------------------------------------------------------------------
	# Paints the whole field background
	# -------------------------------------------------------------------

	def paintwholefield(self, field):

		currentposition = Vector.createblank()
		screenrange = field.getblocksize()
		for currentpositionx in range(0, screenrange.getx()):
			for currentpositiony in range(0, screenrange.gety()):
				currentposition.setfromvalues(currentpositionx, currentpositiony)
				self.display.drawimage(field.getgroundtype(currentposition), field.convertblocktopixel(currentposition))



	# -------------------------------------------------------------------
	# Updates the misc item animation clock
	# -------------------------------------------------------------------

	def updatemiscanimation(self):

		# Deplete the clock, and recharge if it is at zero
		if self.miscanimationclock.deplete(1) == True:
			self.miscanimationclock.recharge()




	# ==========================================================================================
	# Get Information
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Returns the plaque animation frame, either 1 or 2 AS A STRING
	# -------------------------------------------------------------------

	def getplaqueanimationframe(self):

		# Return modulo so that half the time the clock returns 1, the other half 2
		return str(1 + (self.miscanimationclock.getpartition(10) % 2))



	# -------------------------------------------------------------------
	# Returns the coin animation frame, 0-9 AS A STRING
	# -------------------------------------------------------------------

	def getcoinanimationframe(self, game):

		if game.getcoingainstatus() == True:
			outcome = "10"
		else:
			outcome = str(10 - min(10, self.miscanimationclock.getpartition(200)))

		return outcome



	# -------------------------------------------------------------------
	# Returns the crystal animation frame, 0-7 AS A STRING
	# -------------------------------------------------------------------

	def getcrystalanimationframe(self, game):

		if game.getcrystallossstatus() == True:
			outcome = "8"
		else:
			outcome = str(min(7, 50 - self.miscanimationclock.getpartition(50)))

		return outcome

