

import assets.libs.kernelPygame as kernelPygame
from classes import *
from savefilesystem import *

#Setup pygame

#!!! original resolution : (1200,900) !!!
window = kernelPygame.Graphics(resRatio=4/3)
#!!! relative window (nice, userfriendly) !!!
screen_ratio = window.screen_l/1200

window.bckg = "assets/img/bckg.bmp"

#Setup des variables de controlflow du prog
exit = False
formulaMode = True
modelMode = False

#preload d'un modèle et d'une formule
unpacking = Userdata()
unpacking.load(fileset="0",defaultDataFolder = True)
preLoadedModel = unpacking.model
preLoadedFormula = unpacking.formula
del unpacking


while not(exit):
	window.displayBackgroundUpdate()

	if formulaMode :
		#GUI pour la formule
		pass

	if modelMode :
		#GUI pour le modèle
		pass
	
	exit = window()