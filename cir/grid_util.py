# ------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                     #
#                                                    UTILS                                                            #
#                                                                                                                     #
# ------------------------------------------------------------------------------------------------------------------- #
import re
import math


def dist_between(pointA, pointB):
    x1 = pointA[0]
    y1 = pointA[1]
    x2 = pointB[0]
    y2 = pointB[1]

    return math.sqrt(((x2 - x1)*(x2 - x1)) + ((y2 - y1)*(y2 - y1)))

def in_circle(center, radius, point):
    """
    :param center: center of the CIR
    :param radius: radius of the CIR
    :param point: coordinates of the point to be checked (x, y)
    :return: boolean - is the point inside the given CIR
    """
    center_x, center_y = center[0], center[1]
    x, y = point[0], point[1]
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2


def intersecting(circle_1, circle_2):
    """
    Given two circles described by the 3-tuples (x-coordinates, y-coordinates, radius)
    :param circle_1: ((x1, y1), r1)
    :param circle_2: ((x1, y1), r1)
    :return: Boolean
    """
    x1 = circle_1[0][0]
    y1 = circle_1[0][1]
    r1 = circle_1[1] - 3
    x2 = circle_2[0][0]
    y2 = circle_2[0][1]
    r2 = circle_2[1] - 3
    return math.pow(abs(x1 - x2),2) + math.pow(abs(y1 - y2),2) < math.pow((r1 + r2),2)


def inside_polygon(poly, point):
    """
    Return True if a coordinate (x, y) is inside a polygon defined by
    a list of verticies [(x1, y1), (x2, x2), ... , (xN, yN)].
    """
    x = point[0]
    y = point[1]

    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside



def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step


def get_list_drange(start, stop, step):
    i0 = drange(start, stop, step)
    result = [x for x in i0]
    return result


def get_next_point(pointA, pointB, dist):

    x1 = pointA[0]
    y1 = pointA[1]
    x2 = pointB[0]
    y2 = pointB[1]

    new_x = x1 * (1 - dist) + x2 * dist
    new_y = y1 * (1 - dist) + y2 * dist
    new_step = (new_x, new_y)

    return new_step


def get_mirror_point(pointA, pointB):
    """ Showing the mirror point of A if B is center """
    dist = 2
    t = 1
    pointC = get_next_point(pointA, pointB, dist)
    dx = int(((1 - t) * pointB[0]) + (t * pointC[0]))
    dy = int(((1 - t) * pointB[1]) + (t * pointC[1]))

    return (dx, dy)


def show_debug_on_click(grid, current_circle, mybody):
    """  Debug on click event  """
    if grid.show_debug:
        grid.msg("CLICK")
        grid.msg("DEBUG - click tile  : {0}, {1}".format( grid.pos_to_name(current_circle), current_circle ))
        grid.msg("DEBUG - mouse mode  : {0}".format( grid.mouse_mode ))
        grid.msg("DEBUG - grid circles  : {0}".format( len(grid.circles) ))
        grid.msg("DEBUG - grid circles  : {0}".format( [(cir.name, cir.pos) for cir in grid.circles] ))
        grid.msg("DEBUG - panel circles  : {0}".format( len(grid.panel_circles) ))
        grid.msg("DEBUG - panel circles  : {0}".format( [(panel_key, circle.pos) for panel_key, circle in grid.panel_circles.items()] ))
        # grid.msg("DEBUG - occupado    : {0}".format( [(occ, occpos, grid.pos_to_name(occpos)) for occ, occpos in grid.occupado_tiles.items()] ))
        # grid.msg("DEBUG - occupado    : {0}".format( len(grid.occupado_tiles) ))
        # grid.msg("DEBUG - overlap     : {0}".format( [(circle.name, circle.pos) for circle in grid.overlap] ))
        # grid.msg("DEBUG - playing     : {0}".format( len(grid.playing_tiles) ))
        # grid.msg("DEBUG - move track  : {0}".format( mybody.move_track ))
        # grid.msg("DEBUG - all tiles   : {0}".format( len(grid.tiles) ))
        # grid.msg("DEBUG - current room: {0}".format( grid.current_room ))
        # grid.msg("DEBUG - prev room   : {0}".format( grid.previous_room ))
        # grid.msg("DEBUG - revealed    : {0}".format( grid.revealed_tiles ))
        # grid.msg("DEBUG - revealed    : {0}".format( len(grid.revealed_tiles.keys() ) ))
        # grid.msg("DEBUG - game menu   : {0}".format( grid.game_menu ))
        # grid.msg("DEBUG - my body     : {0} {1} {2}".format( mybody in grid.circles, mybody.available, mybody.color ))

def get_short_name(name_with_timestamp):
    """ Removes the timestamp from a name """
    time_stamp_pattern = '-\d{10,}.{1,}'
    if re.search(time_stamp_pattern, name_with_timestamp):
        time_stamp_string = re.search(time_stamp_pattern, name_with_timestamp).group(0)
        circle_name = name_with_timestamp.replace(time_stamp_string, "")
    else:
        circle_name = name_with_timestamp
    return circle_name


class bcolors:
    INFO = '\033[93m'
    DEBUG = '\033[37m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
