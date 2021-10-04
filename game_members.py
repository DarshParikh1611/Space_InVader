import pygame as pg
import random as rndm
from spin_assets import SPIN_ASSET_LOADING as AST
import spin_events as s_event
import spin_functions as sfuncs

pl_ship = AST.player_ship(); pl_lser = AST.player_laser()
green_ship = AST.green_ship(); green_lser = AST.green_laser()
red_ship = AST.red_ship(); red_lser = AST.red_laser()
player_side = AST.pl_side(); enemy_side = AST.enem_side()
pl_xy = AST.player_xy(); e_xy = AST.enem_xy(); lser_xy = AST.laser_xy()
cooldown = AST.pl_cooldown(); win_xy = AST.spin_xy()
pl_outline = AST.player_outline()
green_outline = AST.green_outline_clr(); red_outline = AST.red_outline_clr()

RIGHT_EDGE = pg.Rect(win_xy[0], 0, 1, win_xy[1])
LEFT_EDGE = pg.Rect(-1, 0, 1, win_xy[1])

def list_clearer(some_lst, action="clear"):
    if action == "clear":
        some_lst.clear()
    elif action == "delete":
        for i in some_lst:
            del i
        del some_lst
    else:
        print("Not a valid action")


class Player:
    P_IMG = sfuncs.img_loadscale(pl_ship, pl_xy)
    P_OUTLINE = pl_outline
    PL_COOLDOWN = cooldown
    MAX_HEALTH = 100

    all_players = []
    all_keybindings = {}                                                        #* {pg.K_UP: (action, self), pg.K_DOWN: (action, self), ...}

    @classmethod
    def clear_players(cls, what_action="clear"):
        list_clearer(cls.all_players, what_action)

    @classmethod
    def player_handler(cls, all_keys_pressed, movement_speed):
        for i in cls.all_keybindings:
            if all_keys_pressed[i]:
                what_action = cls.all_keybindings.get(i)[0]
                who = cls.all_keybindings.get(i)[1]
                cls.action_handler(what_action, who, movement_speed)

    @staticmethod
    def action_handler(what_action, who, move_speed):
        if what_action == "shoot":
            who.pl_shoot()
        else:
            who.pl_move(what_action, move_speed)

    @classmethod
    def all_player_draw(cls):
        for p in cls.all_players:
            p.pl_draw()

    @classmethod
    def all_players_lser_coll(cls, laser_list):
        for p in cls.all_players:
            p.pl_lser_coll(laser_list)

    @classmethod
    def all_player_cooldown(cls):
        for p in cls.all_players:
            p.pl_cooldown_countdown()

    @classmethod
    def remove_killed(cls):
        for p in cls.all_players:
            if p.is_dead():
                cls.all_players.pop(cls.all_players.index(p))
                del p

        if cls.all_dead():
            pg.event.post(s_event.All_Dead)

    @classmethod
    def all_dead(cls):
        if len(cls.all_players) > 0:
            return False
        else:
            return True

    def __init__(self, pl_scrn, pl_side, personal_controls):
        self.pscreen = pl_scrn
        self.pscr_x, self.pscr_y = self.pscreen.get_size()
        self.side = pl_side
        for i in personal_controls:
            Player.all_keybindings[i[0]] = (i[1], self)
        self.pl_img = Player.P_IMG
        self.rect = self.pl_img.get_rect()
        tempx, tempy = (self.pscr_x/2 - self.side/2), (self.pscr_y - self.side - 20)  #* some formula
        self.rect.topleft = tempx, tempy
        self.health_bar = pg.Rect(tempx, tempy + self.side, self.side, 10)      #* 10 --> formula...
        self.health = Player.MAX_HEALTH
        self.cooldown_count = 0

        Player.all_players.append(self)

    def get_curr_plscreen(self):
        return self.pscreen

    def get_pscr(self):
        return self.pscr_x, self.pscr_y
    
    def get_pside(self):
        return self.side

    def get_psize(self):
        return self.side, self.side

    def get_plrect(self):
        return self.rect
    
    def get_plloc(self):
        return self.rect.x, self.rect.y
    
    def set_plloc(self, direc, dst):
        if direc == "left": 
            self.rect.x -= dst
            self.health_bar.x -= dst
        if direc == "right": 
            self.rect.x += dst
            self.health_bar.x += dst

    def get_health(self):
        return self.health
    
    def set_health(self, health_val):
        self.health = health_val

    def get_cooldown_counter(self):
        return self.cooldown_count

    def set_cooldown_count(self, cd_val):
        self.cooldown_count = cd_val
    
    def get_pl_indx(self):
        return Player.all_players.index(self)

    def updated_health_bar(self):
        changed_lenght = (self.get_health() / 100) * self.side
        self.health_bar.width = changed_lenght
        return self.health_bar

    def is_dead(self):
        if self.get_health() == 0:
            return True
        else:
            return False
    
    def pl_move(self, pl_move_direction, distance):
        pl_locx = self.get_plloc()[0]
        win_right_edge = self.get_pscr()[0]-self.get_pside()
        if pl_move_direction == "right" and pl_locx < win_right_edge:
            self.set_plloc("right", distance)
        elif pl_move_direction == "left" and pl_locx > 0:
            self.set_plloc("left", distance)

    def pl_lsr_coll(self, lasers):
        plobj_rect = self.get_plrect()
        for hit_lser in lasers:
            if hit_lser.get_lrect().colliderect(plobj_rect):
                self.set_health(self.get_health() - 10)
                hit_lser.l_delete()

    def pl_cooldown_countdown(self):
        cd_c = self.get_cooldown_counter()
        if cd_c <= Player.PL_COOLDOWN and cd_c > 0:
            self.set_cooldown_count(cd_c - 1)

    def pl_shoot(self):
        if self.get_cooldown_counter() == 0:
            Laser(self)
            self.set_cooldown_count(Player.PL_COOLDOWN)

    def player_destroy(self):
        Player.all_players.pop(self.get_pl_indx())
        del self

    def health_color(self):
        curr_health = self.get_health()
        if curr_health == 0:
            health_clr = (0, 0, 0)
        elif curr_health < (33/100 * Player.MAX_HEALTH):
            health_clr = (255, 0, 0)
        elif (33/100 * Player.MAX_HEALTH) < curr_health < (66/100 * Player.MAX_HEALTH):
            health_clr = (255, 255, 0)
        else:
            health_clr = (25, 255, 64)
        return health_clr

    def pl_draw(self):
        self.pscreen.blit(self.pl_img, self.get_plloc())
        pg.draw.rect(self.pscreen, self.health_color(), self.updated_health_bar())

        pl_out = pg.Rect((self.get_plrect().topleft), (self.get_psize()))
        pg.draw.rect(self.pscreen, Player.P_OUTLINE, pl_out, 1)

    def __repr__(self):
        return "The Main Players"

class Laser:
    P_LASER_IMG = sfuncs.img_loadscale(pl_lser, lser_xy)
    G_LASER_IMG = sfuncs.img_loadscale(green_lser, lser_xy)
    R_LASER_IMG = sfuncs.img_loadscale(red_lser, lser_xy)
    l_OPTIONS = [P_LASER_IMG, G_LASER_IMG, R_LASER_IMG]
    laser_lst = []

    @classmethod
    def clear_lasers(cls, what_action="clear"):
        list_clearer(cls.laser_lst, what_action)

    @classmethod
    def auto_lser_move(cls, laser_dst):
        for moving_lasers in cls.laser_lst:
            moving_lasers.lser_move(laser_dst)

    @classmethod
    def auto_lser_draw(cls):
        for drawing_lsers in cls.laser_lst:
            drawing_lsers.lser_draw()

    def __init__(self, origin):
        self.originator = origin
        self.creator = type(self.originator)
        if self.creator == Player:
            self.l_screen = origin.get_curr_plscreen()
            self.lser_image = Laser.l_OPTIONS[0]
            self.lser_rect = self.lser_image.get_rect()
            self.lser_rect.x = origin.get_plrect().x - origin.get_pside()/2     # Why do I need to subtract the side-length?? Shouldn't I add??
            self.lser_rect.y = origin.get_plrect().y - origin.get_pside()
        elif self.creator == Enemies:
            self.l_screen = origin.get_curr_escreen()
            desired_img = self.creator.get_e_color() + 1
            self.lser_image = Laser.l_OPTIONS[desired_img]
            self.lser_rect = self.lser_image.get_rect()
            self.lser_rect.top = origin.get_enemrect().bottom

        Laser.laser_lst.append(self)

    def get_lser_creator(self):
        return self.originator

    def get_ltype(self):
        return self.creator

    def get_lser_loc(self):
        return self.lser_rect.x, self.lser_rect.y

    def get_lrect(self):
        return self.lser_rect
    
    def set_lser_height(self, lser_direction, lser_dstnce):
        if lser_direction == "up":
            self.lser_rect.y -= lser_dstnce
        elif lser_direction == "down":
            self.lser_rect.y =+ lser_dstnce

    def get_lserlst_loc(self):
        return Laser.laser_lst.index(self)

    def get_lsersize(self):
        return self.lser_rect.width, self.lser_rect.height

    def lser_delete(self):
        Laser.laser_lst.pop(self.get_lserlst_loc())
        del self
    
    def lser_move(self, lser_distance):
        if self.creator == Player:
            self.set_lser_height("up", lser_distance)
        elif self.creator == Enemies:
            self.set_lser_height("down", lser_distance)

        if self.get_lser_loc()[1] + self.get_lsersize()[1] == 0:
            self.lser_delete()

    def lser_draw(self):
        self.l_screen.blit(self.lser_image, self.get_lser_loc())

    def __repr__(self):
        return f"{self.get_ltype()}'s Laser"

class SpawnLocater:
    def __init__(self, x_dim):
        slr_dimension = (x_dim * 2, x_dim + x_dim/2)
        self.sl_rect = pg.Rect((10, x_dim + 10), slr_dimension)

    def get_spawnrect(self):
        return self.sl_rect

    def get_spr_xy(self):
        return self.sl_rect.x, self.sl_rect.y
    
    def set_slr_x(self, slr_new_pos):
        self.sl_rect.x = slr_new_pos

    def mov_slr_x(self, amnt):
        self.sl_rect.x += amnt

    def coll_with_enem(self, other_enem_lst):
        coll_bool = False
        for other_enem in other_enem_lst:
            if self.get_spawnrect().colliderect(other_enem.get_enemrect()):
                coll_bool = True
                break
        return coll_bool

class Enemies:
    G_SHIP_IMG = sfuncs.img_loadscale(green_ship, e_xy, rotate=180)
    G_OUTLINE = green_outline
    R_SHIP_IMG = sfuncs.img_loadscale(red_ship, e_xy, rotate=180)
    R_OUTLINE = red_outline
    OPTION = [(G_SHIP_IMG, G_OUTLINE, "Green"), (R_SHIP_IMG, R_OUTLINE, "Red")]
    all_elist = []
    ENEM_DIR = "right"
    ENEM_SIDE = enemy_side
    spawn_loc = SpawnLocater(ENEM_SIDE)

    @classmethod
    def clear_enemies(cls, what_action="clear"):
        list_clearer(cls.all_elist, what_action)

    @classmethod
    def newe_loc_finder(cls):                                                   #? Could be made better?
        spl = cls.spawn_loc
        spl.set_slr_x(10)
        while_cntr = 0
        while spl.coll_with_enem(cls.all_elist) and (while_cntr <= len(cls.all_elist)):
            while_cntr += 1
            spl.mov_slr_x(50)

        if (while_cntr == len(cls.all_elist)) and (len(cls.all_elist) != 0):
            return None
        else:
            return spl.get_spr_xy()

    @classmethod
    def enem_generator(cls, enem_draw_win, max_enemy):
        if len(cls.all_elist) < max_enemy:
            e_genloc = cls.newe_loc_finder()
            if e_genloc != None:
                Enemies(enem_draw_win, enemy_side, e_genloc)

    @classmethod
    def auto_shooter(cls, time_cntr, existing_lser_list):
        pass                                                                    #TODO: Shoot if no existing_lser_list

    @classmethod
    def auto_emover(cls, enem_dst):
        enem_invaded = False
        for i in cls.all_elist:
            if RIGHT_EDGE.colliderect(i.get_enemrect()):
                cls.ENEM_DIR = "left"
                for j in cls.all_elist:
                    j.set_enemheight(enem_dst, "down")
            elif LEFT_EDGE.colliderect(i.get_enemrect()):
                cls.ENEM_DIR = "right"
                for j in cls.all_elist:
                    j.set_enemheight(enem_dst, "down")
            if i.get_enemloc()[1] == i.get_curr_escr_xy()[1]:
                pg.event.post(s_event.Invaded)
                enem_invaded = True
                break
        if not enem_invaded:
            for moving_enemy in cls.all_elist:
                moving_enemy.set_enemx(enem_dst)

    @classmethod
    def enem_coll(cls, laser_list, the_main_players):
        for enems in cls.all_elist:
            enems.enem_lser_coll(laser_list)
            enems.enem_player_coll(the_main_players)

    @classmethod
    def auto_enem_draw(cls):
        for drawing_enems in cls.all_elist:
            drawing_enems.enem_draw()

    @classmethod
    def get_spawn_area(cls):
        return cls.spawn_loc

    def __init__(self, e_scrn, e_side, e_spawnxy):
        self.escreen = e_scrn
        self.escreenx, self.escreeny = self.escreen.get_size()
        self.eside = e_side
        self.e_colorgrp = Enemies.OPTION[rndm.randint(0, 1)]
        self.image = self.e_colorgrp[0]
        self.enem_rect = self.image.get_rect()
        Enemies.all_elist.append(self)
        self.enem_rect.x, self.enem_rect.y = e_spawnxy

    def get_curr_escreen(self):
        return self.escreen

    def get_curr_escr_xy(self):
        return self.escreenx, self.escreeny
    
    def get_eside(self):
        return self.eside

    def get_enemsize(self):
        return self.eside, self.eside
    
    def get_colorgrp(self):
        return self.e_colorgrp

    def get_enemrect(self):
        return self.enem_rect

    def get_enemloc(self):
        return self.enem_rect.x, self.enem_rect.y
    
    def set_enemheight(self, edst, enem_direction):
        if enem_direction == "down":
            self.enem_rect.y += edst
        elif enem_direction == "up":
            self.enem_rect.y -= edst
    
    def set_enemx(self, e_dstnc):
        if Enemies.ENEM_DIR == "right":
            self.enem_rect.x += e_dstnc
        if Enemies.ENEM_DIR == "left":
            self.enem_rect.x -= e_dstnc
    
    def get_enemlst_loc(self):
        return Enemies.all_elist.index(self)

    def enem_fall(self, fall_value):
        self.set_enemheight(fall_value, "down")

    def enem_destroy(self):
        Enemies.all_elist.pop(self.get_enemlst_loc())
        del self

    def enem_lser_coll(self, lser_list):
        enem_obj = self.get_enemrect()
        for l in lser_list:
            if l.get_lrect().colliderect(enem_obj) and l.get_ltype() == Player:
                self.enem_destroy()
                l.lser_delete()
                pg.event.post(s_event.Score_Increase)
    
    def enem_player_coll(self, the_players):
        for p in the_players:
            if p.get_plrect().colliderect(self.get_enemrect()):
                self.enem_destroy()
                p.set_health(p.get_health() - 10)

    def coll_with_enem(self, other_enem):
        return self.get_enemrect().colliderect(other_enem.get_enemrect())

    def enem_draw(self):
        self.escreen.blit(self.image, self.get_enemloc())

        e_out = pg.Rect((self.get_enemrect().topleft), (self.get_enemsize()))
        pg.draw.rect(self.escreen, self.get_colorgrp()[1], e_out, 1)

    def __repr__(self):
        return f"{self.get_colorgrp()[2]} Enemy"
