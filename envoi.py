import requests
import paho.mqtt.client as mqtt
from datetime import datetime
import json
import time
# --- CONFIG MQTT ---
MQTT_BROKER = "broker.hivemq.com"   # Exemple broker public (change si besoin)
MQTT_PORT = 1883
MQTT_TOPIC = "foo/bxmeteo"

# Coordonnées Bordeaux
latitude = 44.84
longitude = -0.58

def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    weather = data["current_weather"]
    return {
        "api_time": weather["time"],
        "temperature": weather["temperature"],
        "windspeed": weather["windspeed"],
        "winddirection": weather["winddirection"],
        "query_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def publish_mqtt(data):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    payload = json.dumps(data)
    client.publish(MQTT_TOPIC, payload)
    print(f"Publié sur MQTT topic '{MQTT_TOPIC}': {payload}")
    client.disconnect()

if __name__ == "__main__":
     while True:
        try:
            weather_data = get_weather()
            publish_mqtt(weather_data)
        except Exception as e:
            print(f"Erreur : {e}")
        print("En attente 10 minutes...\n")
        time.sleep(300)  # Attendre 10 minutes avant la prochaine requête