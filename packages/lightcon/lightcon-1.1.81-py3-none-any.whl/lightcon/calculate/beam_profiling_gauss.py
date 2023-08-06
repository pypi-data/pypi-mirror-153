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
from scipy.optimize import minimize

def _gauss2d_par(par, matrix, decimation):
    Y = gauss2d(np.arange(0, np.shape(matrix)[1]), np.arange(0, np.shape(matrix)[0]), par[0], par[1], par[2], par[3], par[4], par[5], par[6], decimation = decimation)                
    return Y
        
def fun(par, args = {'decimation' : 1}):
    decimation = args.get('decimation') or 1
    matrix = args['matrix']
    score =  np.sum((matrix[::decimation,::decimation] - _gauss2d_par(par, matrix, decimation)) ** 2)
    return score

def gauss2d(xaxis, yaxis, A, xc, yc, sigma_x, sigma_y, phi, y0, decimation = 1):
    sigma_x = np.sqrt(2.0) * sigma_x
    sigma_y = np.sqrt(2.0) * sigma_y
    a = (np.cos(phi)/sigma_x)**2 + (np.sin(phi)/sigma_y)**2
    b = (np.sin(phi)/sigma_x)**2 + (np.cos(phi)/sigma_y)**2
    c = 2.0 * np.sin(phi) * np.cos(phi) * (1.0/sigma_x**2 - 1.0/sigma_y**2)
    
    xx, yy = np.meshgrid(xaxis[::decimation], yaxis[::decimation])
    
    result =  A * np.exp(- (a * (xx - xc) ** 2 + b * (yy - yc) ** 2 + c * (xx - xc)*(yy - yc))) + y0
    
    result[result>A] = A
    
    return result     

def fit_gauss2d(matrix, init, decimation = 1):
    out_minimize = minimize(fun, init, method = 'Nelder-Mead', args = {'maxiter': 2000, 'matrix': matrix, 'decimation' : decimation})    
    print(out_minimize)
    
    a = (np.cos(out_minimize.x[5])/out_minimize.x[3])**2 + (np.sin(out_minimize.x[5])/out_minimize.x[4])**2
    b = (np.sin(out_minimize.x[5])/out_minimize.x[3])**2 + (np.cos(out_minimize.x[5])/out_minimize.x[4])**2
    c = 2.0 * np.sin(out_minimize.x[5]) * np.cos(out_minimize.x[5]) * (1.0/out_minimize.x[3]**2 - 1.0/out_minimize.x[4]**2)
        
    phi = 0.5 * np.arctan(c/(a-b))
    sigma_x = np.sqrt(np.cos(2.0 * phi) / 2.0 / (a * np.cos(phi) **2 - b * np.sin(phi)**2)) * np.sqrt(2.0)
    sigma_y = np.sqrt(np.cos(2.0 * phi) / 2.0 / (-a * np.sin(phi) **2 + b * np.cos(phi)**2)) * np.sqrt(2.0)
    sigma_xy = c / (c * c - 4.0 * a * b)
    
    gamma =  np.sign(sigma_x ** 2 - sigma_y ** 2)
    sigma_p = 2.0 * np.sqrt(2.0) * np.sqrt((sigma_x ** 2 + sigma_y ** 2) + gamma * np.sqrt((sigma_x ** 2 - sigma_y ** 2) ** 2 + 4.0 * sigma_xy ** 2)) / 4.0
    sigma_s = 2.0 * np.sqrt(2.0) * np.sqrt((sigma_x ** 2 + sigma_y ** 2) - gamma * np.sqrt((sigma_x ** 2 - sigma_y ** 2) ** 2 + 4.0 * sigma_xy ** 2)) / 4.0
    
    out_gauss = {'mean_x': out_minimize.x[1], 'mean_y': out_minimize.x[2], 'sigma_x': sigma_x, 'sigma_y': sigma_y, 'sigma_xy': sigma_xy,
                 'phi': phi, 'sigma_p': sigma_p, 'sigma_s': sigma_s }
    return out_gauss