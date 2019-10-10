import esp32, socket, network
from machine import RTC, Timer, Pin, ADC, PWM, I2C
from math import atan, sqrt
import ubinascii

old_temp = 0

def convert(val):
    if val & (1 << 15):
        val = val - 1 << 16
    return val

# 3.2.2 Interfacing sensors
def interface_sensors():
    if i2c.readfrom_mem(83, 0, 1) == b'\xe5':
        i2c.writeto_mem(83, 0x2D, b"\x08")
        i2c.writeto_mem(83, 0x2C, b'\x0D')
        i2c.writeto_mem(83, 0x1E, b'\x00')
        i2c.writeto_mem(83, 0x1F, b'\x00')
        i2c.writeto_mem(83, 0x20, b'\x00')
        i2c.writeto_mem(83, 0x31, b"\b00001000")
        print("yeet")
        
    if i2c.readfrom_mem(72, 0x0B, 1) == b'\xcb':
        i2c.writeto_mem(72, 0x03, b'\x80')
        print("temp sensor recognized")
    
# 3.2.3 Demo
def spinner_demo(p):
    global old_temp
    ax = convert(int.from_bytes(i2c.readfrom_mem(83, 0x33, 1) + i2c.readfrom_mem(83, 0x32, 1), "big"))/25
    ay = convert(int.from_bytes(i2c.readfrom_mem(83, 0x35, 1) + i2c.readfrom_mem(83, 0x34, 1), "big"))/25
    az = convert(int.from_bytes(i2c.readfrom_mem(83, 0x37, 1) + i2c.readfrom_mem(83, 0x36, 1), "big"))/(25)
    if ax >= -0.5 and ax <= 0.5 and ay >= -0.5 and ay <= 0.5:
        green_led.on()
    else:
        green_led.off()
        
    if ax >= 10 or ax <= -10 or ay >= 10 or ay <= -10 or az >= 10 or az <= -10:
        red_led.on()
    print("XYZ =", ax, ay, az)
    pitch = atan(ax/sqrt(ay*2 + az*2)) * 57.2958
    roll  = atan(ay/sqrt(ax*2 + az*2)) * 57.2958
    try:
        theta = atan(sqrt(ax*2 + ay*2)/az) * 57.2958
    except (Exception):
        theta = 0
    if theta <= -30 or theta >= 30 or pitch <= -30 or pitch >= 30 or roll <= -30 or roll >= 30:
        yellow_led.on()
    else:
        yellow_led.off()
    print("Pitch, Roll, Theta =", pitch, roll, theta)
    data = bytearray(2)
    i2c.readfrom_mem_into(72, 0x00, data)
    value = data[0] << 8 | data[1]
    temp = (value & 0b111111111111) / 128
    if old_temp == 0:
        old_temp = temp
    pwm_cycle = PWM(Pin(13), freq=(10 - int(temp - old_temp)), duty=512)
    print("Temperature =", temp)
    print("--------------------------------------------")

def button_irqhandler_1(p):
    onboard_led = Pin(13, Pin.OUT)
    onboard_led.on()
    green_led.off()
    yellow_led.off()
    interface_sensors()
    
def button_irqhandler_2(p):
    pwm_cycle = PWM(Pin(13), freq=10, duty=512)
    tim1.init(period=1000, mode=Timer.PERIODIC, callback=spinner_demo)

# Initialize timers
tim1 = Timer(0)

# Initialize leds
green_led = Pin(32, Pin.OUT)
yellow_led = Pin(33, Pin.OUT)
red_led = Pin(14, Pin.OUT)

# Initialize buttons
button1 = Pin(21, Pin.IN, Pin.PULL_DOWN)
button1.irq(trigger=Pin.IRQ_RISING, handler=button_irqhandler_1)

button2 = Pin(26, Pin.IN, Pin.PULL_DOWN)
button2.irq(trigger=Pin.IRQ_RISING, handler=button_irqhandler_2)

# Initialize I2C pins
i2c = I2C(scl=Pin(22, Pin.PULL_UP), sda=Pin(23, Pin.PULL_UP), freq=400000)

# comment this out during demo
green_led.off()
yellow_led.off()
red_led.off()
