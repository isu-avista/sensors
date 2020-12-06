import yaml
from pathlib import Path
import json


def import_from(name):
    """Imports a class from the given fully qualified class name

    Args:
        **name (str)**: fully qualified class name

    Returns:
        class that was imported

    Raises:
        Exception: if the provided class name is None or empty
    """
    if name is None or name == "":
        raise Exception("can not import nothing")
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def dynamic_import(module, class_name):
    """Allows for the dynamic import and instantiation of a given class

    Args:
        **module (str)**: The full name of the module holding the class

        **class_name (str)**: The name of the class to be instantiated

    Returns:
        Instance of module.class_name if it specifies an actual class otherwise None
    """
    if module is None or module == "":
        return None
    if class_name is None or module == "":
        return None
    klass = import_from(module + "." + class_name)
    return klass()


def load_sensor_from_dict(dct):
    """Loads a sensor from the information in the provided dict

    Required fields:
        **module**: name of the module

        **cls**: name of the class in the module

        **name**: name of the sensor

        **pinout**: list of dictionaries which are var, pin pairs

    Args:
        dct (dict): dictionary containing the information necessary to load a sensor

    Returns:
        None if the module or class information is missing, otherwise an instance of the sensor
    """
    if "module" not in dct.keys() or dct["module"] == "" or \
            "cls" not in dct.keys() or dct["cls"] == "":
        return None
    sensor = dynamic_import(dct["module"], dct["cls"])
    sensor.set_name(dct["name"])
    if dct["pinout"] is not None:
        pinout = dct["pinout"]
        for po in pinout:
            var = po["var"]
            pin = int(po["pin"])
            sensor.add_pinout(var, pin)
    return sensor


def load_from_config(path):
    """Loads required sensors from a configuration file

    Args:
        **path (str)**: the base path for the location of configuration files
    """
    config_dir = Path(path)
    with open(config_dir / "sensors.yml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    sensors = []

    for d in data['sensors']:
        sensor = load_sensor_from_dict(d)
        if sensor is not None:
            sensors.append(sensor)
    return sensors


def load_from_json(data):
    """Loads a sensor from a JSON representation

    Args:
        **data (:obj: `JSON`)**: JSON specification of a sensor processor
    """
    if data is None:
        return None
    dct = json.loads(data)
    return load_sensor_from_dict(dct)
