

import Libs.kernelPygame

#!!! original resolution : (1200,900) !!!
window = kernelPygame.Graphics(resRatio=4/3)
#!!! relative window (nice, userfriendly) !!!
screen_ratio = window.screen_l/1200

exit = False
while not(exit):
	window.displayBackgroundUpdate()

	
	exit = window()