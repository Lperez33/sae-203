import paho.mqtt.client as mqtt
import json
import sqlite3
import os

#MQTT
MQTT_BROKER = "broker.hivemq.com"  #broker
MQTT_PORT = 1883 #port MQTT
MQTT_TOPIC = "foo/bxmeteo" #topic données publiés


DB_NAME = "mqtt.db"


def insert_data(data):
    """Insère les données JSON dans la base"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO weather (api_time, query_time, temperature, windspeed, winddirection)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("api_time"),
        data.get("query_time"),
        data.get("temperature"),
        data.get("windspeed"),
        data.get("winddirection")
    ))
    conn.commit() # Enregistre
    conn.close() # Ferme la co
    print("Données insérées dans la base ")

#callbacks 

def on_connect(client, userdata, flags, rc):
    print(f"Connecté au broker(code {rc})")
    client.subscribe(MQTT_TOPIC)
    print(f"Abonné au topic '{MQTT_TOPIC}'")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        print("Message :", data)
        insert_data(data)
    except Exception as e:
        print("Erreur", e)



if __name__ == "__main__":
   

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
