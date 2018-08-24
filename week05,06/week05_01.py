import time
import socket
from enum import Enum, auto
from collections import namedtuple


MetricEntry = namedtuple('MetricEntry', 'metric_title value timestamp')


class ClientError(Exception):
    pass


class CommandType(Enum):
    put = auto()
    get = auto()


class ResponseType(Enum):
    ok = auto()
    error = auto()


class ResponseParser:
    @staticmethod
    def parse(resp_string: str):
        lines = resp_string.splitlines()
        if not lines:
            raise ClientError

        if lines[0] == ResponseType.error.name:
            raise ClientError

        filtered = filter(lambda x: x, lines[1:])
        metric_entries = list(map(lambda x: ResponseParser.__parse_metric_str(x), filtered))
        metrics_dict = {}
        for me in metric_entries:
            key = me.metric_title
            tuple_list = metrics_dict.get(key, [])
            tuple_list.append((me.timestamp, me.value))
            metrics_dict[key] = tuple_list

        return metrics_dict

    @staticmethod
    def __parse_metric_str(metric_str: str):
        args = metric_str.split()
        try:
            metric_title = args[0]
            value = float(args[1])
            timestamp = int(args[2])
        except Exception:
            raise ClientError

        return MetricEntry(metric_title, value, timestamp)


class Client:
    def __init__(self, addr, port, timeout=None):
        self.addr = addr
        self.port = port
        self.timeout = timeout

        self.sock = socket.create_connection((addr, port), timeout)

    def put(self, metric_title: str, value: float, timestamp: int=None):
        if timestamp is None:
            timestamp = int(time.time())

        command = RequestBuilder.make_put_command_string(metric_title, value, timestamp)
        try:
            self.sock.send(command.encode())
            resp = self.sock.recv(1024).decode()
            if not resp.startswith(ResponseType.ok.name):
                raise ClientError
        except socket.error:
            raise ClientError

    def get(self, metric_title: str):
        command = RequestBuilder.make_get_command_string(metric_title)
        try:
            self.sock.send(command.encode())
            resp = self.sock.recv(1024).decode()
        except Exception:
            raise ClientError

        metrics_dict = ResponseParser.parse(resp)
        metrics_dict_with_sorted_values = {}
        for key, value in metrics_dict.items():
            metrics_dict_with_sorted_values[key] = sorted(value)

        return metrics_dict_with_sorted_values

    def close(self):
        self.sock.close()

    def __del__(self):
        self.close()


class RequestBuilder:
    @staticmethod
    def make_put_command_string(metric_title: str, value: float, timestamp: int) -> str:
        return f"{CommandType.put.name} {metric_title} {value} {timestamp}\n"

    @staticmethod
    def make_get_command_string(metric_title: str) -> str:
        return f"{CommandType.get.name} {metric_title}\n"


if __name__ == '__main__':
    client = Client("127.0.0.1", 8181, timeout=15)

    client.put("palm.cpu", 0.5, timestamp=1150864247)
    client.put("palm.cpu", 2.0, timestamp=1150864248)
    client.put("palm.cpu", 0.5, timestamp=1150864248)

    client.put("eardrum.cpu", 3, timestamp=1150864250)
    client.put("eardrum.cpu", 4, timestamp=1150864251)

    client.put("eardrum.memory", 4200000)

    print(client.get("*"))
    print(client.get("palm.cpu"))
    print(client.get("palm"))
    print(client.get("111"))

    client.close()
