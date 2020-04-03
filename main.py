from copy import copy
import random

from World import World

WORLD_DIMENSION = (48, 24)
STARTING_GENERATION = 64


def main():
    world = World(WORLD_DIMENSION)

    for _ in range(64):
        world.add_random_bot()

    generations = world.run()

    for gen in generations:
        for bot in gen:
            commands = copy(bot.get_commands())
            for _ in range(5):
                world.add_random_bot(command_list=commands)

            for _ in range(3):
                pos = random.randint(0, 63)
                commands[pos] = random.randint(0, 63)

                world.add_random_bot(command_list=commands)


main()
