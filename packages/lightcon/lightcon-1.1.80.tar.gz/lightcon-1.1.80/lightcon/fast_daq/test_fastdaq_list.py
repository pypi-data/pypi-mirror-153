# -*- coding: utf-8 -*-
"""
=== Light Conversion FastDaq API ===

Example: list connected FastDaq devices.

Author: Vytautas Butkus, Lukas Kontenis
Contact: vytautas.butkus@lightcon.com, lukas.kontenis@lightcon.com
Copyright 2019-2020 Light Conversion
"""
import time
from lightcon.fast_daq import FastDaqWrapper, list_fastdaq_devices

print("Listing fastdaq devices...")
start_t = time.time()

device_info = list_fastdaq_devices(True)
print("Num fastdaq endpoints: {:d}".format(len(device_info)))

print("ID\tName\tSerial")
for ind, info in enumerate(device_info):
    try:
        print("{:d}:\t{:s}\t{:s}".format(ind, info['device_name'], info['serial_number']))
    except Exception:
        print("{:d}:\t{:s}\t{:s}".format(ind, info, 'Not a fastdaq'))

print("Test completed in {:.1f} s".format(time.time() - start_t))
