#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# Harpia DAQ DLL Wrapper
#--------------------------------------------------------------------------
# Copyright (c) 2020 Light Conversion, UAB
# All rights reserved.
# www.lightcon.com
#==========================================================================

import clr   # pip install pythonnet
import numpy as np
import time

import os
dirname = os.path.dirname(__file__)
clr.AddReference(os.path.join(dirname, "LightConversion.Hardware.HarpiaDaq.dll"))
clr.AddReference(os.path.join(dirname, "LightConversion.Abstractions.dll"))
clr.AddReference(os.path.join(dirname, "System.Threading.dll"))
clr.AddReference("mscorlib.dll")

from LightConversion.Hardware.HarpiaDaq import HarpiaDaq
from LightConversion.Abstractions import ClockChannel, SampleClockActiveEdge, TriggerChannel, DaqException
from System.Threading import CancellationTokenSource, CancellationToken
from System import TimeoutException

class HarpiaDaqWrapper:
    daq = None
    DaqException = DaqException
    TimeoutException = TimeoutException
    def __init__(self):
        devices = HarpiaDaq.Devices
        if len(devices) > 0:
            daq = HarpiaDaq.LoadDevice(devices[0])
            is_sync = ('SDAQ' in daq.Device.ProductType.upper()) or ('SDAQ' in daq.Device.SerialNumber.upper())
            daq.Initialize(is_sync)

            if daq.Connected:
                print ("Initialized", daq.Device.ProductType, daq.Device.SerialNumber)            
                self.daq = daq
                time.sleep(1)
        else:
            print ("Harpia DAQ not found")

    def is_connected(self):
        return self.daq.Connected or False
    
    def enable_channels(self, channels):
        '''
        Enables analog input channels of ADC
        
        Parameters
        ----------
        channels : list
            List of strings, for example ['AI0', 'AI1']
        '''
        self.daq.EnableAIChannels(';'.join(channels))
        
    def set_timeout(self, timeout):
        '''
        Sets timeout in milliseconds
        
        Parameters
        ----------
        timeout : number
            Timeout value, given in milliseconds
        '''
        self.daq.AcquisitionTimeout = int(timeout)
        
    def configure_sample_clock(self, channel, active_edge):
        '''
        Configures clock for ADC acquisition
        
        Parameters
        ----------
        channel : str
            'internal', 'PFI0', 'PFI1', 'PFI2', 'PFI3', 'PFI4' or 'PFI5'
        active_edge : str
            'rising' or 'falling'        
        '''
        my_clock_channel = ClockChannel.Internal
        if (channel == 'internal'):
            my_clock_channel = ClockChannel.Internal
        elif ((channel == 'PFI0')):
            my_clock_channel = ClockChannel.PFI0
        elif ((channel == 'PFI1')):
            my_clock_channel = ClockChannel.PFI1
        elif ((channel == 'PFI2')):
            my_clock_channel = ClockChannel.PFI2
        elif ((channel == 'PFI3')):
            my_clock_channel = ClockChannel.PFI3
        elif ((channel == 'PFI4')):
            my_clock_channel = ClockChannel.PFI4
        elif ((channel == 'PFI5')):
            my_clock_channel = ClockChannel.PFI5
        elif ((channel == 'PFI6')):
            my_clock_channel = ClockChannel.PFI6
            
        my_clock_active_edge = SampleClockActiveEdge.Rising
        if (active_edge == 'rising'):
            my_clock_active_edge = SampleClockActiveEdge.Rising
        else:
            my_clock_active_edge = SampleClockActiveEdge.Falling            
            
        self.daq.ConfigureSampleClock(my_clock_channel, 0.8e6, my_clock_active_edge, 1000)
            
    def configure_start_trigger(self, channel):
        '''
        Configures trigger for ADC acquisition
        
        Parameters
        ----------
        channel : str
            'internal', 'PFI0', 'PFI1', 'PFI2', 'PFI3', 'PFI4' or 'PFI5'
        '''
        my_trigger_channel = TriggerChannel.Internal
        if (channel == 'internal'):
            my_trigger_channel = TriggerChannel.Internal
        elif ((channel == 'PFI0')):
            my_trigger_channel = TriggerChannel.PFI0
        elif ((channel == 'PFI1')):
            my_trigger_channel = TriggerChannel.PFI1
        elif ((channel == 'PFI2')):
            my_trigger_channel = TriggerChannel.PFI2
        elif ((channel == 'PFI3')):
            my_trigger_channel = TriggerChannel.PFI3
        elif ((channel == 'PFI4')):
            my_trigger_channel = TriggerChannel.PFI4
        elif ((channel == 'PFI5')):
            my_trigger_channel = TriggerChannel.PFI5
        elif ((channel == 'PFI6')):
            my_trigger_channel = TriggerChannel.PFI6
        
        self.daq.ConfigureStartTrigger(my_trigger_channel)

    def get_daq_data(self, n):
        '''
        Acquires n samples per enabled channel.
        
        Parameters
        ----------
        n : number
            Number of datapoints to acquire per channel
        
        Returns
        -------
        list (m,n):
            Values in volts, where m is number of enabled channels (in ascending order)
        '''
        self.daq.DatapointsPerChannel = n
        cts = CancellationTokenSource()
        ct = cts.Token

        data = self.daq.GetAnalogChannelsData(ct, True)
        data = [item for item in data]
        return np.reshape(data, (int(len(data)/n), n), order='C')
    
    def close(self):
        self.daq.Dispose()



