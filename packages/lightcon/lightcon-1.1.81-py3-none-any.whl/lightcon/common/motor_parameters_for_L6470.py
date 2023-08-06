# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:21:57 2020

@author: butkus
"""

import numpy as np

def motor_parameters_for_L6470(R, Ir, L, Ke, Vbus=24.0, lsopt=True):
    '''Calculates optimal parameter for L6470 driver using given values
    of resistance R [Ohm], rated current Ir [A], inductivity L [H], phase voltage constant Ke [V/Hz]
    and bus voltage Vbus [V]. lsopt=True if low-speed optimization used'''
    KVAL = int(R * Ir * np.sqrt(2.0) / Vbus * (2.0 ** 8))
    FN_SLP = int((2.0 * np.pi * L * Ir * np.sqrt(2.0) + Ke) / 4.0 / Vbus * (2 ** 16))
    INT_SPEED = int(4.0 * R / (2.0 * np.pi * L) * (2**26) * 250.0E-9)
    pars = { 'KVAL_HOLD': KVAL >> 1,
            'KVAL_RUN': KVAL,
            'KVAL_ACC': KVAL,
            'KVAL_DEC': KVAL,
            'INT_SPEED': int(2**14-1) if (INT_SPEED > 2**14 - 1) else INT_SPEED,
            'ST_SLP': int(Ke / 4.0 / Vbus * (2**16)),
            'FN_SLP_ACC': FN_SLP,
            'FN_SLP_DEC': FN_SLP,
            'MIN_SPEED': int(50.0 * (2**24) * 250.0E-9) | ((1 << 12) if lsopt else 0 )            
            }
    
    return pars
    
