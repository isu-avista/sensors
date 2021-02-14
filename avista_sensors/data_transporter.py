import requests
from avista_data.data_point import DataPoint
from avista_data.server import Server
from avista_data.device import Device
from avista_data import db
from collections import deque


class DataTransporter:

    def __init__(self):
        self._markers = deque()

    def transfer(self):
        servers = Server.query.all()
        data = self.collect_data()
        rv = None
        for server in servers:
            ip = server.get_ip_address()
            port = server.get_port()
            rv = requests.post(f'http://{ip}:{port}/api/data', json=data)
        if 'application/json' in rv.headers['Content-Type'] and rv.json()['status'] == "success":
            self.clear_old_data()

    def collect_data(self):
        device = Device.query.first()
        data = {'device': device.to_dict(), 'data': []}
        max_ts = 0
        if len(self._markers) == 0:
            self._markers.append(0)
        for sensor in device.sensors:
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
        if len(self._markers) >= 3:
            drop_ts = self._markers.popleft()
            to_drop = DataPoint.query.filter(DataPoint.timestamp <= drop_ts).all()
            for d in to_drop:
                db.session.delete(d)
            db.session.commit()
