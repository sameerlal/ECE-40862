import sys;
from machine import Pin, I2C, unique_id;
import network;
from umqtt.simple import MQTTClient;
from ucryptolib import aes;
import ubinascii;
from crypt import CryptAes;
import urequests;
import ujson;

sessionIDRecv = False;
sessionID = 0;
ackRecv = False;
ack = 0;

def connectToWifi(ssid, password):
  wlan = network.WLAN(network.STA_IF);
  wlan.active(True);

  if(not(wlan.isconnected())):
    wlan.connect(ssid, password);
    
    while(not(wlan.isconnected())):
      pass;
  
  return;

def myCallback(topic, message):
  global sessionIDRecv;
  global sessionID;
  global ackRecv;
  global ack;
  
  if(topic == b"SessionID"):
    sessionIDRecv = True;
    sessionID = message;
  elif(topic == b"Acknowledgement"):
    ackRecv = True;
    ack = message;
    
  return;

def twosComplement(hexBytesObj):
  test = "{:016b}".format(int.from_bytes(hexBytesObj, "big"));
  testing = bytes([int(x) for x in test]);
  temp = "";
  twosC = "";
  
  for i in range(len(testing)-1, -1, -1):
    if(int(testing[i]) != 1):
      temp += str(int(testing[i]));
    else:
      temp += str(int(testing[i]));
      
      for j in range(i-1, -1, -1):
        temp += str(int(not(testing[j])));
      
      break;
      
  for i in range(len(temp)-1, -1, -1):
    twosC += temp[i];
    
  twosC = int(twosC, 2);
  
  if(testing[0] == 0):
    twosC -= 2**16;
    
  return(twosC);

def leftSwitchIRQ(pinNum, onBoardLED, i2c):
  deviceIDs = i2c.scan();
  
  onBoardLED.on();
  
  print("Initialization and calibration of sensors started...");
  i2c.writeto_mem(deviceIDs[1], 0x31, b"\x00");
  i2c.writeto_mem(deviceIDs[1], 0x2C, b"\x0D");
  i2c.writeto_mem(deviceIDs[1], 0x1E, b"\x00");
  i2c.writeto_mem(deviceIDs[1], 0x1F, b"\x00");
  i2c.writeto_mem(deviceIDs[1], 0x20, b"\x00");
  i2c.writeto_mem(deviceIDs[1], 0x2D, b"\x08");
  
  i2c.writeto_mem(deviceIDs[0], 0x03, b"\x80");
  print("Initialization and calibration of sensors finished.\n");
  
  return;
  
def rightSwitchIRQ(pinNum, onBoardLED, i2c):
  ssid = "Testing";
  password = "Testing123";
  
  print("Connecting to {}...".format(ssid));
  connectToWifi(ssid, password);
  print("Connected to {}\n".format(ssid));
  
  onBoardLED.off();
  
  currState = 0;
  
  client = MQTTClient(client_id="myMac0", server="farmer.cloudmqtt.com", port="14184", user="fuptiwvx", password="o10atNN8t_Fo");
  aclient = MQTTClient(client_id="myMac1", server="farmer.cloudmqtt.com", port="14184", user="fuptiwvx", password="o10atNN8t_Fo");
  aaclient = MQTTClient(client_id="myMac2", server="farmer.cloudmqtt.com", port="14184", user="fuptiwvx", password="o10atNN8t_Fo");
    
  client.set_callback(myCallback);
  aclient.set_callback(myCallback);

  client.connect();
  client.subscribe(b"SessionID");
  
  while(True):
    if(currState == 0):
      print("Waiting for sessionID...");
      client.wait_msg();
    
      if(sessionIDRecv):
        print("SessionID received: {}\n".format(sessionID));
        
        currState = 1;
    elif(currState == 1):
      deviceIDs = i2c.scan();
    
      xAccel = "{:016f}".format(twosComplement(i2c.readfrom_mem(deviceIDs[1], 0x33, 1)+i2c.readfrom_mem(deviceIDs[1], 0x32, 1))*0.02);
      yAccel = "{:016f}".format(twosComplement(i2c.readfrom_mem(deviceIDs[1], 0x35, 1)+i2c.readfrom_mem(deviceIDs[1], 0x34, 1))*0.02);
      zAccel = "{:016f}".format(twosComplement(i2c.readfrom_mem(deviceIDs[1], 0x37, 1)+i2c.readfrom_mem(deviceIDs[1], 0x36, 1))*0.001);

      temp = "{:016f}".format(int.from_bytes(i2c.readfrom_mem(deviceIDs[0], 0x00, 2), "big")/140);
      
      myCrypt = CryptAes(sessionID);
      
      myCrypt.encrypt([xAccel, yAccel, zAccel, temp]);
      
      hmac_signed = myCrypt.sign_hmac(sessionID);
      
      dataJSON = myCrypt.send_mqtt(hmac_signed);
      
      aclient.connect();
      aclient.subscribe(b"Acknowledgement");
      
      print("Sending JSON data...");
      client.publish(b"Sensor_Data", dataJSON);
      print("JSON data sent: {}\n".format(dataJSON));
      
      currState = 2;
    elif(currState == 2):
      print("Waiting for acknowledgement...");
      aclient.wait_msg();
      
      if(ackRecv):
        print("Acknowledgement received: {}\n".format(ack));
        if(ack == b"Successful Decryption"):
          print("Sending sensor values to google sheets...")
          urequests.post("https://maker.ifttt.com/trigger/Spinner1/with/key/6TmM-nq9D6FckShecNcC3", data=ujson.dumps({"value1": "{}, {}, {}".format(xAccel, yAccel, zAccel), "value2": temp}), headers={"content-type": "application/json"});
          print("Sent sensor values to google sheets.\n");
        currState = 0;
        
  return;

def main(argv):
  onBoardLED = Pin(13, Pin.OUT, Pin.PULL_DOWN, value=0);
  leftSwitch = Pin(26, Pin.IN, Pin.PULL_DOWN);
  rightSwitch = Pin(25, Pin.IN, Pin.PULL_DOWN);
  i2c = I2C(scl=Pin(22, Pin.PULL_UP), sda=Pin(23, Pin.PULL_UP), freq=400000);
  
  leftSwitch.irq(trigger=Pin.IRQ_RISING, handler=lambda pinNum: leftSwitchIRQ(pinNum, onBoardLED, i2c));
  rightSwitch.irq(trigger=Pin.IRQ_RISING, handler=lambda pinNum: rightSwitchIRQ(pinNum, onBoardLED, i2c));
  
  return;

if __name__ == "__main__":
  main(sys.argv);