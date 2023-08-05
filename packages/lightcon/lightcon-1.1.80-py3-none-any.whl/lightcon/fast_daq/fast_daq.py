# -*- coding: utf-8 -*-
"""
=== Light Conversion FastDaq API ===

A DLL wrapper class to control the single-channel 2.5 MHz ADC FastDaq device.

Board information and theory of operation can be found:
    https://nova/display/HAR/Fast+Single-Channel+DAQ+Board+v2


Author: Vytautas Butkus, Lukas Kontenis
Contact: vytautas.butkus@lightcon.com, lukas.kontenis@lightcon.com
Copyright 2020 Light Conversion
"""

import clr   # pip install pythonnet
import numpy as np
import time

import os
dirname = os.path.dirname(__file__)
clr.AddReference(os.path.join(dirname, "LightConversion.Hardware.FastDaq.dll"))
clr.AddReference(os.path.join(dirname, "LightConversion.Abstractions.dll"))
clr.AddReference(os.path.join(dirname, "System.Threading.dll"))
clr.AddReference("mscorlib.dll")

from LightConversion.Hardware.FastDaq import FastDaq
from LightConversion.Abstractions import ClockChannel, SampleClockActiveEdge, \
    TriggerChannel, DaqException
from System.Threading import CancellationTokenSource, CancellationToken
from System import TimeoutException


class FastDaqWrapper:
    """Class to control FastDaq."""
    daq = None
    DaqException = DaqException
    TimeoutException = TimeoutException

    def __init__(self, device='Dev0', silent=False):
        """Connect to FastDaq device.

        Args:
            device (:obj:`str`): Device ID string  as returned by
                get_devices().
            silent (bool): Suppress message printing if true.
        """
        devices = FastDaq.Devices
        if device in devices:
            daq = FastDaq.LoadDevice(device)
            daq.Initialize()
            if daq.Connected:
                if not silent:
                    print("Initialized", device,
                          daq.Device.ProductType, daq.Device.SerialNumber)
                self.daq = daq
                time.sleep(0.1)
            return

        if not silent:
            print("FastDaq not found")

    def is_connected(self):
        """Check if connected to a FastDaq device.

        Returns:
            bool: True if connected, False otherwise.
        """
        return self.daq.Connected or False

    def set_timeout(self, timeout):
        """Set timeout in ms.

        Args:
            timeout (int): Timeout in milliseconds.
        """
        self.daq.AcquisitionTimeout = int(timeout)

    def configure_sample_clock(self, channel, active_edge):
        """Set ADC sample clock.

        Args:
            channel (:obj:`str`): Sample clock, 'internal' or 'PFI0'.
            active_edge (:obj:`str`): Active edge, 'rising' or 'falling'.
        """
        my_clock_channel = ClockChannel.Internal
        if channel == 'internal':
            my_clock_channel = ClockChannel.Internal
        elif channel == 'PFI0':
            my_clock_channel = ClockChannel.PFI0
        else:
            print("Invalid clock channel '{:s}'".format(channel))

        my_clock_active_edge = SampleClockActiveEdge.Rising
        if active_edge == 'rising':
            my_clock_active_edge = SampleClockActiveEdge.Rising
        elif active_edge == 'falling':
            my_clock_active_edge = SampleClockActiveEdge.Falling
        else:
            print("Invalid edge '{:s}'".format(channel))

        self.daq.ConfigureSampleClock(
            my_clock_channel, 2.5e6, my_clock_active_edge, 1000)

    def configure_start_trigger(self, channel):
        """Set ADC start trigger source.

        Args:
            channel (:obj:`str`): Trigger source, 'internal' or 'PFI0'.
        """
        my_trigger_channel = TriggerChannel.Internal
        if channel == 'internal':
            my_trigger_channel = TriggerChannel.Internal
        elif channel == 'PFI0':
            my_trigger_channel = TriggerChannel.PFI0
        else:
            print("Invalid start trigger souce '{:s}'".format(channel))

        self.daq.ConfigureStartTrigger(my_trigger_channel)

    def get_daq_data(self, n):
        """Acquire n ADC samples.

        A timeout will occur if the acquisition takes longer than the duration
        set by ``set_timeout``.

        Args:
            n (int): Number of samples to acquire.

        Returns:
            List of ADC samples in Volts.
        """
        self.daq.DatapointsPerChannel = n
        cts = CancellationTokenSource()
        ct = cts.Token

        data = self.daq.GetAnalogChannelsData(ct)
        data = [item for item in data]
        return data

    def set_external_trigger_delay(self, delay):
        """Set ADC sample clock delay in ns.

        Args:
            delay (int): Delay in nanoseconds.
        """
        self.daq.ExternalTriggerDelay = delay

    def close(self):
        self.daq.Dispose()


# === Helper functions ===

def list_fastdaq_devices(return_as_dict = False):

    """Get a list of available FastDaq devices.
    
    Args:
        return_as_dict (bool): Return device info dictionary or list of strings

    Returns:
        list: A list or dict (if return_as_dict==True) of available devices
    """
    devs = FastDaq.Devices
    if return_as_dict:
        return [{'device_name': dev, 'serial_number': item.Device.SerialNumber} for dev, item in [(dev, FastDaq.LoadDevice(dev)) for dev in devs]]
    else:
        return FastDaq.Devices

