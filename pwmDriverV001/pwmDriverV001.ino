#include <Servo.h>

Servo waterPumpServo;

#define speedControlMin 1000
#define speedControlMid 1500
#define speedControlMax 2000


#define pumpPin 5    // Output
#define minusPin1 7  // Output
#define inPin0 8     // Input
#define minusPin2 9  // Output
#define pwmLedPin0 10     // Input
#define minusPin3 11  // Output

long pumpPWM = speedControlMid;

void setup() {
  // initialize both serial ports:

  //Serial.begin(115200);

  // Setup the PWM for the pump speed controller
  waterPumpServo.attach(pumpPin);
  waterPumpServo.writeMicroseconds(speedControlMid);
  
  pinMode(minusPin1, OUTPUT);
  pinMode(minusPin2, OUTPUT);
  pinMode(minusPin3, OUTPUT);
  pinMode(pwmLedPin0, OUTPUT);
  
  digitalWrite(minusPin1, LOW);
  digitalWrite(minusPin2, LOW);
  digitalWrite(minusPin3, LOW);
  digitalWrite(pwmLedPin0, LOW);
  
  pinMode(inPin0, INPUT_PULLUP);
}

void loop() {  
  if (digitalRead(inPin0) == false) {
    pumpPWM = speedControlMax;
    digitalWrite(pwmLedPin0, HIGH);
    //Serial.println("HIGH");
  }
  else {
    pumpPWM = speedControlMid;
    digitalWrite(pwmLedPin0, LOW);
    //Serial.println("LOW");
  }

  waterPumpServo.writeMicroseconds(pumpPWM);
}
