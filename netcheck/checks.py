import speedtest
import json
import subprocess
import humanfriendly
from datetime import datetime
from time import sleep
import random


# class SpeedResult:
#     """
#     Class that represents a single result. up_speed and down_speed are measured
#     in bytes/second.
#     """

#     def __init__(
#             self,
#             name: str,
#             datetime: datetime,
#             down_speed: int,
#             up_speed: int):
#         self.name = test_name
#         self.datetime = datetime
#         self.down_speed = down_speed
#         self.up_speed = up_speed


def make_result(name: str,
                  datetime: datetime,
                  down_speed: int,
                  up_speed: int) -> dict:
    return {
        "name": name,
        "datetime": datetime,
        "down_speed": down_speed,
        "up_speed": up_speed
    }


def __print_datetime(o):
    if isinstance(o, datetime):
        return o.__str__()


def __call_speedtest():
    """
    Calls the speedtest (python) test. Raw result is like:
    {
        "download": 66995568.19996329,
        "upload": 19865040.55315953,
        "ping": 102.133,
        "server": {
            "url": "http://speedtest.manx.net:8080/speedtest/upload.php",
            "lat": "54.1675",
            "lon": "-4.4824",
            "name": "Douglas",
            "country": "Isle of Man",
            "cc": "IM",
            "sponsor": "Manx Telecom",
            "id": "3778",
            "host": "speedtest.manx.net:8080",
            "d": 104.66728373946167,
            "latency": 102.133
        },
        "timestamp": "2020-04-26T09:21:53.532511Z",
        "bytes_sent": 24952832,
        "bytes_received": 83840976,
        "share": null,
        "client": {
            "ip": "82.1.123.106",
            "lat": "54.5829",
            "lon": "-5.9326",
            "isp": "Virgin Media",
            "isprating": "3.7",
            "rating": "0",
            "ispdlavg": "0",
            "ispulavg": "0",
            "loggedin": "0",
            "country": "GB"
        }
    }
    """
    servers = []
    threads = None
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    results = s.results.dict()
    # Results upload and download are bits/s
    return make_result(
        "speedtest-cli",
        datetime.now(),
        int(results['download'] / 8),
        int(results['upload'] / 8)
    )


def __size_to_bytes(size_string: str):
    """
    Converts a human size (14.3GiB) to raw bytes
    """
    return humanfriendly.parse_size(size_string)
    # value = int("".join(filter(str.isdigit, speed_string)))
    # unit = "".join(filter(str.isalpha, speed_string))[:-2]
    # print(f"Value: {value}, Unit: {unit}")


def __call_fast():
    """
    Calls the nodejs fast program. Raw result is like b'170Mbps\n18Mbps\n'
    """
    completed = subprocess.run(["fast", "--upload"], capture_output=True)
    output = str(completed.stdout, 'utf-8')
    # output = "137Mbps\n30Mbps\n"
    speeds = output.splitlines(keepends=False)

    # Remove the 'per second' ps suffix with :-2
    return make_result(
        "fast.com",
        datetime.now(),
        int(__size_to_bytes(speeds[0][:-2])),
        int(__size_to_bytes(speeds[1][:-2])),
    )


def __call_dummy():
    return make_result(
        "dummy",
        datetime.now(),
        random.randint(10000, 10000000),
        random.randint(10000, 10000000)
    )


def execute():
    return __call_fast()


def execute_test():
    sleep(1.2)
    return __call_dummy()
