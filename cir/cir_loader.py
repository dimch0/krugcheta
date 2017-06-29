#######################################################################################################################
#################                                                                                     #################
#################                                                                                     #################
#################                                    Loader                                           #################
#################                                                                                     #################
#################                                                                                     #################
#######################################################################################################################
import csv
import cir_item
import cir_item_body
import cir_item_timer
import cir_item_button
import cir_item_mobile




def set_item_mode_options(grid, mode_vs_options):
    """
    Setting all options to grid.item
    mode_vs_options:
    """

    for item in grid.items:
        for mode_name, mode_options in mode_vs_options.items():

            if item.name == mode_name:
                item.default_options = mode_options
                item.options = item.default_options


def add_optoin_to_mode(category, item_obj, MODE_VS_OPTIONS):
    """ Appending the mode option to the MODE_VS_OPTIONS DICT """
    if category not in MODE_VS_OPTIONS.keys():
        MODE_VS_OPTIONS[category] = []
    MODE_VS_OPTIONS[category].append(item_obj)


def set_grid_items(grid, item):
    """ Assigning all items to the grid object """
    category = item['category']
    item_obj = item['object']

    if category == 'my body':
        if not item_obj in grid.bodies:
            grid.bodies.append(item_obj)
        if not item_obj in grid.items:
            grid.items.append(item_obj)
        return item_obj

    elif hasattr(grid, category):
        grid_attribute = getattr(grid, category)
        if not item_obj in grid_attribute:
            grid_attribute.append(item_obj)
        # if category == "buttons":
        #     grid.buttonz[item_obj.name] = item_obj


def create_new_item(grid, type, attributes):
    """
    This function creates an item of a class by the given type.
    Attributes are set by a given dict (attributes)
    :param grid: grid instance
    :param type: type specified
    :param attributes: generated dict
    :return: a new instance of an item object
    """
    dummy = None

    if type == "body":
        dummy = cir_item_body.BodyItem()
    elif type == "timer":
        dummy = cir_item_timer.TimerItem()
        dummy.timer_tile_radius = grid.tile_radius
    elif type == "button":
        dummy = cir_item_button.ButtonItem()
    elif type == "mobile":
        dummy = cir_item_mobile.MobileItem()
    elif type == "mode_option":
        dummy = cir_item.Item()

    for attribute, value in attributes.items():
        if dummy:
            if hasattr(dummy, attribute):
                setattr(dummy, attribute, value)
            if attribute == "img":
                if hasattr(dummy, "default_img"):
                    setattr(dummy, "default_img", value)
            if attribute == "color":
                if hasattr(dummy, "default_color"):
                    setattr(dummy, "default_color", value)
    return dummy



def load_data(grid, images, fonts, SCENARIO):
    """
    This function loads all items and menu options from external data file.
    :param grid:  grid instance
    :param images:  images instance
    :param fonts:  fonts instance
    :param SCENARIO:  scenario number
    :return: a dict, containing the ITEM OBJECT, scenario, category and type
    """

    with open(grid.data_file, 'rb') as csvfile:

        data = csv.reader(csvfile, delimiter=',')
        HEADER = next(data)
        SCENARIO = SCENARIO

        print "SCENARIO IN LOAD_DATA", SCENARIO

        # --------------------------------------------------------------- #
        #                        SET COLUMN INDEX                         #
        # --------------------------------------------------------------- #
        col_indexes = {}
        for idx, name in enumerate(HEADER):
            col_indexes[name] = idx

        for row in data:
            if not row == HEADER:

                # --------------------------------------------------------------- #
                #                      SET COLS AS ATTRIBUTES                     #
                # --------------------------------------------------------------- #
                scenario_col = row[col_indexes["scenario"]]
                if str(SCENARIO) in scenario_col or "ALL" in scenario_col:
                    type = row[col_indexes["type"]] if len(row[col_indexes["type"]]) > 0 else None
                    category = row[col_indexes["category"]]

                    attributes = {
                        "name": row[col_indexes["name"]] if len(row[col_indexes["name"]]) > 0 else None,
                        "pos": eval(row[col_indexes["pos"]]) if len(row[col_indexes["pos"]]) > 0 else (),
                        "color": getattr(grid, row[col_indexes["color"]]) if len(row[col_indexes["color"]]) > 0 else None,
                        "img": getattr(images, row[col_indexes["img"]]) if len(row[col_indexes["img"]]) > 0 else None,
                        "border": row[col_indexes["border"]] if len(row[col_indexes["border"]]) > 0 else 0,
                        "speed": int(row[col_indexes["speed"]]) if len(row[col_indexes["speed"]]) > 0 else None,
                        "range": int(row[col_indexes["range"]]) if len(row[col_indexes["range"]]) > 0 else None,
                        "font": getattr(fonts, row[col_indexes["font"]]) if len(row[col_indexes["font"]]) > 0 else None,
                        "text_color": getattr(grid, row[col_indexes["text_color"]]) if len(row[col_indexes["text_color"]]) > 0 else None,
                        "duration": int(row[col_indexes["duration"]]) if len(row[col_indexes["duration"]]) > 0 else None,
                        "time_color": getattr(grid, row[col_indexes["time_color"]]) if len(row[col_indexes["time_color"]]) > 0 else None,
                        "modable": row[col_indexes["modable"]] if len(row[col_indexes["modable"]]) > 0 else None,
                    }

                    # --------------------------------------------------------------- #
                    #                         CREATING ITEM                           #
                    # --------------------------------------------------------------- #
                    ITEM_OBJECT = create_new_item(grid, type, attributes)

                    yield {
                        "object": ITEM_OBJECT,
                        "scenario": scenario_col,
                        "type": type,
                        "category": category
                    }


def load_items(grid, images, fonts, scenario):
    """
    Loading all grid items, my body and mode options
    :return: my_body, mode_vs_options
    """
    my_body = None
    mode_vs_options = {}

    for item in load_data(grid, images, fonts, scenario):

        category = item['category']
        item_obj = item['object']
        type = item["type"]

        if type == "mode_option":
            add_optoin_to_mode(category, item_obj, mode_vs_options)
        else:
            if category == "my body":
                my_body = set_grid_items(grid, item)
            else:
                set_grid_items(grid, item)

    # Setting mode_vs_options
    set_item_mode_options(grid, mode_vs_options)

    return my_body, mode_vs_options