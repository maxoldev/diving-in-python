import time
import socket


class ClientError(Exception):
    pass


class Client:
    def __init__(self, addr, port, timeout=None):
        self.addr = addr
        self.port = port
        self.timeout = timeout

        self.sock = socket.create_connection((addr, port), timeout)

    def put(self, metric_title, value, timestamp=None):
        if timestamp is None:
            timestamp = str(int(time.time()))

        command = self.make_put_command_string(metric_title, value, timestamp)
        self.sock.send(command.encode())

    def get(self, metric_title):
        command = self.make_get_command_string(metric_title)
        self.sock.recv(1024)

    @staticmethod
    def make_put_command_string(metric_title: str, value: float, timestamp: int) -> str:
        return f"put {metric_title} {value} {timestamp}\n"

    @staticmethod
    def make_get_command_string(metric_title: str) -> str:
        return f"get {metric_title}\n"


'''
client = Client("127.0.0.1", 8888, timeout=15)

client.put("palm.cpu", 0.5, timestamp=1150864247)
client.put("palm.cpu", 2.0, timestamp=1150864248)
client.put("palm.cpu", 0.5, timestamp=1150864248)

client.put("eardrum.cpu", 3, timestamp=1150864250)
client.put("eardrum.cpu", 4, timestamp=1150864251)
client.put("eardrum.memory", 4200000)

print(client.get("*"))
'''