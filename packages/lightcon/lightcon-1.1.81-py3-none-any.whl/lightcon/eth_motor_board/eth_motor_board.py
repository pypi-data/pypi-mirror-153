# -*- coding: utf-8 -*-
"""Light Conversion EthMotorBoard API.

A class to control motors connected to an EthMotorBoard.

Before using this API:
    - Set the static IP address of the EthMotorBoard using the DIP switch
        matrix on the PCB. All boards and any other devices in the LAN subnet
        must have unique IP addresses.
    - Connect the EthMotorBoard to an Ethernet port on the computer. A
        dedicated USB to Ethernet adapter is recommended.
    - Power up the EthMotorBoard.
    - Configure the Ethernet adapter to use a static IP address 10.1.1.x,
        where x is anything from 1 to 255.

A detailed description of the commands can be found:
    http://nova/display/HAR/EthMotorBoard

Authors: Vytautas Butkus, Lukas Kontenis
Contact: vytautas.butkus@lightcon.com, lukas.kontenis@lightcon.com
Copyright 2019-2021 Light Conversion
"""

import socket
import time
import string
import json

from ..common.leprecan_base import LepreCanBase

class EthMotorBoardCan:
    def __init__(self, emb):
        self.emb = emb
    
    def send(self, base_id, data):
        msb = (int.from_bytes(data, 'big') & 0xffffffff00000000) >> 32
        lsb = int.from_bytes(data, 'big') & 0xffffffff        
        message = "CAN_TRANSMIT {:} {:} {:}\r\n".format(base_id,  msb, lsb)
        # print ('>', base_id, data)
        self.received = self.emb.send(message)
        
    def receive(self):
        if (self.received):
            recv_array = [int(item) for item in self.received.split(' ')]
            base_id = recv_array[0]
            msb = recv_array[1]
            lsb = recv_array[2]
            bytes_array = [(msb >> 24) & 0xff,
                           (msb >> 16) & 0xff,
                           (msb >>  8) & 0xff,
                           (msb >>  0) & 0xff,
                           (lsb >> 24) & 0xff,
                           (lsb >> 16) & 0xff,
                           (lsb >>  8) & 0xff,
                           (lsb >>  0) & 0xff                           
                           ]
            # print('<', base_id, bytes_array)
            return bytes_array

class EthMotorBoard(LepreCanBase):
    """Class to control EthMotorBoards."""

    BUFFER_SIZE = 1024
    sock = None
    connected = False
    name = None
    timeout = 100
    fv = None
    ip_address = None
    max_position = 2**21-1
    
    reg_dict = { 'HardHiZ' : ('HIZ {:} HARD', 0x00A8),
                'AbsPos' : ('',0x0001),
                'Stop' : ('',0x00B8),
                'GoTo' : ('', 0x0060),
                'RunForward' : ('RUN {:} 0', 0x0051),
                'RunReverse' : ('RUN {:} 1', 0x0050),
                'Acc' : ('ACC', 0x0005), 
                 'Dec' : ('DEC', 0x0006),
                 'FnSlpAcc' : ('FN_SLP_ACC', 0x000F),
                 'FnSlpDec' : ('FN_SLP_DEC', 0x0010),
                 'IntSpeed' : ('INT_SPEED', 0x000D),
                 'KTherm' : ('K_THERM', 0x0011), 
                 'KvalAcc' : ('KVAL_ACC', 0x000B),
                 'KvalDec' : ('KVAL_DEC', 0x000C),
                 'KvalHold' : ('KVAL_HOLD', 0x0009),
                 'KvalRun' : ('KVAL_RUN', 0x000A),
                 'MaxSpeed' : ('MAX_SPEED', 0x0007),
                 'MinSpeed' : ('MIN_SPEED', 0x0008),
                 'OcdTh' : ('OCD_TH', 0x0013),
                 'StSlp' : ('ST_SLP', 0x000E),
                 'StallTh' : ('STALL_TH', 0x0014),
                 'StepMode' : ('STEP_MODE', 0x0016),
                 'LSStatus': ('', 0x0100),
                 'LSEnable': ('', 0x0103)}

    status_registers = [
        (0x01, 0x01, 'HiZ'), (0x02, 0x0, 'BUSY'), (0x04, 0x04, 'SW_F'),
        (0x08, 0x08, 'SW_ENV'), (0x60, 0x00, 'Stopped'),
        (0x60, 0x20, 'Acceleration'), (0x60, 0x40, 'Deceleration'),
        (0x60, 0x60, 'Constant speed'), (0x80, 0x80, 'NOTPERF_CMD'),
        (0x100, 0x100, 'WRONG_CMD'), (0x200, 0x0, 'OVLO'),
        (0x400, 0x0, 'TH_WRN'), (0x800, 0x0, 'TH_SD'), (0x1000, 0x0, 'OCD'),
        (0x2000, 0x0, 'STEP_LOSS_A'), (0x4000, 0x0, 'STEP_LOSS_B'),
        (0x8000, 0x8000, 'SCK_MOD')]

    ls_registers = [
        (0x01, 0x01, 'Left LS reached'), (0x02, 0x02, 'Right LS reached')]

    def __init__(self, ip_address='10.1.1.0'):
        """Create an EthMotorBoard control instance."""
        self.ip_address = ip_address

        self.name = self.send('GET BOARD_NAME')
        self.fv = self.send('FIRMWARE_VERSION')

        self.connected = self.fv is not None

        if self.connected:
            print('Successfullly connected to EthMotorBoard, name: {:}, '.format(self.name)
                  + 'firmware version: {:}'.format(self.fv))
        
            self.can_service = EthMotorBoardCan(self)            
            
        else:
            print('Motor board not found at {:}'.format(self.ip_address))

    def setup_motor(self, index, file_name):                
        try:
            with open(file_name, 'r') as f:
                motor_info = json.loads(f.read())            
                
        except FileNotFoundError:
            print ('Configuration not found')
            return        
    
        response = self.send(self.reg_dict['HardHiZ'][0].format(1 << index))
        time.sleep(1)    
        
        for key in motor_info.keys():
            if self.reg_dict.get(key):
                
                response = self.send('SET ' + self.reg_dict[key][0], [index, motor_info[key]])
                print ('<', response, 'for', key)
                
    def send(self, message, args=None):
        """Send a command to the board and get a response.

        TODO: This should probably be called a querry.
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout/1000)
            self.sock.connect((self.ip_address, 80))

            if args is None:
                self.sock.send((str(message)+'\r\n').encode('UTF-8'))
            else:
                self.sock.send((
                    str(message) + ' '
                    + ' '.join([str(arg) for arg in args])
                    + '\r\n').encode('UTF-8'))

            data = self.sock.recv(self.BUFFER_SIZE)
            self.sock.close()
            return data[:-2].decode()
        except socket.timeout:
            return None

    def get_status(self, motor_index=0):
        """Get board status."""
        status = int(self.send('GET STATUS', [motor_index]))
        ls_result = self.send('GET LIMIT_SWITCH', [motor_index])
        ls_status = eval(ls_result)['Logical']
        return [stat for mask, val, stat in self.status_registers
                if status & mask == val] \
            + [stat for mask, val, stat in self.ls_registers
                if ls_status & mask == val]

    def wait_until_stopped(self, motor_index=0):
        """Wait until motor stops."""
        repeat = True
        while repeat:
            status = self.send('GET STATUS ' + str(motor_index))
            repeat = int(status) & 0x60 != 0
            time.sleep(0.05)

    def get_abs_pos(self, motor_index=0):
        """Get motor absolute position in steps."""
        return self.send('GET ABS_POS ' + str(motor_index))

    def move_rel(self, motor_index=0, move_dir=0, pos_delta=0):
        """Move motor a given distance from the current position."""
        ret_code = self.send('MOVE {:d} {:d} {:d}'.format(
            motor_index, move_dir, pos_delta))

        self.check_error(ret_code)

    def move_abs(self, motor_index=0, abs_pos=0):
        """Move motor to an absolute position."""
        ret_code = self.send('GOTO {:d} {:d}'.format(motor_index, abs_pos))
        self.check_error(ret_code)

    def check_error(self, ret_code):
        """Check the return value.

        'ERR0' means that everything is fine. 'ERR4' means that a limit switch
        has been reached. These two codes can be ignored in most cases.
        Anything else indicates an error.
        """
        ret_code = strip_whitespace(ret_code)

        if ret_code not in ['ERR0', 'ERR4']:
            print("Error: " + ret_code)

    def reset_motor(self, motor_index=0, move_dir=0, speed=10000):
        """Reset motor and set current position to 0.

        Move motor in the given direction until a limit switch has been
        reached and set the current position there to 0.
        """
        ret_code = self.send('RUN {:d} {:d} {:d}'.format(
            motor_index, move_dir, speed))

        self.check_error(ret_code)
        self.wait_until_stopped(motor_index)
        ret_code = self.send('RESET_POS {:d}'.format(motor_index))
        self.check_error(ret_code)


# === Helper functions ===

def strip_whitespace(s):
    """Strip whitespace from a string."""
    return s.translate(str.maketrans('', '', string.whitespace))
