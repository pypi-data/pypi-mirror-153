# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 08:50:15 2020

@author: butkus
"""
import serial
import time
import struct
from lightcon.common.serial_tools import get_serial_ports

class TimingController:
    serial_port = None
    device_type = 'N/A'
    hardware_id = 'N/A'
    firmware_version = 'N/A'
    connected = False
    baud_rate = 1000000
        
    def __init__ (self):
        return
    
    def _is_device_supported(self, serial_port):
        try:
            self.serial_port = serial_port
            response = self._read_(b'?\r\n')
            print(response)
            response = response.decode()[:-2]
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
            response = self._read_(b'?\r\n')
            print(response)
            response = response.decode()[:-2]
        except:
            response = ''
        if response != '':
            elements = response.split(':')
            if len(elements) > 1 :
                self.device_type = str(elements[0])
                self.hardware_id = elements[1]
                if len(elements) > 2:
                    self.firmware_version = elements[2]
                else:
                    self.firmware_version = 'N/A'
                
                self.connected = True
                print ('Connected to {:} on {:} ({:}, firmware version: {:})'.format(self.device_type, self.serial_port, self.hardware_id, self.firmware_version))
                return
        
        print ('Could not connect to timing controller on {:}'.format(self.serial_port))
                        
    def _read_(self, message):
        '''For low-level serial messaging'''
        try:
            ser = serial.Serial(self.serial_port, baudrate=1000000)
        except serial.SerialException:
            return '\r\n'.encode()
        
        ser.write(message)
        
        time.sleep(0.1)
        response = ser.read(ser.in_waiting)
        
        ser.close()
        
        return response
        
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
        return self._read_(bytes('set:del {:} {:}\r\n'.format(channel,delay), 'utf-8'))
    
    def set_frequency(self, frequency):
        '''
        Sets internal frequency
        
        Parameters
        ----------
        frequency : number
            Frequency in Hz        
        '''
        return self._read_(bytes('set:freq {:}\r\n'.format(frequency), 'utf-8'))

    def get_delay(self, channel):
        return struct.unpack('i', self._read_(bytes('read:del {:}\r\n'.format(channel), 'utf-8'))[:-2])[0]
    
    def get_enabled(self, channel):
        return struct.unpack('i', self._read_(bytes('read:en {:}\r\n'.format(channel), 'utf-8'))[:-2])[0]
    
    def get_frequency(self):
        return struct.unpack('i', self._read_(bytes('read:freq\r\n', 'utf-8'))[:-2])[0]
    
    def get_trigger_source(self):
        return struct.unpack('i', self._read_(bytes('read:trig\r\n', 'utf-8'))[:-2])[0]
    
    def set_trigger_external(self):
        return self._read_(bytes('set:trig 1\r\n', 'utf-8'))
    
    def set_trigger_internal(self):
        return self._read_(bytes('set:trig 0\r\n', 'utf-8'))
    
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
        ser = serial.Serial(self.serial_port)
        ser.write(bytes('set:all {:}\r\n'.format(flag), 'utf-8'))
        
        to_read = n * 4
        while ser.in_waiting < to_read:
            time.sleep(0.01)
    
        ser.write(b'set:out 0\r\n')        
        buffer = ser.read(to_read)
        
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()        
        ser.close()
        
        delays = [struct.unpack('f', buffer[4*i:(4*i+4)])[0] for i in range(n)]
        
        return delays
    
if __name__ == '__main__':        
    tc = TimingController()
    tc.connect()
    
#    if tc.connected:
#        tc.set_trigger_internal()
#        print ('Trigger source', 'EXTERNAL' if tc.get_trigger_source() == 1 else 'INTERNAL {:} Hz'.format(tc.get_frequency()))
#        print ('\n'.join(['Channel {:}, delay {:} ns, {:}'.format(i, tc.get_delay(i), 'ENABLED' if tc.get_enabled(i)==1 else 'DISABLED') for i in [1,2,3,4]]))
#        
#        tc._read_(b'set:pulse 1 10000\r\n')
        