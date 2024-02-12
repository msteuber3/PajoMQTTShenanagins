import paho.mqtt.client as mqtt
import time as sleepTime
from time import time
import json

fileSource = "./data/5MBDummyData.json"
fileName = " 5MBDummyData.json"
print(fileName)
jsonTestFile = open(fileSource, "r")
jsonContents = jsonTestFile.read() + fileName


# callback functions -
# on_log - log info when connected and disconnect
# on_connect - prints connection details

def on_log(client, userdata, level, buf):
    print("log: ", buf)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected")
    else:
        print("Connection failed. error code ", rc)


def on_message(client, userdata, message):
    print(message.topic + " " + str(message.payload.decode()))
    client.publish(message.topic + "/outbox", "I got %s" % message.payload.decode())


def on_publish(client, userdata, mid):
    print(time())


# Is called when publish() is called. Use this to make sure file size is the same on both ends and also return the time


broker = "10.147.18.165"

client = mqtt.Client("JsonSender")
print("Connecting to broker", broker)
client.username_pw_set("changlab", "electrode")
client.on_connect = on_connect
client.on_log = on_log
client.on_publish = on_publish

client.connect(broker, 1883, 60)
client.loop_start()
with open('./data/5MBDummyData.json') as jsonFile:
    jsonData = json.load(jsonFile)
    client.publish("/fileName", "5MBDummyData.json", 0)
    client.publish("/jsonData/", json.dumps(jsonData))

sleepTime.sleep(4)
client.loop_stop()
client.disconnect()
