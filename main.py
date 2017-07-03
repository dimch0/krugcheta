#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                    Main file                                        #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################

# --------------------------------------------------------------- #
#                            Features                             #
# --------------------------------------------------------------- #
# TODO: Time modifier
# TODO: Item generation
# TODO: Indicate uses
# TODO: Create mini map
# TODO: Define signal function
# TODO: Log statistics during a lifespan
# TODO: Create more rooms
# TODO: Create spirit mode, calculate karma
# TODO: Log messages on screen
# TODO: Create save button
# TODO: Animate item generation
# TODO: Animate item activation
# TODO: Create installation .exe file
# --------------------------------------------------------------- #
#                            Bug fixes                            #
# --------------------------------------------------------------- #
# TODO: Fix movement track
# --------------------------------------------------------------- #
#                            Optional                             #
# --------------------------------------------------------------- #
# TODO: Animate circle kiss
# TODO: Animate instructions
# TODO: Remove mode_vs_options usage
# TODO: Link timer to body

import os
import sys
import time
import pygame

from cir import cir_grid
from cir import cir_draw
from cir import cir_utils
from cir import cir_loader
from cir import cir_effects
from cir import cir_cosmetic


def game_loop():
    """ Main game loop """
    print "Game started"
    GAME_EXIT = False
    START_TIME = time.time()

    while not GAME_EXIT:
        # Mouse
        MOUSE_POS = pygame.mouse.get_pos()
        # Seconds in game
        cir_utils.seconds_in_game(grid, START_TIME)
        # --------------------------------------------------------------- #
        #                                                                 #
        #                            EVENTS                               #
        #                                                                 #
        # --------------------------------------------------------------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_EXIT = True
            # --------------------------------------------------------------- #
            #                                                                 #
            #                            KEY EVENTS                           #
            #                                                                 #
            # --------------------------------------------------------------- #
            elif event.type == pygame.KEYDOWN:
                # --------------------------------------------------------------- #
                #                             'Esc'                               #
                # --------------------------------------------------------------- #
                if event.key == pygame.K_ESCAPE:
                    if not grid.game_menu:
                        grid.game_menu = True
                    elif grid.game_menu and grid.seconds_in_game > 0:
                        grid.game_menu = False
                # --------------------------------------------------------------- #
                #                            IN GAME                              #
                # --------------------------------------------------------------- #
                if not grid.game_menu:
                    # --------------------------------------------------------------- #
                    #                            'Space'                              #
                    # --------------------------------------------------------------- #
                    if event.key == pygame.K_SPACE:
                        # Radar Population
                        if not my_body.move_track and not my_body.in_menu and not my_body.radar_track:
                            my_body.gen_radar_track(grid)
                        # Debug
                        cir_utils.debug_print_space(grid)
                    # t
                    elif event.key == pygame.K_t:
                            # Timers
                            if grid.timers:
                                for timer in grid.timers:
                                    if timer.name == "lifespan":
                                        print "step            :", timer.step
                                        print "filled steps    :", timer.filled_steps
                                        print "number of steps :", timer.number_of_steps
                                        print "len of step     :", timer.len_step
                                        print "-"*35
                                        timer.step -= 20
                                        timer.filled_steps += 20
                    # l
                    elif event.key == pygame.K_l:
                        grid.game_over = True
                        sys.argv.append('Scenario_2')
                        os.execv(sys.executable, [sys.executable] + sys.argv)
                        print "l"
                    # b
                    elif event.key == pygame.K_b:
                        print "b"
                    # r
                    elif event.key == pygame.K_r:
                        my_body.img = images.galab
                        my_body.default_img = my_body.img
                        print "r"
                    # k
                    elif event.key == pygame.K_k:
                        print "k"
                    # Movement Population
                    elif not my_body.in_menu:
                        my_body.gen_movement_arrows(pygame, grid, event)

            # --------------------------------------------------------------- #
            #                                                                 #
            #                          CLICK EVENTS                           #
            #                                                                 #
            # --------------------------------------------------------------- #
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_circle = grid.mouse_in_tile(MOUSE_POS)
                if clicked_circle:
                    # --------------------------------------------------------------- #
                    #                        MOUSE MODES CLICK                        #
                    # --------------------------------------------------------------- #
                    if grid.mouse_mode == "laino":
                        cir_effects.laino_mode_click(grid, clicked_circle)
                    elif grid.mouse_mode == "shit":
                        cir_effects.shit_mode_click(grid, clicked_circle)
                    # --------------------------------------------------------------- #
                    #                          IN GAME MENU                           #
                    # --------------------------------------------------------------- #
                    if grid.game_menu:
                        for button in grid.buttons:
                            if clicked_circle == button.pos and button.available:
                                if button.name in ["play", "replay"]:
                                    grid.game_menu = False
                                    if grid.game_over:
                                        grid.game_over = False
                                elif button.name == "quit":
                                    pygame.quit()
                                    quit()
                    # --------------------------------------------------------------- #
                    #                        CLICK ON GRID ITEMS                      #
                    # --------------------------------------------------------------- #
                    elif not grid.game_menu:
                        for item in grid.items:
                            if item.available:
                                if clicked_circle == item.pos:
                                    # --------------------------------------------------------------- #
                                    #                            BAG MODE                             #
                                    # --------------------------------------------------------------- #
                                    if grid.mouse_mode == "bag":
                                        cir_effects.collect(grid, item)

                                    # Set in_menu for the items with menu (my_body)
                                    item.check_in_menu(grid, clicked_circle)
                                    # Setting option positions
                                    item.set_option_pos(grid)
                                    # Option clicked
                                    if item.in_menu:
                                        grid.clean_mouse()
                                # --------------------------------------------------------------- #
                                #                       CLICK ITEM OPTIONS                        #
                                # --------------------------------------------------------------- #
                                elif clicked_circle in grid.adj_tiles(item.pos) and item.in_menu:
                                    if item.options:
                                        for option in item.options:
                                            if clicked_circle == option.pos:
                                                # Mouse mode
                                                if option.modable:
                                                    grid.set_mouse_mode(option)
                                                # --------------------------------------------------------------- #
                                                #                       CLICK DEFAULT OPTIONS                     #
                                                # --------------------------------------------------------------- #
                                                if option in item.default_options:
                                                    if option.name == "bag":
                                                        print "Gimme the loot!"
                                                    elif option.name == "mitosis":
                                                        item.mitosis(grid)
                                                    # Setting the mode
                                                    item.set_mode(grid, option)
                                                # --------------------------------------------------------------- #
                                                #                        CLICK SUB-OPTIONS                        #
                                                # --------------------------------------------------------------- #
                                                elif option in grid.mode_vs_options[item.mode]:
                                                    if item.mode == "move":
                                                        item.gen_move_track(grid, grid.mode_vs_options[item.mode].index(option))
                                                    elif option.name == "see":
                                                        item.range += 3
                                                        print "seen"
                                                    elif option.name == "smel":
                                                        print "sniff hair"
                                                    elif option.name == "medi":
                                                        item.range += 3
                                                        item.change_speed(10)
                                                    elif option.name == "audio":
                                                        item.range += 1
                                                    elif option.name == "eat":
                                                        item.change_speed(-1)
                                                    # Close menu when sub-option selected
                                                    item.set_in_menu(grid, False)
                                                # Close menu if option has no sub-options
                                                if option.name not in grid.mode_vs_options.keys():
                                                    item.set_in_menu(grid, False)
                                # Clicked outside
                                elif (clicked_circle != item.pos) and (clicked_circle not in grid.adj_tiles(item.pos)):
                                    item.set_in_menu(grid, False)
                # Debug print
                cir_utils.debug_print_click(grid, MOUSE_POS, clicked_circle, my_body)

        # --------------------------------------------------------------- #
        #                                                                 #
        #                             DRAWING                             #
        #                                                                 #
        # --------------------------------------------------------------- #
        # Background
        grid.game_display.fill(grid.dark_grey)
        # --------------------------------------------------------------- #
        #                             IN GAME                             #
        # --------------------------------------------------------------- #
        if not grid.game_menu:
            # Revealed radius
            if grid.revealed_radius:
                cir_draw.draw_revealed_radius(pygame, grid)
            # Mask
            cir_draw.draw_mask(pygame, grid)
            # Grid
            if grid.show_grid:
                cir_draw.draw_grid(pygame, grid)
            # Playing board:
            if grid.show_playing_tiles:
                cir_draw.draw_playing_tiles(pygame, grid)

            # --------------------------------------------------------------- #
            #                             ANIMATIONS                          #
            # --------------------------------------------------------------- #
            # Items
            for item in grid.items:
                if item.available:
                    # Radar
                    if item.radar_track:
                        cir_draw.draw_radar(pygame, grid, item)
                    # if item.pos in grid.revealed_tiles:
                    cir_draw.draw_body(pygame, grid, MOUSE_POS, item)
                    # Item options
                    if item.in_menu:
                        cir_draw.draw_item_options(pygame, grid, MOUSE_POS, item)
                    # Show movement track in color
                    if grid.show_movement and len(item.move_track) > 1:
                        cir_draw.draw_movement(pygame, grid, item)
                    # Image rotation
                    if item.rot_track:
                        item.rotate(pygame)
                    # Item reverse rotation
                    if item.last_direction and not item.move_track:
                        item.rotate_reverse(pygame)

            # Timers
            if grid.timers:
                cir_draw.draw_timers(pygame, grid, my_body)

            # Mouse
            if grid.mouse_mode:
                cir_draw.draw_mouse_image(pygame, grid, MOUSE_POS)
        # --------------------------------------------------------------- #
        #                           GAME MENU                             #
        # --------------------------------------------------------------- #
        elif grid.game_menu:
            # Menu Buttons
            if grid.buttons:
                cir_draw.draw_menu_buttons(pygame, grid, MOUSE_POS)

        # End drawing
        pygame.display.update()
        # --------------------------------------------------------------- #
        #                                                                 #
        #                           CHANGE VARS                           #
        #                                                                 #
        # --------------------------------------------------------------- #
        if not grid.game_menu:
            # Empty bag in needed
            if "bag" in grid.everything.keys():
                cir_effects.empty_bag(grid)

            # Timers
            if grid.timers:
                for timer in grid.timers:
                    timer.tick()
                    # Lifespan timer
                    grid.everything['lifespan'].pos = my_body.pos
                    if grid.everything['lifespan'].is_over:
                        grid.game_over = True
                        sys.argv.append('replay')
                        os.execv(sys.executable, [sys.executable] + sys.argv)

            # Items
            for item in grid.items:
                if item.available:
                    # Overlap
                    item.overlapping(grid)
                    # Movement
                    if item.move_track:
                        item.move()
                    # Clean placeholders
                    grid.clean_placeholders(item)

        # FPS
        clock.tick(grid.fps)
    # END
    pygame.quit()
    quit()

# --------------------------------------------------------------- #
#                                                                 #
#                              MAIN                               #
#                                                                 #
# --------------------------------------------------------------- #
if __name__ == '__main__':
    # --------------------------------------------------------------- #
    #                             Loading                             #
    # --------------------------------------------------------------- #
    pygame.init()
    scenario = cir_utils.set_scenario(sys.argv)
    grid = cir_grid.Grid()
    images = cir_cosmetic.Images(grid, pygame)
    fonts = cir_cosmetic.Fonts(grid, pygame)
    my_body = cir_loader.load_items(grid, images, fonts, scenario)
    grid.set_game_display(pygame)
    pygame.display.set_caption(grid.caption)
    clock = pygame.time.Clock()
    # --------------------------------------------------------------- #
    #                           Settings                              #
    # --------------------------------------------------------------- #
    # Replay
    for button in grid.buttons:
        if 'replay' in sys.argv:
            if button.name == "replay":
                button.available = True
            if button.name == "play":
                button.available = False
    # Start in menu
    if 'Scenario_2' in sys.argv:
        grid.game_menu = False
    else:
        grid.game_menu = True
    # --------------------------------------------------------------- #
    #                             Start                               #
    # --------------------------------------------------------------- #
    game_loop()