from motor_driver import Motor_Driver


class Drone_Driver:
    def __init__(self):
        self.front = (Motor_Driver.motor1, Motor_Driver.motor2)
        self.back = (Motor_Driver.motor3, Motor_Driver.motor4)
        self.left = (Motor_Driver.motor1, Motor_Driver.motor3)
        self.right = (Motor_Driver.motor2, Motor_Driver.motor4)
        self.all = (Motor_Driver.motor1, Motor_Driver.motor2, Motor_Driver.motor3, Motor_Driver.motor4)

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
