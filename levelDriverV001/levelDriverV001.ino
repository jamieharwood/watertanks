#include "FastLED.h"

#define auxInPin0 3     // Input
#define auxInPin1 4     // Input
//#define auxInPin2 5     // Input

#define inPin0 12    // Input
#define inPin1 11    // Input
#define inPin2 10    // Input
#define inPin3 9     // Input

#define inPin4 8     // Input
#define inPin5 7     // Input
#define inPin6 6     // Input
#define inPin7 5     // Input

int input[8];
int led = 0;

// Neo pixels
#define NUM_LEDS 8
#define DATA_PIN 3

// Define the array of leds
CRGB leds[NUM_LEDS];


void setup() {
  // initialize serial port
  //Serial.begin(115200);
  
  pinMode(auxInPin0, INPUT_PULLUP);
  pinMode(auxInPin1, INPUT_PULLUP);
  //pinMode(auxInPin2, INPUT_PULLUP);
  
  pinMode(inPin0, INPUT_PULLUP);
  pinMode(inPin1, INPUT_PULLUP);
  pinMode(inPin2, INPUT_PULLUP);
  pinMode(inPin3, INPUT_PULLUP);
  
  pinMode(inPin4, INPUT_PULLUP);
  pinMode(inPin5, INPUT_PULLUP);
  pinMode(inPin6, INPUT_PULLUP);
  pinMode(inPin7, INPUT_PULLUP);
  
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  //leds[0] = CRGB::Green;
  FastLED.show();
}

void loop() {  
  input[0] = digitalRead(inPin0);
  input[1] = digitalRead(inPin1);
  input[2] = digitalRead(inPin2);
  input[3] = digitalRead(inPin3);
  
  input[4] = digitalRead(inPin4);
  input[5] = digitalRead(inPin5);
  input[6] = digitalRead(inPin6);
  input[7] = digitalRead(inPin7);
  
  for (led = 0; led <
  NUM_LEDS; led++) {
    if ( input[led] == HIGH) {
      // Turn the LED on, then pause
      leds[led] = CRGB::Green;
    }
    else {
      //Serial.println("HIGH");
      leds[led] = CRGB::Black;
    }
  }  
  
  FastLED.show();
  
  //Serial.println("LOW");
}
