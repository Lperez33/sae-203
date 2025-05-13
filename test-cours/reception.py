import random
from paho.mqtt import client as mqtt_client

broker = 'broker.hivemq.com'
port = 1883
topic = "/foo"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code %d\n" % rc)

def on_message(client, userdata, msg):
    s = msg.payload.decode("utf-8")
    print(f"Received `{s}` from `{msg.topic}` topic")

client = mqtt_client.Client(client_id=client_id, protocol=mqtt_client.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.loop_forever()
