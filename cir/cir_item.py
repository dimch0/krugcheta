#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                           Item class, MobileItem class                              #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import cir_utils


class Item(object):
    """
    This is the base class for all CIR items
    It includes the open_menu method.
    """
    def __init__(self):
        # --------------------------------------------------------------- #
        #                            BASICS                               #
        # --------------------------------------------------------------- #
        self.name = None
        self.type = None
        self.category = None
        self.pos = ()
        self.color = None
        self.default_color = self.color
        self.img = None
        self.default_img = self.img
        self.radius = None
        self.default_radius = self.radius
        self._rect = []
        self.border = 0
        self.border_color = None
        self.border_width = None

        # --------------------------------------------------------------- #
        #                            OPTIONS                              #
        # --------------------------------------------------------------- #
        self.has_opts = False
        self.in_menu = False
        self.modable = False
        self.available = True
        self.clickable = True
        self.collectible = False
        self.mode = self.name
        self.options = []
        self.default_options = []
        self.overlap = []
        # --------------------------------------------------------------- #
        #                              STATS                              #
        # --------------------------------------------------------------- #
        self.lifespan = None
        self.time_color = None
        self.room = None
        self.uses = 1
        # --------------------------------------------------------------- #
        #                            ANIMATION                            #
        # --------------------------------------------------------------- #
        self.direction = None
        self.last_rotation = None
        self.birth_time = 0.033
        self.move_track = []
        self.radar_track = []
        self.rot_track = []
        self.rot_revert = []
        self.birth_track = []
        self.fat_track = []
        self.marked_for_destruction = False


    @property
    def rect(self):
        """ This defines the rect argument for the arch drawing """
        if self.radius and self.pos:
            self._rect = [self.pos[0] - self.radius,
                          self.pos[1] - self.radius,
                          2 * self.radius,
                          2 * self.radius]
        else:
            self._rect = []
        return self._rect



    def gen_birth_track(self):
        self.birth_track = range(1, self.radius)


    def gen_fat(self):
        if not self.fat_track:
            result = []
            reverse_result = []
            for fat in range(self.radius / 4):
                result.append(self.radius + fat)
                reverse_result.append(self.radius + fat)

            reverse_result.reverse()
            final_result = result + reverse_result
            final_result.append(self.default_radius)
            self.fat_track = final_result

    # --------------------------------------------------------------- #
    #                                                                 #
    #                          MODE OPTIONS                           #
    #                                                                 #
    # --------------------------------------------------------------- #
    def set_option_pos(self, grid):
        # Returning the options only
        for idx, option in enumerate(self.options):
            if self.in_menu:
                option.pos = grid.adj_tiles(self.pos)[idx]


    def set_mode(self, grid, option):
        """
        Changes the mode of an item to a given options
        :param option: an option item of a menu
        :param grid: grid instance
        """
        self.mode = option.name
        # self.color = option.color
        # self.img = option.img
        if option.options:
            self.options = option.options
        self.set_option_pos(grid)


    def reset_mode(self):
        """
        Resets the item to default mode
        """
        self.mode = self.name
        self.color = self.default_color
        self.img = self.default_img
        self.options = self.default_options


    # --------------------------------------------------------------- #
    #                                                                 #
    #                           ITEM MENU                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def set_in_menu(self, grid, value):
        """ Setting the in_menu attribute to value
        :param value: boolean -True or False
        """
        if value:
            self.in_menu = True
        else:
            self.in_menu = False
        return self.in_menu

    def check_in_menu(self, grid, clicked_circle):
        """
        On a clicked circle - check if this item is in menu and set it
        :param grid: grid instance
        :param clicked_circle: the current clicekd circle
        """

        # Clicked on item
        if clicked_circle == self.pos\
                and self.options\
                and self.clickable\
                and not (self.name != "my_body" and grid.mouse_mode):

            # If default mode:
            if self.mode is self.name:
                if not self.in_menu:
                    self.set_in_menu(grid, True)
                elif self.in_menu:
                    self.set_in_menu(grid, False)
            # If not default mode
            elif self.mode is not self.name:
                if self.in_menu:
                    self.reset_mode()
                elif not self.in_menu:
                    self.set_in_menu(grid, True)

        # Clicked outside
        elif (clicked_circle != self.pos) and (clicked_circle not in grid.adj_tiles(self.pos)) and self.clickable:
            self.set_in_menu(grid, False)


    # --------------------------------------------------------------- #
    #                                                                 #
    #                            OVERLAP                              #
    #                                                                 #
    # --------------------------------------------------------------- #
    def overlapping(self, grid):
        """
        Checks for overlapping items
        if in menu: creates a archive in self.overlap
        if not in menu: restores from self.overlap
        """
        if self.in_menu:
            grid.items.extend(self.options)
            for olapped_item in grid.items:
                for option in self.options:
                    if olapped_item.pos == option.pos and olapped_item.available:
                        if not olapped_item in self.overlap:
                            self.overlap.append(olapped_item)
                            grid.overlapped.append(olapped_item)
                            olapped_item.clickable = False
        else:
            grid.items = list(set(grid.items) - set(self.options))
            if self.overlap:
                for item in self.overlap:
                    item.clickable = True
                    self.overlap.remove(item)
                    if item in grid.overlapped:
                        grid.overlapped.remove(item)


    def intersects(self, item2):
        """ Checks and returns a bool if this item is intersecting with item2 """
        cir1 = (self.pos, self.radius)
        cir2 = (item2.pos, item2.radius)
        return cir_utils.intersecting(cir1, cir2)


    # --------------------------------------------------------------- #
    #                                                                 #
    #                             DESTROY                             #
    #                                                                 #
    # --------------------------------------------------------------- #
    def destroy(self, grid):
        if self in grid.items and not self.birth_track:
            if hasattr(self, "lifespan"):
                self.lifespan = None
            if hasattr(self, "vibe_freq"):
                self.vibe_freq = None
            self.in_menu = False
            if hasattr(self, "move_track"):
                self.move_track = []
            self.gen_birth_track()
            self.birth_track.reverse()
            self.marked_for_destruction = True
