from copy import copy

from graphics import Rectangle, Point, Text

CELL_DIMENSION = (15, 15)

EMPTY = 0
WALL = 1
FOOD = 2
POISON = 3
BOT = 4


def rgb_color(color):
    return "#%02x%02x%02x" % (color[0], color[1], color[2])


BOT_COLOR = rgb_color((0, 100, 255))
FOOD_COLOR = rgb_color((50, 255, 50))
POISON_COLOR = rgb_color((255, 50, 50))
EMPTY_COLOR = rgb_color((150, 150, 150))
BLOCK_COLOR = rgb_color((50, 50, 50))


class Cell(object):
    __window = None

    def __init__(self, pos, cell_type, win, cell_pos, color=EMPTY_COLOR, text=""):

        self.__pos = pos

        self.__cell_pos = cell_pos

        self.__rectangle = Rectangle(Point(pos[0], pos[1]),
                                     Point(pos[0] + CELL_DIMENSION[0], pos[1] + CELL_DIMENSION[1]))
        self.__rectangle.setFill(color)
        self.type = cell_type

        self.__text = Text(self.__rectangle.getCenter(), text)
        self.__text.setSize(7)

        if not self.__window:
            self.__window = win

    def draw(self):
        self.__rectangle.draw(self.__window)

    def set_fill(self, color):
        self.__rectangle.setFill(color)

    def set_text(self, text):
        self.__text.setText(text)

    def get_pos(self):
        return copy(self.__cell_pos)

    def undraw(self):
        try:
            self.__rectangle.undraw()
        except Exception as e:
            print(e)
            pass

    def draw_text(self):
        self.__text.draw(self.__window)

    def undraw_text(self):
        self.__text.undraw()
