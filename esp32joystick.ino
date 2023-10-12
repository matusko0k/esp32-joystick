const int joystickXPin = 34;
const int joystickYPin = 35;

void setup() {
  Serial.begin(115200);

  pinMode(joystickXPin, INPUT);
  pinMode(joystickYPin, INPUT);

  delay(100);
  Serial.println("ESP32-Joystick is ready to send data.");
}

void loop() {
  int xValue = analogRead(joystickXPin);
  int yValue = analogRead(joystickYPin);


  Serial.print("S");
  Serial.print(xValue);
  Serial.print(",");
  Serial.print(yValue);
  Serial.print("E");

  delay(110);
  
}
