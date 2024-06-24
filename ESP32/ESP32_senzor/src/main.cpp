#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

//IP adresa servera
const char *serverName = "http://192.168.183.138:80/gas_sens";
HTTPClient http;

//SSID i PASS za WiFi
const char* SSID = "Zeba SCAN";
const char* PASSWORD = "zebascan";

#define LED_Z 23
#define LED_C 19
#define GAS 35


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
  pinMode(GAS, INPUT);
}

StaticJsonDocument<200> doc;
 
void loop() {
  int reading = analogRead(GAS);
  //Serial.println(reading);

  if (reading > 200) {
    digitalWrite(LED_C, HIGH);
    digitalWrite(LED_Z, LOW);
  } else {
    digitalWrite(LED_C, LOW);
    digitalWrite(LED_Z, HIGH);
  }

  //Kreiranje i slanje JSON poruke putem POST zahtjeva 
  doc["gas"] = String(reading);
  String json;
  serializeJson(doc, json);

  //Print json poruke na serial monitor
  Serial.println(json);

  //Spajanje sa serverom
  http.begin(serverName);

  //Dodavanje
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(json);

  Serial.print("Status code: ");
  Serial.println(httpResponseCode);
  Serial.println(http.getString());

  http.end();

  delay(1000);
}