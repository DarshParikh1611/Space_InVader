import pygame as pg; pg.font.init(); pg.mixer.init()
from pygame.constants import USEREVENT
from spin_assets import SPIN_ASSET_LOADING as AST
import game_members as gm

player_side = AST.pl_side()
win_xy = AST.spin_xy(); bagrnd = AST.bg_img(); 
speed = AST.get_vel(); fps = AST.get_fps()
SCORE_FONT = pg.font.SysFont("segoeprint", 20)

ALL_DEAD = USEREVENT + 1
SCORE_INCREASE = USEREVENT + 2
INVADED = USEREVENT + 3
All_Dead = pg.event.Event(ALL_DEAD, message = "All Players are Dead :(")
Score_Increase = pg.event.Event(SCORE_INCREASE, message = "Great, you killed another one!")
Invaded = pg.event.Event(INVADED, message = "The Enemies Invaded :(")

def img_loadscale(img, dimensions, rotate=0):
    loaded_img = pg.image.load(img)
    scaled_img = pg.transform.scale(loaded_img, dimensions)
    transformed_img = pg.transform.rotate(scaled_img, rotate)
    return transformed_img

class SpaceInvaderGame:
    clock = pg.time.Clock()
    session_score = 0
    max_enem = 5
    is_game_over = False

    @classmethod
    def game_over(cls):
        cls.is_game_over = True

    @staticmethod
    def game_display(dis_scrn, bckgrnd, pl, enem_class, laser_class, gme_score):
        # dis_scrn.fill((0,0,0))
        dis_scrn.blit(bckgrnd, (0,0))
        pl.all_player_draw()

        enem_class.auto_enem_draw()
        laser_class.auto_lser_draw()    

        score_txt = SCORE_FONT.render(f"Score: {gme_score}", 1, (255,255,255))
        dis_scrn.blit(
            score_txt, (10, enem_class.get_spawn_area().get_spr_xy()[1] - 10)
        )                                                                       #FIXME: x,y needs to be more accurate

        pg.display.update()

    @classmethod
    def start_game(cls, game_window):
        cls.space_inVader(game_window)

    @classmethod
    def space_inVader(cls, game_win):
        bckgrnd_img = img_loadscale(bagrnd, win_xy)
        extra_time_counter = 0
        cls.session_score = 0
        run = True
        cls.is_game_over = False

        gm.Player.clear_players()
        gm.Enemies.clear_enemies()
        gm.Laser.clear_lasers()

        main_player = gm.Player(game_win, player_side)

        while run and (not cls.is_game_over):
            cls.clock.tick(fps)
            
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    run = False
                elif e.type == ALL_DEAD:
                    print(e.message)
                    pg.time.delay(20)
                    cls.game_over()
                elif e.type == INVADED:
                    print(e.message)
                    pg.time.delay(20)
                    cls.game_over()
                elif e.type == SCORE_INCREASE:
                    cls.session_score += 10
                    
            gm.Player.remove_killed()

            events = pg.key.get_pressed()
            if events[pg.K_d]:main_player.pl_move("right", speed)
            if events[pg.K_a]:main_player.pl_move("left", speed)
            if events[pg.K_SPACE]:main_player.pl_shoot()

            gm.Enemies.enem_generator(game_win, cls.max_enem)
            gm.Enemies.enem_coll(gm.Laser.laser_lst, gm.Player.all_players)
            gm.Enemies.auto_emover(speed)
            gm.Enemies.auto_shooter(extra_time_counter, gm.Laser.laser_lst)

            gm.Laser.auto_lser_move(speed)

            gm.Player.all_player_cooldown()

            cls.game_display(
                game_win, bckgrnd_img, gm.Player, gm.Enemies, gm.Laser, cls.session_score
            )

            extra_time_counter += 1

        print(f"well played! You scored {cls.session_score} points")

        del events
        gm.Player.clear_players(what_action="delete")
        gm.Enemies.clear_enemies(what_action="delete")
        gm.Laser.clear_lasers(what_action="delete")


if __name__ == '__main__':
    dummy_screen = pg.display.set_mode(AST.spin_xy())
    SpaceInvaderGame.start_game(dummy_screen)