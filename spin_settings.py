import pygame
from spin_assets import SPIN_ASSET_LOADING as ASSET
from spin_buttons import Button

class SettingsPage:
    @staticmethod
    def menu_returner(text_prompt, page_running):
        '''
        Takes in a string prompt, indicating which button was pressed on screen

        If Back button is pressed it signals to close the settings page, 
        ending the process
        '''
        if text_prompt == "Back_Menu":
            page_running = False
        return page_running

    @staticmethod
    def settings_draw(settings_window, settings_background, buttons_class):
        '''
        Takes in the window object, the pygame loaded background image, and the button class

        Displys them all on the settings page
        '''
        settings_window.fill((0,0,0))
        settings_window.blit(settings_background, (0,0))
        buttons_class.all_button_draw()

        pygame.display.update()

    @classmethod
    def settings_open(cls, settings_window, setting_background):
        cls.settings_page(settings_window, setting_background)

    @classmethod
    def settings_page(cls, settings_win, settings_bg):
        '''
        takes in the window object and a pygame loaded background image

        Generates a settings page to edit the 
        '''
        sd_x, sd_y = settings_win.get_size()
        Button.button_maker("return to menu", settings_win, (sd_x-90, sd_y-60)) # Creates the Back button
        settings_run = True
        mouse_up, mouse_down = (-1, -1), (-1, -1)

        while settings_run:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    settings_run = False
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mouse_down = pygame.mouse.get_pos()
                elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                    mouse_up = pygame.mouse.get_pos()

            if (mouse_up != (-1, -1)) and (mouse_down != (-1,-1)):
                what_clicked = Button.check_if_clicked(mouse_up, mouse_down)
                settings_run = cls.menu_returner(what_clicked, settings_run)
                mouse_up, mouse_down = (-1, -1), (-1, -1)

            cls.settings_draw(settings_win, settings_bg, Button)
        
        Button.clear_buttons()                                                  # Cleanup
