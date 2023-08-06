# -*- coding: utf-8 -*-
"""
Created on Tue May 15 13:22:37 2018

@author: butkus
"""

options_list = {
        'PR1':  'Internal WLSc generator for PHAROS',
        'PR2':  'Internal SH generator for PHAROS',
        'PR3':  'Internal WLSc generator for Ti:Sa systems',
        'PR4':  'External probe source from ORPHEUS',
        
        'DL1':  'Physik Instrumente VT-80',
        'DL2':  'Aerotech PRO115SL-300',
        
        'DLC1': '2 ns probe beam delay configuration',
        'DLC2': '4 ns probe beam delay configuration',
        'DLC3': '8 ns probe beam delay configuration',
        'DLC4': '8 ns probe beam delay configuration with polarization rotation',
        'DLC5': '12 ns probe beam delay configuration with polarization rotation',
        'DLC6': '6 ns probe beam delay configuration',
        
        'DM1':  'Multichannel Si NMOS UV/VIS/NIR detector (Hamamatsu S3901 + C7884, 200 - 1100 nm)',
        'DM2':  'Multichannel InGaAs NIR/Mid-IR detector (Hamamatsu C8062-01 + G9208-256W, 1100 - 2600 nm)',
        'DM3':  'Multichannel InGaAs NIR/Mid-IR detector (Hamamatsu G9203-256D, 900 - 1700 nm)',
        'DM4':  'Other multichannel detector',
        
        'DS1':  'Single-channel Si UV/VIS/NIR detector (Thorlabs Det10A/M, 200-1100 nm)',
        'DS2':  'Single-channel InGaAs NIR/Mid-IR detector (Thorlabs Det10C/M, 700 - 1800 nm)',
        'DS3':  'Single-channel InGaAs NIR/Mid-IR detector (Thorlabs Det10D/M, 1200 - 2600 nm)',
        'DS4':  'Other single-channel detector',
        
        'SP0':  'No spectrograph',
        'SP1':  'Andor Kymera 193i with 2 gratings',
        'SP2':  'Andor Shamrock 163i with 2 gratings',
        'SP3':  'Internal spectrograph without reference detection',
        'SP4':  'Internal spectrograph with reference detection',
        'SP5':  'Andor Kymera 328i with 2 gratings',
        
        'BC1':  'Manual Berek\'s compensators',
        'BC2':  'Motorized Berek\'s compensators',
        
        'SH1':  'Manual sample\'s holding unit',
        'SH2':  'Sample mover - motorized sample\'s holding unit',
        
        'NDF1': 'Manual neutral density filters',
        'NDF2': 'Motorized neutral density filters',
        
        'AD1':  'Measurement in reflection mode',
        'AD2':  'Glann-Taylor polarizer',
        'AD3':  'Reference photodiode',
        'AD4':  'Crystal rotator',
        'AD5':  'Beam profiler',
        'AD6':  'Motorized pump mirror adapter',
        'AD7':  'External beam stabilization',
        'AD8':  'Internal beam position tracking',
        'AD9':  'Cryostat adapter',
        'AD10': 'Sample stirrer',
        'AD11': 'Flash photolysis extension',
        'AD12': 'reserved',
        
        'TF1':  'HARPIA-TF with Universal TCSPC photomultiplier detector',
        'TF2':  'HARPIA-TF with High speed TCSPC hybrid detector',
        
        'TB0':  'No Harpia-TB',
        'TB1':  'Harpia-TB',
        
        'MM1':  'Microscopy module',
        'MM2':  'Motorized objective translation stage for microscopy module',
        'MM3':  'Bulk module'
        }

PR_flags = {
        0x01 << (11*4): 'PR1',
        0x02 << (11*4): 'PR2',
        0x04 << (11*4): 'PR3',
        0x08 << (11*4): 'PR4',        
        }

DL_configuration_mask = 0x07 << (10*4)
DL_configuration_values = {
        0 << (10*4): 'DLC1',
        1 << (10*4): 'DLC2',
        2 << (10*4): 'DLC3',
        3 << (10*4): 'DLC4',
        4 << (10*4): 'DLC5',
        5 << (10*4): 'DLC6'
        }

DL_mask = 0x08 << (10*4)
DL_values = {
        0 << (10*4+3): 'DL1',
        1 << (10*4+3): 'DL2'
        }

DM_flags = {
        0x01 << (9*4): 'DM1',
        0x02 << (9*4): 'DM2',
        0x04 << (9*4): 'DM3',
        0x08 << (9*4): 'DM4',
        }

DS_flags = {
        0x01 << (8*4): 'DS1',
        0x02 << (8*4): 'DS2',
        0x04 << (8*4): 'DS3',
        0x08 << (8*4): 'DS4',
        }

SP_mask = 0xF<< (7*4)
SP_values = {
        0<< (7*4): 'SP0',
        1<< (7*4): 'SP1',
        2<< (7*4): 'SP2',
        3<< (7*4): 'SP3',
        4<< (7*4): 'SP4',
        5<< (7*4): 'SP5'
        }

BC_mask = 0x01 << (6*4)
BC_values = {
        0 << (6*4): 'BC1',
        1 << (6*4): 'BC2'
        }

NDF_mask = 0x02 << (6*4)
NDF_values = {
        0 << (6*4 + 1):  'NDF1',
        1 << (6*4 + 1):  'NDF2'
        }

SH_flags = {
        0x04 << (6*4): 'SH1',
        0x08 << (6*4): 'SH2'
        }

AD_flags = {
        0x001 << (3*4): 'AD12',
        0x002 << (3*4): 'AD11',
        0x004 << (3*4): 'AD10',
        0x008 << (3*4): 'AD9',
        0x010 << (3*4): 'AD8',
        0x020 << (3*4): 'AD7',
        0x040 << (3*4): 'AD6',
        0x080 << (3*4): 'AD5',
        0x100 << (3*4): 'AD4',
        0x200 << (3*4): 'AD3',
        0x400 << (3*4): 'AD2',
        0x800 << (3*4): 'AD1'
        }

TF_flags = {
        0x01 << (2*4): 'TF1',
        0x02 << (2*4): 'TF2'
        }

TB_mask = 0x08 << (2*4)
TB_values = {
        #0x00: 'TB0',
        0x08 << (2*4): 'TB1'
        }

MM_flags = {
        0x001 << (0*4): 'MM1',
        0x002 << (0*4): 'MM2',
        0x004 << (0*4): 'MM3',
        }


code = {
        'Probe sources': {
                'flags': PR_flags
                },
        'Delay line': {
                'mask': DL_configuration_mask,
                'values': DL_configuration_values
                },
        'Delay line configuration': {
                'mask': DL_mask,
                'values': DL_values
                },
        'Multichannel detector': {
                'flags': DM_flags
                },
        'Single-channel detector': {
                'flags': DS_flags
                },
        'Spectrograph': {
                'mask': SP_mask,
                'values': SP_values
                },
        'Berek\'s rotator': {
                'mask': BC_mask,
                'values': BC_values
                },
        'Nautral density filters': {
                'mask': NDF_mask,
                'values': NDF_values
                },
        'Sample holder': {
                'flags': SH_flags
                },
        'Additional options': {
                'flags': AD_flags
                },
        'HARPIA-TF': {
                'flags': TF_flags
                },
        'HARPIA-TB': {
                'mask': TB_mask,
                'values': TB_values},
        'Microscopy extenstion': {
                'flags': MM_flags
                }
        }

def decode(model='PM5A333D6B0A'):
    '''Decodes Harpia model number PMxxxxxxxxxxx to human-readable object'''
    if (model[:2] != 'PM'):
        return None
        
    if (len(model) == 12):
        model = model + 'M00'
        
    if (len(model) != 15) and (model[12] != 'M'):
        return None

    model = model[:12] + model[13:]

    if (int(model[6])>5):
        return None

    if (int(model[3], 16) > 0x05) and (int(model[3], 16) < 0x08):
        return None

    if (int(model[11], 16) & 0x04 != 0):
        return None

    number = int(model[2:], 16)
    
    decode = []
    
    for entry in code:                
        if 'flags' in code[entry]:
            for flag in code[entry]['flags']:
                if flag & number != 0:
                    option = code[entry]['flags'][flag]
                    decode.append({'option': option, 'description': options_list.get(option)})
                    #print (option, options_list.get(option))
        if 'mask' in code[entry]:
            case = code[entry]['mask'] & number
            if code[entry]['values'].get(case):
                option = code[entry]['values'][case]
                if (options_list.get(option) is not None):
                    decode.append({'option': option, 'description': options_list.get(option)})
            #print (option, options_list.get(option))
            
    return decode
    
def encode(options):
    '''Encodes options, as list of option strings, to product number PMxxxxxxxxx'''
    number = 0
    
    for entry in code:                
        if 'flags' in code[entry]:
            for key, val in code[entry]['flags'].items():
                if val in options:
                    number += key                                
        if 'mask' in code[entry]:
            for key, val in code[entry]['values'].items():
                if val in options:
                    number+= key
                    
    model = 'PM' + hex(number+(1 << (12*4)))[3:].upper()
    
    if 'MM' in [option[:2] for option in options]:
        return model[:-2]+'M'+model[-2:]
    
    return model[:-2]