import os
import warnings
import paho.mqtt.client as mqtt


# callback functions -
# on_log - log info when connected and disconnect
def on_log(client, userdata, level, buf):
    print("log: ", buf)

# on_connect - prints connection details
def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("connected")
    else:
        print("Connecion failed. error code ", rc)


# on_message - called when a message is received and processes that message

# Input contract:
# Each message contains two properties, a topic, and a payload.
# This callback only works when all of those are not null
# Message properties - ("File-Name", fileName) and ("File-Size", fileSize)
# File size is a string representation of the file size in bytes
# Message topic is the pathname
def on_message(client, userdata, message):
    try:
        filename = message.properties.UserProperty[0][1]
        recievedfilesize = message.properties.UserProperty[1][1]
        writedata = open("." + message.topic + filename, "w")
        writedata.write(message.payload.decode())
        filesize = os.path.getsize("." + message.topic + filename)
        if filesize != int(recievedfilesize):
            warnings.warn("PACKET LOSS OF " + str(int(recievedfilesize) - filesize) + " BYTES")
    except Exception as e:
        print(e)


# client.publish(message.topic + "/outbox", "I got %s" % message.payload.decode())
def on_subscribe(client, userdata, mid, qos, properties):
    print("Successfully subscribed")
    print(mid)


broker = "10.147.18.165"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "JsonSubscriber", protocol=mqtt.MQTTv5)
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
