import sys;
import network;
from umqtt.simple import MQTTClient;
from random import randint, getrandbits
from machine import unique_id, Pin, PWM
import ubinascii
from ucryptolib import aes
import ujson
from crypt import CryptAes
import urequests;
import time

payloadRecv = False;
payload = 0;
red_led = Pin(14, Pin.OUT)
green_led = PWM(Pin(33), freq=1, duty=512) # pretend the onboard led is green
red_led.off()
currState = 0;

def connectToWifi(ssid, password):
  wlan = network.WLAN(network.STA_IF);
  wlan.active(True);

  if(not(wlan.isconnected())):
    wlan.connect(ssid, password);
    
    while(not(wlan.isconnected())):
      pass;
  
  return;

def myCallback1(topic, message):
  global payloadRecv;
  global payload;
  
  if(topic == b"Sensor_Data"):
    payloadRecv = True;
    payload = "{}".format(message)[2:-1];
    
  return;

def myCallback2(topic, message):
  global currState;
  global payloadRecv;
  global payload;
  
  if(topic == b"SessionID" and message == b"Confirmed"):
    currState = 1
    
  return;

def main():
  global currState
  ssid = "Testing";
  password = "Testing123";
  machine_id = ubinascii.hexlify(unique_id()).decode()
  print("Machine ID:", machine_id)
  connectToWifi(ssid, password);
  
  print("Connected to {}\n".format(ssid));
  
  client = MQTTClient(client_id=machine_id, server="farmer.cloudmqtt.com", port="14184", user="fuptiwvx", password="o10atNN8t_Fo");
  client.connect();
  client.set_callback(myCallback1);
  client.subscribe(b"Sensor_Data");
  
  while(True):
    time.sleep(1)
    if(currState == 0):
      seshid = str(randint(10000000,99999999)) + str(randint(10000000,99999999))
      print("session id", seshid)
      client.publish(b"SessionID", seshid);
      AES = CryptAes(seshid)
      currState = 1
      
    elif(currState == 1):
      currState = 0;
      client.wait_msg();
      if(payloadRecv):
        dec_payload_json = AES.decrypt(payload)
        if AES.verify_hmac(dec_payload_json) is True:
          print(dec_payload_json)
          print("Successful Decryption")
          ifttt_dict = {"value1": "{},{},{}".format(dec_payload_json["X"], dec_payload_json["Y"], dec_payload_json["Z"]), "value2": dec_payload_json["Temp"]}
          urequests.post("https://maker.ifttt.com/trigger/Spinner_2/with/key/l8EYTnrtKDTrocLKOWlaDyMMS0213VgEZiz6H6sFe7I", data=ujson.dumps(ifttt_dict), headers={"content-type": "application/json"});
          client.publish(b"Acknowledgement", b"Successful Decryption");
          if abs(float(dec_payload_json["X"])) > 1 or abs(float(dec_payload_json["Y"])) > 1 or abs(float(dec_payload_json["Z"])) > 1:
              red_led.on()
          else:
              red_led.off()
          green_led = PWM(Pin(33), freq=(5*int(abs(float(dec_payload_json["Temp"]) - 21))), duty=512)
        else:
          red_led.off()
          currState = 0;
          print("Failed Authentication")
          client.publish(b"Acknowledgement", b"Failed Authentication");

if __name__ == "__main__":
  main();