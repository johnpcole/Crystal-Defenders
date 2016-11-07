from . import enemyunit_class as EnemyUnitClass

def createconfig(startposition, health, speed, coinvalue, groundsize, physicalvulnerability,
				 													magicalvulnerability, flies, crystalvalue, name):
	return EnemyUnitClass.DefineEnemyUnit(startposition, health, speed, coinvalue, groundsize, physicalvulnerability,
				 													magicalvulnerability, flies, crystalvalue, name)

