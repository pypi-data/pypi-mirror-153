# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 15:47:29 2020

@author: butkus
"""

import struct

def float_to_hex(f):
    return int(struct.unpack('<I', struct.pack('<f', f))[0])

def hex_to_float(f):
    return float(struct.unpack('<f', struct.pack('<I', f))[0])

def bytes_array_to_int (data):
    result = 0
 
    for i, val in enumerate(data):
        result = result + (val << (i * 8))
                                 
    return result