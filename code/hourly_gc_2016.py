import numpy as np
import pandas as pd
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from glob import glob
from matplotlib.colors import BoundaryNorm
from mpl_toolkits.basemap import Basemap
from get_merge_data import get_merge
mons = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
plt.style.use('seaborn-darkgrid')
plt.rcParams['figure.figsize'] = (9,6)

SPECIES = 'ozone'
if SPECIES == 'acetone':
    gc_spec = 'ACET'
    cv_spec = SPECIES
    label=SPECIES
    unit='ppt' ; scale=1e12
elif SPECIES=='ozone':
    gc_spec = 'O3'
    cv_spec = 'O3'
    label = '$O_3$'
    unit = 'ppb' ; scale=1e9
elif SPECIES=='ch4':
    gc_spec='CH4'
    cv_spec='CH4 all (ppbV)'
    label='$CH_4$'
    unit='ppb' ; scale=1e9
elif SPECIES=='co':
    gc_spec='CO'
    cv_spec='CO (ppbV)'
    label='CO'
    unit='ppb' ; scale=1e9
elif SPECIES=='no':
    gc_spec = 'NO'
    cv_spec = 'NO (pptV)'
    label = 'NO' ; unit = 'ppt' ; scale=1e12
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
    o3.append(fh.variables['SpeciesConc_'+gc_spec][:])
o3=np.array(o3)*scale

filepath='/users/mjr583/scratch/NCAS_CVAO/CVAO_datasets/'
savepath='/users/mjr583/scratch/NCAS_CVAO/plots'
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
hourly=df.resample('H').mean()
ohourly=odf.resample('H').mean()
df=pd.concat([hourly,ohourly], axis=1, sort=False)

cvao = df[cv_spec]['2016']
#cvao = cvao.resample('H').mean()

o3 = np.concatenate(o3,axis=0)

surf_o3 = o3[:,0,27,31]
plt.plot(surf_o3,color='k',label='GEOS-Chem')
plt.plot(cvao.values[:],color='Orange',label='CVAO')
x = len(surf_o3)
plt.xticks(np.arange(x/24,x,x/12),mons)
plt.legend()
plt.ylabel(label+' ('+unit+')')
plt.savefig('/users/mjr583/scratch/gc/plots/'+SPECIES+'/hourly_2016.png')
plt.close()

MAX = max(np.nanmax(cvao.values), np.nanmax(surf_o3))
MIN = min(np.nanmin(cvao.values), np.nanmax(surf_o3))


plt.plot(cvao,cvao, color='grey', linewidth=0.5, linestyle='--')
plt.scatter(cvao, surf_o3)
plt.xlim(MIN,MAX)
plt.ylim(MIN,MAX)
plt.xlabel('CVAO '+label+' ('+unit+')')
plt.ylabel('GEOS-Chem '+label+' ('+unit+')')
plt.savefig('/users/mjr583/scratch/gc/plots/'+SPECIES+'/scatter.png')
