#include "Arduino_BMI270_BMM150.h"

float data[7];

// float label1 = 3596;
// float label2 = 2401;
// float label3 = 9892;
// float label4 = 6790;

float start;

bool acc_recv, gyro_recv;

void setup() {
  Serial.begin(921600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  delay(2000);
  start = (float)(millis()/1000.0);
}

void loop() {
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(data[2], data[1], data[3]);
    acc_recv = true;
  }

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(data[5], data[4], data[6]);
    gyro_recv = true;
  }

  if(acc_recv & gyro_recv){
    data[0] = (float)(millis()/1000.0) - start;
    Serial.write((unsigned char *)&data, sizeof(data));
    acc_recv = false;
    gyro_recv= false;
  }
}
