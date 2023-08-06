import os
import sys
import time
from struct import unpack_from
import argparse

from .sxlogic import open_fpga, close_fpga, call_fpga, start_fpga, read_fpga, read_byte, stop_fpga

default_herz = 15625
#default_herz = 18750

def fpgacap():
    global frameno

    parser = argparse.ArgumentParser(prog='fpgacap', description='SxImage FPGA CLI')
    parser.add_argument('-d','--decimal', action='store_true', help='decimal display')
    parser.add_argument('-u','--unsigned', action='store_true', help='unsigned display')
    parser.add_argument('-r','--rgb', action='store_true', help='rgb image')
    parser.add_argument('-g','--gray', action='store_true', help='grayscale image')
    parser.add_argument('--heat', action='store_true', help='heatmap image')
    parser.add_argument('--wav', action='store_true', help='audio frame')
    parser.add_argument('--text', action='store_true', help='text output')
    parser.add_argument('--rec', type=int, help='record')
    parser.add_argument('--measure', action='store_true', help='measure')
    parser.add_argument('-w','--width', type=int, default=None)
    parser.add_argument('--height', type=int, default=None)
    parser.add_argument('-z','--zoom', type=int, default=None)
    parser.add_argument('-l','--loop', action='store_true')
    parser.add_argument('-c','--continuous', type=int, default=None)
    parser.add_argument('-o','--out', default=None)
    parser.add_argument('--size', type=int, default=1, help='word size, bytes')
    parser.add_argument('--interval', type=int, default=200)
    parser.add_argument('--timeout', type=int, default=2000)
    parser.add_argument('--baud', type=int, default=1000000)
    parser.add_argument('--hz', type=int, default=default_herz)
    parser.add_argument('port')
    args = parser.parse_args()

    if args.rgb or args.gray or args.heat:
        import cv2
        import numpy as np

    if args.wav:
        import wave

    if args.rec:
        if not args.wav:
            print('The --wav option must be present with --rec')
            sys.exit(1)
        if not args.out:
            print('The --out option must be present with --rec')
            sys.exit(1)
    elif args.rgb or args.gray or args.heat or args.wav:
        if not args.width:
            print('The -w/--width option must be present with --rgb, --gray, --heat or --wav')
            sys.exit(1)
    elif args.loop:
        if not args.width:
            print('The -w/--width option must be present with --loop')
            sys.exit(1)

    if args.loop:
        if args.wav:
            print('Cannot use --loop with --wav option')
            sys.exit(1)
            
    frameno = 0
    if args.loop and args.out:
        while frameno < 9999:
            name = "%s-%04d.tiff" % (args.out, frameno)
            if not os.path.exists(name):
                break
            frameno += 1
        if frameno >= 10000:
            print('Exceeded maximum frame series')
            sys.exit(1)
        if frameno > 0:
            print('Resuming capture series at '+name)

    def calc_size():
        if args.rgb:
            h = args.height if args.height else args.width
            return (h, args.width * 3)
        elif args.gray or args.heat:
            h = args.height if args.height else args.width
            return (h, args.width * args.size)
        elif args.wav:
            return (args.width, 2)
        elif args.height:
            return (args.height, args.width * args.size)
        return (args.width, args.size)

    def scroll(buf1, buf2):
        keep = buf1[len(buf2):]
        return keep + buf2

    def toint(b):
        if b > 127:
            return int(b) - 256
        return int(b)

    def emitrow(buf, split=None):
        if split:
            n = len(buf)//split
            if args.decimal:
                if split == 1:
                    a = [unpack_from('b', buf, i)[0] for i in range(n)]
                elif split == 2:
                    a = [unpack_from('>h', buf, i*2)[0] for i in range(n)]
                elif split == 4:
                    a = [unpack_from('>i', buf, i*4)[0] for i in range(n)]
                else:
                    raise Exception('Invalid decimal size %d' % split)
            elif args.unsigned:
                if split == 1:
                    a = [unpack_from('B', buf, i)[0] for i in range(n)]
                elif split == 2:
                    a = [unpack_from('>H', buf, i*2)[0] for i in range(n)]
                elif split == 4:
                    a = [unpack_from('>I', buf, i*4)[0] for i in range(n)]
                else:
                    raise Exception('Invalid unsigned size %d' % split)
            else:
                a = [buf[split*i:split*(i+1)].hex() for i in range(n)]
            print('\t'.join([str(x) for x in a]))
        elif args.decimal:
            print('\t'.join(['%d' % toint(x) for x in buf]))
        elif args.unsigned:
            print('\t'.join(['%d' % x for x in buf]))
        else:
            print(buf.hex())

    def emit(buf, split=None):
        if args.height:
            chunk = len(buf)//args.height
            for i in range(args.height):
                emitrow(buf[i*chunk:(i+1)*chunk], split)
        else:
            emitrow(buf, split)

    def write_img(img):
        global frameno
        if args.loop:
            name = "%s-%04d.tiff" % (args.out, frameno)
            cv2.imwrite(name, img)
            frameno += 1
        else:
            cv2.imwrite(args.out, img)

    def write_wav_ary(chunks):
        total = sum([len(ba) for ba in chunks])
        wav = wave.open(args.out, 'wb')
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(args.hz)
        wav.setnframes(total//2)
        for ba in chunks:
            le = bytearray()
            for i in range(len(ba)//2):
                le.append(ba[1+2*i])
                le.append(ba[2*i])
            wav.writeframes(bytes(le))
        wav.close()

    def write_wav(ba):
        le = bytearray()
        for i in range(len(ba)//2):
            le.append(ba[1+2*i])
            le.append(ba[2*i])
        wav = wave.open(args.out, 'wb')
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(args.hz)
        wav.setnframes(len(ba)//2)
        wav.writeframes(bytes(le))
        wav.close()

#        outf = open('audio.hex','w')
#        for i in range(len(ba)//2):
#            outf.write(ba[i*2:(i+1)*2].hex()+'\n')
#        outf.close()

    def show_rgb(ba, width, height, zoom):
        if height == None:
            height = width
        img = np.fromstring(ba, dtype=np.uint8).reshape(height, width, 3)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if zoom:
            img = cv2.resize(img, (height*zoom, width*zoom))
        cv2.imshow('capture', img)
        if args.out:
            write_img(img)

    def show_gray(ba, width, height, size, zoom):
        if height == None:
            height = width
        if size == 1:
            img = np.frombuffer(ba, dtype=np.uint8).reshape(height, width)
        elif size == 2:
            dt = np.dtype('>H')
            img = np.frombuffer(ba, dtype=dt).reshape(height, width)
            img = (img / 256.0).astype(np.uint8)
        else:
            raise Exception('Invalid gray image channel size %d' % size)
        if zoom:
            img = cv2.resize(img, (height*zoom, width*zoom))
        cv2.imshow('capture', img)
        if args.out:
            write_img(img)

    def show_heat(ba, width, height, size, zoom):
        if height == None:
            height = width
        if size == 1:
            img = np.frombuffer(ba, dtype=np.uint8).reshape(height, width)
        elif size == 2:
            dt = np.dtype('>H')
            img = np.frombuffer(ba, dtype=dt).reshape(height, width)
        else:
            raise Exception('Invalid gray image channel size %d' % size)
        mx = float(np.amax(img))
        if mx > 0.0:
            img = (img * (255.0 / mx))
        heat = cv2.applyColorMap(img.astype(np.uint8), cv2.COLORMAP_HOT)
        if zoom:
            heat = cv2.resize(heat, (width*zoom, height*zoom))
        cv2.imshow('capture', heat)
        if args.out:
            write_img(heat)

    def play_wav(ba):
        if args.out:
            write_wav(ba)

    timeout = args.timeout / 1000.0

    if args.text:
        open_fpga(args.port, args.baud, timeout=timeout)
        buf = bytearray()
        run = True
        while run:
            one = read_byte()
            if len(one) > 0:
                if one != b'\n' and one != b'\r':
                    buf.extend(one)
                elif one == b'\n':
                    print(buf.decode('utf-8'))
                    #print(buf)
                    buf = bytearray()
            else:
                run = False
    elif args.rec:
        open_fpga(args.port, args.baud, timeout=timeout)
        print('Recording ...')
        t = time.monotonic()
        end_time = t + args.rec
        chunks = []
        start_fpga()
        while t < end_time:
            chunks.append(read_fpga(256,1))
            t = time.monotonic()
        print('Stopping ...')
        stop_fpga(True)
        write_wav_ary(chunks)
    elif args.measure:
        (n, sz) = calc_size()
        open_fpga(args.port, args.baud, timeout=timeout)
        start_t = time.monotonic()
        end_t = start_t + 1.0
        start_fpga()
        t = start_t
        count = 0
        while t < end_t:
            read_fpga(sz, n)
            count += 1
            t = time.monotonic()
        stop_fpga(True)
        rate = count / (t - start_t)
        print(rate)
    elif args.loop:
        (n, sz) = calc_size()
        open_fpga(args.port, args.baud, timeout=timeout)
        run = True
        while run:
            start = int(time.monotonic() * 1000)
            data = call_fpga(sz, n)
            elapsed = int(time.monotonic() * 1000) - start
            remaining = max(args.interval - start, 10)
            if len(data) == (n * sz):
                if args.rgb:
                    show_rgb(data, args.width, args.height, args.zoom)
                    run = cv2.waitKey(remaining) < 0
                elif args.gray:
                    show_gray(data, args.width, args.height, args.size, args.zoom)
                    run = cv2.waitKey(remaining) < 0
                elif args.heat:
                    show_heat(data, args.width, args.height, args.size, args.zoom)
                    run = cv2.waitKey(remaining) < 0
                else:
                    emit(data, args.size)
                    time.sleep(remaining / 1000.0)
            else:
                print('Read timeout (%d of %d)' % (len(data),n*sz))
                time.sleep(remaining / 1000.0)
    elif args.continuous:
        (n, sz) = calc_size()
        open_fpga(args.port, args.baud, timeout=timeout)
        data = call_fpga(sz, n)
        if len(data) != (n * sz):
            raise Exception('Read timeout (%d of %d)' % (len(data),n*sz))
        n = args.continuous
        run = True
        while run:
            if args.rgb:
                show_rgb(data, args.width, args.height, args.zoom)
                run = cv2.waitKey(10) < 0
            elif args.gray:
                show_gray(data, args.width, args.height, args.size, args.zoom)
                run = cv2.waitKey(10) < 0
            elif args.heat:
                show_heat(data, args.width, args.height, args.size, args.zoom)
                run = cv2.waitKey(10) < 0
            else:
                emit(data, args.size)
                time.sleep(1.0 / 1000.0)
            if run:
                data2 = read_fpga(sz, n)
                if len(data2) != (n * sz):
                    raise Exception('Read timeout (%d of %d)' % (len(data),n*sz))
                data = scroll(data, data2)
        print('Stopping ...')
        stop_fpga(True)
    elif args.width:
        (n, sz) = calc_size()
        open_fpga(args.port, args.baud, timeout=timeout)
        data = call_fpga(sz, n)
        if len(data) == (n * sz):
            if args.rgb:
                show_rgb(data, args.width, args.height, args.zoom)
                cv2.waitKey(0)
            elif args.gray:
                show_gray(data, args.width, args.height, args.size, args.zoom)
                cv2.waitKey(0)
            elif args.heat:
                show_heat(data, args.width, args.height, args.size, args.zoom)
                cv2.waitKey(0)
            elif args.wav:
                play_wav(data)
            else:
                emit(data, args.size)
        else:
            print('Read timeout (%d of %d)' % (len(data),n*sz))
    else:
        ser = open_fpga(args.port, args.baud, timeout=timeout)
        ser.write(b' ')
        total = 0
        while True:
            x = ser.read(args.size)
            if len(x):
                emit(x)
                total += len(x)
            else:
                break
        print(total, 'bytes')

    close_fpga()

if __name__ == '__main__':
    fpgacap()
