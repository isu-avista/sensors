import requests
from avista_data.data_point import DataPoint
from avista_data.server import Server
from avista_data.device import Device
from avista_data.sensor import Sensor
from collections import deque
import logging


class DataTransporter:
    """Abstract base class for all sensor processors.

    Attributes:
        **_markers (deque)**: queue of timestamps when the last time data was sent to the server
    """

    def __init__(self, db):
        """Constructs a new sensor processor"""
        self._markers = deque()
        self.db = db

    def transfer(self):
        """Collects and transfers data to each of the known sensors, and then if the data was transferred removes
        that data from the database
        """
        servers = self.db.query(Server).all()
        data = self.collect_data()
        rv = None
        print("Transferring data")
        logging.info("Transferring data")
        for server in servers:
            ip = server.get_ip_address()
            port = server.get_port()
            rv = requests.post(f'http://{ip}:{port}/api/data', json=data)
            print(f"sending data to: http://{ip}:{port}/api/data")
            logging.info(f"transferring data to: http://{ip}:{port}/api/data")
        if rv is not None and 'application/json' in rv.headers['Content-Type'] and rv.json()['status'] == "success":
            self.clear_old_data()

    def collect_data(self):
        """Collects the data from the database.

        Specifically, for the specified device, it collects each sensor attached to the device.
        Then, for each sensor it collects the datapoints since the last data submission.
        The collected data is then returned.

        Returns:
            the collected data as a dictionary.
        """
        device = self.db.query(Device).first()
        data = {'device': device.to_dict(), 'data': []}
        max_ts = 0
        if len(self._markers) == 0:
            self._markers.append(0)
        for sensor in self.db.query(Sensor).all():
            points = []
            for d in filter(lambda s: s.timestamp > self._markers[0], sensor.data):
                points.append(d.to_dict())
                if d.get_timestamp() > max_ts:
                    max_ts = d.get_timestamp()
            sensor_data = {'sensor': sensor.to_dict(), 'data_points': points}
            data['data'].append(sensor_data)
        self._markers.append(max_ts)
        return data

    def clear_old_data(self):
        """Finds and removes all data with a timestamp less than the smallest timestamp in the markers deque."""
        if len(self._markers) >= 3:
            drop_ts = self._markers.popleft()
            to_drop = self.db.query(DataPoint).filter(DataPoint.timestamp <= drop_ts).all()
            for d in to_drop:
                self.db.delete(d)
            self.db.commit()
