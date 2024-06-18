#include <WiFi.h>
#include <PubSubClient.h>
#include <math.h>

const char* ssid = "BATISTA 2,4GHZ";
const char* password = "JBCLIENTE";

const char* mqtt_server = "mqtt.eclipseprojects.io";
const int mqtt_port = 1883;
const char* mqtt_topic = "Batista_SensorTemperaturaQuarto";

WiFiClient espClient;
PubSubClient client(espClient);

#define Pot 34
float LeituraPot = 0; 
const float BETA = 3435.0; 

void setup() {
  Serial.begin(115200);
  pinMode(Pot, INPUT);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("Conectado ao WiFi!");

  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  LeituraPot = analogRead(Pot);
  float Temperatura = calcular_temperatura(LeituraPot); 

  char msg[20];
  snprintf(msg, 20, "%f", LeituraPot); 

  client.publish(mqtt_topic, msg);
  Serial.println(LeituraPot);
  Serial.println(Temperatura);

  delay(2000);
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("Conectando ao MQTT broker...");
    if (client.connect("ESP32Client")) {
      Serial.println("Conectado ao MQTT broker!");
    } else {
      Serial.print("Falha na conexão com MQTT, rc=");
      Serial.print(client.state());
      delay(5000);
    }
  }
}

float calcular_temperatura(float analog_value) { 
    float resistance_nominal = 10; 
    float beta = 3435.0; 
    float resistance = resistance_nominal / ((1023.0 / analog_value) - 1.0);
    float temperature_kelvin = 1.0 / ((log(resistance / resistance_nominal) / beta) + 1.0 / 298.15);
    float temperature_celsius = temperature_kelvin - 273.15;
    return temperature_celsius;
}


