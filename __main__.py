import sys
import multiprocessing

from src.console import Console
from nve_server import NVEServer

def server_run(device_ip = sys.argv[1], subnet = sys.argv[2]):
    server = NVEServer(sys.argv[1], sys.argv[2])
    server.start()

server = multiprocessing.Process(target=server_run)
console = 