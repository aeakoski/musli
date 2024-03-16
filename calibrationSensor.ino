#include <Servo.h>

Servo sorterServo;

const int photoresistorPin = A0; // Photoresistor connected to analog pin A0
const int calibrationDuration = 3000; // Calibration duration in milliseconds (3 seconds)
const int discardDuration = 500; // Duration to discard initial readings in milliseconds (500 milliseconds)
const int servoPin = 9;

const int servoStandardAngle = 95;
const int servoSortAngle = 45;

int calibrationOffset = 0;

void calibrate(){
  unsigned long startTime = millis(); // Record start time for calibration
  int calibrationCount = 0;
  int calibrationValues[calibrationDuration / 5]; // Assuming 5 ms delay in the loop
  int index = 0;
  
  // Calibration phase
  while (millis() - startTime < calibrationDuration) {
    int sensorValue = analogRead(photoresistorPin);
    calibrationValues[index++] = sensorValue; // Store sensor values in array
    calibrationCount++;
    delay(5);
  }
  
  // Sort the calibration values
  for (int i = 0; i < calibrationCount - 1; i++) {
    for (int j = i + 1; j < calibrationCount; j++) {
      if (calibrationValues[i] > calibrationValues[j]) {
        // Swap values
        int temp = calibrationValues[i];
        calibrationValues[i] = calibrationValues[j];
        calibrationValues[j] = temp;
      }
    }
  }
  
  // Calculate calibration median
  if (calibrationCount % 2 == 0) {
    calibrationOffset = (calibrationValues[calibrationCount / 2 - 1] + calibrationValues[calibrationCount / 2]) / 2;
  } else {
    calibrationOffset = calibrationValues[calibrationCount / 2];
  }
}

void servoWiggle(){
  sorterServo.write(servoStandardAngle);
  delay(1000);
  sorterServo.write(servoSortAngle);
  delay(200);
  sorterServo.write(servoStandardAngle);
  delay(1000);
  sorterServo.write(servoSortAngle);
  delay(200);
  sorterServo.write(servoStandardAngle);
  delay(1000);
  sorterServo.write(servoSortAngle);
  delay(200);
  sorterServo.write(servoStandardAngle);
  
}

void servoSort(){
  sorterServo.write(servoSortAngle);
  delay(250);
  sorterServo.write(servoStandardAngle);
  delay(250);
}

void setup() {
  Serial.begin(9600);
  sorterServo.attach(servoPin);
  servoWiggle();
  delay(discardDuration); // Discard initial readings
  calibrate();
  servoSort();
}

void loop() {
    int sensorValue = analogRead(photoresistorPin);
    int calibratedValue = sensorValue - calibrationOffset; // Subtract calibration average
    if(calibratedValue < -4){
      servoSort();
      }
    Serial.println(calibratedValue);
    delay(2);
}