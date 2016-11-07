from controls_component import controls_module as Controller
from game_component import game_module as Game
from field_component import field_module as Field
from display_component import display_module as Display
from defenderarmy_component import defenderarmy_module as DefenderArmy
from enemyarmy_component import enemyarmy_module as EnemyArmy
from common_components.userinterface_framework import userinterface_module as GUI



def runapplication():

	# ===============================================================================================================
	GUI.init()
	# ===============================================================================================================

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
	# Define objects used to drive game            #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

	field = Field.createfield()
	enemyarmy = EnemyArmy.createarmy()
	defenderarmy = DefenderArmy.createarmy(field)
	controls = Controller.createcontroller(field, defenderarmy)
	display = Display.createdisplay(field, controls)
	game = Game.creategame()

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# Paint field and Start level 1                 #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	display.paintwholefield(field)

	# ===============================================================================================================
	# ===============================================================================================================

	while controls.getquitstate() == False:

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
		# Process user input and resulting events       #
		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

		# Process any input events (mouse clicks, mouse moves)
		coinstolose = controls.processinput(field)

		# Take coins out of user's account, if necessary for any actions performed
		game.spendcoins(coinstolose)

		# If mouse cursor location on field has changed, and we are in selection mode,
		# update the selection property on the field and defender army objects
		if controls.shouldfieldselectionbeupdated() == True:

			# Update field selection data
			field.updateselection(controls)

			# Update defender selection data
			defenderarmy.updateselection(controls)

			# Update control selection data
			controls.updateselection(field, defenderarmy)

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
		# User tries to add or upgrade a defender to the game   #
		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

		# If the user has clicked on the field, put the game in the correct add or upgrade state
		# (User states intention to add defender to specific field location or upgrade existing defender)
		controls.invokeaddorupgradedefender(game, defenderarmy)

		# If the user has added or upgraded a defender, update the defender army
		if defenderarmy.addorupgradedefender(controls) == True:

		# Add new defender footprint to the field, if a new defender was added to the army
			field.adddefendertofield()

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
		# Process Defenders & Enemies, walking + combat #
		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

		# Only process defenders and enemies if the game is NOT paused
		if controls.getprocesswavestate() == True:

			# Loop over all enemies in the collection
			for currentenemy in enemyarmy.units:

				# Move each enemy along the path
				crystalstolose = currentenemy.move(field)

				# Take crystals out of user's account, if necessary
				game.losecrystals(crystalstolose)

			# Loop over all defenders in the collection
			for currentdefender in defenderarmy.units:

				# Identify the target enemy for each defender
				enemyarmy.identifytargetenemy(currentdefender)

				# Move each defender
				currentdefender.move(field, enemyarmy)

				# Recharge defender's strike, and if ready and on top of enemy, discharge
				# If the strike is successful, follow up with enemy take hit and gain coins actions
				if currentdefender.combatenemy(enemyarmy) == True:

					# Take health away from enemy(s), and if necessary, remove from game if dead
					coinstogain = enemyarmy.takehit(currentdefender, defenderarmy)

					# Add coins to user's account, if necessary
					game.gaincoins(coinstogain)

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
		# If all crystals are gone, game over           #
		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

		# If the game is flagged as game over
		if game.isgameover() == True:

			# Reset game/control variables & Update all button states to reflect new wave plaque
			controls.initialisegame()

			# Set wave to 0, will change to 1 next cycle
			game.initialisegame()

			# Remove Enemies from army collection
			enemyarmy.wipearmy()

			# Remove Defenders from army collection
			defenderarmy.wipearmy()

			# Remove Defenders from field
			field.wipedefendersfromfield()

			# Refresh Screen
			display.refreshscreen(enemyarmy, defenderarmy, field, controls, game)

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
		# Else, if all enemies dead, start next level   #
		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

		# If the game is NOT flagged as game over
		else:

			# If all enemy units are dead
			if enemyarmy.isanyonealive() == False:

				# If all defender units are positioned at their base coordinates
				if defenderarmy.isanyoneawayfrombase() == False:

					# Pause game in "between waves" mode
					controls.startnextlevel()

					# Start next level
					game.startnextlevel()

					# Repopulate enemy army with new enemies for the next level
					enemyarmy.populatearmy(game, field)

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
		# Refresh button states, display and maintain refresh rate  #
		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

		# Refresh screen if all frames are required, or important frames if only some
		display.refreshscreen(enemyarmy, defenderarmy, field, controls, game)

	# ===============================================================================================================
	GUI.quit()
	# ===============================================================================================================

