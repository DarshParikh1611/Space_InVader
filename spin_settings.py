import pygame
from spin_assets import SPIN_ASSET_LOADING as ASSET
from spin_menu_buttons import Button

class SettingsPage:
    @staticmethod
    def menu_returner(text_prompt, page_running):
        if text_prompt == "Back_Menu":
            page_running = False

        return page_running

    @staticmethod
    def settings_draw(settings_window, all_buttons):
        settings_window.fill((0,0,0))
        all_buttons.all_button_draw()

        pygame.display.update()

    @classmethod
    def settings_open(cls, settings_window):
        cls.settings_page(settings_window)

    @classmethod
    def settings_page(cls, settings_win):
        sd_x, sd_y = settings_win.get_size()
        returnToMenu = Button.button_maker("return to menu", settings_win, (sd_x-90, sd_y-60), (80,50))
        settings_running = True
        mouse_up, mouse_down = (-1, -1), (-1, -1)

        while settings_running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    settings_running = False
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mouse_down = pygame.mouse.get_pos()
                elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                    mouse_up = pygame.mouse.get_pos()

            if (mouse_up != (-1, -1)) and (mouse_down != (-1,-1)):
                what_clicked = Button.check_if_clicked(mouse_up, mouse_down)
                settings_running = cls.menu_returner(what_clicked, settings_running)
                mouse_up, mouse_down = (-1, -1), (-1, -1)

            cls.settings_draw(settings_win, Button)
        
        Button.clear_buttons()

if __name__ == '__main__':
    dummy_screen = pygame.display.set_mode(ASSET.spin_xy())
    SettingsPage.settings_open(dummy_screen)