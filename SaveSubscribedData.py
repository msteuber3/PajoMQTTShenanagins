import paho.mqtt.client as mqtt
import json
import time
from time import time


# callback functions -
# on_log - log info when connected and disconnect
def on_log(client, userdata, level, buf):
    print("log: ", buf)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected")
    else:
        print("Connecion failed. error code ", rc)


def on_message(client, userdata, message):
    filename = ""
    if message.topic == "/fileName/":
        filename = message.payload
    elif message.topic == "/jsonData/":
        writeData = open("5MBDummyData.json", "w")
        writeData.write(message.payload.decode())


# client.publish(message.topic + "/outbox", "I got %s" % message.payload.decode())
def on_subscribe(client, userdata, mid, qos):
    print("Successfully subscribed")
    print(mid)


# on_connect - prints connection details
broker = "10.147.18.165"

client = mqtt.Client("JsonSubscriber")
print("Connecting to broker", broker)
client.username_pw_set("changlab", "electrode")
client.on_connect = on_connect
client.on_log = on_log
client.on_message = on_message
client.on_subscribe = on_subscribe

client.connect(broker, 1883, 60)
client.subscribe("/jsonData/", 0)
client.loop_forever()

# client.loop_stop()
# client.disconnect()
