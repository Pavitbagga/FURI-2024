/*
Author: Jason Huang
Date: 27-May-23 
Rev: 01
 
Purpose: Utilize Arduino Nano 33 BLE Sense Rev 2 with it's integrated BLE and on-board sensors, to send acquired data to Raspberry Pi 3/4
 
*/
 
#include "Arduino_BMI270_BMM150.h"
#include <ArduinoBLE.h>
#include <Arduino_HS300x.h>
 
unsigned int previousHumidity = 0;
unsigned int previousTemperature = 0;
 
//int x, y, z;
float previousdegreesX = 0.0;
int degreesX = 0;
 
// Define the UUID for the service and characteristics
#define SERVICE_UUID        "12345678-1234-5678-1234-56789abcdef0"
#define CHARACTERISTIC_UUID "12345678-1234-5678-1234-56789abcdef1"
 
// Create a BLE service and characteristic
BLEService bleService(SERVICE_UUID);
 
BLEIntCharacteristic anglecharacteristic(CHARACTERISTIC_UUID, BLERead | BLENotify); // Standard 16-bit characteristic
BLEIntCharacteristic tempCharacteristic("2A6E", BLERead | BLENotify); // Standard 16-bit Temperature characteristic
BLEUnsignedIntCharacteristic humidCharacteristic("2A6F", BLERead | BLENotify); // Unsigned 16-bit Humidity characteristic
  
void setup() {
   
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");
 
 
  if (!HS300x.begin()) {
 
    Serial.println("Failed to initialize humidity temperature sensor!");
    while (1);
 
  }
   
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
 
  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
   
  pinMode(LED_BUILTIN, OUTPUT); // Initialize the built-in LED pin
   
  if (!BLE.begin()) { // Initialize BLE
      Serial.println("starting BLE failed!");
      while (1);
  }
  
  BLE.setLocalName("JH_ArduinoNano33BLESense_R2");    // Set name for connection
  BLE.setAdvertisedService(bleService); // Advertise ble service
   
  bleService.addCharacteristic(anglecharacteristic);     // Add string characteristic
  bleService.addCharacteristic(tempCharacteristic);     // Add temperature characteristic
  bleService.addCharacteristic(humidCharacteristic);    // Add humidity characteristic
 
  BLE.addService(bleService); // Add environment service
   
  anglecharacteristic.setValue(0);   // Set initial string value
  tempCharacteristic.setValue(0);     // Set initial temperature value
  humidCharacteristic.setValue(0);    // Set initial humidity value
     
  BLE.advertise(); // Start advertising
  Serial.print("Peripheral device MAC: ");
  Serial.println(BLE.address());
  Serial.println("Waiting for connections…");
}
 
void loop() {
   
  BLEDevice central = BLE.central(); // Wait for a BLE central to connect
 
 
  // If central is connected to peripheral
  if (central) {
      Serial.print("Connected to central MAC: ");
      Serial.println(central.address()); // Central's BT address:
 
      digitalWrite(LED_BUILTIN, HIGH); // Turn on the LED to indicate the connection
 
      while (central.connected()) {
        updateReadings();
        delay(100);
      }
 
      digitalWrite(LED_BUILTIN, LOW); // When the central disconnects, turn off the LED
      Serial.print("Disconnected from central MAC: ");
      Serial.println(central.address());
  }
   
 
}
 
 
unsigned int getHumidity() {
    // Get humidity as unsigned 16-bit int for BLE characteristic
    return (unsigned int) (HS300x.readHumidity()*100);
}
 
unsigned int getTemperature() {
    // Get humidity as unsigned 16-bit int for BLE characteristic
    return (unsigned int) (HS300x.readTemperature()*100);
}
 
 
void updateReadings() {
 
    float x, y, z;
    unsigned int humidity = getHumidity();
    unsigned int temperature = getTemperature();
     
    if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
 
      x = 100*x;
      degreesX = map(x, 0, 97, 0, 90);
 
    }
   
    if (degreesX != previousdegreesX) { // If reading has changed
        Serial.print("Angle X: ");
        Serial.println(degreesX);
        anglecharacteristic.writeValue(degreesX); // Update characteristic
        previousdegreesX = degreesX;          // Save value
    }
 
    if (temperature != previousTemperature) { // If reading has changed
        Serial.print("Temperature: ");
        Serial.println(temperature);
        tempCharacteristic.writeValue(temperature); // Update characteristic
        previousTemperature = temperature;          // Save value
    }
 
    if (humidity != previousHumidity) { // If reading has changed
        Serial.print("Humidity: ");
        Serial.println(humidity);
        humidCharacteristic.writeValue(humidity);
        previousHumidity = humidity;
    }
 
}