#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;
const int buttonPin = 0; // Boot button on GPIO0
int buttonState = 0;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_BT"); // Bluetooth device name
  pinMode(buttonPin, INPUT_PULLUP); // Initialize the button pin as an input with an internal pull-up resistor
}

void loop() {
  buttonState = digitalRead(buttonPin);
  if (buttonState == LOW) { // Check if the button is pressed
    SerialBT.println("Pressed");
    delay(500); // Simple debounce
  }
}
