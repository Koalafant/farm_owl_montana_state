from code.pi.motor_driver import Motor_Driver as MD


class Drone_Driver:
    def __init__(self):
        self.front = (MD.motor1, MD.motor2)
        self.back = (MD.motor3, MD.motor4)
        self.left = (MD.motor1, MD.motor3)
        self.right = (MD.motor2, MD.motor4)
        self.all = (MD.motor1, MD.motor2, MD.motor3, MD.motor4)

    def thrust(self, speed: int):
        pass

    def move_forward(self, percent: float):
        pass

    def move_backward(self, percent: float):
        pass

    def move_left(self, percent: float):
        pass

    def move_right(self, percent: float):
        pass

    def move_up(self, percent: float):
        pass

    def move_down(self, percent: float):
        pass

    def debug(self):
        print(f'{self.all}')


def main():
    dd = Drone_Driver()

    dd.debug()


if __name__ == "__main__":
    main()
