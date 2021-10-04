import os
# import pygame

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

WHITE = (255,255,255)
PLAYER_OUTLINE = (160,160,160)
GREEN_OUTLINE = (0,255,0)
RED_OUTLINE = (255,0,0)

SPIN_WIDTH, SPIN_HEIGHT = 800, 800

PLAYERS = 1
FPS = 60
PLAYER_SIDE = 50
ENEM_SIDE = 50
LSER_W, LSER_H = 100, 90
VEL = 10
PLAYER_COOLDOWN = 20

# possible: "keyboard_space" or "arrow_enter"
ALL_CONTROLS = {
    'FIRST_CONTROLS': (True, "arrow_enter"), 
    'SECOND_CONTROLS': (False, ""), 
    'THIRD_CONTROLS': (False, "")
}

BACKGROUND_IMAGE = os.path.join('assets', 'background-black.png')

GREEN_SHIP_IMAGE = os.path.join('assets', 'pixel_ship_green_small.png')
RED_SHIP_IMAGE = os.path.join('assets', 'pixel_ship_red_small.png')
BLUE_SHIP_IMAGE = os.path.join('assets', 'pixel_ship_blue_small.png')
PLAYER_SHIP_IMAGE = os.path.join('assets', 'pixel_ship_yellow.png')

LASER_GREEN_IMAGE = os.path.join('assets', 'pixel_laser_green.png')
LASER_RED_IMAGE = os.path.join('assets', 'pixel_laser_red.png')
LASER_BLUE_IMAGE = os.path.join('assets', 'pixel_laser_blue.png')
LASER_PLAYER_IMAGE = os.path.join('assets', 'pixel_laser_yellow.png')

MENU_FONT = os.path.join('fonts', 'OCRAEXT.TTF')
BUTTON_FONT = os.path.join('fonts', '8514sys.fon')
BACKUP_BUTTON_FONT = os.path.join('fonts', 'backup', 'GOST_common.ttf')
SCORE_FONT = os.path.join('fonts', 'ROGFonts-Regular.otf')
BACKUP_SCORE_FONT = os.path.join('fonts', 'backup', 'GOST_common.ttf')

class SPIN_ASSET_LOADING:                                                       # Make a screen centre coordinate?
    @staticmethod
    def spin_w():
        return SPIN_WIDTH

    @staticmethod
    def spin_h():
        return SPIN_HEIGHT

    @staticmethod
    def spin_xy():
        return SPIN_WIDTH, SPIN_HEIGHT

    @staticmethod
    def number_of_players():
        return PLAYERS
    
    @staticmethod
    def get_fps():
        return FPS

    @staticmethod
    def pl_side():
        return PLAYER_SIDE

    @staticmethod
    def player_xy():
        return PLAYER_SIDE, PLAYER_SIDE

    @staticmethod
    def enem_side():
        return ENEM_SIDE

    @staticmethod
    def enem_xy():
        return ENEM_SIDE, ENEM_SIDE

    @staticmethod
    def laser_x():
        return LSER_W

    @staticmethod
    def laser_y():
        return LSER_H

    @staticmethod
    def laser_xy():
        return LSER_W, LSER_H

    @staticmethod
    def get_vel():
        return VEL

    @staticmethod
    def pl_cooldown():
        return PLAYER_COOLDOWN

    @staticmethod
    def control_set():
        controls_list = []
        for i in ALL_CONTROLS:
            if ALL_CONTROLS.get(i)[0]:
                controls_list.append(ALL_CONTROLS.get(i)[1])
        return controls_list

    @staticmethod
    def bg_img():
        return CURR_DIR + "\\" + BACKGROUND_IMAGE

    @staticmethod
    def green_ship():
        return CURR_DIR + "\\" + GREEN_SHIP_IMAGE

    @staticmethod
    def red_ship():
        return CURR_DIR + "\\" + RED_SHIP_IMAGE

    @staticmethod
    def blue_ship():
        return CURR_DIR + "\\" + BLUE_SHIP_IMAGE

    @staticmethod
    def player_ship():
        return CURR_DIR + "\\" + PLAYER_SHIP_IMAGE

    @staticmethod
    def green_laser():
        return CURR_DIR + "\\" + LASER_GREEN_IMAGE

    @staticmethod
    def red_laser():
        return CURR_DIR + "\\" + LASER_RED_IMAGE

    @staticmethod
    def blue_laser():
        return CURR_DIR + "\\" + LASER_BLUE_IMAGE

    @staticmethod
    def player_laser():
        return CURR_DIR + "\\" + LASER_PLAYER_IMAGE

    @staticmethod
    def player_outline():
        return PLAYER_OUTLINE

    @staticmethod
    def red_outline_clr():
        return RED_OUTLINE
    
    @staticmethod
    def green_outline_clr():
        return GREEN_OUTLINE
    
    @staticmethod
    def menu_font():
        return CURR_DIR + "\\" + MENU_FONT
    
    @staticmethod
    def button_font():
        return CURR_DIR + "\\" + BUTTON_FONT

    @staticmethod
    def backup_button_font():
        return CURR_DIR + "\\" + BACKUP_BUTTON_FONT

    @staticmethod
    def score_font():
        return CURR_DIR + "\\" + SCORE_FONT

    @staticmethod
    def backup_score_font():
        return CURR_DIR + "\\" + BACKUP_SCORE_FONT
