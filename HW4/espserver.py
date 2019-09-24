import esp32, socket, network
from machine import Pin, Timer
# Global variables
temp = 0 # measure temperature sensor data
hall = 0 # measure hall sensor data
red_led_state = "ON" # string, check state of red led, ON or OFF
green_led_state = "ON" # string, check state of red led, ON or OFF

def web_page():
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    TEMP, HALL, RED_LED_STATE, GREEN_LED_STAT
    """
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h2 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h2>ESP32 WEB Server</h2>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p><a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    <p>
    GREEN LED Current State: <strong>""" + green_led_state + """</strong>
    </p>
    <p>
    <a href="/?green_led=on"><button class="button">GREEN ON</button></a>
    </p>
    <p><a href="/?green_led=off"><button class="button button2">GREEN OFF</button></a>
    </p>
    </body>
    </html>"""
    return html_webpage


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

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)


while True:
    # Adapted from example on https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
    red_led = Pin(15, Pin.OUT)
    green_led = Pin(32, Pin.OUT)
    hall = esp32.hall_sensor()
    temp = esp32.raw_temperature()
    cl, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = cl.recv(1024)
    request = str(request, 'utf-8')
    print('Content = %s \n' % request)
    if '?red_led=on' in request:
        red_led.value(1)
        red_led_state = "ON"
    else:
        red_led.value(0)
        red_led_state = "OFF"
        
    if '?green_led=on' in request:
        green_led.value(1)
        green_led_state = "ON"
    else:
        green_led.value(0)
        green_led_state = "OFF"    
    
    response = web_page()
    cl.send('HTTP/1.1 200 OK\n')
    cl.send('Content-Type: text/html\n')
    cl.send('Connection: close\n\n')
    cl.send(response)
    cl.close()
    