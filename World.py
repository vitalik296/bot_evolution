import random
from copy import copy

from graphics import GraphWin, Text, Point

from Bot import COMMAND_LIST_LEN, Bot
from Cell import Cell, WALL, EMPTY, CELL_DIMENSION, FOOD, FOOD_COLOR, POISON_COLOR, EMPTY_COLOR, BLOCK_COLOR

WINDOW_DIMENSION = (1200, 600)
OFFSET = 100
BOT_MIN_COUNT = 8
FILL_MULTIPLIER = 0.5
DAY_LIMIT = 500000
GENERATION_LIMIT = 10000

DEBUG = False


class Singleton(type):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instance


class World(metaclass=Singleton):

    def __init__(self, dimension):
        self.__dimension = dimension
        self.__square = (self.__dimension[0] - 2) * (self.__dimension[1] - 2)
        self.__day = 0
        self.__generation = 1

        self.__cells = []

        self.__bots = []
        self.__foods = []
        self.__poisons = []

        self.__day_counter = None
        self.__generation_counter = None
        self.__bot_counter = None

        self.__last_try = []
        self.__try_texts = []

        self.__win = GraphWin(title="World Evolution v2.0", width=WINDOW_DIMENSION[0], height=WINDOW_DIMENSION[1])

        self.__create_window()

    def __create_window(self):
        for row in range(self.__dimension[1]):
            for coll in range(self.__dimension[0]):
                cell_position = (OFFSET + CELL_DIMENSION[0] * coll, OFFSET + CELL_DIMENSION[1] * row)

                if row == 0 or row == self.__dimension[1] - 1 or coll == 0 or coll == self.__dimension[0] - 1 or\
                        (coll == 15 and row < 18) or (coll == 32 and row > 13):
                    cell_type = WALL
                    cell = Cell(pos=cell_position, cell_type=cell_type, win=self.__win, cell_pos=(coll, row),
                                color=BLOCK_COLOR)
                else:
                    cell_type = EMPTY
                    cell = Cell(pos=cell_position, cell_type=cell_type, win=self.__win, cell_pos=(coll, row))

                cell.draw()

                self.__cells.append(cell)

        self.__day_counter = Text(Point(150, OFFSET + CELL_DIMENSION[1] * (self.__dimension[1] + 2)),
                                  f"Day: {self.__day}")
        self.__day_counter.draw(self.__win)

        self.__generation_counter = Text(Point(OFFSET + CELL_DIMENSION[0] * self.__dimension[0] - 100,
                                               OFFSET + CELL_DIMENSION[1] * (self.__dimension[1] + 2)),
                                         f"Generation: {self.__generation}")
        self.__generation_counter.draw(self.__win)

        self.__bot_counter = Text(Point(OFFSET + CELL_DIMENSION[0] * self.__dimension[0] - 375,
                                        OFFSET + CELL_DIMENSION[1] * (self.__dimension[1] + 2)),
                                  f"Bots count: {len(self.__bots)}")
        self.__bot_counter.draw(self.__win)

        text = Text(Point(OFFSET + self.__dimension[0] * CELL_DIMENSION[0] + 2 * OFFSET, OFFSET),
                    "Last generation duration:").draw(self.__win)
        text.setSize(18)

        for i in range(10):
            text = Text(Point(OFFSET + self.__dimension[0] * CELL_DIMENSION[0] + 2 * OFFSET,
                              OFFSET + 2 * CELL_DIMENSION[0] * (i + 1)), "")
            text.draw(self.__win)
            self.__try_texts.append(text)

    def __get_empty_cell(self):
        try_num = 0
        while True:
            if try_num >= 50:
                return None
            coll = random.randint(1, self.__dimension[0] - 2)
            row = random.randint(1, self.__dimension[1] - 2)

            if self.__cells[row * self.__dimension[0] + coll].type == 0:
                break
            try_num += 1

        return self.__cells[row * self.__dimension[0] + coll]

    def __add_interaction(self):
        if len(self.__foods) + len(self.__poisons) <= FILL_MULTIPLIER * self.__square:

            cell = self.__get_empty_cell()

            inter_seed = random.randint(0, 10500)

            if inter_seed % 3 == 0:
                self.__poisons.append(cell)
                cell.type = 3
                cell.set_fill(POISON_COLOR)
            else:
                self.__foods.append(cell)
                cell.type = 2
                cell.set_fill(FOOD_COLOR)

    def remove_food(self, cell):
        self.__foods.remove(cell)
        cell.set_fill(EMPTY_COLOR)
        cell.type = EMPTY

    def change_to_food(self, cell):
        self.__poisons.remove(cell)
        self.__foods.append(cell)
        cell.set_fill(FOOD_COLOR)
        cell.type = FOOD

    def add_random_bot(self, command_list=None):

        bot_cell = self.__get_empty_cell()

        if not bot_cell:
            return

        if not command_list:
            command_list = [24 for _ in range(COMMAND_LIST_LEN)]

        self.__bots.append(Bot(bot_cell, copy(command_list), self))

        self.__bot_counter.setText(f"Bots count: {len(self.__bots)}")

    def remove_bot(self, bot_to_del):
        self.__bots.remove(bot_to_del)
        self.__bot_counter.setText(f"Bots count: {len(self.__bots)}")

    def get_cell(self, pos):
        return self.__cells[pos[1] * self.__dimension[0] + pos[0]]

    def add_poison(self, cell):
        self.__poisons.append(cell)
        cell.type = 3
        cell.set_fill(POISON_COLOR)

    def __update_try_texts(self):
        i = 1
        for text in self.__try_texts:
            try:
                text.setText(self.__last_try[-i][0])
            except IndexError:
                break
            i += 1

    def __add_try(self, res):
        self.__last_try.append(res)
        self.__update_try_texts()

    def run(self):
        while True:

            if DEBUG:
                input()

            self.__day += 1
            self.__day_counter.setText(f"Day: {self.__day}")

            for bot in self.__bots:
                bot.step()
                self.__add_interaction()
                # sleep(0.05)

            if len(self.__bots) <= BOT_MIN_COUNT or self.__day >= DAY_LIMIT or self.__generation >= GENERATION_LIMIT:
                self.__add_try((self.__day, self.__generation))
                self.__day = 0
                self.__generation += 1
                self.__generation_counter.setText(f"Generation: {self.__generation}")

                if self.__bots:
                    yield copy(self.__bots)
                else:
                    self.__win.getMouse()
                    self.__win.close()
                    return []
