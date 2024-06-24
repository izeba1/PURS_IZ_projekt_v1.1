#include <Arduino.h>
#include <WiFi.h>
#include <WiFiServer.h>
#include <WiFiClient.h>

//SSID i PASS za WiFi
const char* SSID = "Zeba SCAN";
const char* PASSWORD = "zebascan";

WiFiServer server(80);
WiFiClient client;

#define LED_Z 23
#define LED_C 19
#define BUZ 18
#define FAN 16


//Spajanje na WiFi
void setup() {
  Serial.begin(9600);

  WiFi.begin(SSID, PASSWORD);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED){
    Serial.print('.');
    delay(500);
  }
  Serial.println(WiFi.localIP());

  //Definiranje pinMode
  pinMode(LED_C, OUTPUT);
  pinMode(LED_Z, OUTPUT);
  pinMode(FAN, OUTPUT);
  pinMode(BUZ, OUTPUT);
}



void loop() {
    server.begin();
    client = server.available();
  if (client) {
    Serial.println("connecter");
    String zahtjev = client.readStringUntil('\r');
    Serial.println(zahtjev);
    client.flush();

    if (zahtjev.indexOf("POST /ON") != -1) {
      digitalWrite(BUZ, HIGH);
      digitalWrite(FAN, HIGH);
      digitalWrite(LED_C, HIGH);
      digitalWrite(LED_Z, LOW);
      Serial.println("Ventilator ON");
    } else if (zahtjev.indexOf("POST /OFF") != -1) {
      digitalWrite(BUZ, LOW);
      digitalWrite(FAN, LOW);
      digitalWrite(LED_C, LOW);
      digitalWrite(LED_Z, HIGH);
      Serial.println("Ventilator OFF");
    }

    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println("Connection: close");
    client.println();
    client.stop();
  }

  if (digitalRead(FAN) == LOW) {
    digitalWrite(LED_Z, HIGH);
    delay(500);
    digitalWrite(LED_Z, LOW);
    delay(500);
  }
}