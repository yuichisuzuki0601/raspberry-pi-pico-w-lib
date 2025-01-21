import gc
import time
import socket
import struct

NTP_SERVER = 'pool.ntp.org'
NTP_DELTA = 2208988800
JST_OFFSET = 9 * 60 * 60

ERROR_MESSAGE = "Cannot determine the time"

def __fetch_time():
    try:
        addr = socket.getaddrinfo(NTP_SERVER, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)

        msg = b'\x1b' + 47 * b'\0'
        s.sendto(msg, addr)
        msg, addr = s.recvfrom(1024)

        s.close()
        gc.collect()

        t = struct.unpack("!12I", msg)[10]
        t -= NTP_DELTA

        return t
    except OSError:
        raise OSError("ERR: Failed to fetch time from NTP server")

def __format_time(timestamp, offset = 0, timezone_name = "UTC"):
    tm = time.localtime(timestamp + offset)
    milliseconds = time.ticks_ms() % 1000

    sign = '-' if offset < 0 else '+'
    hours = abs(offset) // 3600
    minutes = (abs(offset) % 3600) // 60

    timezone_offset = '{}{:02d}:{:02d}'.format(sign, hours, minutes)

    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:03d} {} {}".format(
        tm[0], tm[1], tm[2], tm[3], tm[4], tm[5], milliseconds,
        timezone_offset, timezone_name
    )

def now():
    try:
        utc_timestamp = __fetch_time()
        return __format_time(utc_timestamp, timezone_name = "UTC")
    except OSError:
        return ERROR_MESSAGE

def jstNow():
    try:
        utc_timestamp = __fetch_time()
        return __format_time(utc_timestamp, JST_OFFSET, "JST")
    except OSError:
        return ERROR_MESSAGE
