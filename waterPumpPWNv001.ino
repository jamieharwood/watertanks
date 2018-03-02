// Wire Slave Receiver
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Receives data as an I2C/TWI slave device
// Refer to the "Wire Master Writer" example for use with this

// Created 29 March 2006

// This example code is in the public domain.


#include <Wire.h>

#include <Servo.h>
Servo waterPumpServo;

#define speedControlMin 1000
#define speedControlMid 1500
#define speedControlMax 2000

// Output
#define pumpPin 4
#define hosePin 2
#define irrigationPin 3
 
void setup() {
  Wire.begin(20);                // join i2c bus with address #DEC 20 = HEX 14
  Wire.onReceive(receiveEvent); // register event
  //Serial.begin(9600);           // start serial for output
  
  // Setup the PWM for the pump speed controller
  waterPumpServo.attach(pumpPin);
  waterPumpServo.writeMicroseconds(speedControlMid);

  pinMode(hosePin, INPUT_PULLUP);
  pinMode(irrigationPin, INPUT_PULLUP);
}

void loop() {
  int hoseVal = !digitalRead(hosePin);
  int IrrigationVal = !digitalRead(irrigationPin);
  
  if (hoseVal == HIGH) {
    Wire.write(10);
    //Serial.println("hose on");
  } else {
    Wire.write(11);
    //Serial.println("hose off");
  }
  
  if (IrrigationVal) {
    Wire.write(12);
    //Serial.println("irrigation on");
  } else {
    Wire.write(13);
    //Serial.println("irrigation off");
  }
  delay(100);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  while (1 < Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    //Serial.print(c);         // print the character
  }
  int x = Wire.read();    // receive byte as an integer
  //Serial.println(x);         // print the integer
  
  if (x==1)
    waterPumpServo.writeMicroseconds(speedControlMid);
  else if (x==2)
    waterPumpServo.writeMicroseconds(speedControlMax);
}
