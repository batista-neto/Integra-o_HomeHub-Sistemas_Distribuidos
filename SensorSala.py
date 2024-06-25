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

def variacoes_temperatura(media, desvio_padrao, num_minutos):
    temperatura_atual = media
    temperaturas = []

    for _ in range(num_minutos):
        variacao = random.normalvariate(0, desvio_padrao)
        temperatura_atual += variacao
        temperaturas.append(round(temperatura_atual, 1))

    return temperaturas

media_temperatura = 29
desvio_padrao = 0.2      
num_minutos = 60         

temperaturas = variacoes_temperatura(media_temperatura, desvio_padrao, num_minutos)


while True:
    dados = temperaturas
  
    client.publish(mqtt_topic, str(dados))
    
    print("Dados publicados: " + str(dados))
    
    time.sleep(2)
