import pygame
from spin_buttons import Button
from spin_assets import SPIN_ASSET_LOADING as ASSET
from spin_settings import SettingsPage as setting_pge
from spin_game import SpaceInvaderGame as actual_game
import spin_custom as custom_pge

menu_txt_fnt = ASSET.menu_font()

class MenuPage:
    TOP_TEXT = "SPACE INVADERS"
    MENU_FONT = pygame.font.Font(menu_txt_fnt, 50)
    MENU_TEXT = MENU_FONT.render(TOP_TEXT, 1, (255,255,255))
    MTXT_width, MTXT_height = MENU_TEXT.get_size()

    @staticmethod
    def page_opener(page_prompt, page_screen, page_background):
        menu_button_backup = Button.button_backup()
        Button.clear_buttons()
        if page_prompt == "Start_Game":
            actual_game.start_game(page_screen, page_background)
        elif page_prompt == "Open_Settings":
            setting_pge.settings_open(page_screen, page_background)
        elif page_prompt == "Create_Custom":
            custom_pge.custom_page(page_screen, page_background)
        Button.button_restore(menu_button_backup)

    @classmethod
    def menu_display(cls, displ_screen, background_img, all_buttons):
        displ_screen.fill((0,0,0))
        displ_screen.blit(background_img, (0,0))
        
        midt, ht = cls.MTXT_width / 2, cls.MTXT_height
        midx, hx = displ_screen.get_width() / 2, displ_screen.get_height()
        tx, ty = midx - midt, hx - (hx/2) - ht
        displ_screen.blit(cls.MENU_TEXT, (tx, ty))
        
        all_buttons.all_button_draw()
        
        pygame.display.update()

    @classmethod
    def main_menu(cls, menu_displ, bground):
        mds_x, mds_y = menu_displ.get_size()
        settings_x, settings_y = mds_x - 60, mds_y - 60
        play_x, play_y = (mds_x / 2) - 80, mds_y - (mds_y / 2) + 50
        custom_x, custom_y = (mds_x / 2) + 80, mds_y - (mds_y / 2) + 50
        Button.button_maker("settings", menu_displ, (settings_x, settings_y))
        Button.button_maker("play", menu_displ, (play_x, play_y))
        Button.button_maker("custom play", menu_displ, (custom_x, custom_y))
        menu_running = True
        mouse_up, mouse_down = (-1, -1), (-1, -1)

        while menu_running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    menu_running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = pygame.mouse.get_pos()
                elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                    mouse_up = pygame.mouse.get_pos()

            if (mouse_up != (-1, -1)) and (mouse_down != (-1,-1)):
                what_clicked = Button.check_if_clicked(mouse_up, mouse_down)
                cls.page_opener(what_clicked, menu_displ, bground)
                mouse_up, mouse_down = (-1, -1), (-1, -1)

            cls.menu_display(menu_displ, bground, Button)

        print(79 * "#" + "\n" + "Regards, Darsh. Happy gaming!! :)")
        Button.clear_buttons()
