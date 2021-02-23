from dotenv import load_dotenv
from avista_sensors.service import Service
from pathlib import Path
import os

path = Path(os.getcwd()) / ".avistaenv"
if path.exists():
    load_dotenv(path)

if __name__ == '__main__':
    service = Service.get_instance()
    service.initialize()
    # service.start()
    service.run()

