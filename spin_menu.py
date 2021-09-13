import pygame
from spin_menu_buttons import Button
from spin_assets import SPIN_ASSET_LOADING as ASSET
from spin_settings import SettingsPage as setting_pge
from spin_game import SpaceInvaderGame as actual_game

def page_opener(page_prompt, page_screen):                                      #? Just send events over?
    if page_prompt == "Start_Game":
        menu_button_backup = Button.button_backup()
        Button.clear_buttons()
        actual_game.start_game(page_screen)
        Button.button_restore(menu_button_backup)
    elif page_prompt == "Open_Settings":
        menu_button_backup = Button.button_backup()
        Button.clear_buttons()
        setting_pge.settings_open(page_screen)
        Button.button_restore(menu_button_backup)
    elif page_prompt == "Create_Custom":
        print("\nwill create a custom game...\n    Whenever I choose to actually make its program...\n")
    # elif page_prompt == "Back_Menu":
    #     print("will go back to main menu")
    else:
        print("Not a valid page to go to")

def menu_display(displ_screen, all_buttons):
    displ_screen.fill((0,0,0))
    all_buttons.all_button_draw()

    pygame.display.update()

def main_menu(menu_displ):
    mds_x, mds_y = menu_displ.get_size()
    Button.button_maker("settings", menu_displ, (mds_x-60, mds_y-60), (50, 50))
    Button.button_maker("play", menu_displ, (mds_x/2 - 80, mds_y/2 - 50), (80, 50))
    Button.button_maker("custom play", menu_displ, (mds_x/2 + 80, mds_y/2 - 50), (80, 50))
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
            page_opener(what_clicked, menu_displ)
            mouse_up, mouse_down = (-1, -1), (-1, -1)

        menu_display(menu_displ, Button)

    print(79 * "#")
    print("Regards, Darsh. Happy gaming!! :)")
    Button.clear_buttons()

if __name__ == '__main__':
    dummy_screen = pygame.display.set_mode(ASSET.spin_xy())
    main_menu(dummy_screen)
