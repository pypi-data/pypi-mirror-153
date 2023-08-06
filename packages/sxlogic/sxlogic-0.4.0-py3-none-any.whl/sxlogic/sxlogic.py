import os
import sys
import json
import serial

########## SETTINGS

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def app_folder():
    prog = 'sxlogic'
    if sys.platform == 'win32':
        folder = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', prog)
        make_dir(folder)
        return folder
    else:
        folder = os.path.join(os.path.expanduser('~'), '.' + prog)
        make_dir(folder)
        return folder

def load_settings():
    filename = os.path.join(app_folder(), 'settings.json')
    if os.path.exists(filename):
        with open(filename) as fd:
            return json.loads(fd.read())
    return {}

def save_settings(settings):
    filename = os.path.join(app_folder(), 'settings.json')
    outf = open(filename, 'w')
    outf.write(json.dumps(settings))
    outf.close()

########## FPGA

ser = None

def open_fpga(port, baud = None, timeout=2.0):
    global ser

    if baud == None:
        baud = 1000000
    ser = serial.Serial(port, baud, timeout=timeout)
    return ser

def start_fpga():
    global ser

    if not ser:
        raise Exception('FPGA I/O not open')

    ser.write(b' ')

def call_fpga(size, count):
    global ser

    if not ser:
        raise Exception('FPGA I/O not open')

    ser.write(b' ')
    buf = bytearray()
    for i in range(count):
        x = ser.read(size)
        if len(x) == size:
            buf.extend(x)
        else:
            break
    return bytes(buf)

def read_fpga(size, count):
    global ser

    if not ser:
        raise Exception('FPGA I/O not open')

    buf = bytearray()
    for i in range(count):
        x = ser.read(size)
        if len(x) == size:
            buf.extend(x)
        else:
            break
    return bytes(buf)

def read_byte():
    global ser

    if not ser:
        raise Exception('FPGA I/O not open')

    return ser.read()

def stop_fpga(flush):
    global ser

    if not ser:
        raise Exception('FPGA I/O not open')

    ser.write(b'!')
    if flush:
        flushed = 0
        while len(ser.read()):
            flushed += 1
        print(flushed, 'flushed')

def close_fpga():
    if ser:
        ser.close()
