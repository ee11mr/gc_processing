import numpy as np
import pandas as pd
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from glob import glob
from matplotlib.colors import BoundaryNorm
from mpl_toolkits.basemap import Basemap

filepath='/users/mjr583/scratch/gc/rundirs/merra2_4x5_tropchem/OutputDir/'
savepath='/users/mjr583/scratch/gc/plots/'
fh = Dataset(filepath+'GEOSChem.SpeciesConc.20160101_0000z.nc4','r')
nmonth=12
lat = fh.variables['lat'][:]
lon = fh.variables['lon'][:]
p = fh.variables['ilev'][:]

o3=[]
for i,infile in enumerate(sorted(glob(filepath+'GEOSChem.SpeciesConc.2016*01_0000z.nc4'))):
    print(i, infile)
    fh = Dataset(infile)
    o3.append(fh.variables['SpeciesConc_O3'][:])
o3=np.array(o3)*1e9

filepath='/users/mjr583/scratch/NCAS_CVAO/CVAO_datasets/'
savepath='/users/mjr583/scratch/NCAS_CVAO/plots'
filen=filepath+'20191007_CV_Merge.csv'
df=pd.read_csv(filen,index_col=0,dtype={'Airmass':str})
df.index=pd.to_datetime(df.index,format='%d/%m/%Y %H:%M')
cols=list(df)
for col in cols:
    try:
        df[col] = df[col].loc[~(df[col] <= 0. )]
    except:
        pass
cvao = df['O3']['2016']
cvao = cvao.resample('H').mean()

o3 = np.concatenate(o3,axis=0)
mf = pd.DataFrame(o3[:,0,27,31])
mf.index = cvao.index

cv_daily_mean = cvao.groupby(cvao.index.hour).mean()
mf_daily_mean = mf.groupby(mf.index.hour).mean()

f,ax1 = plt.subplots()
ax2=ax1.twinx()

ln1=ax1.plot(cv_daily_mean,label='CV')
ln2=ax2.plot(mf_daily_mean,'r--',label='GC')
ax2.set_ylim([27.25,30.25])
lns = ln1+ln2
labs=[l.get_label() for l in lns]
ax1.legend(lns,labs)
ax1.set_xlabel('Hour')
ax1.set_ylabel('$O_3$ (ppb)')
plt.savefig('/users/mjr583/scratch/gc/plots/annual_mean_diurnal.png')
print('DONE!!')
