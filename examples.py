from connections import connect_mqtt, connect_internet
from time import sleep
from constants import ssid, mqtt_server, mqtt_user, mqtt_pass
from machine import Pin
from dht import DHT11
import ujson




sensor_pin = Pin(15, Pin.IN, Pin.PULL_UP)
sensor = DHT11(sensor_pin)

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
        #     sleep(1)

        # while True:
            sensor.measure()
            temp = sensor.temperature()
            humidity = sensor.humidity()
            
            # Data payload
            data = {
                "temp": temp,
                "humidity": humidity
            }
            print ("temp:",temp)
            print ("humidity",humidity)
            message = ujson.dumps(data)
            
            client.publish("temp&&humidity", message)
        
            sleep(2)

       

    except KeyboardInterrupt:
        print('keyboard interrupt')
        
        
if __name__ == "__main__":
    main()