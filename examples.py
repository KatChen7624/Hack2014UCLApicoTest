from connections import connect_mqtt, connect_internet
from time import sleep
from constants import ssid, mqtt_server, mqtt_user, mqtt_pass
from machine import Pin
from dht import DHT11
import ujson
from lib.hcsr04 import HCSR04




sensor_pin = Pin(15, Pin.IN, Pin.PULL_UP)
sensor = DHT11(sensor_pin)




ultrasensor1 = HCSR04(trigger_pin=16, echo_pin=0)

distance = ultrasensor1.distance_cm()

print('Distance:', distance, 'cm')



# Function to handle an incoming message

def cb(topic, msg):
#     print(f"Topic: {topic}, Message: {msg}")
    if topic == b"direction":
        if msg ==b"forward":
            print("Message from direction",msg) 
            #your forward function
        elif msg ==b"backward":
            print("Message from direction",msg) 
            #your backward function
        elif msg ==b"left":
            print("Message from direction",msg) 
            #your  left
        elif msg ==b"right":
            print("Message from direction",msg) 
            #your right
        elif msg ==b"stop":
            print("Message from direction",msg) 
            #your stop


    

def main():
    try:
        connect_internet(ssid,"87654321")
        client = connect_mqtt(mqtt_server, mqtt_user, mqtt_pass)

        client.set_callback(cb)
        client.subscribe("direction")
        while True:
            client.check_msg()
            sensor.measure()
            #may need to modify the name of the sensor
            temp = sensor.temperature()
            humidity = sensor.humidity()
            
            #To Tal: change the name of ultrasensor1 to whatever you named it
            distance_front = ultrasensor1.distance_cm()
            #To Tal: change the name of the second sensor
            distance_back=ultrasensor1.distance_cm()  
            
            # Data payload
            data = {
                "temp": temp,
                "humidity": humidity
            }

            ultraData = {
                "front": distance_front,
                "back": distance_back
            }
            print ("temp:",temp)
            print ("humidity",humidity)
            print ('Distance front:', distance_front, 'cm')
            print ("Distance back:", distance_back, 'cm')
            message = ujson.dumps(data)
            ultraMessage=ujson.dumps(ultraData)
            client.publish("temp&&humidity", message)
            client.publish("ultrasonic",ultraMessage)
            # To Tal: I change the sleep time from 2s to 1s, it may affect the performance of your car
            # You can change it back if you want
            sleep(1)

       

    except KeyboardInterrupt:
        print('keyboard interrupt')
        
        
if __name__ == "__main__":
    main()