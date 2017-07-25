#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                 Grid class                                          #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import json
import time
from cir_utils import in_circle, inside_polygon, intersecting
from math import sqrt


CONFIG_JSON_FILE = "data/config.json"

class Grid(object):
    """ master class for the grid """

    def __init__(self, pygame=None):
        # -------------------------------------------------- #
        #                      SETTINGS                      #
        # -------------------------------------------------- #
        self.pygame = pygame
        self.cathetus = 0
        self.display_width = 0
        self.display_height = 0
        self.game_display = None
        self.set_config()
        self.game_menu = True
        self.game_over = False
        self.start_time = None
        self.seconds_in_game = 0
        self.seconds_in_pause = 0
        self.clock = pygame.time.Clock()
        # -------------------------------------------------- #
        #                        TILES                       #
        # -------------------------------------------------- #
        self.tiles = []
        self.set_display()
        self.center_tile = None
        self.find_center_tile()
        self.playing_tiles = []
        self.set_playing_tiles()
        self._occupado_tiles = []
        self.revealed_radius = [((self.center_tile), self.tile_radius)]
        self.revealed_tiles = [self.center_tile]
        # -------------------------------------------------- #
        #                        ROOMS                       #
        # -------------------------------------------------- #
        self.current_room = 1
        self.items = []
        self.buttons = []
        self.rooms = {}
        # -------------------------------------------------- #
        #                        ITEMS                       #
        # -------------------------------------------------- #
        self.everything = {}
        self.mode_vs_options = {}
        self.timer_vs_items = {}
        # -------------------------------------------------- #
        #                        MOUSE                       #
        # -------------------------------------------------- #
        self.mouse_mode = None
        self.mouse_img = None
        self.mode_img = None
        # -------------------------------------------------- #
        #                        THEME                       #
        # -------------------------------------------------- #
        self.fog_color = self.dark_grey
        self.room_color = self.grey


    def set_game_display(self):
        self.game_display = self.pygame.display.set_mode((self.display_width, self.display_height))

    def set_config(self):
        """
        Setting attributes from the config.json file
        and calculating the display metrics
        """
        try:
            with open(CONFIG_JSON_FILE) as jsonfile:
                conf = json.load(jsonfile)
            for section in conf.keys():
                for status, value in conf[section].items():
                    setattr(self, status, value)
        except Exception as e:
            print "ERROR, could not set config:", e

    def get_tiles(self):
        """
        Generating the grid tiles
        """
        self.tiles = []
        for x in range(0, self.cols + 1):
            for y in range(1, self.rows):
                if x % 2 == y % 2:
                    centre_x = self.tile_radius + (x * self.cathetus)
                    centre_y = y * self.tile_radius
                    centre = (centre_x, centre_y)
                    if not centre in self.tiles:
                        self.tiles.append(centre)

    def set_display (self):
        ##### Setting the display metrics ####
        self.cathetus = int(sqrt(((2 * self.tile_radius) ** 2) - (self.tile_radius ** 2)))
        self.display_width = (self.cathetus * self.cols) + (self.tile_radius * 2)
        self.display_height = self.rows * self.tile_radius
        self.set_game_display()
        self.pygame.display.set_caption(self.caption)
        self.get_tiles()

    def find_center_tile(self):
        """
        :return: the center tile (x, y) of the grid
        """
        mid_x = int(self.display_width / 2)
        mid_y = int(self.display_height / 2)
        for tile in self.tiles:
            if in_circle(tile, self.tile_radius, (mid_x, mid_y)):
                self.center_tile = tile
                break
        return self.center_tile

    def mouse_in_tile(self, MOUSE_POS):
        """
        :param MOUSE_POS: position of the mouse
        :return: returns the current tile, the mouse is in
         or None if there is no such
        """
        current_tile = None
        for tile in self.tiles:
            if in_circle(tile, self.tile_radius, MOUSE_POS):
                current_tile = tile
        return current_tile

    @property
    def occupado_tiles(self):
        """ Playing tiles intersecting with any items """
        result = []
        for tile in self.playing_tiles:
            for item in self.items:
                circle_1 = (tile, self.tile_radius)
                circle_2 = (item.pos, self.tile_radius)
                if intersecting(circle_1, circle_2):
                    result.append(tile)

        self._occupado_tiles = set(result)

        return self._occupado_tiles

    # def update_occupado_tiles(self):
    #     """ Playing tiles intersecting with any items """
    #     result = []
    #     for tile in self.playing_tiles:
    #         for item in self.items:
    #             circle_1 = (tile, self.tile_radius)
    #             circle_2 = (item.pos, self.tile_radius)
    #             if intersecting(circle_1, circle_2):
    #                 result.append(tile)
    #     self.occupado_tiles = set(result)

    def set_playing_tiles(self):
        """
        Defining the playing tiles
        """
        hex_board = [
            (self.center_tile[0], self.center_tile[1] - (9 * self.tile_radius)),
            (self.center_tile[0] + (5 * self.cathetus), self.center_tile[1] - (4 * self.tile_radius)),
            (self.center_tile[0] + (4 * self.cathetus), self.center_tile[1] + (5 * self.tile_radius)),
            (self.center_tile[0], self.center_tile[1] + (9 * self.tile_radius) + 1),
            (self.center_tile[0] - (4 * self.cathetus) - 1, self.center_tile[1] + (4 * self.tile_radius)),
            (self.center_tile[0] - (4 * self.cathetus) - 1, self.center_tile[1] - (4 * self.tile_radius))
        ]
        for tile in self.tiles:
            if inside_polygon(hex_board, tile):
                if not tile in self.playing_tiles:
                    self.playing_tiles.append(tile)

    def adj_tiles(self, center):
        """
        :param grid: the center tile
        :return: a list of 6 adjacent to the center tiles
        """
        self_x = center[0]
        self_y = center[1]
        return [
                (self_x, self_y - 2 * self.tile_radius),
                (self_x + self.cathetus, self_y - self.tile_radius),
                (self_x + self.cathetus, self_y + self.tile_radius),
                (self_x, self_y + 2 * self.tile_radius),
                (self_x - self.cathetus, self_y + self.tile_radius),
                (self_x - self.cathetus, self_y - self.tile_radius)
               ]

    def set_rev_tiles(self):
        """ Reveal tiles in the revealed areas (radius) """
        for tile in self.tiles:
            if tile in self.playing_tiles and tile not in self.revealed_tiles:
                for rev_rad in self.revealed_radius:
                    if in_circle(rev_rad[0], rev_rad[1], tile):
                        self.revealed_tiles.append(tile)
        return self.revealed_tiles


    def clean_placeholders(self, item):
        """ Cleans the placeholders (eg for mitosis) """
        if item.name == "placeholder":
            for other_item in self.items:
                if other_item.pos == item.pos:
                    try:
                        item.available = False
                        self.items.remove(item)
                    except Exception as e:
                        print "ERROR", e

    # --------------------------------------------------------------- #
    #                             MOUSE                               #
    # --------------------------------------------------------------- #
    def clean_mouse(self):
        self.mouse_mode = None
        self.mouse_img = None

    def set_mouse_mode(self, option):
        self.mouse_mode = option.name
        if option.img and option.modable:
            self.mouse_img = option.img

    # --------------------------------------------------------------- #
    #                             ROOMS                               #
    # --------------------------------------------------------------- #
    def save_current_room(self):
        """ Saves the current room to self.rooms """
        self.rooms[self.current_room] = {
            "items": self.items,
            "revealed_radius": self.revealed_radius
        }

    def load_current_room(self):
        """ loads the current room from self.rooms
        or an empty room if the number is not in self.rooms """
        if not self.current_room in self.rooms.keys():
            self.rooms[self.current_room] = {
            "items"          : [],
            "revealed_radius": [],
            }
        self.items = self.rooms[self.current_room]["items"]
        self.revealed_radius = self.rooms[self.current_room]["revealed_radius"]
        self.revealed_tiles = []
        self.set_rev_tiles()

    def change_room(self, room):
        """ Saves the current room and loads a new room """
        self.save_current_room()
        self.current_room = room
        self.load_current_room()

    # --------------------------------------------------------------- #
    #                            SECONDS                              #
    # --------------------------------------------------------------- #
    def seconds_in_game_tick(self):
        """ Counts the seconds in the game """

        if time.time() > self.start_time + self.seconds_in_game + self.seconds_in_pause:
            if not self.game_menu:
                self.seconds_in_game += 1
                if self.show_seconds:
                    print "Game second: {0}".format(self.seconds_in_game)
            else:
                self.seconds_in_pause += 1
                if self.show_seconds:
                    print "Pause second: {0}".format(self.seconds_in_pause)
