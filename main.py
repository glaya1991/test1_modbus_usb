#!/usr/bin/env python3

import sys
import string  # , keyboard
from os import terminal_size
import serial.tools.list_ports
import serial
import time
import os
import random
import threading

import crc16_modbus
import  colors_def

import gui
from tkinter import END, INSERT, SEL

# ----- define ------------------------ #
DEF_TERMINAL = 0

memo1_cnt = 0
memo2_cnt = 0

thread_alive = 0

memo_recv_pause = 0

# ----- Help function ----------------- #

def help_func():
    print('')
    print('-h - help')
    print('-b xxxx - set baudrate as xxxx bit/s: 115200, 57600, 38400, 19200, 9600 etc.')
    print('\t default: 115200 bit/s')
    print('-p xxxx - set port name as xxxx: /dev/tty* or COMxx')
    print('\t default: /dev/ttyUSB0')
    print('\t or: COM7')
    print('-n xxxx - set received data threshold as xxxx byte: 4, 8, 16 etc.')
    print('\t default: 4 byte')
    print('-m xxxx - set data mode as xxxx: hex, dec, sym(symbol)')
    print('\t default: hex')
    print('-t xxxx - set time delay')
    print('\t default: 0.1')
    print('')
    print('example: sudo /../../prog_serial.py -b 115200 -p /dev/ttyUSB0 -n 10 -m hex')
    print('example: ../../prog_serial.py -b 115200 -p COM7 -n 10 -m hex')
    print('')


# ----- Exit function ----------------- #

def exit_func():
    print("exit!")
    global global_ch_exit
    global_ch_exit = 1
    # quit()
    return


# ----- Info function ----------------- #

def info_func():
    global _port
    global _baudrate
    global N_TX
    global mode
    print("Port=", _port, ', baudrate=', _baudrate, ', N_TX=', N_TX, ', mode=', mode)
    return


# ----- Send/receive function: MODBUS --------- #
def modbus_func():
    '''
    in1=input(">> data TX: ")

    # linux
    #ser.write(in1.encode()) #linux

    # windows
    in2 = in1.split(' ')
    in3 = []
    for val in in2:
        in3.append(int(val, 16))
    ser.write(in3)
    '''

    flag_en = 1
    query = []
    func = 0
    addr = 0
    num = 0
    data0 = 0

    try:
        id = int(input("id (in hex!): "), 16)
        query.append(id)
    except Exception:
        print("Wrong id/n")
        return

    try:
        func = int(input("func (in hex!): "), 16)
    except Exception:
        print("Wrong func/n")
        return

    if (func == 3) or (func == 4):
        query.append(func)
        try:
            addr = int(input("addr (in dec!): "))
        except Exception:
            print("Wrong addr/n")
            return
        query.append(((addr) >> 8) & 0xFF)
        query.append(((addr)) & 0xFF)

        try:
            num = int(input("num (in dec!): "))
        except Exception:
            print("Wrong num/n")
            return
        query.append(((num) >> 8) & 0xFF)
        query.append(((num)) & 0xFF)

        query_size = 6
        res = crc16_modbus.CRC16(query, query_size)
        query.append(res >> 8)
        query.append(res & 0xFF)

    elif (func == 16):
        query.append(func)
        try:
            addr = int(input("addr (in dec!): "))
        except Exception:
            print("Wrong addr/n")
            return
        query.append(((addr) >> 8) & 0xFF)
        query.append(((addr)) & 0xFF)

        try:
            num = int(input("num (in dec!): "))
        except Exception:
            print("Wrong num/n")
            return
        query.append(((num) >> 8) & 0xFF)
        query.append(((num)) & 0xFF)
        count = num << 1
        query.append(count)

        try:
            data0 = int(input("data_ho[0] (in dec!): "))
        except Exception:
            print("Wrong data/n")
            return
        for i in range(count):
            # query.append(random.randint(1, 100))
            query.append((data0 + i) & 0xFF)
        query_size = 7 + count
        res = crc16_modbus.CRC16(query, query_size)
        query.append(res >> 8)
        query.append(res & 0xFF)
    else:
        print("No such func/n")
        return

    print(''.join('{:02X} '.format(val) for val in query))
    ser.write(query)

    # read old version -- now in thread
    # n = ser.in_waiting
    # delay_cnt = 0
    # while n==0 and delay_cnt<100:
    #     n = ser.in_waiting
    #     delay_cnt += 1
    #     time.sleep(tdelay)
    #
    # out = []
    # delay_cnt = 0
    # #print(n)
    # while(n!=0) and  delay_cnt<100:
    #     out.extend(ser.read(n))
    #     delay_cnt += 1
    #     time.sleep(tdelay)
    #     n = ser.in_waiting
    #     #print(n)
    #
    # n = len(out)
    # if n != 0:
    #     print("n={:d}: ".format(n), end=' ')
    #
    #     if mode == 'hex':
    #         for i in out:
    #             print("{:x}".format(i), end=' ')
    #
    #     elif mode == 'dec':
    #         for i in out:
    #             print("{:d}".format(i), end=' ')
    #
    #     else:
    #         print(out, end=' ')
    #
    #     res = crc16_modbus.CRC16(out, n-2)
    #     if (res == (out[-1]+out[-2]*256)):
    #         print("__OK__", end = ' ')
    #     else:
    #         print("__!!! FAIL !!!__", end = ' ')
    #
    #     print("")
    # else:
    #     print('Wrong request')

    return


def modbus_func2(id, func, addr, num, data0):
    '''
    in1=input(">> data TX: ")

    # linux
    #ser.write(in1.encode()) #linux

    # windows
    in2 = in1.split(' ')
    in3 = []
    for val in in2:
        in3.append(int(val, 16))
    ser.write(in3)
    '''

    global  memo1_cnt

    flag_en = 1
    query = []

    query.append(id)
    if (func == 0x03) or (func == 0x04):
        query.append(func)
        query.append(((addr) >> 8) & 0xFF)
        query.append(((addr)) & 0xFF)
        query.append(((num) >> 8) & 0xFF)
        query.append(((num)) & 0xFF)
        query_size = 6
        res = crc16_modbus.CRC16(query, query_size)
        query.append(res >> 8)
        query.append(res & 0xFF)

    elif (func == 0x10):
        query.append(func)
        query.append(((addr) >> 8) & 0xFF)
        query.append(((addr)) & 0xFF)
        query.append(((num) >> 8) & 0xFF)
        query.append(((num)) & 0xFF)
        count = num << 1
        query.append(count)
        for i in range(count):
            # query.append(random.randint(1, 100))
            query.append((data0 + i) & 0xFF)
        query_size = 7 + count
        res = crc16_modbus.CRC16(query, query_size)
        query.append(res >> 8)
        query.append(res & 0xFF)
    else:
        flag_en = 0

    '''
    memo1_cnt+=1
    if (flag_en):
        if DEF_TERMINAL:
            print(''.join('{:02X} '.format(val) for val in query))
        else:
            gui.memo_msg.insert(1.0, "".join('{:02X} '.format(val) for val in query).join("\r\n"))
            # gui.memo_send.insert(INSERT, "%d) " % memo1_cnt)
            # gui.memo_send.insert(INSERT, "".join('{:02X} '.format(val) for val in query).join("\r\n"))
    '''
    if flag_en == 0:
        query = []

    # ser.write(query)

        # read data old version^ now in thread
        # n = ser.in_waiting
        # delay_cnt = 0
        # while n == 0 and delay_cnt < 100:
        #     n = ser.in_waiting
        #     delay_cnt += 1
        #     time.sleep(tdelay)
        #
        # out = []
        # delay_cnt = 0
        # # print(n)
        # while (n != 0) and delay_cnt < 100:
        #     out.extend(ser.read(n))
        #     delay_cnt += 1
        #     time.sleep(tdelay)
        #     n = ser.in_waiting
        #     # print(n)
        #
        # n = len(out)
        # if n != 0:
        #     print("n={:d}: ".format(n), end=' ')
        #
        #     if mode == 'hex':
        #         for i in out:
        #             print("{:x}".format(i), end=' ')
        #
        #     elif mode == 'dec':
        #         for i in out:
        #             print("{:d}".format(i), end=' ')
        #
        #     else:
        #         print(out, end=' ')
        #
        #     if (n>2):
        #         res = crc16_modbus.CRC16(out, n - 2)
        #         if res == (out[-1] + out[-2] * 256):
        #             print("__OK__", end=' ')
        #         else:
        #             print("__!!! FAIL !!!__", end=' ')
        #
        #     print("")
    return query

def recv_msg():
    global memo2_cnt
    global memo_recv_pause
    
    mode = dict_mode[gui.var1.get()]

    n = ser.in_waiting
    delay_cnt = 0
    while n == 0 and delay_cnt < 10:
        n = ser.in_waiting
        delay_cnt += 1
        time.sleep(tdelay)

    out = []
    delay_cnt = 0
    # print(n)
    while (n != 0) and delay_cnt < 10:
        out.extend(ser.read(n))
        delay_cnt += 1
        time.sleep(tdelay)
        n = ser.in_waiting
        # print(n)

    char_pt = ord('.')
    n = len(out)
    if n != 0 and memo_recv_pause == 0:
        # if DEF_TERMINAL:
        #     print("n={:d}: ".format(n), end=' ')
        # else:
        #     memo2_cnt += 1
        #     gui.memo_recv.insert(INSERT, "{:d}) n={:d}: ".format(memo2_cnt, n))

        if DEF_TERMINAL:
            print("n={:d}: ".format(n), end=' ')
        else:
            memo2_cnt += 1
            gui.memo_recv.insert(INSERT, "{:d}: ".format(memo2_cnt, n))
            gui.memo_recv.see("end")

        if mode == 'hex':
            if DEF_TERMINAL:
                print("".join("{:02X} ".format(val) for val in out))
            else:
                gui.memo_recv.insert(INSERT, "".join("{:02X} ".format(val) for val in out).join("\r\n"))
                gui.memo_recv.see("end")

        elif mode == 'dec':
            if DEF_TERMINAL:
                print("".join("{:d} ".format(val) for val in out))
            else:
                gui.memo_recv.insert(INSERT, "".join("{:0d} ".format(val) for val in out).join("\r\n"))
                gui.memo_recv.see("end")

        elif mode == 'sym':

            for i in out:
                try:
                    if (i == 0xa) or (i == 0xd): i = char_pt  # doesn't work, if <14
                    if DEF_TERMINAL:
                        print(chr(i), end='')
                    else:
                        gui.memo_recv.insert(INSERT, chr(i))
                        gui.memo_recv.see("end")

                except:
                    if DEF_TERMINAL:
                        print('x', end=' ')
                    else:
                        gui.memo_recv.insert(INSERT, "x")
                        gui.memo_recv.see("end")

            if DEF_TERMINAL:
                print('\r\n', out, end=' ')
            else:
                gui.memo_recv.insert(INSERT, "\r\n")
                gui.memo_recv.see("end")

        else:
            if DEF_TERMINAL:
                print(out, end=' ')
            else:
                gui.memo_recv.insert(INSERT, "else var\r\n")
                gui.memo_recv.see("end")

    return out

def func_recv():
    global thread_alive
    while thread_alive:
        msg_recv = recv_msg()
        n = len(msg_recv)
        if (n > 2):
            res = crc16_modbus.CRC16(msg_recv, n - 2)
            # if res == (msg_recv[-1] + msg_recv[-2] * 256):
            #     print("__OK__", end=' ')
            # else:
            #    print("__!!! FAIL !!!__", end=' ')
        if(n>0):
            print("\r\n")

    return

def func_read():
    str1 = gui.memo_send.get(1.0, END)
    gui.lbl1.config(text="memo1: {0}".format(str1))
    gui.memo_send.insert(INSERT, ".end")
    return

def func_clear():
    global memo1_cnt
    memo1_cnt = 0
    gui.memo_send.delete(1.0, END)
    return


def func_clear2():
    global memo2_cnt
    memo2_cnt = 0
    gui.memo_recv.delete(1.0, END)
    return

def func_clear_memo_recv():
	global memo_recv_pause
	memo_recv_pause=1-memo_recv_pause
	if memo_recv_pause:
		gui.btn_pause1.config(text="start")
	else:
		gui.btn_pause1.config(text="pause")	
	return	
	
def func_create_modbus_msg():
    id = int(gui.ent1.get(), 16)
    func = int(gui.ent2.get(), 16)
    addr = int(gui.ent3.get(), 16)
    num = int(gui.ent4.get(), 16)
    msg = modbus_func2(id, func, addr, num, 0)
    if msg:
        gui.memo_msg.delete(1.0, END)
        gui.memo_msg.insert(1.0, "".join('{:02X} '.format(val) for val in msg))
        #gui.memo_msg.insert(1.0, "".join('{:02X} '.format(val) for val in msg).join("\r\n"))
    else:
        gui.memo_msg.delete(1.0, END)
        gui.memo_msg.insert(1.0, "error")
    return

def func_send():
    msg_memo = str(gui.memo_send.get(1.0, END))
    msg0 = msg_memo.replace("\n", " ").replace("\r", " ").split()
    print(msg0)
    msg = []
    for i in msg0:
        msg.append(int(i, 16))

    ser.write(msg)
    time.sleep(0.1)
    return

def func_test1():
    msg = modbus_func2(0x7f, 0x03, 0, 1, 0)
    ser.write(msg)
    time.sleep(0.5)
    return

def func_test2():
    while 1:
        gui.memo_recv.insert(INSERT, "test2\r\n")
        time.sleep(2)
    return


def main():
    global thread_alive

    thread_recv = threading.Thread(target=func_recv)
    thread_alive = 1
    thread_recv.start()

    # thread_test2 = threading.Thread(target=func_test2)
    # thread_test2.start()

    print(gui.scrolly_recv.keys())

    gui.create_place()
    gui.btn_send.config(command=func_send)  # func_test1
    gui.btn_clr1.config(command=func_clear)
    gui.btn_clr2.config(command=func_clear2)
    gui.btn_get_msg.config(command=func_create_modbus_msg)
    gui.btn_pause1.config(command=func_clear_memo_recv)
    

    gui.start()

    thread_alive = 0
    thread_recv.join(5)


    # ----- main loop --------------------- #

    # test write/read
    test_en = 0
    if test_en:
        Nblocks = 32
        n_num = 8
        n_addr = int(Nblocks/n_num)
        for cnt in range(1):
            modbus_func2(0x7f, 0x03, 0, Nblocks, 0)

            for i in range(n_addr):  # addr
                modbus_func2(0x7f, 0x10, i*n_num, n_num, 0x30 + i * 0x10)

            for i in range(n_addr):  # addr
                modbus_func2(0x7f, 0x03, i*n_num, n_num, 0)

            modbus_func2(0x7f, 0x03, 0, Nblocks, 0)


    test_en = 0
    if test_en:
        Nblocks = 1
        while True:
            modbus_func2(0x7f, 0x03, 0, Nblocks, 0)
            time.sleep(0.5)
            input("press")

            # modbus_func2(0x7f, 0x03, 0, Nblocks*2, 0)
            # time.sleep(2)
            #
            # modbus_func2(0x7f, 0x03, 0, Nblocks*3, 0)
            # time.sleep(2)
            #
            # modbus_func2(0x7f, 0x03, 0, Nblocks*4, 0)
            # time.sleep(2)

    # test write/read for 2 mcu
    test_en = 0
    if test_en:
        id1 = 0x7f
        id2 = 0x1a
        Nblocks = 32
        n_num = 8
        n_addr = int(Nblocks/n_num)

        for cnt in range(10):
            modbus_func2(id1, 0x03, 0, Nblocks, 0)
            modbus_func2(id2, 0x03, 0, Nblocks, 0)

            for i in range(n_addr):  # addr
                modbus_func2(id1, 0x10, i*n_num, n_num, 0x30 + i * 0x10)
                modbus_func2(id2, 0x10, i*n_num, n_num, 0x34 + i * 0x10)

            for i in range(n_addr):  # addr
                modbus_func2(id1, 0x03, i*n_num, n_num, 0)
                modbus_func2(id2, 0x03, i*n_num, n_num, 0)

            modbus_func2(id1, 0x03, 0, Nblocks, 0)
            modbus_func2(id2, 0x03, 0, Nblocks, 0)


    global_ch_exit = 0  # flag exit: if 1 - exit programm!

    # while global_ch_exit == 0:
    #     modbus_func()

    return



# ------------------------------------- #
#        MAIN                           #
# ------------------------------------- #

# linux:
# _port = '/dev/ttyUSB0'

# Win
_port = 'COM7'
_baudrate = 2000000
N_TX = 512
mode = 'hex'
dict_mode = {'1': 'hex', '2': 'dec', '3': 'sym'}

tdelay = 0.001
_wr_en = 0

# available com ports
comlist = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(comlist):
    print("{}: {} [{}]".format(port, desc, hwid))


_port = input("COM-Port: ")
print("")

# ----- Set serial port parametrs ----- #

N_arg = len(sys.argv)
# print('Number of arguments:', N_arg, 'arguments.')
# print(sys.argv)

cnt = 0
if N_arg > 1:  # if program has arguments in command line
    for i in range(N_arg):
        if sys.argv[i] == '-b':
            try:
                _baudrate = int(sys.argv[i + 1])
                cnt += 1
            except Exception:
                print("Wrong Baudrate! Print -h for help!")
                exit()

        elif sys.argv[i] == '-p':
            try:
                _port = sys.argv[i + 1]
                cnt += 1
            except Exception:
                print("Wrong Port! Print -h for help!")
                exit()

        elif sys.argv[i] == '-n':
            try:
                N_TX = int(sys.argv[i + 1])
                cnt += 1
            except Exception:
                print("Wrong N_TX! Print -h for help!")
                exit()

        elif sys.argv[i] == '-m':
            try:
                mode = (sys.argv[i + 1])
                cnt += 1
                if ((mode in dict_mode.values()) == False):
                    print("Wrong mode! Print -h for help!")
                    exit()
            except Exception:
                print("Wrong mode!")
                exit()

        elif sys.argv[i] == '-t':
            try:
                tdelay = float(sys.argv[i + 1])
                cnt += 1
            except Exception:
                print("Wrong delay time!")
                exit()

        elif sys.argv[i] == '-w':
            try:
                _wr_en = int(sys.argv[i + 1])
                cnt += 1
            except Exception:
                print("Wrong wr_en!")
                exit()

        elif sys.argv[i] == '-h':
            help_func()
            exit()

        else:
            pass

    if (cnt > 1) and (cnt == ((N_arg - 1) >> 1)):
        print("Arguments commited")
    else:
        print("Arguments not commited"); exit()

else:  # if program has _no_ arguments in command line

    # !!!! UNCOMMENT ME  !!!!
    # input1 = input(">> Default settings? - yes=1, no=2, q=quit, h=help\n>>")  # /dev/ttyUSB0
    input1 = 1

    if (input1 == '2'):
        _port = input(">> Port: ")
        _baudrate = input(">> Baudrate: ")
        _N_TX = input(">> N_TX: ")
        try:
            N_TX = int(_N_TX)
        except Exception:
            print("Wrong! (default: N_TX=4)")
            N_TX = 4

    elif (input1 == 'q'):
        exit()

    elif (input1 == 'h'):
        help_func()
        exit()

    else:
        pass

    # !!!! UNCOMMENT ME  !!!!
    # in1 = input(">> Mode: HEX=1, DEC=2, SYMBOL=3, q=quit: ")
    in1 = 1

    mode = dict_mode.get(in1)
    if mode == None:
        mode = 'hex'
    if in1 == 'q':
        exit()


wr_en = _wr_en
# write rx data:
if wr_en == 1:
    t0 = time.localtime()
    date0 = '{:04d}{:02d}{:02d}'.format(t0.tm_year, t0.tm_mon, t0.tm_mday)
    time0 = '{:02d}:{:02d}:{:02d}'.format(t0.tm_hour, t0.tm_min, t0.tm_sec)
    filename = os.getcwd() + '/rxdata_' + date0 + '_' + time0 + '.txt'
    file1 = open(filename, 'w')
    print(filename, '\r\n')
    # file1.write("")


print('!!! Exit - Ctrl+Shift+C !!!')

# ----- Open serial port -------------- #

try:
    ser = serial.Serial(
        port=_port,  # '/dev/ttyUSB0', 'COM1'
        baudrate=_baudrate,
        # parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
except Exception:
    print('No such port!')
    exit()

if (ser.isOpen() == True):
    print("Port is already opened!")
else:
    try:
        ser.open()
    except Exception:
        print('Cannot open port!')
        exit()
    print("Port is open!")

print(ser.name)
n = ser.in_waiting
out = ser.read(n)  # first read???


# ----- Test ColorsName -> (R,G,B) -------------- #
for i in colors_def.systemColorsWin:
    icolor = colors_def.systemColorsWin.index(i)
    rgb16 = (0,0,0)
    rgb16 = gui.root.winfo_rgb(i)
    rgb8 = (rgb16[0]>>8, rgb16[1]>>8, rgb16[2]>>8)
    print(icolor, ") ", i, " rgb16: \"#{0:04X}{1:04X}{2:04X}\"".format(rgb16[0],rgb16[1],rgb16[2]), ", rgb8:  \"#{0:02X}{1:02X}{2:02X}\"".format(rgb8[0],rgb8[1],rgb8[2]))


# ----- Main Prog -------------- #
main()
exit("Exit")
