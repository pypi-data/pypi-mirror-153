#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# Laser Control REST API
#--------------------------------------------------------------------------
# Copyright (c) 2018-2022 Light Conversion (UAB MGF "Šviesos konversija")
# All rights reserved.
# www.lightcon.com
#==========================================================================

import time

from ..common.http_methods import HTTP_methods


class LaserClient (HTTP_methods):
    """Common laser control class for PHAROS and CARBIDE lasers."""

    silent = True
    connected = False

    def get_status(self):
        """Get laser status JSON."""
        endpoint_name = 'get_status'
        if (endpoint_name in self.endpoints):
            return self._get(self.endpoints[endpoint_name])
        else:
            return "Function not supported"

    def get_frequency(self):
        """Get output frequency (divided by PP) in kilohertz."""
        endpoint_name = 'get_frequency'
        if (endpoint_name in self.endpoints):
            return self._get(self.endpoints[endpoint_name])
        else:
            return "Function not supported"

    def get_pp(self):
        """Get PP divider."""
        endpoint_name = 'get_pp'
        if (endpoint_name in self.endpoints):
            return self._get(self.endpoints[endpoint_name])
        else:
            return "Function not supported"

    def set_pp(self, value, blocking=False):
        """Set PP divider."""
        endpoint_name = 'set_pp'
        if (endpoint_name in self.endpoints):
            self._put(self.endpoints[endpoint_name], str(value))
        else:
            return "Function not supported"

        if blocking:
            while self.get_pp() != value:
                time.sleep(0.2)

    def enable_output(self):
        """Enable laser output."""
        endpoint_name = 'enable_output'
        if (endpoint_name in self.endpoints):
            self._post(self.endpoints[endpoint_name])
        else:
            return "Function not supported"

    def close_output(self):
        """Disable laser output."""
        endpoint_name = 'close_output'
        if (endpoint_name in self.endpoints):
            self._post(self.endpoints[endpoint_name])
        else:
            return "Function not supported"

class Pharos (LaserClient):
    endpoints = {'get_status':      '/Basic',
                 'get_frequency':   '/Basic/ActualOutputFrequency',
                 'get_pp':          '/Basic/ActualPpDivider',
                 'set_pp':          '/Basic/TargetPpDivider',
                 'enable_output':   '/Basic/EnableOutput',
                 'close_output':    '/Basic/CloseOutput'}

    def __init__ (self, ip_address, port=20020, version='v1'):
        self.url = 'http://{}:{}/{}/'.format(ip_address, port, version)
        self.connected = self._get('Basic') != {}
        if self.connected:
            print ('Pharos initialized at', self.url)

class Carbide (LaserClient):
    """CARBIDE laser control class."""
    endpoints = {'get_status':      '/Basic',
                 'get_frequency':   '/Basic/ActualOutputFrequency',
                 'get_pp':          '/Basic/ActualPpDivider',
                 'set_pp':          '/Basic/TargetPpDivider',
                 'enable_output':   '/Basic/EnableOutput',
                 'close_output':    '/Basic/CloseOutput'}

    def __init__ (self, ip_address, port=20010, version='v1'):
        self.url = 'http://{}:{}/{}/'.format(ip_address, port, version)
        self.connected = self._get('Basic') != {}
        if self.connected:
            print ('Carbide initialized at', self.url)

class Flint (LaserClient):
    """FLINT laser control class.

    FLINT API is slightly different from PHAROS and CARBIDE, and therefore
    overloads more of the LaserClient base class functions.
    """
    endpoints = {'get_status':      '/Basic/GetStatus',
                 'turn_on':         '/Basic/TurnOn',
                 'turn_off':        '/Basic/TurnOff',
                 'goto_standby':    '/Basic/GoToStandby',
                 'main_get_status':   '/MainOutput/GetStatus',
                 'main_open_shutter':    '/MainOutput/OpenShutter',
                 'main_close_shutter':   '/MainOutput/CloseShutter',
                 'main_set_splitter_percentage': '/MainOutput/SetSplitterPercentage',
                 'main_set_target_output_power': '/MainOutput/SetTargetOutputPower',
                 'sec_get_status':   '/SecondaryOutput/GetStatus',
                 'sec_open_shutter': '/SecondaryOuptut/OpenShutter',
                 'sec_close_shutter': '/SecondaryOuptut/CloseShutter',
                 'sec_set_attenuator_percentage': '/SecondaryOutput/SetAttenuatorPercentage',
                 'sec_set_target_output_power': '/SecondaryOutput/SetTargetOutputPower',
                 'adv_get_available_features': '/Advanced/GetAvailableFeatures'}

    def __init__ (self, ip_address, port=11200, version='v0'):
        self.url = 'http://{}:{}'.format(ip_address, port)
        self.connected = self._get('/Basic/GetStatus') != {}

        features = self.get_available_features()['LaserFeatures']
        self.features = {}
        for key in features.keys():
            self.features[key] = features[key]

        if self.connected:
            print ('FLINT initialized at', self.url)

    def get_status(self, output=''):
        """Get laser status JSON.

        Output can be '', 'main', or 'sec'.
        """
        if output != '':
            output += '_'
        endpoint_name = output + 'get_status'
        if (endpoint_name in self.endpoints):
            return self._get(self.endpoints[endpoint_name])
        else:
            return "Function not supported"

    def get_available_features(self):
        """Get a list of features installed in the laser."""
        endpoint_name = 'adv_get_available_features'
        if (endpoint_name in self.endpoints):
            return self._get(self.endpoints[endpoint_name])
        else:
            return "Function not supported"

    def open_shutter(self, output='main'):
        """Open laser shutter.

        Output can be '', 'main' or 'sec'.
        """
        if output == 'main' and not self.features.get('HasMainOutput') or \
            output == 'sec' and not self.features.get('HasSecondaryOutput'):
                print("Shutter not installed")
                return False

        if output != '':
            output += '_'

        endpoint_name = output + 'open_shutter'
        if (endpoint_name in self.endpoints):
            self._post(self.endpoints[endpoint_name])
        else:
            return "Function not supported"

        return True

    def close_shutter(self, output='main'):
        """Close laser shutter.

        Output can be '', 'main' or 'sec'.
        """
        if output == 'main' and not self.features.get('HasMainOutput') or \
            output == 'sec' and not self.features.get('HasSecondaryOutput'):
                print("Shutter not installed")
                return False

        if output != '':
            output += '_'

        endpoint_name = output + 'close_shutter'
        if (endpoint_name in self.endpoints):
            self._post(self.endpoints[endpoint_name])
        else:
            return "Function not supported"

        return True

    def set_attenuator(self, val, output='main'):
        """Set output attenuator transmission in percentage.

        Output can be 'main' or 'sec'.
        NOTE: depending on laser model, there can be no attenuators, one or
            more installed. In some cases the output attenuator might be the
            secondary one, whereas the main one is used for beam division to
            different channales, e.g. for SPM.
        """
        if val < 0 or val > 100:
            print("Invalid value")
            return False

        if output == 'main':
            if not self.features.get('HasMainOutput'):
                print("Attenuator not installed")
                return True
            self._put(self.endpoints['main_set_splitter_percentage'])
        elif output == 'sec':
            if not self.features.get('HasSecondaryAttenuator'):
                print("Attenuator not installed")
                return False
            self._put(self.endpoints['sec_set_attenuator_percentage'])
        return True
