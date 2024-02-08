#include "Arduino_BMI270_BMM150.h"
#include <ArduinoBLE.h>

BLEService bleService("917649A0-D98E-11E5-9EEC-0002A5D5C51B"); // Custom UUID

BLECharacteristic imuAccCharacteristic("917649A1-D98E-11E5-9EEC-0002A5D5C51B", BLERead | BLENotify, 12 );
BLECharacteristic imuGyroCharacteristic("917649A2-D98E-11E5-9EEC-0002A5D5C51B", BLERead | BLENotify, 12 );

union 
 {
  float a[3];
  // unsigned char bytes[12];      
 } accData;

union 
 {
  float g[3];
  // unsigned char bytes[12];         
 } gyroData;
 

void setup() {

  // initialze serial port for debugging communications
  Serial.begin(9600); // initialize Serial communication
  while (!Serial);    // wait for the serial port to open
  Serial.println("Started");
  
  // initialize IMU
  // Serial.println("Initializing IMU device...");
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
 
  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");

  Serial.print("Gyro sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");

  pinMode(LED_BUILTIN, OUTPUT); // Initialize the built-in LED pin

  if (!BLE.begin()) { // Initialize BLE
      Serial.println("starting BLE failed!");
      while (1);
  }

  BLE.setLocalName("A_Nano_33BLE_IMU");    // Set name for connection
  BLE.setAdvertisedService(bleService); // Advertise ble service

  bleService.addCharacteristic(imuAccCharacteristic);     // Add Acc characteristic
  bleService.addCharacteristic(imuGyroCharacteristic);     // Add Gyro characteristic

  BLE.addService(bleService); // Add environment service

  const unsigned char initializerAcc[12] = { 0,0,0,0,0,0,0,0,0,0,0,0 };
  const unsigned char initializerGyro[12] = { 0,0,0,0,0,0,0,0,0,0,0,0 };
 
  imuAccCharacteristic.setValue( initializerAcc, 12);
  imuGyroCharacteristic.setValue( initializerGyro, 12 );

  BLE.advertise(); // Start advertising
  Serial.print("Peripheral device MAC: ");
  Serial.println(BLE.address());
  Serial.println("Waiting for connections…");  
}

void loop() {
  BLEDevice central = BLE.central(); // Wait for a BLE central to connect

  if (central) {
    
    Serial.print("Connected to central MAC: ");
    Serial.println(central.address()); // Central's BT address:

    digitalWrite(LED_BUILTIN, HIGH); // Turn on the LED to indicate the connection

    while (central.connected()) {
      
    
      if (IMU.accelerationAvailable()) IMU.readAcceleration(accData.a[0], accData.a[1], accData.a[2]);
      if (IMU.gyroscopeAvailable()) IMU.readGyroscope(gyroData.g[0], gyroData.g[1], gyroData.g[2]);

      // Serial.print( "(ax,ay,az): " ); 
      // Serial.print("("); Serial.print(accData.a[0]); Serial.print(","); Serial.print(accData.a[1]); Serial.print(","); Serial.print(accData.a[2]); Serial.print(")");Serial.println();
      // Serial.print( "(gx,gy,gz): " ); 
      // Serial.print("("); Serial.print(gyroData.g[0]); Serial.print(","); Serial.print(gyroData.g[1]); Serial.print(","); Serial.print(gyroData.g[2]); Serial.print(")");Serial.println();

      // Pointer to the union can be used to pass the floats as a bytearray
      unsigned char *acc = (unsigned char *)&accData;
      unsigned char *gyro = (unsigned char *)&gyroData;

     imuAccCharacteristic.setValue( acc, 12 );
     imuGyroCharacteristic.setValue( gyro, 12 );      
      
    } // while central.connected  
    digitalWrite(LED_BUILTIN, LOW); // When the central disconnects, turn off the LED
    Serial.print("Disconnected from central MAC: ");
    Serial.println(central.address());
  } // if central
} // end loop(){}
