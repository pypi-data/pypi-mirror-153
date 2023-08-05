#!/usr/bin/env python3
#==========================================================================
# (c) 2011-2019  Total Phase, Inc.
#--------------------------------------------------------------------------
# Project : Komodo Examples
# File    : loopback.py
#--------------------------------------------------------------------------
# Demonstrates how to open ports, acquire features, write and read data.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#========================================================================*/

#==========================================================================
# IMPORTS
#========================================================================*/
from __future__ import division, with_statement, print_function
from .komodo_py import *

class Komodo:
    port = 0
    timeout = 1000 #ms
    bitrate = 1000000 #Hz
    
    def __init__ (self, port = 0, timeout = 1000, bitrate = 1000000):
        self.port = port
        self.timeout = timeout
        self.bitrate = bitrate
    
    def connect(self):
        # Connect to and configure
        self.kma = km_open(self.port)
        
        # Setup CAN channel A for writing and B for listening
        reta = km_acquire(self.kma, KM_FEATURE_CAN_A_CONFIG  |
                               KM_FEATURE_CAN_A_CONTROL |
                               KM_FEATURE_CAN_A_LISTEN)
        
        # Set bitrate
        reta = km_can_bitrate(self.kma, KM_CAN_CH_A, self.bitrate)
        
        # Set timeout
        km_timeout(self.kma, self.timeout)
        
        # Set target power
        km_can_target_power(self.kma, KM_CAN_CH_A, KM_TARGET_POWER_ON)
        
        km_enable(self.kma)

    def close(self):
        km_disable(self.kma)
        km_can_target_power(self.kma, KM_CAN_CH_A, KM_TARGET_POWER_OFF)
    
        # Close and exit
        km_close(self.kma)
    
    def send(self, can_id, data):
        info      = km_can_info_t()
        data_out  = array('B', data)
        data_in   = array('B', [0]*len(data_out))
        
        pkt       = km_can_packet_t()
        pkt.dlc   = len(data_out)
        pkt.id    = can_id
        
        km_can_write(self.kma, KM_CAN_CH_A, 0, pkt, data_out)
    
    def receive(self):
        data_in = array('B', [0]*8)
        ret = 0
        while(ret == 0):
            (ret, info, pkt, data_in) = km_can_read(self.kma, data_in)
            
        return list(data_in)
##==========================================================================
## MAIN PROGRAM
##==========================================================================
#base_id = 0x190
#
#komodo_open()
#
##komodo_send(base_id + 5, [0x01, 0x02, 0x03, 0, 0, 5, 0, 0])
#
#komodo_send(base_id + 6, [0x01, 0x00, 0x00, 0, 0, 0, 0, 0])
#
#print(komodo_receive())
#
#
#komodo_close()
#
#
#
#
#


