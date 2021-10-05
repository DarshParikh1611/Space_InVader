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
    '''
    Takes a list and the action to be perfomed. Default action is to clear

    string action = "clear" || "delete"

    Either clears the list or deletes the list, depending on the action
    '''
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
    all_keybindings = {}                                                        #* {pg.K_UP: ("action", obj), pg.K_a: ("action", obj), ...}

    @classmethod
    def clear_players(cls, what_action="clear"):
        '''
        Takes a string prompt about what action to perform. Default action is 
        clear

        string action = "clear" || "delete"

        Performs the desired action on the list of all existing players
        '''
        list_clearer(cls.all_players, what_action)

    @classmethod
    def player_handler(cls, all_keys_pressed, movement_speed):
        '''
        Takes in the pygame event list and the speed at which the player objects
        should move
        
        Figures out if a specific keybinding was pressed. If so it performs the 
        action (moving left, right or shooting) of the player.
        '''
        for i in cls.all_keybindings:
            if all_keys_pressed[i]:
                what_action = cls.all_keybindings.get(i)[0]
                who = cls.all_keybindings.get(i)[1]
                cls.action_handler(what_action, who, movement_speed)

    @staticmethod
    def action_handler(what_action, who, move_speed):
        '''
        Takes in a string action prompt, which player object performs the action
        and the amount the object must move (in case the action was to move)

        string what_action = "shoot" || "left" || "right"

        Instructs the player object to perform the action
        '''
        if what_action == "shoot":
            who.pl_shoot()
        else:
            who.pl_move(what_action, move_speed)

    @classmethod
    def all_player_draw(cls):
        '''
        Draws all the players on their respective window screen(s)
        '''
        for p in cls.all_players:
            p.pl_draw()

    @classmethod
    def all_players_lser_coll(cls, laser_list):
        '''
        Takes the list of laser objects (Laser.lser_list)

        Checks if any of the players has collided with the lasers
        '''
        for p in cls.all_players:
            p.pl_lser_coll(laser_list)

    @classmethod
    def all_player_cooldown(cls):
        '''
        Reduces the cooldown counter for every player
        '''
        for p in cls.all_players:
            p.pl_cooldown_countdown()

    @classmethod
    def remove_killed(cls):
        '''
        Checks if a player is dead and if so removes them
        
        If everyone is dead it posts a pygame event relaying the same
        '''
        for p in cls.all_players:
            if p.is_dead():
                cls.all_players.pop(cls.all_players.index(p))
                del p

        if cls.all_dead():
            pg.event.post(s_event.All_Dead)

    @classmethod
    def all_dead(cls):
        '''
        Checks if there are any players left or not. 

        Returns a boolean
        '''
        if len(cls.all_players) > 0:
            return False
        else:
            return True

    def __init__(self, pl_scrn, pl_side, personal_controls):
        '''
        Takes a window object, the side length of the player, and the 
        keybindings of that player

        Creates the player object. Does not automatically draw them
        '''
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
        '''
        Returns the window object the player resides on
        '''
        return self.pscreen

    def get_pscr(self):
        '''
        Returns the dimensions of the window object the player resides on
        '''
        return self.pscr_x, self.pscr_y
    
    def get_pside(self):
        '''
        Returns the side lenght of the player object
        '''
        return self.side

    def get_psize(self):
        '''
        Returns the width and height of the player object
        '''
        return self.side, self.side

    def get_plrect(self):
        '''
        Returns the player's rect object
        '''
        return self.rect
    
    def get_plloc(self):
        '''
        Returns the player's x and y location on the window
        '''
        return self.rect.x, self.rect.y
    
    def set_plloc(self, direc, dst):
        '''
        Takes in the direction and distance of movement

        str direc = "left" | "right"

        Moves the player object
        '''
        if direc == "left": 
            self.rect.x -= dst
            self.health_bar.x -= dst
        if direc == "right": 
            self.rect.x += dst
            self.health_bar.x += dst

    def get_health(self):
        '''
        Returns the current health of the player
        '''
        return self.health
    
    def set_health(self, health_val):
        '''
        Takes in a health integer

        Sets the player's health to that new health
        '''
        self.health = health_val

    def get_cooldown_counter(self):
        '''
        Returns the cooldown integer of the player
        '''
        return self.cooldown_count

    def set_cooldown_count(self, cd_val):
        '''
        Takes in an integer for the cooldown value

        Sets the cooldown integer to the new value
        '''
        self.cooldown_count = cd_val
    
    def get_pl_indx(self):
        '''
        Return the index of the player from the class list
        '''
        return Player.all_players.index(self)

    def updated_health_bar(self):                                               #? Can't this be done without returning anything?
        '''
        Returns the health bar but after updating its lenght according to the
        player's health
        '''
        changed_lenght = (self.get_health() / 100) * self.side
        self.health_bar.width = changed_lenght
        return self.health_bar

    def is_dead(self):
        '''
        Checks if the player is dead

        Returns a boolean
        '''
        if self.get_health() == 0:
            return True
        else:
            return False
    
    def pl_move(self, pl_move_direction, distance):
        '''
        Takes in the direction of movement and the distance

        str pl_move_direction = "left" || "right"

        Moves the player object in that direction for the specified distance
        '''
        pl_locx = self.get_plloc()[0]
        win_right_edge = self.get_pscr()[0]-self.get_pside()
        if pl_move_direction == "right" and pl_locx < win_right_edge:
            self.set_plloc("right", distance)
        elif pl_move_direction == "left" and pl_locx > 0:
            self.set_plloc("left", distance)

    def pl_lsr_coll(self, lasers):
        '''
        Takes in the Laser class's laser list (Laser.lser_list)

        Checks if the player collided with any lasers from the list
        '''
        plobj_rect = self.get_plrect()
        for hit_lser in lasers:
            if hit_lser.get_lrect().colliderect(plobj_rect):
                self.set_health(self.get_health() - 10)
                hit_lser.l_delete()

    def pl_cooldown_countdown(self):
        '''
        Updates (reduces) the player cooldown if its above 0
        '''
        cd_c = self.get_cooldown_counter()
        if cd_c <= Player.PL_COOLDOWN and cd_c > 0:
            self.set_cooldown_count(cd_c - 1)

    def pl_shoot(self):
        '''
        Shoots a laser
        '''
        if self.get_cooldown_counter() == 0:
            Laser(self)
            self.set_cooldown_count(Player.PL_COOLDOWN)

    def player_destroy(self):
        '''
        Removes the player from the class's player list, and deletes the player
        '''
        Player.all_players.pop(self.get_pl_indx())
        del self

    def health_color(self):
        '''
        Returns a color (r, g, b) depending upon the player's health
        '''
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
        '''
        Draws the player on the window object
        '''
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
        '''
        Takes a string prompt about what action to perform. Default action is
        to clear

        str what_action = "clear" || "delete"

        Either clears or deletes all the lasers in existence
        '''
        list_clearer(cls.laser_lst, what_action)

    @classmethod
    def auto_lser_move(cls, laser_dst):
        '''
        Takes in the distance a laser should travel

        Moves every laser by that much distance
        '''
        for moving_lasers in cls.laser_lst:
            moving_lasers.lser_move(laser_dst)

    @classmethod
    def auto_lser_draw(cls):
        '''
        Draws all the lasers on their respective window object(s)
        '''
        for drawing_lsers in cls.laser_lst:
            drawing_lsers.lser_draw()

    def __init__(self, origin):
        '''
        Takes in an object as the origin, the so called creator who initialized 
        the laser

        Creates a laser object. Doesnt automatically start drawing it
        '''
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
        '''
        Returns the object that created the list
        '''
        return self.originator

    def get_ltype(self):
        '''
        Returns the type (class) of the laser's creator
        '''
        return self.creator

    def get_lser_loc(self):
        '''
        Returns the x and y location of the laser on its window object
        '''
        return self.lser_rect.x, self.lser_rect.y

    def get_lrect(self):
        '''
        Returns the laser's rect object
        '''
        return self.lser_rect
    
    def set_lser_height(self, lser_direction, lser_dstnce):
        '''
        Takes in the direction and distance the laser has to travel

        str lser_direction = "up" || "down"

        Moves the laser
        '''
        if lser_direction == "up":
            self.lser_rect.y -= lser_dstnce
        elif lser_direction == "down":
            self.lser_rect.y =+ lser_dstnce

    def get_lserlst_loc(self):
        '''
        Returns the laser's index in the Laser class's list of existing lasers
        '''
        return Laser.laser_lst.index(self)

    def get_lsersize(self):
        '''
        Returns the width and height of the laser object
        '''
        return self.lser_rect.width, self.lser_rect.height

    def lser_delete(self):
        '''
        Removes the laser followed by deleting it
        '''
        Laser.laser_lst.pop(self.get_lserlst_loc())
        del self
    
    def lser_move(self, lser_distance):
        '''
        Takes in the distance to move a laser

        Moves the laser by that distance
        '''
        if self.creator == Player:
            self.set_lser_height("up", lser_distance)
        elif self.creator == Enemies:
            self.set_lser_height("down", lser_distance)

        if self.get_lser_loc()[1] + self.get_lsersize()[1] == 0:
            self.lser_delete()

    def lser_draw(self):
        '''
        Draws the laser on the window object it exists on
        '''
        self.l_screen.blit(self.lser_image, self.get_lser_loc())

    def __repr__(self):
        return f"{self.get_ltype()}'s Laser"

class SpawnLocater:
    def __init__(self, x_dim):
        '''
        Takes the width of the area in which enemies will spawn randomly
        
        Creates that spawn area
        '''
        slr_dimension = (x_dim * 2, x_dim + x_dim/2)
        self.sl_rect = pg.Rect((10, x_dim + 10), slr_dimension)

    def get_spawnrect(self):
        '''
        Returns the spawn area's rect object
        '''
        return self.sl_rect

    def get_spr_xy(self):
        '''
        Returns the spawn area's x and y location
        '''
        return self.sl_rect.x, self.sl_rect.y
    
    def set_slr_x(self, slr_new_pos):
        '''
        Takes in a new x position for the spawn area. 
        
        Moves it there
        '''
        self.sl_rect.x = slr_new_pos

    def mov_slr_x(self, amnt):
        '''
        Takes a distance amount

        Moves the spawn area to the right by that much distance
        '''
        self.sl_rect.x += amnt

    def coll_with_enem(self, other_enem_lst):
        '''
        Takes in the Enemy class's enemy list (Enemy.all_elist)

        Returns a boolean indicating whether                                    #TODO Document this
        '''
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
        '''
        Takes a string prompt about what action to perform. Default action is 
        clear

        string action = "clear" || "delete"

        Performs the desired action on the list of all existing players
        '''
        list_clearer(cls.all_elist, what_action)

    @classmethod
    def newe_loc_finder(cls):                                                   #? Could be made better?
        '''
        Returns the x and y location where a new enemy can be created
        '''
        spl = cls.spawn_loc
        spl.set_slr_x(10)
        loop_cntr = 0
        while spl.coll_with_enem(cls.all_elist) and (loop_cntr <= len(cls.all_elist)):
            loop_cntr += 1
            spl.mov_slr_x(50)

        if (loop_cntr == len(cls.all_elist)) and (len(cls.all_elist) != 0):
            return None
        else:
            return spl.get_spr_xy()

    @classmethod
    def enem_generator(cls, enem_draw_win, max_enemy):
        '''
        Takes in a window object and the maximum amount of enemies possible
        '''
        if len(cls.all_elist) < max_enemy:
            e_genloc = cls.newe_loc_finder()
            if e_genloc != None:
                Enemies(enem_draw_win, enemy_side, e_genloc)

    @classmethod
    def auto_shooter(cls, time_cntr, existing_lser_list):
        pass                                                                    #TODO: Shoot if no existing_lser_list

    @classmethod
    def auto_emover(cls, enem_dst):
        '''
        Takes in the distance an emeny will move

        Moves all the enemies by that distance. If any touch the edge all the 
        enemies are moved down by the same distance
        '''
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
        '''
        Takes in the Laser class's laser list (Laser.lser_list) and the Player 
        class's player list (Player.all_players)
        '''
        for enems in cls.all_elist:
            enems.enem_lser_coll(laser_list)
            enems.enem_player_coll(the_main_players)

    @classmethod
    def auto_enem_draw(cls):
        '''
        Draws all the enemies on their respective window(s)
        '''
        for drawing_enems in cls.all_elist:
            drawing_enems.enem_draw()

    @classmethod
    def get_spawn_area(cls):                                                    #? Is this even needed?
        '''
        Returns the spawn locater object 
        '''
        return cls.spawn_loc

    def __init__(self, e_scrn, e_side, e_spawnxy):
        '''
        Takes in a window object, the side length of the enemy and the enemy's 
        spawn location

        Creates an enemy object
        '''
        self.escreen = e_scrn
        self.escreenx, self.escreeny = self.escreen.get_size()
        self.eside = e_side
        self.e_colorgrp = Enemies.OPTION[rndm.randint(0, 1)]
        self.image = self.e_colorgrp[0]
        self.enem_rect = self.image.get_rect()
        Enemies.all_elist.append(self)
        self.enem_rect.x, self.enem_rect.y = e_spawnxy

    def get_curr_escreen(self):
        '''
        Returns the enemy's window object
        '''
        return self.escreen

    def get_curr_escr_xy(self):
        '''
        Returns the dimensions of the window object
        '''
        return self.escreenx, self.escreeny
    
    def get_eside(self):
        '''
        Returns the side length of the enemy
        '''
        return self.eside

    def get_enemsize(self):
        '''
        Returns the dimensions of the enemy
        '''
        return self.eside, self.eside
    
    def get_colorgrp(self):
        '''
        Returns the color of the enemy -> "green" || "red"
        '''
        return self.e_colorgrp

    def get_enemrect(self):
        '''
        Returns the enemy's rect object
        '''
        return self.enem_rect

    def get_enemloc(self):
        '''
        Returns the location of the enemy
        '''
        return self.enem_rect.x, self.enem_rect.y
    
    def set_enemheight(self, edst, enem_direction):
        '''
        Takes the distance and a direction string

        str direction = "down" || "up"

        Moves the enemy by the specificed distance
        '''
        if enem_direction == "down":
            self.enem_rect.y += edst
        elif enem_direction == "up":
            self.enem_rect.y -= edst
    
    def set_enemx(self, e_dstnc):
        '''
        Takes the distance integer

        Moves the enemy left or right by that distance
        '''
        if Enemies.ENEM_DIR == "right":
            self.enem_rect.x += e_dstnc
        if Enemies.ENEM_DIR == "left":
            self.enem_rect.x -= e_dstnc
    
    def get_enemlst_loc(self):
        '''
        Return the index of the player from the class list
        '''
        return Enemies.all_elist.index(self)

    def enem_fall(self, fall_value):
        '''
        Takes a distance integer

        Makes the enemy fall by that much distance
        '''
        self.set_enemheight(fall_value, "down")

    def enem_destroy(self):
        '''
        Removes the enemy followed by deleting it
        '''
        Enemies.all_elist.pop(self.get_enemlst_loc())
        del self

    def enem_lser_coll(self, lser_list):
        '''
        Takes the Laser class's laser list (Laser.lser_list)

        Checks if the enemy collided with any laser. If so removes it the laser 
        and the enemy, as well as increases the score by 10
        '''
        enem_obj = self.get_enemrect()
        for l in lser_list:
            if l.get_lrect().colliderect(enem_obj) and l.get_ltype() == Player:
                self.enem_destroy()
                l.lser_delete()
                pg.event.post(s_event.Score_Increase)
    
    def enem_player_coll(self, the_players):
        '''
        Takes the Player class's player list (Player.all_players)

        Checks if the enemy has collided with any player. If so it removes the 
        enemy and signals the player to reduce its health
        '''
        for p in the_players:
            if p.get_plrect().colliderect(self.get_enemrect()):
                self.enem_destroy()
                p.set_health(p.get_health() - 10)

    def coll_with_enem(self, other_enem):
        '''
        Takes an Enemy object

        Checks if the two enemies are colliding.

        Returns a boolean
        '''
        return self.get_enemrect().colliderect(other_enem.get_enemrect())

    def enem_draw(self):
        '''
        Draws the enemy on its window
        '''
        self.escreen.blit(self.image, self.get_enemloc())

        e_out = pg.Rect((self.get_enemrect().topleft), (self.get_enemsize()))
        pg.draw.rect(self.escreen, self.get_colorgrp()[1], e_out, 1)

    def __repr__(self):
        return f"{self.get_colorgrp()[2]} Enemy"
