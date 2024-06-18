import time
import random
import paho.mqtt.client as mqtt

mqtt_broker = "mqtt.eclipseprojects.io"
mqtt_port = 1883
mqtt_topic = "Batista_SensorTemperaturaSala"

def gerar_dados():
    return random.uniform(20, 35)

def on_connect(client, userdata, flags, rc):
    print("Conectado com o código de resultado: " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect


client.connect(mqtt_broker, mqtt_port, 60)


while True:
    dados = gerar_dados()
    
  
    client.publish(mqtt_topic, str(dados))
    
    print("Dados publicados: " + str(dados))
    
    time.sleep(2)
