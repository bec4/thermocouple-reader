I. Arduino Program Overview

ALGORITHM AND USE

MultiThermocoupleReader.ino will:
- Iterate through connected thermocouples
- For each one, read the temperature and serial print according to user options (which can be changed below)
- Repeat as loop

Note that the algorithm does not store any information about the temperatures it has read. As soon as it reads and prints a temperature, it erases that value.

CHANGING THE READOUT

MultiThermocoupleReader.ino is programmed to run an arbitrary number of MAX31855 chips, each connected to its own thermocouple, and read out the temperature from each thermocouple as serial
text. The readout can be changed:
- The separator between data points can be changed (variable: separator)
- The program can be set to ignore nan values OR print them out regardless (variable: printNans)
- The program can be set to print a thermocouple index (number) before each data point to easily identify which reading is which (variable: printIdx)

These settings can be leveraged to have the program to print out the information in .csv format:
separator = ",";
printIdx = false;

These settings also allow use of the Arduino serial plotter to visualize the data:
separator = " ";
printNans = false;
printIdx = false;

ADDING THERMOCOUPLES

To add thermocouples:
- Add pin definition for the CS pin of the new thermocouple
- Instantiate as an Adafruit_MAX31855 object using the correct pins
- Change thermocNum to match the new amount of thermocouples
- Add new theromcouples to thermocList


II. Hardware Overview

CONNECTIONS

Each chip should be connected to a thermocouple, and to the arduino.

Vcc and ground should be connected to a 3.3V source and ground of the microcontroller respectively.

The CLK and DO pins on every chip should have a shared connection to the same pin on the microcontroller. The default pins are: CLK -> 12, DO -> 13.
The CS pin of each chip should be connected to a different pin on the microcontroller. The default pins for six thermocouples are

DEBUGGING

- Getting nans as output: Check connections between the thermocouple and the board. Thermocouple tips that are shorted together will all produce nans (fix is ongoing).
- Getting 0C as output: Check connections between the thermocouple and the board
- Data table is not orderly/characters are missing: Check connection between arduino and computer
- Thermocouples reading incorrect values: Check thermocouple polarity. Make sure only thermocouple wires are used between the thermocouple tip and the chip, as different wire materials will
produce incorrect readings.
- Sudden spikes in temperature occur when connecting or disconnecting thermocouples. If they are recurring, make sure that thermocouple's connection is stable
