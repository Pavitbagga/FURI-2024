#include "Arduino_BMI270_BMM150.h"

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Acceleration in G's");
  Serial.println("X\tY\tZ");

  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Gyroscope in degrees/second");
  Serial.println("X\tY\tZ");

  Serial.print("Magnetic field sample rate = ");
  Serial.print(IMU.magneticFieldSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Magnetic Field in uT");
  Serial.println("X\tY\tZ");

  delay(2000);
}

void loop() {
  float acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(acc_x, acc_y, acc_z);

    Serial.print("Acc:\t");
    Serial.print(acc_x);
    Serial.print('\t');
    Serial.print(acc_y);
    Serial.print('\t');
    Serial.print(acc_z);
    Serial.print('\t');
  }

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gyro_x, gyro_y, gyro_z);

    Serial.print("Gyro:\t");
    Serial.print(gyro_x);
    Serial.print('\t');
    Serial.print(gyro_y);
    Serial.print('\t');
    Serial.print(gyro_z);
    Serial.print('\t');
  }

  if (IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(mag_x, mag_y, mag_z);

    Serial.print("Mag:\t");
    Serial.print(mag_x);
    Serial.print('\t');
    Serial.print(mag_y);
    Serial.print('\t');
    Serial.println(mag_z);
  }
}
