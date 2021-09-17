import pygame as pg

def img_loadscale(img, dimensions, rotate=0):
    loaded_img = pg.image.load(img)
    scaled_img = pg.transform.scale(loaded_img, dimensions)
    transformed_img = pg.transform.rotate(scaled_img, rotate)
    return transformed_img