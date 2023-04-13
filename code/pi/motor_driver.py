from machine import Pin, PWM


class Motor_Driver:
    motor1 = motor2 = motor3 = motor4 = freq = led = None

    def __init__(self, motor1, motor2, motor3, motor4, freq, led):
        self.motor1 = PWM(Pin(motor1), freq=freq)
        self.motor2 = PWM(Pin(motor2), freq=freq)
        self.motor3 = PWM(Pin(motor3), freq=freq)
        self.motor4 = PWM(Pin(motor4), freq=freq)
        self.led = Pin(led)

    def spin(self, speed: int):
        pass
