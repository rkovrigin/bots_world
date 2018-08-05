from time import sleep
from world import World


def main():
    world = World(10, 10, 10)
    # world.show()
    world.cycle()
    # world.show()
    world.print_bots()
    world.show()
    world._map.print_2d()

    # for i in range(10):
    #     world.show()
    #     world.diag_shake()
    #     sleep(0.2)


if __name__ == "__main__":
    main()
