import asyncio
from collections import namedtuple
from functools import reduce
from enum import Enum, auto


MetricEntry = namedtuple('MetricEntry', 'metric_title value timestamp')


class CommandType(Enum):
    put = auto()
    get = auto()


class ClientServerProtocol(asyncio.Protocol):
    event_list: [MetricEntry] = []

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, command: str) -> str:
        args = command.split()
        if args[0] == CommandType.put.name:
            try:
                metric_title = args[1]
                value = float(args[2])
                timestamp = int(args[3])
            except Exception:
                return self.wrong_command_str

            self.event_list.append(MetricEntry(metric_title, value, timestamp))
            return self.ok_command_str
        elif args[0] == CommandType.get.name:
            try:
                metric_title = args[1]
            except Exception:
                return self.wrong_command_str

            metric_list = self.get_metric_list(metric_title)

            metric_entry_strings = reduce(lambda a, x: a + x + '\n', map(self.metric_entry_to_string, metric_list), '')
            response = self.wrap_with_ok(metric_entry_strings)
            return response
        else:
            return self.wrong_command_str

    def get_metric_list(self, metric_title: str) -> [MetricEntry]:
        if metric_title == "*":
            return self.event_list
        else:
            filtered = list(filter(lambda x: x.metric_title == metric_title, self.event_list))
            return filtered

    @staticmethod
    def wrap_with_ok(string: str) -> str:
        return f'ok\n{string}\n'

    @staticmethod
    def metric_entry_to_string(metric_entry: MetricEntry) -> str:
        return f"{metric_entry.metric_title} {metric_entry.value} {metric_entry.timestamp}"
        
    @property
    def ok_command_str(self):
        return self.wrap_with_ok('')

    @property
    def wrong_command_str(self):
        return "error\nwrong command\n\n"


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server("127.0.0.1", 8181)
