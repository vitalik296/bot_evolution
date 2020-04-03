from Cell import EMPTY, WALL, FOOD, POISON, BOT, EMPTY_COLOR, BOT_COLOR

COMMAND_LIST_LEN = 64


class Bot(object):
    __world = None

    def __init__(self, cell, command_list, world=None):
        self.energy = 64
        self.__is_alive = True
        self.__current_command = 0
        self.__command_list = command_list

        self.__iteration = 0

        if not self.__world:
            self.__world = world

        self.__cell = cell
        self.__activate_cell()

    def __activate_cell(self):
        self.__cell.set_fill(BOT_COLOR)
        self.__cell.set_text(self.energy)
        self.__cell.type = BOT
        self.__cell.draw_text()

    def __deactivate_cell(self):
        self.__cell.undraw_text()
        self.__cell.set_fill(EMPTY_COLOR)
        self.__cell.type = EMPTY

    def __get_command(self):
        return self.__command_list[self.__current_command]

    def __change_current_command(self, change):
        self.__current_command += change
        self.__current_command %= COMMAND_LIST_LEN

    def change_energy(self, change_count):
        self.energy += change_count
        self.__cell.set_text(self.energy)

    def __get_direction(self, direction):
        x, y = self.__cell.get_pos()

        if direction in (1, 2, 3):
            x += 1
        elif direction in (5, 6, 7):
            x -= 1

        if direction in (7, 0, 1):
            y -= 1
        elif direction in (3, 4, 5):
            y += 1

        return x, y

    def __change_position(self, new_pos):
        self.__deactivate_cell()

        new_cell = self.__world.get_cell(new_pos)

        self.__cell = new_cell
        self.__activate_cell()

    def __eat(self, cell):
        self.__world.remove_food(cell)
        self.change_energy(10)

    def move(self, direction):
        new_pos = self.__get_direction(direction)

        cell = self.__world.get_cell(new_pos)

        cell_type = cell.type

        if cell_type == EMPTY:
            self.__change_position(new_pos)
            self.__change_current_command(5)
        elif cell_type == WALL:
            self.__change_current_command(1)
        elif cell_type == FOOD:
            self.__eat(cell)
            self.__change_position(new_pos)
            self.__change_current_command(3)
        elif cell_type == POISON:
            self.die()
            self.__world.add_poison(self.__cell)
            return
        else:
            self.__change_current_command(2)

        self.change_energy(-1)

    def take(self, direction):
        cell_pos = self.__get_direction(direction)
        cell = self.__world.get_cell(cell_pos)

        cell_type = cell.type

        if cell_type == EMPTY:
            self.__change_current_command(5)
        elif cell_type == WALL:
            self.__change_current_command(1)
        elif cell_type == FOOD:
            self.__eat(cell)
            self.__change_current_command(3)
        elif cell_type == POISON:
            self.__world.change_to_food(cell)
            self.__change_current_command(4)
        else:
            self.__change_current_command(2)

        self.change_energy(-1)

    def see(self, direction):
        self.__iteration += 1

        cell = self.__get_direction(direction)
        cell_type = self.__world.get_cell(cell).type

        if cell_type == EMPTY:
            self.__change_current_command(5)
        elif cell_type == WALL:
            self.__change_current_command(1)
        elif cell_type == FOOD:
            self.__change_current_command(3)
        elif cell_type == POISON:
            self.__change_current_command(4)
        else:
            self.__change_current_command(2)

        self.step()

    def wait(self):
        self.__change_current_command(1)
        self.change_energy(-1)

    def die(self):
        self.__is_alive = False

        self.__deactivate_cell()

        self.__world.remove_bot(self)

    def step(self):

        if not self.__is_alive:
            return

        if self.__iteration >= 15:
            self.change_energy(-1)
            self.__change_current_command(1)
            return

        command = self.__get_command()

        if command < 8:
            self.move(command)
        elif command < 16:
            self.take(command % 8)
        elif command < 24:
            self.see(command % 8)
        elif command == 24:
            self.wait()
        else:
            self.__iteration += 1
            self.__change_current_command(command)
            self.step()

        if self.energy <= 0 and self.__is_alive:
            self.die()
            return

        self.__iteration = 0

    def get_commands(self):
        return self.__command_list
