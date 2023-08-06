#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# 
#--------------------------------------------------------------------------
# Copyright (c) 2021 Light Conversion, UAB
# All rights reserved.
# www.lightcon.com
#==========================================================================
import numpy as np

def general_iso (matrix, mask = None):    
    xx, yy = np.meshgrid(np.arange(0, np.shape(matrix)[1]), np.arange(0, np.shape(matrix)[0]))
    
    if mask is not None:
        matrix = matrix * mask    
        
    sum_xy = np.sum(matrix)
    mean_x = np.sum(matrix * xx) / sum_xy
    mean_y = np.sum(matrix * yy) / sum_xy
    
    sigma_x = np.sqrt(np.sum(matrix * (xx - mean_x) ** 2) / sum_xy)
    sigma_y = np.sqrt(np.sum(matrix * (yy - mean_y) ** 2) / sum_xy)
    sigma_xy = np.sum(matrix * (xx - mean_x) * (yy - mean_y)) / sum_xy
    
    phi = 0.5 * np.arctan(2 * sigma_xy / (sigma_x ** 2 - sigma_y **2))
    
    gamma =  np.sign(sigma_x ** 2 - sigma_y ** 2)
    dx = 2.0 * np.sqrt(2.0) * np.sqrt((sigma_x ** 2 + sigma_y ** 2) + gamma * np.sqrt((sigma_x ** 2 - sigma_y ** 2) ** 2 + 4.0 * sigma_xy ** 2))
    dy = 2.0 * np.sqrt(2.0) * np.sqrt((sigma_x ** 2 + sigma_y ** 2) - gamma * np.sqrt((sigma_x ** 2 - sigma_y ** 2) ** 2 + 4.0 * sigma_xy ** 2))

    return {'mean_x': mean_x, 'mean_y':  mean_y, 'sigma_x' : sigma_x, 'sigma_y' : sigma_y, 'sigma_xy': sigma_xy, 'sigma_p' : dx / 4.0, 'sigma_s': dy / 4.0, 'phi': phi}
    
def get_illuminated_pixels_mask(matrix):
    percentage = 0.05
    eta_T = 2.0
    
    area = [int(np.shape(matrix)[1] * percentage), int (np.shape(matrix)[0] * percentage)] 
    
    averages = [np.average(matrix[0:area[0],0:area[1]]),    #upper left corner
                np.average(matrix[0:area[0],-area[1]:]),    #upper right corner
                np.average(matrix[-area[0]:,0:area[1]]),    #lower left corner
                np.average(matrix[-area[0]:,-area[1]:])     #lovwe right corner
                ]
        
    background_level = np.min(averages)
    
    noise_offset = np.min(averages) * eta_T
    
    percentile = np.percentile(matrix, 95)
    
    if (noise_offset  > percentile):        
        noise_offset = percentile
        print ('updated eta_T', percentile / np.min(averages))
    
    res = np.select([matrix>=noise_offset], [1])    
    return (res, background_level)


def iterative_iso (matrix):    
    xx, yy = np.meshgrid(np.arange(0, np.shape(matrix)[1]), np.arange(0, np.shape(matrix)[0]))
        
    illuminated_pixels, background_level = get_illuminated_pixels_mask(matrix)    
    
    distance_coeff= 3.0
    
    matrix = matrix - background_level
    matrix = matrix * illuminated_pixels
        
    out = general_iso (matrix)
    
    while True:
        out_old = out
        mask = np.logical_and(np.logical_and(xx > out['mean_x'] - distance_coeff * out['sigma_x'], xx < out['mean_x'] + distance_coeff * out['sigma_x']), 
                              np.logical_and(yy > out['mean_y'] - distance_coeff * out['sigma_y'], yy < out['mean_y'] + distance_coeff * out['sigma_y'])) + 0
                              
        out = general_iso (matrix, mask)                      
        if (out_old == out):
            break
        
    return out  