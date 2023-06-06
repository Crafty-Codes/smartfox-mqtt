import xml.etree.ElementTree as ET
import requests
from paho.mqtt import client as mqtt_client
import time
import random

smartfox = "http://192.168.178.100/values.xml"
keys = ["toGridValue", "hidProduction"]

broker = 'mqtt-broker'
port = 1883
client_id = f'publish-smartfox-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)

    client.on_connect = on_connect

    client.connect(broker, port)
    return client


def publish(client):
    while True:
        time.sleep(5)

        try:
            response = requests.get(smartfox)
            xml = ET.fromstring(response.text)

            for value in xml:
                valueId = value.attrib["id"]

                if valueId in keys:
                    topic = f'smartfox/{valueId}'

                    result = client.publish(topic, float(value.text.split()[0]))
                    status = result[0]

                    if status == 0:
                        print(f"Send `{value.text}` to topic `{topic}`")
                    else:
                        print(f"Failed to send message to topic {topic}")

        except Exception as e:
            print(e)


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
