#include <ArduinoBLE.h>
#include <Arduino_LSM6DS3.h>


#define BLE_UUID_ACCELEROMETER_SERVICE "1101"
#define BLE_UUID_ACCELEROMETER_X "2101"
#define BLE_UUID_ACCELEROMETER_Y "2102"
#define BLE_UUID_ACCELEROMETER_Z "2103"


#define BLE_UUID_GYROSCOPE_SERVICE "2743"
#define BLE_UUID_GYROSCOPE_X "2744"
#define BLE_UUID_GYROSCOPE_Y "2745"
#define BLE_UUID_GYROSCOPE_Z "2746"


#define BLE_DEVICE_NAME "Nate's Nano 33 IoT"
#define BLE_LOCAL_NAME "Nate's Nano 33 IoT"


BLEService accelerometerService(BLE_UUID_ACCELEROMETER_SERVICE);
BLEService gyroscopeService(BLE_UUID_GYROSCOPE_SERVICE);


BLEFloatCharacteristic accelerometerCharacteristicX(BLE_UUID_ACCELEROMETER_X, BLERead | BLENotify);
BLEFloatCharacteristic accelerometerCharacteristicY(BLE_UUID_ACCELEROMETER_Y, BLERead | BLENotify);
BLEFloatCharacteristic accelerometerCharacteristicZ(BLE_UUID_ACCELEROMETER_Z, BLERead | BLENotify);


BLEFloatCharacteristic gyroscopeCharacteristicX(BLE_UUID_GYROSCOPE_X, BLERead | BLENotify);
BLEFloatCharacteristic gyroscopeCharacteristicY(BLE_UUID_GYROSCOPE_Y, BLERead | BLENotify);
BLEFloatCharacteristic gyroscopeCharacteristicZ(BLE_UUID_GYROSCOPE_Z, BLERead | BLENotify);


float ax, ay, az;
float gx, gy, gz;


void setup() {
  Serial.begin(9600);
  // while (!Serial)
    ;


  // initialize IMU
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1)
      ;
  }


  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println("Hz");


  // initialize BLE
  if (!BLE.begin()) {
    Serial.println("Starting Bluetooth® Low Energy module failed!");
    while (1)
      ;
  }


  // set advertised local name and service UUID
  //
  BLE.setDeviceName(BLE_DEVICE_NAME);
  BLE.setLocalName(BLE_DEVICE_NAME);
  BLE.setAdvertisedService(gyroscopeService);
  BLE.setAdvertisedService(accelerometerService);


  // add characteristics and service
  //
  accelerometerService.addCharacteristic(accelerometerCharacteristicX);
  accelerometerService.addCharacteristic(accelerometerCharacteristicY);
  accelerometerService.addCharacteristic(accelerometerCharacteristicZ);
 
  gyroscopeService.addCharacteristic(gyroscopeCharacteristicX);
  gyroscopeService.addCharacteristic(gyroscopeCharacteristicY);
  gyroscopeService.addCharacteristic(gyroscopeCharacteristicZ);
 
  accelerometerCharacteristicX.writeValue(0);
  accelerometerCharacteristicY.writeValue(0);
  accelerometerCharacteristicZ.writeValue(0);


  gyroscopeCharacteristicX.writeValue(0);
  gyroscopeCharacteristicY.writeValue(0);
  gyroscopeCharacteristicZ.writeValue(0);


  BLE.addService(accelerometerService);
  BLE.addService(gyroscopeService);


  // start advertising
  //
  BLE.advertise();


  Serial.println("BLE Accelerometer Peripheral");
}


void loop() {
  BLE.poll();
  BLEDevice central = BLE.central();


  // obtain and write accelerometer data
  //


  // if a central is connected to peripheral:
  if (central) {
    Serial.print("Connected to central: ");
    // print the central's MAC address:
    Serial.println(central.address());


    // while the central is still connected to peripheral:
    while (central.connected()) {
      if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
        IMU.readAcceleration(ax, ay, az);
        IMU.readGyroscope(gx, gy, gz);
        Serial.println(ax);
        accelerometerCharacteristicX.writeValue(ax);
        accelerometerCharacteristicY.writeValue(ay);
        accelerometerCharacteristicZ.writeValue(az);


        gyroscopeCharacteristicX.writeValue(gx);
        gyroscopeCharacteristicY.writeValue(gy);
        gyroscopeCharacteristicZ.writeValue(gz);
      }
    }


    // when the central disconnects, print it out:
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
  }
}
