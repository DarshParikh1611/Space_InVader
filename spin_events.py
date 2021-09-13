import pygame
from pygame.constants import USEREVENT

# ALL_DEAD = USEREVENT + 1
# INVADED = USEREVENT + 3
GAME_OVER = USEREVENT + 1
SCORE_INCREASE = USEREVENT + 2

GAME_PLAY = USEREVENT + 3
OPEN_SETTINGS = USEREVENT + 4
CUSTOM_PLAY = USEREVENT + 5
MENU_RETURN = USEREVENT + 6

All_Dead = pygame.event.Event(GAME_OVER, message = "All Players are Dead :(")
Score_Increase = pygame.event.Event(SCORE_INCREASE)
Invaded = pygame.event.Event(GAME_OVER, message = "The Enemies Invaded :(")
Game_Play = pygame.event.Event(GAME_PLAY)
Open_Settings = pygame.event.Event(OPEN_SETTINGS)
Custom_Play = pygame.event.Event(CUSTOM_PLAY)
Menu_Return = pygame.event.Event(MENU_RETURN)
