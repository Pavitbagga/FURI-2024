#include "Arduino_BMI270_BMM150.h"
#include "SensorFusion.h"

SF fusion;

float ax, ay, az, gx, gy, gz, mx, my, mz;
float pitch, roll, yaw;
float deltat;

#define DEG_TO_RAD 0.017453292519943295769236907684886

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
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az);
  }

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gx, gy, gz);
  }

  if (IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(mx, my, mz);
  }

  deltat = fusion.deltatUpdate();

  fusion.MadgwickUpdate(gx*DEG_TO_RAD, gy*DEG_TO_RAD, gz*DEG_TO_RAD, ax, ay, az, mx, my, mz, deltat); 

  pitch = fusion.getPitch();
  roll = fusion.getRoll();    
  yaw = fusion.getYaw();

  Serial.print("Pitch:\t"); Serial.println(pitch);
  Serial.print("Roll:\t"); Serial.println(roll);
  Serial.print("Yaw:\t"); Serial.println(yaw);
  Serial.println();
}
