import random
from paho.mqtt import client as mqtt_client

broker = 'broker.hivemq.com'
port = 1883
topic = "/foo"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
    else:
        print(f"❌ Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"📤 Message published with mid: {mid}")

# Création du client avec MQTT v5 (compatible v3.1.1 aussi)
client = mqtt_client.Client(client_id=client_id, protocol=mqtt_client.MQTTv5)

client.on_connect = on_connect
client.on_publish = on_publish

client.connect(broker, port)
client.loop_start()  # nécessaire pour les callbacks

msg = "A single message from my computer"
result = client.publish(topic, msg)

# Optionnel : attendre que la publication soit terminée
result.wait_for_publish()

if result.is_published():
    print(f"✔️ Sent `{msg}` to topic `{topic}`")
else:
    print(f"❌ Failed to send message to topic {topic}")

client.loop_stop()
client.disconnect()
