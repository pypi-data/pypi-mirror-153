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

class BeamAlignmentSystem(HTTP_methods):    
    silent = True
    connected = False
            
    def __init__ (self, ip_address, port=20050, version='v1'):
        self.url = 'http://{}:{}/{}/'.format(ip_address, port, version)        
        self.connected = True;
        if self.connected:
            print ('Beam Alignment System initialized at', self.url)
        
    #==============================================================================
    # /Basic
    #==============================================================================    
    def get_radius(self, system, quadrant):
        return self._get(str(system) + '/Quadrant/'+str(quadrant)+'/Radius')                
    
    def get_quadrant(self, system, quadrant):
        return self._get(str(system) + '/Quadrant/'+str(quadrant))
    
    def align_whole_system(self, system):
        self._post(str(system) + '/AlignSystem')
        
    def get_aligning(self, system):
        return self._get(str(system) + '/Aligning')
    
    def set_autoalign_on(self, system):
        self._put(str(system)+'/AutoAlign', '1')
        
    def set_autoalign_off(self, system):
        self._put(str(system)+'/AutoAlign', '0')
        
    def get_actuator_position(self, system, actuator):
        return {'X': self._get(str(system) +'/Actuator/'+str(actuator)+'/Position/X'),
                'Y': self._get(str(system) + '/Actuator/'+str(actuator)+'/Position/Y')}
        
    def set_actuator_position(self, system, actuator, x, y):
        self._post(str(system) + '/Actuator/'+str(actuator)+'/Position/'+str(x)+'/'+str(y))    