# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added

### Changed

### Deleted

## [0.5.4](https://github.com/isu-avista/sensors/releases/tag/v0.5.4) - 2021-02-17
### Added

### Changed
* Shifted SensorSweep from a thread to a process

### Deleted

## [0.5.3](https://github.com/isu-avista/sensors/releases/tag/v0.5.3) - 2021-02-17
### Added

### Changed
* Added some commands for debugging the data transporter

### Deleted

## [0.5.2](https://github.com/isu-avista/sensors/releases/tag/v0.5.2) - 2021-02-17
### Added

### Changed
* Added some commands for debugging the data transporter

### Deleted

## [0.5.1](https://github.com/isu-avista/sensors/releases/tag/v0.5.1) - 2021-02-16
### Added

### Changed
* Updated dependencies
* Added fake-rpi as a dependency to begin the process of improving the tests
* Modified the travis-ci spec to start the process of automated testing

### Deleted

## [0.5.0](https://github.com/isu-avista/sensors/releases/tag/v0.5.0) - 2021-02-13
### Added
* Added a class `DataTransporter` which collects data and sends it to a server

### Changed
* Changed the constructor for `SensorSweep` to take as parameters the periodicity
  and holding period values
* Change the name of `ManagerState` to be `SweepState` to be in alignment with the
  rest of the code.
* Integrated the `DataTransporter` with the main loop of the `SensorSweep`
* Updated documentation

### Deleted

## [0.4.0](https://github.com/isu-avista/sensors/releases/tag/v0.4.0) - 2021-02-02
### Added

### Changed
* Updated docstrings and documentation for all sensor implementations
* Sensors now return a dictionary where keys will fill the name field for a data point
  and the value of the pair will be the data value

### Deleted
* Removed all the previously added print statements

## [0.3.0](https://github.com/isu-avista/sensors/releases/tag/v0.3.0) - 2021-01-29
### Added
* Added an abstract setup method to sensor_processor for inheriting processors to 
  reference parameters after they've been added to their dictionaries

### Changed

### Deleted

## [0.2.1](https://github.com/isu-avista/sensors/releases/tag/v0.2.1) - 2021-01-29
### Added
* Added new sensor implementations to avista_sensors.impl.__init\__.py

### Changed

### Deleted

## [0.2.0](https://github.com/isu-avista/sensors/releases/tag/v0.2.0) - 2021-01-27
### Added
* DHTProcessor class to read from dht22 temperature sensor
* IRTempProcessor class to read from mlx90614 ir temperature sensor
* SoundProcessor class to read from electret 4466 microphone
* VibrationProcessor class to read from mpu6050 accelerometer
* IRBeamProcessor class to read from ir break beam

### Changed
* Replaced uses of sensor pinouts with parameters

### Deleted

## [0.1.6](https://github.com/isu-avista/sensors/releases/tag/v0.1.6) - 2021-01-10
### Added

### Changed
- Added a check to make sure sensor processors are not None in ProcessorManager._execute()

### Deleted

## [0.1.5](https://github.com/isu-avista/sensors/releases/tag/v0.1.5) - 2020-12-13
### Added

### Changed
- Modified tests to use current version of data
- Modified processor_manager to be more integrated with flask

### Deleted

## [0.1.4](https://github.com/isu-avista/sensors/releases/tag/v0.1.4) - 2020-12-05
### Added

### Changed
- Updated the sphinx documentation

### Deleted

## [0.1.3](https://github.com/isu-avista/sensors/releases/tag/v0.1.3) - 2020-12-05
### Added

### Changed
- Removed test for restart from processor manager tests
- correct several typos

### Deleted

## [0.1.2](https://github.com/isu-avista/sensors/releases/tag/v0.1.2) - 2020-12-05
### Added

### Changed
- Minor change to SimulatedProcessor field names

### Deleted

## [0.1.1](https://github.com/isu-avista/sensors/releases/tag/v0.1.1) - 2020-12-05
### Added
- Tests for all classes to reach 100% coverage (excluding SensorProcessor which is at 97%)
- Fully documented all classes

### Changed
- Improved implementation of both RandomProcessor and SimulatedProcessor so that they work correctly
- Added multithreading to the processor manager
- Updated the [README.md](README.md)

### Deleted

## [0.1.0](https://github.com/isu-avista/sensors/releases/tag/v0.1.0) - 2020-12-03

### Added
- All the base classes required
- This changelog
- Readme
- Basic project structure
- Initial Simulated Data Sensor Processor
- Added initial tests
- GitHub pages documentation
- Mostly tested to the 100% coverage level

### Changed
- Nothing

### Removed
- Nothing