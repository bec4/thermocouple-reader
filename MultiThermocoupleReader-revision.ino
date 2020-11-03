/* To add thermocouples:
- Add pin definition
- Instantiate as an Adafruit_MAX31855 object
- Change thermocNum
- Add new theromcouples to thermocList
*/

// Required libraries
#include <SPI.h>
#include "Adafruit_MAX31855.h"

// Pin definitions (for shared pins)
#define CLK 12
#define DO  13

// Pin definitions (for thermocouple-specific pins)
#define CS1 4
#define CS2 5
#define CS3 6
#define CS4 9
#define CS5 10
#define CS6 11

// Initializing thermocouples
Adafruit_MAX31855 thermoc1(CLK, CS1, DO);
Adafruit_MAX31855 thermoc2(CLK, CS2, DO);
Adafruit_MAX31855 thermoc3(CLK, CS3, DO);
Adafruit_MAX31855 thermoc4(CLK, CS4, DO);
Adafruit_MAX31855 thermoc5(CLK, CS5, DO);
Adafruit_MAX31855 thermoc6(CLK, CS6, DO);

// User Options
const int loopDelay = 1000; // Loop delay in ms
const int thermocNum = 6; // Number of thermocouple slots hooked up
const String separator = "  |  "; // Column separator for serial readout. Set to one space to use plotter
const bool printNans = true; // Print nans on serial readout? Set to false to use plotter
const bool printIdx = true; // Print the index of the thermocouple before printing the value measured?

//
Adafruit_MAX31855 thermocList[] {thermoc1, thermoc2, thermoc3, thermoc4, thermoc5, thermoc6}; // Thermocouple list

//~/~/~/~/~/ new variables
String command;
float temperature;
int i;
int error;

void readAndPrint (int thermocIdx){
  float temp = thermocList[thermocIdx].readCelsius(); // Ask the thermocouple for temperature in Celsius
  
  if (!isnan(temp) || printNans) { // If the value is not a nan or we are outputting nans...
    if (printIdx) { // If we want to print the index of each thermocouple before their value
    Serial.print(thermocIdx + 1); // Print index
    Serial.print(": ");
    }
  
    Serial.print(temp); // Print this thermocouple's temperature
    Serial.print(separator);
    Serial.println(thermocList[thermocIdx].readError());
  
    Serial.print(separator); // Print the separator between different thermocouple columns
  }
  if (thermocIdx == thermocNum - 1) { // If we are on the last thermocouple
    Serial.println(); // Go to the next line
  }
}

void setup() {
  Serial.begin(9600); // Initialize serial connection
  while (!Serial) delay(1); // Wait for serial to start up (REQUIRED)
  
  ///////////
  //Serial.println("Starting...");
  delay(500); // Wait for MAX chips to stabilize
  //Serial.println("Ready");
  ///////////
}

void loop() {
  
  if (Serial.available() > 0) {
    
    command = Serial.readString();

    for (i = 0; i < thermocNum; i++) {
      temperature = thermocList[i].readCelsius();
      error = thermocList[i].readError();

      if (!isnan(temperature) && error == 0) {
        Serial.println(temperature);
      }
    }
    //Serial.println(thermocList)
  }

  ///////////
  //for (int thermocIdx = 0; thermocIdx < thermocNum; thermocIdx ++) { // Iterate through all of our thermocouples
  //  readAndPrint(thermocIdx); // Record and print current temperature for this thermocouple
  //}
  
  //delay(loopDelay); // Loop delay
  ///////////
}
