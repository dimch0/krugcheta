#######################################################################################################################
#################                                                                                     #################
#################                                 Grid class                                          #################
#################                                                                                     #################
#######################################################################################################################
import pdb
import json
from cir_utils import in_circle
from math import sqrt


CONFIG_JSON_FILE = "cir/cir_config.json"

class Grid(object):
    """
    master class for the grid
    """
    def __init__(self):
        self.cathetus = 0
        self.display_width = 0
        self.display_height = 0

        self.set_config()
        self._tiles = []
        self.center_tile = None
        self.find_center_tile()
        self._occupado_tiles = []
        self.playing_tiles = []
        self.revealed_tiles = []
        self.revealed_radius = []
        self.items = []
        self.mouse_mode = None
        self.mouse_img = None
        self.mode = []

    def set_config(self):
        """
        Setting attributes from the cir_config.json file
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
        # Setting the display metrics
        self.tile_radius = self.tile_radius / self.scale
        self.cathetus = int(sqrt(((2 * self.tile_radius) ** 2) - (self.tile_radius ** 2)))
        self.display_width = (self.cathetus * self.cols) + (self.tile_radius * 2)
        self.display_height = self.rows * self.tile_radius

    @property
    def tiles(self):
        """
        Generating the grid tiles
        """
        # TODO: define the playing board
        for x in range(0, self.cols + 1):
            for y in range(1, self.rows):
                if x % 2 == y % 2:
                    centre_x = self.tile_radius + (x * self.cathetus)
                    centre_y = y * self.tile_radius
                    centre = (centre_x, centre_y)
                    if not centre in self._tiles:
                        self._tiles.append(centre)
        return self._tiles

    def mouse_in_tile(self, mouse_pos):
        """
        :param mouse_pos: position of the mouse
        :return: returns the current tile, the mouse is in
         or None if there is no such
        """
        current_tile = None
        for tile in self.tiles:
            if in_circle(tile, self.tile_radius, mouse_pos):
                current_tile = tile
        return current_tile

    @property
    def occupado_tiles(self):
        """
        Marking the occupado grid tiles
        """
        self._occupado_tiles = [item.pos for item in self.items]
        return self._occupado_tiles


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