import paho.mqtt.client as mqtt
import time


# callback functions -
# on_log - log info when connected and disconnect
def on_log(client, userdata, level, buf):
    print("log: ", buf)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected")
    else:
        print("Connecion failed. error code ", rc)


# on_connect - prints connection details
broker = "10.147.18.165"

client = mqtt.Client("changlab")
print("Connecting to broker", broker)
client.username_pw_set("changlab", "electrode")
client.on_connect = on_connect
client.on_log = on_log

client.connect(broker, 1883, 60)
client.loop_start()

time.sleep(4)
client.loop_stop()
client.disconnect()
