############### Imports ###############
import random
import time

import machine
import network
import ubinascii
from umqttsimple import MQTTClient

#######################################

#### Network credentials ####
ssid = "iPhone de Marcos"
password = "hola1234"
mqtt_server = "172.20.10.2"
mqtt_user = "iot"
mqtt_pass = "2024"

###########################

#### MQTT setup ####
client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = b"notification"

##################

#### Connect to Wi-Fi ####
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    pass

print("Connection successful")
print(station.ifconfig())

########################


#### Function to generate random data ####
def generate_data():
    humidity = random.randint(30, 90)
    temperature = round(random.uniform(15.0, 30.0), 2)
    status = "OK" if humidity < 70 else "Error"
    return {"humidity": humidity, "status": status, "temperature": temperature}


#######################################


#### Connect to MQTT broker ####
def connect_mqtt():
    client = MQTTClient(client_id, mqtt_server, user=mqtt_user, password=mqtt_pass)
    client.connect()
    print("Connected to MQTT broker")
    return client


###############################


#### Main loop to publish data ####
def main():
    client = connect_mqtt()
    while True:
        data = generate_data()
        msg = str(data).replace("'", '"')
        client.publish(topic_pub, msg)
        print(f"Published: {msg}")
        time.sleep(5)


if __name__ == "__main__":
    main()

##################################
