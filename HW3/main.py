import sys, esp32, network, ntptime
from machine import RTC, Timer, Pin, TouchPad, deepsleep, wake_reason

def green_led_touch_callback(green_led_touch, green_led):
    if green_led_touch.read() >= 485: 
        green_led.value(0)
    else:
        green_led.value(1)

def green_led_touch():
    green_led_timer = Timer(1)
    green_led_touch = TouchPad(Pin(4))
    green_led = Pin(21, Pin.OUT)
    green_led_timer.init(mode=Timer.PERIODIC, period=10, callback=lambda x: green_led_touch_callback(green_led_touch, green_led))
  
def sleep_callback(p):
    ext1_pins = [Pin(39, Pin.IN), Pin(36, Pin.IN)]
    touchRed = TouchPad(Pin(14)).config(550)
    esp32.wake_on_ext1(ext1_pins, esp32.WAKEUP_ANY_HIGH)
    esp32.wake_on_touch(True)
    print("I am awake, but going to deepsleep")
    redLed = Pin(13, Pin.OUT, value=0)
    deepsleep(60000)

# Main stuff here
redLed = Pin(13, Pin.OUT, value=1)

if(wake_reason() == 3):
    print("Woke up due to EXT1")
elif(wake_reason() == 5):
    print("Woke up due to Touchpad")
elif(wake_reason() == 4):
    print("Woke up due to timer")
else:
    print("Unknown wake code")
    
# Wi-fi settings    
ssid = "IP multiple times a day"
password = "santhosh97"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if(not(wlan.isconnected())):
    wlan.connect(ssid, password)
    while(not(wlan.isconnected())):
        pass

print("Connected to:", ssid)
print("MAC Address:", wlan.config("mac"))
print("IP Address:", wlan.ifconfig()[0])

# Setting time using ntp
ntptime.settime()
rtc = RTC()
year, month, day, weekday, hours, minutes, seconds, microseconds = rtc.datetime()
rtc.datetime((year, month, day, weekday, hours - 4, minutes, seconds, microseconds))
myDateTimeTimer = Timer(0)
myDateTimeTimer.init(mode=Timer.PERIODIC, period=15000, callback=lambda x:print("Date: ", rtc.datetime()[2], "/", rtc.datetime()[1], "/", rtc.datetime()[0], "\n Time: ", rtc.datetime()[4], ":", rtc.datetime()[5], ":", rtc.datetime()[6]))
    
green_led_touch()
sleep_timer = Timer(2)
sleep_timer.init(mode=Timer.PERIODIC, period=30000, callback=sleep_callback)
