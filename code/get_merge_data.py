#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:58:34 2019
Function to grab data from the CVAO merge file. Requires start/end dates 
and resample frequency (e.g. H, D, M, Y)
@author: mjr583
"""
import pandas as pd
def get_merge(start_year,end_year,sample,*args):
    filepath='/users/mjr583/scratch/NCAS_CVAO/CVAO_datasets/'
    filen=filepath+'20191007_CV_Merge.csv'
    df=pd.read_csv(filen,index_col=0,dtype={'Airmass':str})
    df.index=pd.to_datetime(df.index,format='%d/%m/%Y %H:%M')

    filen=filepath+'cv_ovocs_2018_M_Rowlinson.csv'
    odf = pd.read_csv(filen, index_col=0)
    odf.index = pd.to_datetime(odf.index,format='%d/%m/%Y %H:%M')
    
    cols=list(df) ; ocols = list(odf)
    for col in cols:
        try:
            df[col] = df[col].loc[~(df[col] <= 0. )]
        except:
            pass
    for col in ocols:
        odf = odf.loc[~(odf[col] <= 0.)]
    cols=cols+ocols
    merge=df.resample(sample).mean()
    ovoc_merge=odf.resample(sample).mean()
    df=pd.concat([merge,ovoc_merge], axis=1, sort=False)
    df = df[str(start_year):str(end_year)]
    
    for ar in args:
        df = df[ar]
    return df