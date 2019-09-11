from machine import RTC, Timer, Pin, ADC, PWM
from time import sleep

flipper = True
first = False

def adc_callback(p):
    if first:
        if flipper:
            red.freq(int(adc.read()/25))
        else:
            green.duty(int(adc.read()))

def button_irqhandler(p):
    global flipper
    global first
    if flipper:
        print("Changing green duty")
    else:
        print("Changing red freq")
    first = True
    flipper = not flipper

year = int(input("Year? "))
month = int(input("Month? "))
day = int(input("Day? "))
weekday = int(input("Weekday? "))
hour = int(input("Hour? "))
minute = int(input("Minute? "))
second = int(input("Second? "))
microsecond = int(input("Microsecond? "))

rtc = RTC()
rtc.datetime((year, month, day, weekday, hour, minute, second, microsecond))

# Hardware timer
timer_hardware = Timer(0)
timer_hardware.init(period=30000, mode=Timer.PERIODIC, callback=lambda t:print(rtc.datetime()))

# PWM 0
red = PWM(Pin(15), freq=100, duty=256)
green = PWM(Pin(12), freq=100, duty=256)

# Software timer and ADC
adc = ADC(Pin(32))
adc.width(ADC.WIDTH_9BIT)
adc.atten(ADC.ATTN_11DB)
timer_software = Timer(-1)
timer_software.init(period=100, mode=Timer.PERIODIC, callback=adc_callback)

# Button
button = Pin(21, Pin.IN, Pin.PULL_DOWN)
button.irq(trigger=Pin.IRQ_RISING, handler=button_irqhandler)

while True:
    pass