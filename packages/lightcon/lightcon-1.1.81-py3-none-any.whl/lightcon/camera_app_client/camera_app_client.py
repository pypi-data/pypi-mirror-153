#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# Harpia REST API Interface
#--------------------------------------------------------------------------
# Copyright (c) 2018 Light Conversion (UAB MGF "Šviesos konversija")
# All rights reserved.
# www.lightcon.com
#==========================================================================

from ..common import HTTP_methods

class CameraApp(HTTP_methods):
    silent = True
    connected = False
            
    def __init__ (self, ip_address, port=20042, version='v1'):
        self.url = 'http://{}:{}/{}/'.format(ip_address, port, version)
        if version == '':
            self.url = 'http://{}:{}/'.format(ip_address, port)
            
        self.connected = self._get('/') != {}
        if self.connected:
            print ('Camera App Service initialized at', self.url)
        
    #==============================================================================
    # /Basic
    #==============================================================================
        
    def get_beam_parameters(self):
        return self._get('/BeamProfiler/BeamParameters')
    
    def enable_beam_profiler(self):
        self._put('/BeamProfiler/IsEnabled', '1')

    def disable_beam_profiler(self):
        self._put('/BeamProfiler/IsEnabled', '0')
        
    def get_beam_profiler_status(self):
        return self._get('/BeamProfiler/IsEnabled')
    
    def set_beam_profiler_mode(self, mode=['ISO','GAUSS'][0]):
        self._put('/BeamProfiler/Mode', mode)
        
    def get_beam_profiler_mode(self):
        return self._get('/BeamProfiler/Mode')
        
    def get_camera_alldata(self, index = None):
        return self._get('/Camera/AllData')            
    
    def get_camera_exposure(self):
        return self._get('/Camera/Exposure')
    
    def set_camera_exposure(self, exposure_in_ms):
        self._put('/Camera/Exposure', str(exposure_in_ms))
        
    def get_camera_serial_number(self):
        return self._get('/Camera/SerialNumber')
    
    def get_camera_background(self):
        return self._get('/Camera/Background')
    
    def set_camera_averaging(self, avaraging):
        self._put('/Camera/Averaging', str(averaging))
        
    def get_camera_averaging(self):
        return self._get('/Camera/Averaging')
    
    def set_camera_gain(self, gain):
        self._put('/Camera/Gain', str(gain))
        
    def get_camera_gain(self):
        return self._get('/Camera/Gain')
    
    def get_camera_pixel_size(self):
        return self._get('/Camera/PixelSize')
    
    def get_camera_sensor_information(self):
        return self._get('/Camera/SensorInformation')

    
    
    
    