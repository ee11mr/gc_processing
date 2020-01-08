#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 17:41:30 2019

@author: mjr583
"""
import numpy as np
from netCDF4 import Dataset
from glob import glob

def get_gc_var(year, species):
    filepath='/users/mjr583/scratch/gc/rundirs/merra2_4x5_tropchem/OutputDir/'
    fh = Dataset(filepath+'GEOSChem.SpeciesConc.20160101_0000z.nc4','r')
    lat = fh.variables['lat'][:]
    lon = fh.variables['lon'][:]
    p = fh.variables['ilev'][:]

    var=[]
    for i,infile in enumerate(sorted(glob(filepath+'GEOSChem.SpeciesConc.'+str(year)+'*01_0000z.nc4'))):
        print(i, infile)
        fh = Dataset(infile)
        var.append(fh.variables['SpeciesConc_'+species][:])
    var=np.array(var)
    return var, (lat, lon, p)

xx, yy = get_gc_var(2016, 'O3')
print(xx)