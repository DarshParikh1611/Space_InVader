import pygame as pg

def img_loadscale(img, dimensions, rotate=0):
    '''
    Returns a pygame loaded image with all the necessary transformations
    '''
    loaded_img = pg.image.load(img)
    scaled_img = pg.transform.scale(loaded_img, dimensions)
    transformed_img = pg.transform.rotate(scaled_img, rotate)
    return transformed_img

def keybinds(the_control_set):
    '''
    Takes in a string, either "keyboard_space" or "arrow_enter"
    
    Gives a list containing the pygame keys on which the controls are
    '''
    keybind = None
    if the_control_set == "keyboard_space":
        keybind = [(pg.K_a, "left"), (pg.K_d, "right"), (pg.K_SPACE, "shoot")]
    if the_control_set == "arrow_enter":
        keybind = [(pg.K_LEFT, "left"), (pg.K_RIGHT, "right"), (pg.K_RETURN, "shoot")]
        
    return keybind