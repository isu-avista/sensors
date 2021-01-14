# rpm_proecessor.py

from avista_sensors.sensor_processor import SensorProcessor

# When we create I2CSensorProcess or SPISensorProcessor
# Then the import statement would be either
# from avista_sensors.i2csensor_processor import I2CSensorProcessor
# or
# from avista_sensors.spisensor_processor import SPISensorProcessor
# or
# from avista_sensors.gpiosensor_processor import GPIOSensorProcessor
#
# we would then replace (SensorProcessor) component of the class definition below with either
# (I2CSensorProcessor) or (SPISensorProcessor) or (GPIOSensorProcessor)
#
# All of this is dependent on the type of sensor communication used

class RPMProcessor(SensorProcessor):

  def _read_sensor(self, ts):
  
    # write any code you need to extract raw data from the sensor
    raw_data = read(address)
    
    # write mathematical code that converts this data to useable form
    useable = raw_data / 100
    
    return useable

