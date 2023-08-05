import numpy as np
from beam_profiling_iso import iterative_iso, general_iso
from beam_profiling_gauss import fit_gauss2d

filename = r'C:/Darbai/[Harpia]/R&D/Beam diagnostics/L191104_pixel45.40.txt'
filename = r'C:/Darbai/[Harpia]/R&D/Beam diagnostics/out_gauss.txt'
filename = r'C:/Darbai/[Harpia]/[Manual]/TestReportZScan/capture_2021_07_08_133515.txt'

matrix = (np.loadtxt(filename))


out_iso = iterative_iso(matrix)

init_gauss = [np.max(matrix) - np.min(matrix), out_iso['mean_x'], out_iso['mean_y'], out_iso['sigma_x'], out_iso['sigma_y'], out_iso['phi'], np.min(matrix)]    

out_gauss = fit_gauss2d(matrix, init_gauss, decimation = 50)

# generated = {'mean_x': 300.0, 'mean_y': 150, 'sigma_x': 50.5, 'sigma_y': 52.0, 'phi': 0.53}
# pixel_size = 1.0

generated = {'mean_x': 3.989 / 3.45e-3 , 'mean_y': 3.102 / 3.45e-3, 'sigma_x': 3.555/2.3548200450309493 / 3.45e-3, 'sigma_y': 3.502/2.3548200450309493 / 3.45e-3, 'phi': - np.pi / 6.0}
pixel_size = 3.45e-3


print("{:<10}{:>10s}{:>10s}{:>10s}".format('','ISO','GAUSS','ORIGINAL'))
for key in out_iso.keys():
    print ("{:<10}{:>10.2f}{:>10.2f}{:>10.2f}".format(
            key, 
            out_iso.get(key) * (pixel_size if key != 'phi' else 180.0/np.pi),
            out_gauss.get(key) * (pixel_size if key != 'phi' else 180.0/np.pi),
            (generated.get(key) or 0.0) * (pixel_size if key != 'phi' else 180.0/np.pi),)
            )