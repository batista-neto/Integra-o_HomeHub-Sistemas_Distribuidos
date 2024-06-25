import time
import random
import paho.mqtt.client as mqtt
import requests
import json
from datetime import datetime
import pytz
import csv
import os

mqtt_broker = "mqtt.eclipseprojects.io"
mqtt_port = 1883
mqtt_topic = "Batista_SensorTemperaturaCozinha" 
client_id = 'Sensor_Simulador'  

api_endpoint = 'http://cidadesinteligentes.lsdi.ufma.br'  
resource_uuid = 'ccfd7f60-fea6-4ed7-ad5a-9ca2bf19f738'  
capability_name = "Medidor_TemperaturaCozinha"

data_list = []

def gerar_dados():
    return random.uniform(25, 40)

def send_data_to_interscity(sensor_data):
    timestamp = datetime.now(pytz.utc).isoformat()
    data_payload = {
        "data": [
            {
                "timestamp": timestamp,
                "value": sensor_data
            }
        ]
    }

    try:
        response = requests.post(api_endpoint + "/adaptor/resources/" + resource_uuid + "/data/environment_monitoring", json=data_payload)
        if response.status_code == 201:
            print(f"Dados de temperatura enviados para a API do InterSCity: {sensor_data}°C")
        else:
            print(f"Erro ao enviar dados para a API do InterSCity:", response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar dados para a API do InterSCity:", e)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao Broker MQTT")
        else:
            print("Falha ao conectar, código de retorno", rc)

    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.connect(mqtt_broker, mqtt_port)
    return client

def save_to_csv(data):
    file_exists = os.path.isfile('sensor_data.csv')
    with open('sensor_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['timestamp', 'sensor_data'])  # Escreve o cabeçalho se o arquivo não existe
        writer.writerows(data)

def run():
    client = connect_mqtt()

    try:
        while True:
            sensor_data = gerar_dados()
            timestamp = datetime.now(pytz.utc).isoformat()
            data_list.append([timestamp, sensor_data])

            send_data_to_interscity(sensor_data) 
            client.publish(mqtt_topic, str(sensor_data))  
            print(f"Dados publicados no MQTT: {sensor_data}°C")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nInterrupção detectada. Salvando dados no arquivo CSV...")
        save_to_csv(data_list)
        print("Dados salvos com sucesso. Saindo...")

if __name__ == '__main__':
    run()
