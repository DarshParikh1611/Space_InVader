import pygame; print("\n")
from spin_assets import SPIN_ASSET_LOADING as asset
from spin_menu import main_menu

spin_screen = asset.spin_xy()
SPIN_GAME_SCREEN = pygame.display.set_mode(spin_screen)

def splash_screen(): pass


main_menu(SPIN_GAME_SCREEN)


#TODO: Make this the main function with everything in here...if possible.