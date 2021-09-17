import pygame
import spin_events as SEVE

class Button:
    B_COLOR = (255, 255, 255)
    butt_lst = []

    @classmethod
    def button_backup(cls):
        backup_list = []
        for i in cls.butt_lst:
            backup_list.append(i)
        return backup_list

    @classmethod
    def button_restore(cls, backed_buttons):
        for i in backed_buttons:
            cls.butt_lst.append(i)

    @classmethod
    def clear_buttons(cls):                                                     #? delete?
        # for i in cls.butt_lst:
        #     del i
        cls.butt_lst.clear()

    @classmethod
    def button_maker(cls, button_type, b_screen, xy_loc_tuple, dimension_tuple):
        if button_type == "settings":
            newly_created_button = _SettingsButton(b_screen, xy_loc_tuple, dimension_tuple)
        elif button_type == "custom play":
            newly_created_button = _CustomPlayButton(b_screen, xy_loc_tuple, dimension_tuple)
        elif button_type == "play":
            newly_created_button = _PlayButton(b_screen, xy_loc_tuple, dimension_tuple)
        elif button_type == "return to menu":
            newly_created_button = _MenuReturner(b_screen, xy_loc_tuple, dimension_tuple)
        else:
            print("No button of that type...")
            newly_created_button = None                                         #? Could cause problems? Any better way of making this not work?
        return newly_created_button

    @classmethod
    def check_if_clicked(cls, m_up, m_down):
        clicked_smth = False
        string_prompt = ""
        for button in cls.butt_lst:
            butt_sq = button.get_buttrect()
            upclick = butt_sq.collidepoint(m_up)
            downclick = butt_sq.collidepoint(m_down)
            
            if upclick and downclick:
                button.is_clicked()
                clicked_smth = True
                break

        if clicked_smth:
            for e in pygame.event.get():
                if e.type == SEVE.GAME_PLAY:
                    string_prompt = "Start_Game"
                elif e.type == SEVE.OPEN_SETTINGS:
                    string_prompt = "Open_Settings"
                elif e.type == SEVE.CUSTOM_PLAY:
                    string_prompt = "Create_Custom"
                elif e.type == SEVE.MENU_RETURN:
                    string_prompt =  "Back_Menu"
        else:
            string_prompt = "nothing to do"
        
        return string_prompt

    @classmethod
    def all_button_draw(cls):
        for draw_button in cls.butt_lst:
            draw_button.butt_draw()

    @classmethod
    def get_b_list(cls):                                                        #? Returning original verses a copy?
        return cls.butt_lst

    def __init__(self, spawn_screen, spawn_loc, spawn_size):
        self.b_displ_scr = spawn_screen
        self.butt_rect = pygame.Rect((spawn_loc), (spawn_size))
        Button.butt_lst.append(self)

    def get_buttrect(self):
        return self.butt_rect
    
    def get_bscreen(self):
        return self.b_displ_scr

    def is_clicked(self):
        pass

    def butt_draw(self):
        pygame.draw.rect(self.b_displ_scr, Button.B_COLOR, self.butt_rect, 1)

    def __repr__(self):
        return "Just another random button"

class _SettingsButton(Button):
    def __init__(self, s_screen, s_spawn_loc, s_spawn_size):
        super().__init__(s_screen, s_spawn_loc, s_spawn_size)
    
    def is_clicked(self):
        pygame.event.post(SEVE.Open_Settings)

    def __repr__(self):
        return "The Settings button"

class _PlayButton(Button):
    def __init__(self, p_screen, p_spawn_loc, p_spawn_size):
        super().__init__(p_screen, p_spawn_loc, p_spawn_size)
    
    def is_clicked(self):
        pygame.event.post(SEVE.Game_Play)

    def __repr__(self):
        return "The Play button"

class _CustomPlayButton(Button):
    def __init__(self,c_screen, c_spawn_loc, c_spawn_size):
        super().__init__(c_screen, c_spawn_loc, c_spawn_size)

    def is_clicked(self):
        pygame.event.post(SEVE.Custom_Play)

    def __repr__(self):
        return "The Custom Play button"

class _MenuReturner(Button):
    def __init__(self, m_screen, m_spawn_loc, m_spawn_size):
        super().__init__(m_screen, m_spawn_loc, m_spawn_size)

    def is_clicked(self):
        pygame.event.post(SEVE.Menu_Return)

    def __repr__(self):
        return "The Return to Menu button"
