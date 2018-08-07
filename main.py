from time import sleep
from world import World


def main():
    world = World(10, 10, 10)
    # world.show()
    # world.cycle()
    # world.show()
    # world.print_bots()
    # world._map.print_manual()
    # world._map.print_2d()
    world.show_animation()

    # for i in range(10):
    #     world.show()
    #     world.diag_shake()
    #     sleep(0.2)


if __name__ == "__main__":
    main()
