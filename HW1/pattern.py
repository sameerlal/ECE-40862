from machine import Pin
from time import sleep

red_led = Pin(27, Pin.OUT)
green_led = Pin(12, Pin.OUT)
push_1 = Pin(15, Pin.IN, Pin.PULL_UP)
push_2 = Pin(14, Pin.IN, Pin.PULL_UP)

red_led.value(0)
green_led.value(0)

count_1 = 0
count_2 = 0

tab = True
exiter = True
blinker = True

while(exiter):
    sleep(0.1)
    if tab:
        if push_1.value() == 0 and push_2.value() == 0:
            print("Case 1")
            red_led.value(0)
            green_led.value(0)
        elif push_1.value() == 0 and push_2.value() == 1:
            print("Case 2")
            count_2 += 1
            red_led.value(0)
            green_led.value(1)
        elif push_1.value() == 1 and push_2.value() == 0:
            print("Case 3")
            count_1 += 1
            red_led.value(1)
            green_led.value(0)
        elif push_1.value() == 1 and push_2.value() == 1:
            print("Case 4")
            count_2 += 1
            count_1 += 1
            red_led.value(0)
            green_led.value(0)
    else:
        red_led.value(blinker)
        green_led.value(not blinker)
        blinker = not blinker
    
    if count_1 >= 10 or count_2 >= 10:
        tab = False
        if (count_1 >= 10 and push_2.value() == 1) or (count_2 >= 10 and push_1.value() == 1):
            red_led.value(0)
            green_led.value(0)
            print("You have successfully implemented LAB1 DEMO!!!")
            exiter = False
