# first written by nandflash("저장장치") <github@printk.info> since 2020-06-25

import socket
import serial
import json

import sys
import logging
from logging.handlers import RotatingFileHandler
import os.path
from time import sleep

####################

logger = logging.getLogger(__name__)


class SDSSerial:
    def __init__(self):
        self._ser = serial.Serial()
        self._ser.port = Options["serial"]["port"]
        self._ser.baudrate = Options["serial"]["baudrate"]
        self._ser.bytesize = Options["serial"]["bytesize"]
        self._ser.parity = Options["serial"]["parity"]
        self._ser.stopbits = Options["serial"]["stopbits"]

        self._ser.close()
        self._ser.open()

        self._pending_recv = 0

        # 시리얼에 뭐가 떠다니는지 확인
        self.set_timeout(5.0)
        data = self._recv_raw(1)
        self.set_timeout(None)
        if not data:
            logger.critical("no active packet at this serial port!")

    def _recv_raw(self, count=1):
        return self._ser.read(count)

    def recv(self, count=1):
        # serial은 pending count만 업데이트
        self._pending_recv = max(self._pending_recv - count, 0)
        return self._recv_raw(count)

    def send(self, a):
        self._ser.write(a)

    def set_pending_recv(self):
        self._pending_recv = self._ser.in_waiting

    def check_pending_recv(self):
        return self._pending_recv

    def check_in_waiting(self):
        return self._ser.in_waiting

    def set_timeout(self, a):
        self._ser.timeout = a


class SDSSocket:
    def __init__(self):
        addr = Options["socket"]["address"]
        port = Options["socket"]["port"]

        self._soc = socket.socket()
        self._soc.connect((addr, port))

        self._recv_buf = bytearray()
        self._pending_recv = 0

        # 소켓에 뭐가 떠다니는지 확인
        self.set_timeout(5.0)
        data = self._recv_raw(1)
        self.set_timeout(None)
        if not data:
            logger.critical("no active packet at this socket!")

    def _recv_raw(self, count=1):
        return self._soc.recv(count)

    def recv(self, count=1):
        # socket은 버퍼와 in_waiting 직접 관리
        if len(self._recv_buf) < count:
            new_data = self._recv_raw(1024)
            self._recv_buf.extend(new_data)
        if len(self._recv_buf) < count:
            return None

        self._pending_recv = max(self._pending_recv - count, 0)

        res = self._recv_buf[0:count]
        del self._recv_buf[0:count]
        return res

    def send(self, a):
        self._soc.sendall(a)

    def set_pending_recv(self):
        self._pending_recv = len(self._recv_buf)

    def check_pending_recv(self):
        return self._pending_recv

    def check_in_waiting(self):
        if len(self._recv_buf) == 0:
            new_data = self._recv_raw(1024)
            self._recv_buf.extend(new_data)
        return len(self._recv_buf)

    def set_timeout(self, a):
        self._soc.settimeout(a)


def init_logger():
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def init_logger_file():
    if Options["log"]["to_file"]:
        filename = Options["log"]["filename"]
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler = RotatingFileHandler(os.path.abspath(Options["log"]["filename"]), mode='a', backupCount=100)
        handler.setFormatter(formatter)
        handler.suffix = '%Y%m%d'
        logger.addHandler(handler)
        handler.doRollover()


def init_option(argv):
    # option 파일 선택
    if len(argv) == 1:
        option_file = "./options_standalone.json"
    else:
        option_file = argv[1]

    # configuration이 예전 버전이어도 최대한 동작 가능하도록,
    # 기본값에 해당하는 파일을 먼저 읽고나서 설정 파일로 업데이트 한다.
    global Options

    # 기본값 파일은 .py 와 같은 경로에 있음
    default_file = os.path.join(os.path.dirname(os.path.abspath(argv[0])), "config.json")

    with open(default_file) as f:
        config = json.load(f)
        logger.info("addon version {}".format(config["version"]))
        Options = config["options"]
    with open(option_file) as f:
        Options2 = json.load(f)

    # 업데이트
    for k, v in Options.items():
        if type(v) is dict and k in Options2:
            Options[k].update(Options2[k])
            for k2 in Options[k].keys():
                if k2 not in Options2[k].keys():
                    logger.warning("no configuration value for '{}:{}'! try default value ({})...".format(k, k2, Options[k][k2]))
        else:
            if k not in Options2:
                logger.warning("no configuration value for '{}'! try default value ({})...".format(k, Options[k]))
            else:
                Options[k] = Options2[k]


def dump_loop():
    conn.set_timeout(0.0)
    logs = []
    while True:
        try:
            data = conn.recv(conn.check_in_waiting())
        except:
            continue

        if data:
            logs = []
            for b in data:
#               if b == 0xA1 or len(logs) > 500:
#                   logger.info("".join(logs))
#                   logs = ["{:02X}".format(b)]
#               elif b <= 0xA0: logs.append(   "{:02X}".format(b))
#               elif b == 0xFF: logs.append(   "{:02X}".format(b))
#               elif b == 0xB0: logs.append( ": {:02X}".format(b))
#               else:           logs.append(",  {:02X}".format(b))
                logs.append(" {:02X}".format(b))
            logger.info("".join(logs))
        sleep(0.01)

    logger.info("".join(logs))
    logger.warning("dump done.")
    conn.set_timeout(None)


if __name__ == "__main__":
    global conn

    # configuration 로드 및 로거 설정
    init_logger()
    init_option(sys.argv)
    init_logger_file()

    if Options["serial_mode"] == "socket":
        logger.info("initialize socket...")
        conn = SDSSocket()
    else:
        logger.info("initialize serial...")
        conn = SDSSerial()

    dump_loop()
