#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# Harpia REST API Interface
#--------------------------------------------------------------------------
# Copyright (c) 2018 Light Conversion (UAB MGF "Šviesos konversija")
# All rights reserved.
# www.lightcon.com
#==========================================================================

import urllib
import json
import time
from ..common import HTTP_methods

class WinTopas (HTTP_methods):
    silent = True
    connected = False
            
    def __init__ (self, ip_address, serial_number, port=8008, version='v0'):
        self.url = 'http://{}:{}/{}/{}/PublicAPI'.format(ip_address, port, serial_number, version)
            
        self.connected = True;
        if self.connected:
            print ('WinTopas System initialized at', self.url)
        
    def get_optical_system_data(self):
        return self._get(r'/Optical/WavelengthControl/OpticalSystemData')
    
    def set_wavelength(self, wavelength):
        self._put(r'/Optical/WavelengthControl/SetWavelengthUsingAnyInteraction', str(wavelength))
        
    def get_wavelength(self):
        return self._get(r'/Optical/WavelengthControl/Output/Wavelength')
    
    def get_output(self):
        return self._get(r'/Optical/WavelengthControl/Output')
    
    def finish_user_action(self):
        self._put(r'/Optical/WavelengthControl/FinishWavelengthSettingAfterUserActions', r'{"RestoreShutter" :false}')    
        