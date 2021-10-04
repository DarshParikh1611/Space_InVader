import pygame; print("\n")
from spin_assets import SPIN_ASSET_LOADING as asset
from spin_menu import MenuPage as menu
import spin_functions as sfunc

spin_screen = asset.spin_xy(); win_xy = asset.spin_xy()
bimg = asset.bg_img(); space_background = sfunc.img_loadscale(bimg, win_xy)
SPIN_GAME_SCREEN = pygame.display.set_mode(spin_screen)

def splash_screen(): pass


menu.main_menu(SPIN_GAME_SCREEN, space_background)


#TODO: Make this the main function with everything in here...if possible.