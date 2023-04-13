from drone_driver import Drone_Driver


class Controller:
    def __init__(self, front_set, back_set, left_set, right_set):
        self.front_set = front_set
        self.back_set = back_set
        self.left_set = left_set
        self.right_set = right_set

    def forward(self, distance):
        pass

    def backward(self, distance):
        pass

    def left(self, distance):
        pass

    def right(self, distance):
        pass

    def up(self, distance):
        pass

    def down(self, distance):
        pass


def main():
    drone_driver = Drone_Driver()
    pass


if __name__ == "__main__":
    main()
