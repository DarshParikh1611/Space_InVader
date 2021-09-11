import pygame as pg; pg.font.init(); pg.mixer.init()
import random as rndm
from spin_assets import SPIN_ASSET_LOADING as AST

win_xy = AST.spin_xy(); bagrnd = AST.bg_img(); fps = AST.get_fps()
pl_ship = AST.player_ship(); pl_lser = AST.player_laser()
green_ship = AST.green_ship(); green_lser = AST.green_laser()
red_ship = AST.red_ship(); red_lser = AST.red_laser()
player_side = AST.pl_side(); enemy_side = AST.enem_side()
pl_xy = AST.player_xy(); e_xy = AST.enem_xy(); lser_xy = AST.laser_xy()
cooldown = AST.pl_cooldown(); speed = AST.get_vel()
pl_outline = AST.player_outline()
green_outline = AST.green_outline_clr(); red_outline = AST.red_outline_clr()
SCORE_FONT = pg.font.SysFont("segoeprint", 20)
SPIN_WIN = pg.display.set_mode(win_xy)
pg.display.set_caption("Space InVader ;)")
RIGHT_EDGE = pg.Rect(win_xy[0], 0, 1, win_xy[1])
LEFT_EDGE = pg.Rect(-1, 0, 1, win_xy[1])

def img_loadscale(img, dimensions, rotate=0):
    loaded_img = pg.image.load(img)
    scaled_img = pg.transform.scale(loaded_img, dimensions)
    transformed_img = pg.transform.rotate(scaled_img, rotate)
    return transformed_img

def game_display(dis_scrn, bckgrnd, pl, enemy_class, laser_class, gme_score):
    # dis_scrn.fill((0,0,0))
    dis_scrn.blit(bckgrnd, (0,0))
    pl.all_player_draw()
    pl_hlth = pl.all_players[0].get_health()                                                # TODO: move this into player class itself

    enemy_class.auto_enem_draw()
    laser_class.auto_lser_draw()    

    score_txt = SCORE_FONT.render(f"Score: {gme_score}", 1, (255,255,255))
    dis_scrn.blit(score_txt, (10, win_xy[1] - 50))
    health_txt = SCORE_FONT.render(f"Health: {pl_hlth}", 1, (255,255,255))
    dis_scrn.blit(health_txt, ((win_xy[0] - 135, win_xy[1] - 50)))

    pg.display.update()


class Player:
    P_IMG = img_loadscale(pl_ship, pl_xy)
    P_OUTLINE = pl_outline
    PL_COOLDOWN = cooldown

    all_players = []

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
                cls.all_players.pop(p)
                del p

    @classmethod
    def all_dead(cls):
        if len(cls.all_players) > 0:
            return False
        else:
            return True

    def __init__(self, pl_scrn, pl_side):
        self.pscreen = pl_scrn
        self.pscr_x, self.pscr_y = self.pscreen.get_size()
        self.side = pl_side
        self.pl_img = Player.P_IMG
        self.rect = self.pl_img.get_rect()
        tempx, tempy = (self.pscr_x/2-self.side/2), (self.pscr_y-self.side-20)
        self.rect.topleft = tempx, tempy
        self.health = 100
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
        if direc == "left": self.rect.x -= dst
        if direc == "right": self.rect.x += dst

    def get_health(self):
        return self.health
    
    def set_health(self, health_val):
        self.health = health_val

    def get_cooldown_counter(self):
        return self.cooldown_count

    def set_cooldown_count(self, cd_val):
        self.cooldown_count = cd_val

    def is_dead(self):
        if self.get_health() == 0:
            return True
        else:
            return False
    
    def pl_move(self, pl_move_direction, distance):
        pl_locx = self.get_plloc()[0]
        win_right_edge = self.get_pscr()[0]-self.get_pside()
        if pl_move_direction == "right" and pl_locx != win_right_edge:
            self.set_plloc("right", distance)
        elif pl_move_direction == "left" and pl_locx != 0:
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

    def pl_draw(self):
        self.pscreen.blit(self.pl_img, self.get_plloc())

        pl_out = pg.Rect((self.get_plrect().topleft), (self.get_psize()))
        pg.draw.rect(self.pscreen, Player.P_OUTLINE, pl_out, 1)

    def __repr__(self):
        return "The Main Player"

class Laser():
    P_LASER_IMG = img_loadscale(pl_lser, lser_xy)
    G_LASER_IMG = img_loadscale(green_lser, lser_xy)
    R_LASER_IMG = img_loadscale(red_lser, lser_xy)
    l_OPTIONS = [P_LASER_IMG, G_LASER_IMG, R_LASER_IMG]
    laser_lst = []

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
            self.lser_rect.x = origin.get_plrect().x - origin.get_pside()/2     # Why do i need to subtract the side-length????
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

class Enemies():
    G_SHIP_IMG = img_loadscale(green_ship, e_xy, rotate=180)
    G_OUTLINE = green_outline
    R_SHIP_IMG = img_loadscale(red_ship, e_xy, rotate=180)
    R_OUTLINE = red_outline
    OPTION = [(G_SHIP_IMG, G_OUTLINE, "Green"), (R_SHIP_IMG, R_OUTLINE, "Red")]
    all_elist = []
    ENEM_DIR = "right"
    ENEM_SIDE = enemy_side
    spawn_loc = SpawnLocater(ENEM_SIDE)

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
                                                                                # TODO: Shoot if no existing_lser_list
        pass
    
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
            if i.get_enemloc()[1] == i.get_curr_escr_xy()[1]:                   #? screen from self or global?
                SpaceInvaderGame.game_over()
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
                SpaceInvaderGame.session_score += 10
    
    def enem_player_coll(self, the_players):
        for p in the_players:
            if p.get_plrect().colliderect(self.get_enemrect()):
                self.enem_destroy()
                p.player_destroy()

    def coll_with_enem(self, other_enem):
        return self.get_enemrect().colliderect(other_enem.get_enemrect())

    def enem_draw(self):
        self.escreen.blit(self.image, self.get_enemloc())

        e_out = pg.Rect((self.get_enemrect().topleft), (self.get_enemsize()))
        pg.draw.rect(self.escreen, self.get_colorgrp()[1], e_out, 1)

    def __repr__(self):
        return f"{self.get_colorgrp()[2]} Enemy"

class SpaceInvaderGame:
    bckgrnd_img = img_loadscale(bagrnd, win_xy)
    clock = pg.time.Clock()
    session_score = 0
    max_enem = 5
    is_game_over = False

    @classmethod
    def game_over(cls):
        cls.is_game_over = True

    @classmethod
    def space_inVader(cls, game_draw_win):
        extra_time_counter = 0
        cls.session_score = 0
        main_player = Player(game_draw_win, player_side)
        run = True
        cls.is_game_over = False

        while run and (not cls.is_game_over):
            cls.clock.tick(fps)
            
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    run = False

            Player.remove_killed()
            if Player.all_dead():
                print("Game Over")
                pg.time.delay(20)
                cls.game_over()
                continue

            events = pg.key.get_pressed()
            if events[pg.K_d]:main_player.pl_move("right", speed)
            if events[pg.K_a]:main_player.pl_move("left", speed)
            if events[pg.K_SPACE]:main_player.pl_shoot()

            Enemies.enem_generator(game_draw_win, cls.max_enem)
            Enemies.enem_coll(Laser.laser_lst, Player.all_players)
            Enemies.auto_emover(speed)
            Enemies.auto_shooter(extra_time_counter, Laser.laser_lst)

            Laser.auto_lser_move(speed)

            Player.all_player_cooldown()

            game_display(game_draw_win, cls.bckgrnd_img, Player, Enemies, Laser, cls.session_score)

            extra_time_counter += 1
        
        print(f"well played! You scored {cls.session_score} points")

if __name__ == '__main__':
    SpaceInvaderGame.space_inVader(SPIN_WIN)
