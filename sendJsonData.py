import paho.mqtt.client as mqtt
import time


fileSource = "./data/SampleText.json"
jsonTestFile = open(fileSource)


# callback functions -
# on_log - log info when connected and disconnect
# on_connect - prints connection details

def on_log(client, userdata, level, buf):
    print("log: ", buf)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected")
    else:
        print("Connecion failed. error code ", rc)


def on_message(client, userdata, message):
    print(message.topic + " " + str(message.payload.decode()))
    client.publish(message.topic + "/outbox", "I got %s" % message.payload.decode())



#TODO - on_publish
def on_publish(client, userdata, mid):
# Is called when publish() is called. Use this to make sure file size is the same on both ends and also return the time


broker = "10.147.18.165"

client = mqtt.Client("changlab")
print("Connecting to broker", broker)
client.username_pw_set("changlab", "electrode")
client.on_connect = on_connect
client.on_log = on_log

client.connect(broker, 1883, 60)
client.loop_start()
#client.publish("/jsonData/", jsonTestFile)
time.sleep(4)
client.loop_stop()
client.disconnect()
