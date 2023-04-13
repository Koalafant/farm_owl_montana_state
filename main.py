import utime, math
from machine import Pin, PWM


# Entry Point into Raspberry Pi
def main():
    led = Pin(25, Pin.OUT)
    pwm_led = PWM(led)
    pwm_led.freq(1000)
    led_value = 0
    led_brightness = 5

    while True:
        print(led_value)
        led_value += led_brightness
        pwm_led.duty_u16(int(led_value * 500))
        utime.sleep_ms(100)
        if led_value >= 100:
            led_value = 100
            led_brightness = -5
        elif led_value <= 0:
            led_value = 0
            led_brightness = 5


if __name__ == "__main__":
    main()
