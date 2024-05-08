#include <DHT.h>

#define DHTPIN 2          // DHT22 sensor's data line is connected to pin D2
#define WET_PIN 16        // Wet Indicator at Digital pin D0
#define DRY_PIN 2         // Dry Indicator at Digital pin D4
#define SENSE_PIN A0      // Sensor input at Analog pin A0
#define WATER_PUMP_PIN 5  // Water Pump pin D5

DHT dht(DHTPIN, DHT22);

void setup() {
  pinMode(WATER_PUMP_PIN, OUTPUT);
  digitalWrite(WATER_PUMP_PIN, HIGH);  // Ensure pump is initially off

  Serial.begin(9600);
  dht.begin();

  pinMode(WET_PIN, OUTPUT);
  pinMode(DRY_PIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the serial input
    String input = Serial.readStringUntil('\n');

    // Convert the received string to an integer
    int duration = input.toInt();

    // Check if duration is valid and greater than 0
    if (duration == 0) {
      Serial.print("Received pump duration command: ");
      Serial.println(duration);

      digitalWrite(WATER_PUMP_PIN, LOW);  // Turn on water pump
      delay(2 * 1000);              // Run pump for specified duration in seconds
      //digitalWrite(WATER_PUMP_PIN, HIGH); // Turn off water pump

      Serial.println("Water pump turned off");
    }
    else if(duration == 10) {
      digitalWrite(WATER_PUMP_PIN, HIGH);
      delay(2* 1000);
      Serial.println("Water pump turned on");
    } else {
      Serial.println("Invalid or zero duration received");
    }
  }

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  int value = analogRead(SENSE_PIN);
  int moisture = map(value, 0, 1023, 0, 100);

  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.println(" %");
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.println(" *C");
  Serial.print("Moisture: ");
  Serial.println(moisture);

  delay(5000);  // Delay 1 second before taking next sensor readings
}