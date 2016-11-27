from ...common_components.vector_datatype import vector_module as Vector
from operator import attrgetter # , itemgetter, methodcaller
from actordrawlist_subcomponent import actordrawlist_module as DisplayActor
from actoreraselist_subcomponent import actoreraselist_module as EraseBlock



class DefineActorList:
	# ==========================================================================================
	# Object Setup
	# ==========================================================================================



	def __init__(self):

		# Sets up the library of actors, to efficiently determine z-orders
		self.actors = []

		# Sets up the library of field blocks to redraw, to efficiently erase actors
		self.blocks = []

		# Sets up the list of field block ids
		self.blockids = []


	# ==========================================================================================
	# Perform Actions
	# ==========================================================================================



	# -------------------------------------------------------------------
	# Add an actor to the actors list,
	# and its equivalent blocks to the erase list
	# -------------------------------------------------------------------

	def additem(self, itemname, itemposition, itemdimensions, itemzorder, itemhealth, field):

		# Add actor to list for painting the actor
		self.addactortoactorlist(itemname, itemposition, itemdimensions, itemzorder, itemhealth)

		# Add actor equivalent blocks to list for erasing the actor
		self.addactortoeraselist(itemposition, itemdimensions, field)



	# -------------------------------------------------------------------
	# Clears the actor and erase lists
	# -------------------------------------------------------------------

	def clearlists(self):

		del self.actors[:]
		del self.blocks[:]
		del self.blockids[:]



	# -------------------------------------------------------------------
	# Clears the actor and erase lists
	# -------------------------------------------------------------------

	def orderactors(self):

		self.actors.sort(key=attrgetter('zorder'))


	# -------------------------------------------------------------------
	# Add an actor to the actors list
	# -------------------------------------------------------------------

	def addactortoactorlist(self, itemname, itemposition, itemdimensions, itemzorder, itemhealth):

		self.actors.append(DisplayActor.createdrawitem(itemposition, itemdimensions, itemname, itemzorder, itemhealth))



	# -------------------------------------------------------------------
	# Add an actors equivalent blocks to the erase list
	# -------------------------------------------------------------------

	def addactortoeraselist(self, itemposition, itemdimensions, field):

		# Get top left and bottom right coordinates in block units
		topleft = field.convertpixeltoblock(itemposition)
		bottomright = field.convertpixeltoblock(Vector.add(itemposition, itemdimensions))

		# Loop over all blocks within the actor's image
		block = Vector.createblank()
		for blockx in range(topleft.getx(), bottomright.getx() + 1):
			for blocky in range(topleft.gety(), bottomright.gety() + 1):

				# Add an erase block instruction
				block.setfromvalues(blockx, blocky)
				self.adduniqueblocktoeraselist(block, field)




	# -------------------------------------------------------------------
	# Add blocks to the erase list, if they're not already on it
	# -------------------------------------------------------------------

	def adduniqueblocktoeraselist(self, blockposition, field):

		# Only add the block if it's in the field confines
		if field.issingleblockonboard(blockposition) == True:

			# Create the block's unique identifier
			thisidentifier = blockposition.getx() + (1000 * blockposition.gety())

			# Only add the block if it's not already on the list
			if (thisidentifier in self.blockids) == False:

				# Add to erase lists
				self.addblocktoeraselist(blockposition, thisidentifier, field)



	# -------------------------------------------------------------------
	# Add an individual block to the erase & identifier lists
	# -------------------------------------------------------------------

	def addblocktoeraselist(self, blockposition, blockidentifier, field):

		# Add identifier to identifier list
		self.blockids.append(blockidentifier)

		# Add block's pixel position and ground type to erase list
		self.blocks.append(EraseBlock.createeraseitem(field.convertblocktopixel(blockposition),
																				field.getgroundtype(blockposition)))



	# ==========================================================================================
	# Get Information
	# ==========================================================================================

# Getters are not used for this class, because the class's sole object instance is a child of
# of another object, and the parent is the only thing which interacts with this object


