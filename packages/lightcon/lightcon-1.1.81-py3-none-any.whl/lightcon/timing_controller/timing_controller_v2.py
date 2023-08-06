# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 08:50:15 2020

@author: butkus
"""
import serial
import time
import struct
from lightcon.common.serial_tools import get_serial_ports

class TimingControllerV2:
    serial_port = None
    device_type = 'N/A'
    hardware_id = 'N/A'
    firmware_version = 'N/A'
    connected = False
    baud_rate = 1000000
    ser = None
        
    def __init__ (self):
        return
    
    def __dispose__ (self):
        if self.ser:
            self.ser.close()
    
    def _is_device_supported(self, serial_port):
        try:
            self.serial_port = serial_port
            response = self._read_(b'?\n')
            self.ser.close()
            self.ser = None
            response = response.decode()[:-1].replace('\r', '').replace('\n','')
        except:
            response = ''
        return [response != '', response]      
        
    
    def connect(self, serial_port = None, index = None):
        if serial_port is None:
            ports = get_serial_ports()
            supported_devices = [[port] + self._is_device_supported(port) for port in ports]
            supported_devices  = [tuple(dev) for dev in supported_devices if dev[1]]
            if len(supported_devices) == 1:
                self.serial_port = supported_devices[0][0]
            elif len(supported_devices) > 1:
                if index is None:
                    print ('Multiple supported devices found: \n' + '\n'.join('\t'.join([str(i), entry[0], entry[2]]) for i, entry in enumerate(supported_devices)))
                    print ('Invoke function with the correspondindg index value')
                else:
                    self.serial_port = supported_devices[index][0]
            else:
                print ('No supported devices found on serial bus')
                return
        else:
            self.serial_port = serial_port
        
        try:
            response = self._read_(b'?\n')
            response = response.decode()[:-1].replace('\r', '').replace('\n','')
        except:
            response = ''
        if response != '':
            elements = response.split(':')
            if len(elements) == 3:
                self.device_type = str(elements[0])
                self.hardware_id = elements[1]
                self.firmware_version = elements[2]
                
                self.connected = True
                print ('Connected to {:} on {:} ({:}, firmware version: {:})'.format(self.device_type, self.serial_port, self.hardware_id, self.firmware_version))
                return
        
        print ('Could not connect to timing controller on {:}'.format(self.serial_port))
                        
    def _read_(self, message):
        '''For low-level serial messaging'''
        try:
            if self.ser == None:
                self.ser = serial.Serial(self.serial_port, baudrate=1000000)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()      
        except serial.SerialException:
            return '\n'.encode()
        
        self.ser.write(message)
        
        cnt = 0
        while self.ser.in_waiting == 0 and cnt < 20:
            cnt = cnt + 1
            time.sleep(0.01)
            
        response = self.ser.read(self.ser.in_waiting)
        
        
        
        return response
        
    def _write_(self, message):
        '''For low-level serial messaging'''
        try:
            if self.ser == None:
                self.ser = serial.Serial(self.serial_port, baudrate=1000000)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()      
        except serial.SerialException:
            return '\n'.encode()
        
        self.ser.write(message)        
    
    def set_delay(self, channel, delay):
        '''
        Sets delay of given channel
        
        Parameters
        ----------
        channel : number
            Channel 0-3
        delay : nubmer
            Delay value in nanoseconds
        '''
        return self._read_(bytes('set:del {:} {:}\n'.format(channel,delay), 'utf-8'))
        

    def get_delay(self, channel):
        return int(self._read_(bytes('get:del {:}\n'.format(channel), 'utf-8'))[:-1].decode())
    
    def get_output(self):
        return int(self._read_(bytes('get:output\n', 'utf-8'))[:-1].decode())
    
    def set_output(self, output):
        self._write_(bytes('set:output {:}\n'.format(output), 'utf-8'))
    
    def get_enabled(self, channel):
        output_status = self.get_output()
        flag = 1 << channel
        return output_status & flag != 0
    
    def enable_channel(self, channel):
        output_status = self.get_output()
        output = output_status | (1 << channel)
        self.set_output(output)
        
    def disable_channel(self, channel):
        output_status = self.get_output()
        output = output_status - (output_status & (1 << channel))
        self.set_output(output)
        
    def set_master_delay(self, delay):
        self._write_(bytes('set:masterdel {:}\n'.format(delay), 'utf-8'))
        
    def get_master_delay(self):
        return int(self._read_(bytes('get:masterdel\n', 'utf-8'))[:-1].decode())

    def get_master_frequency(self):
        return int(self._read_(bytes('get:extfreq\n', 'utf-8'))[:-1].decode())
            
    def read_stopwatch(self, n, flag = 62):
        '''
        Reads stopwatch values
        
        Parameters
        ----------
        n : number
            Number of start-stop events to capture
        flag : number
            Channel enabling flag
                bit0: no effect, trigger output cannot be turned off
                bit1: delay 1a control
                bit2: delay 1b control
                bit3: delay 2 control
                bit4: delay 3 control
                bit5: stopwatch arming control
        Returns
        -------
        delays : array(number)
            Array of timing values in microseconds
        '''
        if self.ser == None:
            self.ser = serial.Serial(self.serial_port, baudrate=1000000)
        self.ser.write(b'tdc:out 1\n')
        self.ser.write(bytes('set:output {:}\n'.format(flag), 'utf-8'))
        
        to_read = n * 4
        cnt = 0
        while self.ser.in_waiting < to_read:
            cnt = cnt+1
            if cnt > 100:
                print("TIMEOUT", self.ser.in_waiting, self.ser.read(self.ser.in_waiting))
                return
            time.sleep(0.01)
    
        self.ser.write(b'set:output 8\n')
        self.ser.write(b'tdc:out 0\n')        
        
        time.sleep(0.03)
        
        buffer = self.ser.read(to_read)
        
#        self.ser.close()
        
        delays = [struct.unpack('f', buffer[4*i:(4*i+4)])[0] for i in range(n)]
        print(buffer.hex())
        return delays
#    
if __name__ == '__main__':        
    tc = TimingControllerV2()
    tc.connect()
    out = tc.read_stopwatch(10)
    print(out)
    tc.__dispose__()
