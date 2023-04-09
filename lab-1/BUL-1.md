# Function and characteristics of ultrasound-based TOF sensors for distance measurement

## Materials used
- [HC-SR04](https://www.electronicshub.org/hc-sr04-ultrasonic-sensor/) ultrasonic sensor
- [Arduino nano](https://store.arduino.cc/arduino-nano) microcontroller
- [Breadboard](https://www.arduino.cc/en/Tutorial/BuiltInExamples/Breadboard) for prototyping
- [PlatformIO](https://platformio.org/) for code compilation and uploading

## Setup

We use the HC-SR04 ultrasonic sensor to measure the distance between the sensor and an object. The sensor has 4 pins: VCC, GND, Trig and Echo. The VCC and GND pins are used to power the sensor. The Trig pin is used to send a 10us pulse to the sensor to start the measurement. The Echo pin is used to receive the echo signal from the sensor. The echo signal is a pulse that is sent back from the sensor to the microcontroller. The length of the echo signal is proportional to the distance between the sensor and the object. The sensor has a maximum range of 4m.

The following diagram shows the connections between the sensor and the microcontroller.

![HC-SR04 connections](https://raw.githubusercontent.com/robotics-4-all/robotics-4-all.github.io/master/notebooks/images/HC-SR04_bb.png)

## Code

The following code is used to measure the distance between the sensor and an object. The code is written in C++ and uses the [Arduino](https://www.arduino.cc/) framework. The code is compiled and uploaded to the microcontroller using [PlatformIO](https://platformio.org/).

```cpp
#include <Arduino.h>

#define ECHO_PIN 2
#define TRIGGER_PIN 3
#define LED_PIN 13

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Init");
  pinMode(ECHO_PIN, INPUT);
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);
  long microsencondsFlightTime = pulseIn(ECHO_PIN, HIGH);
  Serial.println(microsencondsFlightTime);
  if (microsencondsFlightTime < 2900) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
```

## Results
### Part 1: The sensor

> What happens if the transmission parameters of Arduino and Computer do not match?

The following error is displayed in the serial monitor.

```bash
Error: Invalid sync byte
```
the error is caused by the baud rate mismatch between the Arduino and the computer. The baud rate of the Arduino is 115200 and the baud rate of the computer is 9600. The baud rate of the Arduino can be changed in the code by changing the value of the `Serial.begin()` function. If the values mismatch, the commputer will not be able to read the data from the serial monitor properly.

> What is the maximum Baud-rate?

The maximun baudrate depends on the microcontroller. The Arduino nano can reportedly support a baudrate of higher than 115200 if not using the cap from the arduino IDE. [Source](https://forum.arduino.cc/t/baud-rate-max-absolute/447715/2)

> How is the TOF measurement calculated?

The TOF measurement is calculated by measuring the time it takes for the ultrasonic signal to travel from the sensor to the object and back to the sensor. The time is measured in microseconds. The distance is calculated by multiplying the time by the speed of sound (343m/s) and dividing the result by 2. The result is in meters.

The full procedure involves the following steps:

1. Send a 10us pulse to the sensor to start the measurement.
2. Wait for the echo signal to be received.
3. Measure the time it takes for the echo signal to be received.
4. Calculate the distance by multiplying the time by the speed of sound and dividing the result by 2, in our case we reported back the raw time in microseconds for later processing in the notebook.

> What is the data-flow from the sensor to the Arduino to the Computer?

The data is first capture on the sensor and then sent to the Arduino thru the GPIO pins. The Arduino then sends the data to the computer using the UART to USB converter. We can use the serial monitor or pyserial to read the data from the serial port.

    ┌───────────────────┐  ┌─────────────┐  ┌───────────┐ ┌────┐
    │ Ultrasonic Sensor │  │Arduino Nano │  │UART TO USB│ │PC  │
    │                   │  │             │  │CH340      │ │    │
    │ Trigger Pin ◄─────┼──┘ Digital I/O │  │           │ │    │
    │ Echo Pin──────────┼──► Digital I/O │  │  USB──────┼─┼─►  │
    │                   │  │             │  │           │ │    │
    │                   │  │             │  │           │ │    │
    │                   │  │TX/RX────────┼──┼─►         │ └────┘
    │                   │  │             │  └───────────┘
    └───────────────────┘  └─────────────┘


## Part 2: The interface

In this part the sensor was connected to the oscilloscope with two probes while it was working. One probe to the trigger pin and the other one to the echo pin. The results were recorded and can be seen in the following screenshots.

![Trigger pin](https://raw.githubusercontent.com/robotics-4-all/robotics-4-all.github.io/master/notebooks/images/trigger.png)