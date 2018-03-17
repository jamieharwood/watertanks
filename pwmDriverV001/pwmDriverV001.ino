#include "FastLED.h"
#include <Servo.h>

Servo waterPumpServo;

#define speedControlMin 1000
#define speedControlMid 1500
#define speedControlMax 2000


#define pumpPin 4    // Output
//#define minusPin1 7  // Output
#define inPin0 5     // Input
//#define minusPin2 9  // Output
//#define pwmLedPin0 10     // Input
//#define minusPin3 11  // Output

long pumpPWM = speedControlMid;

#define NUM_LEDS 4
#define DATA_PIN 3

// Define the array of leds
CRGB leds[NUM_LEDS];


void setup() {
  // initialize serial port
  //Serial.begin(115200);

  // Setup the PWM for the pump speed controller
  waterPumpServo.attach(pumpPin);
  waterPumpServo.writeMicroseconds(speedControlMid);
  
  //pinMode(minusPin1, OUTPUT);
  //pinMode(minusPin2, OUTPUT);
  //pinMode(minusPin3, OUTPUT);
  //pinMode(pwmLedPin0, OUTPUT);
  
  //digitalWrite(minusPin1, LOW);
  //digitalWrite(minusPin2, LOW);
  //digitalWrite(minusPin3, LOW);
  //digitalWrite(pwmLedPin0, LOW);
  
  pinMode(inPin0, INPUT_PULLUP);
  
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
}

void loop() {  
  if (digitalRead(inPin0) == false) {
    pumpPWM = speedControlMax;
    //digitalWrite(pwmLedPin0, HIGH);
    
    // Turn the LED on, then pause
    leds[0] = CRGB::Red;
    FastLED.show();
    
    //Serial.println("HIGH");
  }
  else {
    pumpPWM = speedControlMid;
    //digitalWrite(pwmLedPin0, LOW);
    
    // Now turn the LED off, then pause
    leds[0] = CRGB::Green;
    FastLED.show();
  
    //Serial.println("LOW");
  }

  waterPumpServo.writeMicroseconds(pumpPWM);
}
