import os

WHITE = (255,255,255)
PLAYER_OUTLINE = (160,160,160)
GREEN_OUTLINE = (0,255,0)
RED_OUTLINE = (255,0,0)

SPIN_WIDTH, SPIN_HEIGHT = 800, 800

FPS = 60
PLAYER_SIDE = 50
ENEM_SIDE = 50
LSER_W, LSER_H = 100, 90
VEL = 10
PLAYER_COOLDOWN = 20

BACKGROUND_IMAGE = os.path.join('assets', 'background-black.png')

GREEN_SHIP_IMAGE = os.path.join('assets', 'pixel_ship_green_small.png')
RED_SHIP_IMAGE = os.path.join('assets', 'pixel_ship_red_small.png')
BLUE_SHIP_IMAGE = os.path.join('assets', 'pixel_ship_blue_small.png')
PLAYER_SHIP_IMAGE = os.path.join('assets', 'pixel_ship_yellow.png')

LASER_GREEN_IMAGE = os.path.join('assets', 'pixel_laser_green.png')
LASER_RED_IMAGE = os.path.join('assets', 'pixel_laser_red.png')
LASER_BLUE_IMAGE = os.path.join('assets', 'pixel_laser_blue.png')
LASER_PLAYER_IMAGE = os.path.join('assets', 'pixel_laser_yellow.png')

class SPIN_ASSET_LOADING:                                                       #TODO: Make a screen centre coordinate

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
    def bg_img():
        return BACKGROUND_IMAGE

    @staticmethod
    def green_ship():
        return GREEN_SHIP_IMAGE

    @staticmethod
    def red_ship():
        return RED_SHIP_IMAGE

    @staticmethod
    def blue_ship():
        return BLUE_SHIP_IMAGE

    @staticmethod
    def player_ship():
        return PLAYER_SHIP_IMAGE

    @staticmethod
    def green_laser():
        return LASER_GREEN_IMAGE

    @staticmethod
    def red_laser():
        return LASER_RED_IMAGE

    @staticmethod
    def blue_laser():
        return LASER_BLUE_IMAGE

    @staticmethod
    def player_laser():
        return LASER_PLAYER_IMAGE

    @staticmethod
    def player_outline():
        return PLAYER_OUTLINE

    @staticmethod
    def red_outline_clr():
        return RED_OUTLINE
    
    @staticmethod
    def green_outline_clr():
        return GREEN_OUTLINE
