#include <Arduino.h>
#define ECHO_PIN 2
#define TRIGGER_PIN 3
#define LED_PIN 13

void setup()
{

  Serial.begin(115200);
  Serial.println("Init");
  pinMode(ECHO_PIN, INPUT);
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}
void loop()
{

  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);
  long microsencondsFlightTime = pulseIn(ECHO_PIN, HIGH);

  // programming threshold for distances lower and higher than 2m=> 5800us=∆t
  Serial.println(microsencondsFlightTime);
  if (microsencondsFlightTime < 5800)
  {
    digitalWrite(LED_PIN, HIGH);
  }
  else
  {
    digitalWrite(LED_PIN, LOW);
  }
}

void distanceInCentimeters(long microseconds)
{
  double speedOfSound = 343.0;
  double distance = (microseconds * speedOfSound) / 2.0;
  return distance / 100.0;
}
