#include <Arduino.h>

const int pwmPin = 2;  // GPIO pin for PWM output (replace with your desired pin)
const int freq = 5000; // PWM signal frequency in Hz
const int pwmChannel = 0; // LEDC channel, ESP32 has 16 channels (0-15)
const int resolution = 8; // Resolution in bits. 8 bits = 0-255 duty cycle range

void setup() {
  // Initialize PWM on the specified pin, frequency, and resolution
  ledcSetup(pwmChannel, freq, resolution);

  // Attach the pin to the PWM channel
  ledcAttachPin(pwmPin, pwmChannel);

  // Start with a 50% duty cycle
  ledcWrite(pwmChannel, 127); // 50% of 255 (Max value for 8-bit resolution)
}

void loop() {
  ledcWrite(pwmChannel, 255);
  delay(1000);
  ledcWrite(pwmChannel, 0);
  delay(1000);
}
