# Avista-Sensors

## Description

This is the sensors package upon which all iot sensor code will rely. To better understand
the design and concepts surrounding this project please see the main 
[architecture wiki](https://github.com/isu-avista/architecture/wiki) and this
[project's wiki](https://github.com/isu-avista/sensors/wiki).

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Credits](#credits)
4. [License](#license)

## Installation

To install this module us the following command:

```
pip3 install git+ssh://git@github.com/isu-avista/sensors.git
```

## Usage

This project provides a framework for integrating IoT sensors into the overall ISU-Avista
project. Furthermore, it provides the capability to dynamically load these sensors at runtime
and via the database a means to persist which sensors were loaded in the first place. Each
sensor is actually a SensorProcessor instance which pulls information from GPIO pins and converts
this to a DataPoint instance at a provided timestamp.

In order to make use of this framework, one must understand the 
[Template Method Design Pattern](https://refactoring.guru/design-patterns/template-method). 
This pattern is the basis of the SensorProcessor class. When adding new sensors to the device
(which have not already had a processor created) we need only implement a processor for that
sensor. To implement such a processor, an individual need only execute the following steps:
 
1. Add a new class to the `avista_sensors.impl` package (i.e. "new_sensor.py" with class `NewSensor`)
2. This `NewSensor` class will need to extend `SensorProcessor` from `avista_sensors.sensor_processor` module
3. Implement the method `_read_sensor(self, ts)` which contains the logic to convert pin readings to
   a specific data point and returns this converted value.
   
Examples (minus the reading of pins) can be found in the `SimulatedProcess` and `RandomProcessor` classes
in the `avista_sensors.impl` package.

You can also see the complete documentation of the code on the [documentation page](https://isu-avista.github.io/sensors/)

## Credits

This module was contributed to by:

- Isaac D. Griffith

## License

Copyright (c) 2020 Idaho State University Empirical Software Engineering Laboratory

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.