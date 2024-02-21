#include "BluetoothSerial.h"

const int buttonPin = 0; // Boot button on GPIO0
int buttonState = 0;

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP); // Initialize the button pin as an input with an internal pull-up resistor
}

void loop() {
  buttonState = digitalRead(buttonPin);
  if (buttonState == LOW) { // Check if the button is pressed
    Serial.println("Pressed");
    delay(500); // Simple debounce
  }
}
