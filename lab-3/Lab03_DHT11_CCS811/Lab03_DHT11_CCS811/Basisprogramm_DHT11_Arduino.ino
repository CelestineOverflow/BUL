#include "DHT.h"     // OneWire Bibliothek - Adafruit
#define DHTPIN 2     // OneWire Pin
#define LED 13       // LED


#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE, 6);

void setup() {
  Serial.begin(9600); 
  dht.begin();
  pinMode(LED, OUTPUT);
}  

void loop() {
  // Wait a second between measurements.
  delay(1000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit
  float f = dht.readTemperature(true);



  
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  Serial.print("Humidity: "); 
  Serial.print(h);
  Serial.print("\n");
  Serial.print("Temperature: "); 
  Serial.print(t);
  Serial.print("\n");
  if (t>22){
    digitalWrite(LED, HIGH);
  }
  else {
    digitalWrite(LED, LOW);
  }
}
