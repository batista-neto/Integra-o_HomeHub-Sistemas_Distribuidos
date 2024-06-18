import time
import csv
import os
from paho.mqtt import client as mqtt_client

broker = 'mqtt.eclipseprojects.io'
port = 1883
topic_publish1 = "Batista_SensorTemperaturaCozinha"
topic_publish2 = "Batista_SensorTemperaturaQuarto"
topic_publish3 = "Batista_SensorTemperaturaSala"
client_id = 'BROKER_PC_SUB'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao Broker MQTT")
        else:
            print("Falha ao conectar, código de retorno", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client):
    def on_message(client, userdata, msg):
        received_data = msg.payload.decode()
        if msg.topic == topic_publish1:
            print(f"Recebido o dado `{received_data}` do tópico `{msg.topic}`")
        elif msg.topic == topic_publish2:
            print(f"Recebido o dado `{received_data}` do tópico `{msg.topic}`")
        elif msg.topic == topic_publish3:
            print(f"Recebido o dado `{received_data}` do tópico `{msg.topic}`")

    client.subscribe(topic_publish1)
    client.subscribe(topic_publish2)
    client.subscribe(topic_publish3)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
