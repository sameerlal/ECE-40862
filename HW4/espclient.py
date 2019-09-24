import esp32, socket, network
from machine import Pin, Timer
from time import sleep

def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

def send_to_thingspeak(s):
    temp = str(esp32.raw_temperature())
    hall = str(esp32.hall_sensor())
    http_get("https://api.thingspeak.com/update?api_key=874AXTQANC5L2GCO&field1=" + temp + "&field2=" + hall)
    print("Temperature:", temp)
    print("Hall:", hall)

API_KEY = "874AXTQANC5L2GCO"
red_led = Pin(15, Pin.OUT)
green_led = Pin(32, Pin.OUT)

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

tim0 = Timer(0)
tim0.init(period=10000, mode=Timer.PERIODIC, callback=send_to_thingspeak)







