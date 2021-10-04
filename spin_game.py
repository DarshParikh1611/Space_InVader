import pygame as pg; pg.font.init(); pg.mixer.init()
from spin_assets import SPIN_ASSET_LOADING as AST
import game_members as gm
import spin_events as SEVE
import spin_functions as sfuncs

player_side = AST.pl_side() 
speed = AST.get_vel(); fps = AST.get_fps()
score_txt_fnt = AST.score_font()
backup_score_txt_fnt = AST.backup_score_font()
player_amount = AST.number_of_players()
all_keys = AST.control_set()

class SpaceInvaderGame:
    try:
        SCORE_FONT = pg.freetype.Font(score_txt_fnt, 20)
    except:
        print("Couln't use the intended font for score display")
        SCORE_FONT = pg.font.Font(backup_score_txt_fnt, 20)
    clock = pg.time.Clock()
    session_score = 0
    max_enem = 5
    is_game_over = False

    @classmethod
    def game_over(cls):
        cls.is_game_over = True

    @classmethod
    def game_display(cls, dis_scrn, bckgrnd, pl, enem_class, laser_class, gme_score):
        # dis_scrn.fill((0,0,0))
        dis_scrn.blit(bckgrnd, (0,0))
        pl.all_player_draw()

        enem_class.auto_enem_draw()
        laser_class.auto_lser_draw()    

        score_txt = cls.SCORE_FONT.render(f"Score: {gme_score}", 1, (255,255,255))
        dis_scrn.blit(
            score_txt, (10, enem_class.get_spawn_area().get_spr_xy()[1] - 10)
        )                                                                       #FIXME: x,y needs to be more accurate

        pg.display.update()

    @classmethod
    def start_game(cls, game_window, game_background):
        cls.space_inVader(game_window, game_background)

    @classmethod
    def space_inVader(cls, game_win, game_bg):
        extra_time_counter = 0
        cls.session_score = 0
        run = True
        cls.is_game_over = False
        gave_up = False                                                         # To check whether game ended normally or was quit

        gm.Player.clear_players()
        gm.Enemies.clear_enemies()
        gm.Laser.clear_lasers()

        if player_amount >= 1:                                                  #TODO Improve
            first_player_controls = sfuncs.keybinds(all_keys[0])
            first_player = gm.Player(game_win, player_side, first_player_controls)
            if player_amount >= 2:
                second_player_controls = sfuncs.keybinds(all_keys[1])
                second_player = gm.Player(game_win, player_side, second_player_controls)
            if player_amount == 3:
                third_player_controls = sfuncs.keybinds(all_keys[2])
                third_player = gm.Player(game_win, player_side, third_player_controls) 

        while run and (not cls.is_game_over):
            cls.clock.tick(fps)
            
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    run = False
                    gave_up = True
                elif e.type == SEVE.GAME_OVER:
                    print(e.message)
                    pg.time.delay(20)
                    cls.game_over()
                elif e.type == SEVE.SCORE_INCREASE:
                    cls.session_score += 10
                    
            gm.Player.remove_killed()

            events = pg.key.get_pressed()
            gm.Player.player_handler(events, speed)

            gm.Enemies.enem_generator(game_win, cls.max_enem)
            gm.Enemies.enem_coll(gm.Laser.laser_lst, gm.Player.all_players)
            gm.Enemies.auto_emover(speed)
            gm.Enemies.auto_shooter(extra_time_counter, gm.Laser.laser_lst)

            gm.Laser.auto_lser_move(speed)

            gm.Player.all_player_cooldown()

            cls.game_display(
                game_win, game_bg, gm.Player, gm.Enemies, gm.Laser, cls.session_score
            )

            extra_time_counter += 1

        if gave_up:
            print("LOSER")
        else:
            print(f"well played! You scored {cls.session_score} points")

        del events                                                              
        gm.Player.clear_players(what_action="delete")
        gm.Enemies.clear_enemies(what_action="delete")
        gm.Laser.clear_lasers(what_action="delete")
