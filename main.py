import utime
from machine import Pin, PWM
from code.pi import drone_driver as DD


def test_mode():
    led = Pin(25, Pin.OUT)
    pwm_led = PWM(led)
    pwm_led.freq(1000)
    throttle_value = 0
    throttle_increment = 5

    while True:
        print(throttle_value)

        # Increase throttle
        throttle_value += throttle_increment

        # Duty cycle
        pwm_led.duty_u16(int(throttle_value * 500))

        utime.sleep_ms(100)

        # 0 - 100 throttle
        if throttle_value >= 100:
            throttle_value = 100
            throttle_increment = -5
        elif throttle_value <= 0:
            throttle_value = 0
            throttle_increment = 5


# Entry Point for flight control
def main():
    print("hello")
    dd = DD.Drone_Driver()

    dd.debug()


if __name__ == "__main__":
    main()
