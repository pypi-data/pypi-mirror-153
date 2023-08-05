#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# Harpia REST API Interface
#--------------------------------------------------------------------------
# Copyright (c) 2018 Light Conversion (UAB MGF "Šviesos konversija")
# All rights reserved.
# www.lightcon.com
#==========================================================================

import json
import socket
from ..common.http_methods import HTTP_methods
    
class Harpia (HTTP_methods):
    """REST API interaction logic with Harpia spectrometer"""
    
    silent = True
    connected = False
            
    def __init__ (self, ip_address, port=20050, version='v1'):
        self.url = 'http://{}:{}/{}/'.format(ip_address, port, version)        
        self.connected = self._get('Basic') != {}
        if self.connected:
            print ('Harpia initialized at', self.url)
        
    #==============================================================================
    # /Basic
    #==============================================================================
    
    def reload_factory_defaults(self):
        self._post('Basic/ReloadFactoryDefaults')

    def pump_probe_signal(self, close_shutters = True, target_delay = None):
        query = 'Basic/PumpProbeSpectrum/' + str(close_shutters).lower() 
        if target_delay != None:
            query = query + '/' + str(target_delay)            
        return self._get(query)
    
    def background_raw_signal(self):
        return self._get('Basic/BackgroundRawSignal')
    
    def raw_signal(self):
        return self._get('Basic/RawSignal')

    def spectra_per_acquisition(self):
        return self._get('Basic/NumberOfSpectraPerAcquisition')
    
    def set_spectra_per_acquisition(self, number):
        self._put('Basic/NumberOfSpectraPerAcquisition', str(number))
        
    def datapoints_per_spectrum(self):
        return self._get('Basic/DatapointsPerSpectrum')
    
    def wavelength_axis(self):
        return self._get('Basic/WavelengthAxis')    
    
    def laser_frequency(self):
        return self._get('Basic/LaserFrequency')

    #==============================================================================
    # /Detectors
    #==============================================================================
    
    def available_detectors(self):
        return self._get('Detectors/AvailableDetectors')
    
    def current_detector(self):
        return self._get('Detectors/CurrentDetector')
    
    def set_current_detector(self, detector_number):
        self._put('Detectors/CurrentDetector', str(detector_number))

    #==============================================================================
    # /Shutters
    #==============================================================================
    def open_pump_shutter(self):
        self._post('Shutters/OpenPumpShutter')
        
    def close_pump_shutter(self):
        self._post('Shutters/ClosePumpShutter')
                    
    def open_probe_shutter(self):
        self._post('Shutters/OpenProbeShutter')
        
    def close_probe_shutter(self):
        self._post('Shutters/CloseProbeShutter')
        
    def open_gate_shutter(self):
        self._post('Shutters/OpenGateShutter')
        
    def close_gate_shutter(self):
        self._post('Shutters/OpenGateShutter')
        
    def open_third_beam_shutter(self):
        self._post('Shutters/OpenThirdBeamShutter')
        
    def close_pump_open_probe_shutters(self):
        self._post('Shutters/ClosePumpOpenProbeShutters')
        
    def open_pump_close_probe_shutters(self):
        self._post('Shutters/OpenPumpCloseProbeShutters')
        
    def open_all_shutters(self):
        self._post('Shutters/OpenAllShutters')
        
    def close_all_shutters(self):
        self._post('Shutters/CloseAllShutters')
        
        
    #==============================================================================
    # /Chopper
    #==============================================================================
        
    def chopper_is_on(self):
        return self._get('Chopper/IsOn')
    
    def chopper_start(self):
        self._post('Chopper/Start')
    
    def chopper_stop(self):
        self._post('Chopper/Stop')
    
    def chopper_is_locked(self):
        return self._get('Chopper/IsLocked')
    
    def chopper_clock_source(self):
        return self._get('Chopper/ClockSource')
    
    def set_chopper_clock_source_internal(self):
        self._put('Chopper/ClockSource', '\"internal\"')
        
    def set_chopper_clock_source_external(self):
        self._put('Chopper/ClockSource', '\"external\"')

    def chopper_clock_divider(self):
        return self._get('Chopper/ClockDivider')
    
    def set_chopper_clock_divider(self, divider):
        self._put('Chopper/ClockDivider', str(divider))
        
    def chopper_actual_frequency(self):
        return self._get('Chopper/ActualFrequency')
    
    def chopper_target_frequency(self):
        return self._get('Chopper/ActualFrequency')
    
    def set_chopper_target_frequency(self, frequency):
        self._put('Chopper/TargetFrequency', str(frequency))
        
    def chopper_phase_error(self):
        return self._get('Chopper/PhaseError')
        
    def chopper_target_phase(self):
        return self._get('Chopper/TargetPhase')
    
    def set_chopper_target_phase(self, phase):
        self._put('Chopper/TargetPhase', str(phase))
        
    #==============================================================================
    # /DelayLine 
    #==============================================================================
    
    def delay_line_actual_delay(self):
        return self._get('DelayLine/ActualDelay')
    
    def delay_line_target_delay(self):
        return self._get('DelayLine/TargetDelay')    
        
    def set_delay_line_target_delay(self, delay):
        self._put('DelayLine/TargetDelay', str(delay))
    
    def delay_line_actual_distance(self):
        return self._get('DelayLine/ActualDistance')
        
    def set_delay_line_target_distance(self, distance):
        self._put('DelayLine/TargetDistance', str(distance))
        
    def set_delay_line_target_distance(self, distance):
        self._put('DelayLine/TargetDistance', str(distance))
        
    def delay_line_go_to_zero(self):
        self._post('DelayLine/GoToZero')
        
    def delay_line_set_as_zero(self):
        self._post('DelayLine/SetAsZero')

    #==============================================================================
    # /CrystalRotator
    #==============================================================================
    
    def crystal_rotator_is_moving(self):
        return self._get('CrystalRotator/IsMoving')
        
    def crystal_rotator_start(self):
        self._post('CrystalRotator/Start')

    def crystal_rotator_stop(self):
        self._post('CrystalRotator/Stop')

    #==============================================================================
    # /SampleMover
    #==============================================================================

    def sample_mover_go_to_zero(self):
        self._post('SampleMover/GoToZero')
        
    def sample_mover_go_to_xy_and_wait_for_stop(self, x, y):
        query = 'SampleMover/GoToXYAndWaitForStop/' + str(x) + '/' + str(y)            
        self._post(query)

    def set_sample_mover_velocity(self, velocity):
        self.put('SampleMover/Velocity', str(velocity))
        
    def sample_mover_velocity(self):
        return self._get('SampleMover/Velocity')
    
    
    #==============================================================================
    # /MotorizedSpectrograph    
    #==============================================================================
    
    def motorized_spectrograph_wavelength(self):
        return self._get('MotorizedSpectrograph/Wavelength')
        
    def set_motorized_spectrograph_wavelength(self, wavelength):
        self._put('MotorizedSpectrograph/Wavelength', str(wavelength))

    def motorized_spectrograph_output_port(self):
        return self._get('MotorizedSpectrograph/OutputPort')
        
    def set_motorized_spectrograph_output_port(self, port):
        self._put('MotorizedSpectrograph/OutputPort', port)
    
    def motorized_spectrograph_detector_offset(self):
        return self._get('MotorizedSpectrograph/DetectorOffset')
        
    def set_motorized_spectrograph_detector_offset(self, offset):
        self._put('MotorizedSpectrograph/DetectorOffset', str(offset))

    def motorized_spectrograph_grating_offset(self):
        return self._get('MotorizedSpectrograph/GratingOffset')
        
    def set_motorized_spectrograph_grating_offset(self, offset):
        self._put('MotorizedSpectrograph/GratingOffset', str(offset))
        
    def motorized_spectrograph_focus(self):
        return self._get('MotorizedSpectrograph/Focus')
        
    def set_motorized_spectrograph_focus(self, focus):
        self._put('MotorizedSpectrograph/Focus', str(focus))

    def motorized_spectrograph_gratings_info(self):
        return self._get('MotorizedSpectrograph/GratingsInfo')

    def motorized_spectrograph_grating(self):
        return self._get('MotorizedSpectrograph/Grating')
        
    def set_motorized_spectrograph_grating(self, grating):
        self._put('MotorizedSpectrograph/Grating', str(grating))
        
    #==============================================================================
    # /BerekRotator
    #==============================================================================
    
    def berek_rotator_go_to_zero(self):
        self._post('BerekRotator/GoToZero')
        
    def berek_rotator_actual_rotate_angle(self):
        return self._get('BerekRotator/ActualRotateAngle')
    
    def berek_rotator_actual_tilt_angle(self):
        return self._get('BerekRotator/ActualTiltAngle')
    
    def set_berek_rotator_target_rotate_angle(self, angle):
        self._put('BerekRotator/TargetRotateAngle', str(angle))
        
    def set_berek_rotator_target_tilt_angle(self, angle):
        self._put('BerekRotator/TargetTiltAngle', str(angle))        
    
    #==============================================================================
    # /PumpMotorizedVNDF
    #==============================================================================
    
    def pump_vndf_start_tune(self):
        self._post('PumpMotorizedVNDF/StartTune')
    
    def pump_vndf_stop_tune(self):
        self._post('PumpMotorizedVNDF/StopTune')
        
    def pump_vndf_go_by_percent(self, percent):
        self._post('PumpMotorizedVNDF/GoByPercent/' + str(percent))
        
    def pump_vndf_go_to_zero(self):
        self._post('PumpMotorizedVNDF/GoToZero')
        
    def pump_vndf_angle(self):
        return self._get('PumpMotorizedVNDF/Angle')
    
    def set_pump_vndf_angle(self, angle):
        self._put('PumpMotorizedVNDF/Angle', str(angle))

    def pump_vndf_transmittance(self):
        return self._get('PumpMotorizedVNDF/Transmittance')
    
    def set_pump_vndf_transmittance(self, transmittance):
        self._put('PumpMotorizedVNDF/Transmittance', str(transmittance))

    #==============================================================================
    # /ProbeMotorizedVNDF
    #==============================================================================
    
    def probe_vndf_start_tune(self):
        self._post('ProbeMotorizedVNDF/StartTune')
    
    def probe_vndf_stop_tune(self):
        self._post('ProbeMotorizedVNDF/StopTune')
        
    def probe_vndf_go_by_percent(self, percent):
        self._post('ProbeMotorizedVNDF/GoByPercent/' + str(percent))
        
    def probe_vndf_go_to_zero(self):
        self._post('ProbeMotorizedVNDF/GoToZero')
        
    def probe_vndf_angle(self):
        return self._get('ProbeMotorizedVNDF/Angle')
    
    def set_probe_vndf_angle(self, angle):
        self._put('ProbeMotorizedVNDF/Angle', str(angle))

    def probe_vndf_transmittance(self):
        return self._get('ProbeMotorizedVNDF/Transmittance')
    
    def set_probe_vndf_transmittance(self, transmittance):
        self._put('ProbeMotorizedVNDF/Transmittance', str(transmittance))

    #==============================================================================
    # /DetectorMotorizedVNDF
    #==============================================================================
    
    def detector_vndf_start_tune(self):
        self._post('DetectorMotorizedVNDF/StartTune')
    
    def detector_vndf_stop_tune(self):
        self._post('DetectorMotorizedVNDF/StopTune')
        
    def detector_vndf_go_by_percent(self, percent):
        self._post('DetectorMotorizedVNDF/GoByPercent/' + str(percent))
        
    def detector_vndf_go_to_zero(self):
        self._post('DetectorMotorizedVNDF/GoToZero')
        
    def detector_vndf_angle(self):
        return self._get('DetectorMotorizedVNDF/Angle')
    
    def set_detector_vndf_angle(self, angle):
        self._put('DetectorMotorizedVNDF/Angle', str(angle))

    def detector_vndf_transmittance(self):
        return self._get('DetectorMotorizedVNDF/Transmittance')
    
    def set_detector_vndf_transmittance(self, transmittance):
        self._put('DetectorMotorizedVNDF/Transmittance', str(transmittance))        


    #==============================================================================
    # /InGaAsDetector
    #==============================================================================
    
    def ingaas_detector_integration_time(self):
        return self._get('InGaAsDetector/IntegrationTime')
    
    def set_ingaas_detector_integration_time(self, time):
        self._put('InGaAsDetector/IntegrationTime', str(time))



    #==============================================================================
    # /HarpiaTF
    #==============================================================================

    def harpia_tf_spcm_trace(self):
        return self._get('/HarpiaTF/SPCM/Trace')

    def harpia_tf_spcm_rates(self):
        return self._get('/HarpiaTF/SPCM/Rates')
    
    def harpia_tf_spcm_time_axis(self):
        return self._get('/HarpiaTF/SPCM/TimeAxis')

    #==============================================================================
    # /TimingController
    #==============================================================================

    def set_timing_controller_frequency(self, frequency):
        return self._put('TimingController/Frequency', str(frequency))
    
    def timing_controller_frequency(self):
        return self._get('TimingController/Frequency')

    #==============================================================================
    # /ProbeSource
    #==============================================================================
    
    def probe_source_temperature(self):
        return self._get('ProbeSource/Temperature')
    
    def probe_source_turn_on(self):
        return self._post('ProbeSource/TurnOn')

    def probe_source_turn_off(self):
        return self._post('ProbeSource/TurnOff')
    
    def set_probe_source_internal_pulse_frequency(self, frequency):
        return self._put('ProbeSource/InternalPulseFrequency', str(frequency))
    
    def set_probe_source_trigger_mode_internal(self):
        self._put('ProbeSource/TriggerMode', r'"internal"')
        
    def set_probe_source_trigger_mode_external(self):
        self._put('ProbeSource/TriggerMode', r'"external"')
        
    
    
    #==============================================================================
    #     /FlashPhotolysis
    #==============================================================================
        
    def flash_photolysis_raw_signal(self):
        return self._get('FlashPhotolysis/RawSignal')
    
    def flash_photolysis_pump_probe_spectrum(self, close_shutters = True, target_delay = None):
        query = 'FlashPhotolysis/PumpProbeSpectrum/' + str(close_shutters).lower() 
        if target_delay != None:
            query = query + '/' + str(target_delay)            
        return self._get(query)
    
    
    
    #==============================================================================
    #     /HarpiaTB/DelayLine
    #==============================================================================

    def harpiatb_delay_line_actual_delay(self):
        return self._get('HarpiaTB/DelayLine/ActualDelay')
    
    def harpiatb_delay_line_target_delay(self):
        return self._get('HarpiaTB/DelayLine/TargetDelay')    
    
    def harpiatb_set_delay_line_target_delay(self, delay):
        self._put('HarpiaTB/DelayLine/TargetDelay', str(delay))
        
    def harpiatb_delay_line_go_to_zero(self):
        self._post('HarpiaTB/DelayLine/GoToZero')
        
    def harpiatb_delay_line_set_as_zero(self):
        self._post('HarpiaTB/DelayLine/SetAsZero')
        
        
    #==============================================================================
    #    /HarpiaTB/Chopper
    #==============================================================================
        
    def harpiatb_chopper_is_on(self):
        return self._get('HarpiaTB/Chopper/Chopper/IsOn')
    
    def harpiatb_chopper_start(self):
        self._post('HarpiaTB/Chopper/Chopper/Start')
    
    def harpiatb_chopper_stop(self):
        self._post('HarpiaTB/Chopper/Chopper/Stop')
    
    def harpiatb_chopper_is_locked(self):
        return self._get('HarpiaTB/Chopper/Chopper/IsLocked')
    
    def harpiatb_chopper_clock_source(self):
        return self._get('HarpiaTB/Chopper/Chopper/ClockSource')
    
    def harpiatb_set_chopper_clock_source_internal(self):
        self._put('HarpiaTB/Chopper/Chopper/ClockSource', '\"internal\"')
        
    def harpiatb_set_chopper_clock_source_external(self):
        self._put('HarpiaTB/Chopper/Chopper/ClockSource', '\"external\"')

    def harpiatb_chopper_clock_divider(self):
        return self._get('HarpiaTB/Chopper/Chopper/ClockDivider')
    
    def harpiatb_set_chopper_clock_divider(self, divider):
        self._put('HarpiaTB/Chopper/Chopper/ClockDivider', str(divider))
        
    def harpiatb_chopper_actual_frequency(self):
        return self._get('HarpiaTB/Chopper/Chopper/ActualFrequency')
    
    def harpiatb_chopper_target_frequency(self):
        return self._get('HarpiaTB/Chopper/Chopper/ActualFrequency')
    
    def harpiatb_set_chopper_target_frequency(self, frequency):
        self._put('HarpiaTB/Chopper/Chopper/TargetFrequency', str(frequency))
        
    def harpiatb_chopper_phase_error(self):
        return self._get('HarpiaTB/Chopper/Chopper/PhaseError')
        
    def harpiatb_chopper_target_phase(self):
        return self._get('HarpiaTB/Chopper/Chopper/TargetPhase')
    
    def harpiatb_set_chopper_target_phase(self, phase):
        self._put('HarpiaTB/Chopper/Chopper/TargetPhase', str(phase))
        
    #==============================================================================
    #      /BeamAlignmentSystem
    #==============================================================================
        
    def internal_quadrant_detectors(self):
        return self._get('InternalQuadrantDetectors')
    
    def internal_quadrant_detectors_trigger_delay(self):
        return self._get('InternalQuadrantDetectors/ExternalTriggerDelay')
    
    def set_internal_quadrant_detectors_trigger_delay(self, delay):
        return self._put('InternalQuadrantDetectors/ExternalTriggerDelay', str(delay))
    
    #===========================================================================
    #     /Microscope
    #===========================================================================
    
    def microscope_camera_alldata(self, index=None):
        return self._get('Microscope/Camera/AllData')
    
    def microscope_sample_stage_position(self, axis='X', **kwargs):
        """Get current sample stage XYZ position.
        
        Axis must be 'X', 'Y' or 'Z'.
        """
        axis = axis.upper()
        if axis not in ['X', 'Y', 'Z']:
            raise ValueError("Axis must be X,Y or Z")

        return self._get('Microscope/SampleStagePosition' + axis)

    def microscope_sample_stage_position_X(self):
        """Get current sample stage X position."""
        return self.microscope_sample_stage_position(axis='X')

    def microscope_sample_stage_position_Y(self):
        """Get current sample stage Y position."""
        return self.microscope_sample_stage_position(axis='Y')

    def microscope_sample_stage_position_Z(self):
        """Get current sample stage Z position."""
        return self.microscope_sample_stage_position(axis='Z')
    
    def microscope_set_sample_stage_position(
            self, position, axis='X', blocking=True, **kwargs):
        """Move XYZ sample stage.

        Axis must be 'X', 'Y' or 'Z'.

        The move is blocking, i.e. control is returned after the move is
        completed. Set 'blocking' to False to just issue the move command
        without waiting for any feedback. Note that a nonblocking moving
        command does not even wait for the move to start, so, for example,
        querrying the speed right after this command to see when the move is
        done might return a zero because the move hasn't even started yet.
        """
        axis = axis.upper()
        if axis not in ['X', 'Y', 'Z']:
            raise ValueError("Axis must be X,Y or Z")

        cmd_str = 'Microscope/SampleStagePosition' + axis

        if blocking:
            cmd_str += 'NonBlocking'
            
        return self._put(cmd_str, str(position))

    def microscope_set_sample_stage_position_X(self, position, **kwargs):
        """Move to sample stage X position."""
        self.microscope_set_sample_stage_position(position, axis='X', **kwargs)

    def microscope_set_sample_stage_position_Y(self, position, **kwargs):
        """Move to sample stage Y position."""
        self.microscope_set_sample_stage_position(position, axis='Y', **kwargs)

    def microscope_set_sample_stage_position_Z(self, position, **kwargs):
        """Move to sample stage Z position."""
        self.microscope_set_sample_stage_position(position, axis='Z', **kwargs)


    #==============================================================================
    #     /MotorizedPumpMirror
    #==============================================================================
    
    def motorized_pump_mirror(self):
        return self._get('MotorizedPumpMirror')
    
    def motorized_pump_mirror_position_X(self):
        return self._get('MotorizedPumpMirror/PositionX')
    
    def motorized_pump_mirror_set_position_X(self, position):
        return self._put('MotorizedPumpMirror/PositionX', str(position))

    def motorized_pump_mirror_set_relative_position_X(self, position):
        return self._put('MotorizedPumpMirror/RelativePositionX', str(position))
    
    def motorized_pump_mirror_position_Y(self):
        return self._get('MotorizedPumpMirror/PositionY')
    
    def motorized_pump_mirror_set_position_Y(self, position):
        return self._put('MotorizedPumpMirror/PositionY', str(position))

    def motorized_pump_mirror_set_relative_position_Y(self, position):
        return self._put('MotorizedPumpMirror/RelativePositionY', str(position))
    
    
    # =============================================================================
    # /ZScan    
    # =============================================================================
    
    def zscan_response (self):
        return self._get('ZScan/Response')
    
    def zscan_set_samples_per_point (self, samples):
        self._put('ZScan/SamplesPerPoint', str(samples))
    
    def zscan_set_position (self, position):
        self._put('ZScan/Position', str(position))
    
    def zscan_position (self):
        return self._get('ZScan/Position')

    