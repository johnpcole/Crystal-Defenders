from . import defenderunit_class as DefenderUnitClass

def createconfig(baseposition, movespeed, combatspeed, combatstrength, battleradius, defendertype, groundsize,
																strikeradius, collateralradius, realm, ammunition):
	return DefenderUnitClass.DefineDefenderUnit(baseposition, movespeed, combatspeed, combatstrength, battleradius,
										defendertype, groundsize, strikeradius, collateralradius, realm, ammunition)

