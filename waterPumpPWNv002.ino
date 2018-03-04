#include <ArduinoJson.h>
#include <Servo.h>

Servo waterPumpServo;

#define speedControlMin 1000
#define speedControlMid 1500
#define speedControlMax 2000

// Output
#define hosePinButton 2
#define irrigationPinButton 3

#define hosePin 5
#define irrigationPin 6

#define pumpPin 4

#define tank0Level0 22
#define tank0Level1 23
#define tank0Level2 24
#define tank0Level3 25
#define tank0Level4 26

#define tank1Level0 27
#define tank1Level1 28
#define tank1Level2 29
#define tank1Level3 30
#define tank1Level4 31

#define tankLevelSensors 10

long tankLevelBuffer[tankLevelSensors];

long pumpPWM = speedControlMid;
long hoseButtonPressed = 0;
long irrigationButtonPressed = 0;
long hose = 0;
long irrigation = 0;

int loopCount = 0;
String lastSendBuffer = "";
boolean valuesUpdated = false;

void setup() {
  // initialize both serial ports:
  Serial.begin(115200);
  Serial1.begin(115200);

  // Setup the PWM for the pump speed controller
  waterPumpServo.attach(pumpPin);
  waterPumpServo.writeMicroseconds(speedControlMid);

  pinMode(hosePinButton, INPUT_PULLUP);
  pinMode(irrigationPinButton, INPUT_PULLUP);

  pinMode(hosePin, OUTPUT);
  pinMode(irrigationPin, OUTPUT);

  pinMode(tank0Level0, INPUT_PULLUP);
  pinMode(tank0Level1, INPUT_PULLUP);
  pinMode(tank0Level2, INPUT_PULLUP);
  pinMode(tank0Level3, INPUT_PULLUP);
  pinMode(tank0Level4, INPUT_PULLUP);

  pinMode(tank1Level0, INPUT_PULLUP);
  pinMode(tank1Level1, INPUT_PULLUP);
  pinMode(tank1Level2, INPUT_PULLUP);
  pinMode(tank1Level3, INPUT_PULLUP);
  pinMode(tank1Level4, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(hosePinButton) == true) {
    hoseButtonPressed = 0;
  }
  else {
    hoseButtonPressed = 1;
  }

  if (digitalRead(irrigationPinButton) == true) {
    irrigationButtonPressed = 0;
  }
  else {
    irrigationButtonPressed = 1;
  }

  tankLevelBuffer[0] = digitalRead(tank0Level0);
  tankLevelBuffer[1] = digitalRead(tank0Level1);
  tankLevelBuffer[2] = digitalRead(tank0Level2);
  tankLevelBuffer[3] = digitalRead(tank0Level3);
  tankLevelBuffer[4] = digitalRead(tank0Level4);

  tankLevelBuffer[5] = digitalRead(tank1Level0);
  tankLevelBuffer[6] = digitalRead(tank1Level1);
  tankLevelBuffer[7] = digitalRead(tank1Level2);
  tankLevelBuffer[8] = digitalRead(tank1Level3);
  tankLevelBuffer[9] = digitalRead(tank1Level4);
  
  DynamicJsonBuffer jsonBuffer;

  JsonObject& root = jsonBuffer.createObject();

  root["hoseButton"] = String(hoseButtonPressed);
  root["irrigationButton"] = String(irrigationButtonPressed);

  root["tank0Level0"] = String(tankLevelBuffer[0]);
  root["tank0Level1"] = String(tankLevelBuffer[1]);
  root["tank0Level2"] = String(tankLevelBuffer[2]);
  root["tank0Level3"] = String(tankLevelBuffer[3]);
  root["tank0Level4"] = String(tankLevelBuffer[4]);

  root["tank1Level0"] = String(tankLevelBuffer[5]);
  root["tank1Level1"] = String(tankLevelBuffer[6]);
  root["tank1Level2"] = String(tankLevelBuffer[7]);
  root["tank1Level3"] = String(tankLevelBuffer[8]);
  root["tank1Level4"] = String(tankLevelBuffer[9]);

  String newSendFuffer;
  root.printTo(newSendFuffer);

  //Serial.println("l: " + lastSendBuffer);
  //Serial.println("n: " + newSendFuffer);
    
  if (lastSendBuffer.equals(newSendFuffer) == false or loopCount > 60) {
    root.printTo(Serial1);
    Serial1.println();
    
    lastSendBuffer = newSendFuffer;
    loopCount = 0;
  }
  
  if (valuesUpdated == true) {
    waterPumpServo.writeMicroseconds(pumpPWM);

    if (hose == 0) {
      digitalWrite(hosePin, true);
    }
    else {
      digitalWrite(hosePin, false);
    }

    if (irrigation == 0) {
      digitalWrite(irrigationPin, true);
    }
    else {
      digitalWrite(irrigationPin, false);
    }

    valuesUpdated == false;
  }

  loopCount++;
  delay(1000);
}

void serialEvent1() {
  DynamicJsonBuffer jsonBuffer;
  int bufferSize  = 250;

  // read from port 1, send to port 0:
  if (Serial1.available()) {
    //int inByte = Serial1.read();
    char inByte[bufferSize];

    Serial1.readBytesUntil(char(0), inByte, bufferSize);

    String newBuffer = String(inByte);

    JsonObject& root = jsonBuffer.parseObject(newBuffer);

    pumpPWM = root["pumpPWM"];
    hose = root["hose"];
    irrigation = root["irrigation"];

    //Serial.println("pumpPWM: " + String(pumpPWM));// & root["pumpPWM"));
    //Serial.println("Hose: " + String(hose));
    //Serial.println("Irrigation: " + String(irrigation));

    //Serial.println(newBuffer);

    valuesUpdated = true;
  }
}
