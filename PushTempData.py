import os.path
import paho.mqtt.client as mqtt
import time as sleepTime
import time
import datetime
import json
import paho.mqtt.properties as props
from paho.mqtt.packettypes import PacketTypes


fileSource = "../Test/OfficeTemp.txt"
fileName = "OfficeTemp.txt"

# callback functions -
# on_log - log info when connected and disconnect
# on_connect - prints connection details

def on_log(client, userdata, level, buf):
    print("log: ", buf)


def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("connected")
    else:
        print("Connection failed. error code ", rc)


def on_message(client, userdata, message, properties):
    print(message.topic + " " + str(message.payload.decode()))
    client.publish(message.topic + "/outbox", "I got %s" % message.payload.decode())


def on_publish(client, userdata, mid, rc, properties):
    print(datetime.datetime.now())
    

# Reads data from the data file opened in binary mode one MB at a time using a generator
def count_generator(reader):     
    MBChunk = reader(1024 * 1024)
    while MBChunk:
        yield MBChunk
        MBChunk = reader(1024 * 1024)

# Is called when publish() is called. Use this to make sure file size is the same on both ends and also return the time


broker = "10.147.18.165"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="OfficeTemperatureDataSender", protocol=mqtt.MQTTv5)
print("Connecting to broker", broker)
client.username_pw_set("changlab", "electrode")
client.on_connect = on_connect
client.on_log = on_log
client.on_publish = on_publish

client.connect(broker, 1883, 60)
curLen = 0
size = 1
client.loop_start()

# Set publish properties
publish_properties = props.Properties(PacketTypes.PUBLISH)  # set the publish property to the PUBLISH packet type
props.MaximumPacketSize = 20

while True:
    client.loop()
    with open(fileSource, 'rb') as file:
        c_generator = count_generator(file.raw.read)
        size = sum(buffer.count(b'\n') for buffer in c_generator) #Stores the length of the sum of all line breaks of all individual chunks read by the generator 
        if size > curLen:   # Watches for a change in the size of fileSource, publishes the last line of fileSource when length is changed 
            curLen = size
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
            sendData = file.readline().decode()
            publish_properties.UserProperty = [('File-Name', fileName),  # Property 1 - File name
                                       ("File-Size", str(len(sendData)))]  # Property 2 - File size
            payload = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ": " + sendData
            client.publish("/TemperatureData/",payload, 0, False, properties=publish_properties)
            publish_properties.UserProperty.clear()
    
    
