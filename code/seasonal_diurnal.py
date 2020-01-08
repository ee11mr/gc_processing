import numpy as np
import pandas as pd
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from glob import glob
from matplotlib.colors import BoundaryNorm
from mpl_toolkits.basemap import Basemap
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
    gc_spec='NO'
    cv_spec='NO (pptV)'
    label='NO' ; unit='ppt' ; scale=1e12

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
mf = pd.DataFrame(o3[:,0,27,31])
mf.index = cvao.index

m31 = 24*31 ; m30 = 24*30 ; m29 = 24*29 ; m28 = 24*28
mf_djf = pd.concat([mf[-m31:],mf[:m31+m29]])
mf_mam = mf[m31+m29:m31*3+m30+m29]
mf_jja = mf[m31*3+m30+m29:m31*5+m30*2+m29]
mf_son = mf[m31*5+m30*2+m29:m31*6+m30*4+m29]
MF = [mf_djf, mf_mam, mf_jja, mf_son]
cv_djf = pd.concat([cvao[-m31:],cvao[:m31+m29]])
cv_mam = cvao[m31+m29:m31*3+m30+m29]
cv_jja = cvao[m31*3+m30+m29:m31*5+m30*2+m29]
cv_son = cvao[m31*5+m30*2+m29:m31*6+m30*4+m29]
CV = [cv_djf, cv_mam, cv_jja, cv_son]

cv_seas=[] ; mf_seas=[]
for i in range(4):
    a = CV[i].groupby(CV[i].index.hour).mean()
    aa = a - a.mean()
    cv_seas.append(aa)
    
    b = MF[i].groupby(MF[i].index.hour).mean()
    bb = b - b.mean()
    mf_seas.append(bb)
    
    
    #cv_seas.append(CV[i].groupby(CV[i].index.hour).mean())
    #mf_seas.append(MF[i].groupby(MF[i].index.hour).mean())

f,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,sharex=True)
ax=[ax1,ax2,ax3,ax4]
titles=['DJF','MAM','JJA','SON']
for i in range(4):
    ax2=ax[i].twinx()
    ln1=ax[i].plot(cv_seas[i],'-',color='Orange',label='CVAO')
    ln2=ax2.plot(mf_seas[i],'k-',label='GEOS-Chem')
    ax[i].set_ylabel(label+' ('+unit+')')
    ax[i].title.set_text(titles[i])
lns = ln1+ln2
labs=[l.get_label() for l in lns]
ax1.legend(lns,labs, loc=0)
ax3.set_xlabel('Hour')
ax4.set_xlabel('Hour')
plt.tight_layout()
plt.savefig('/users/mjr583/scratch/gc/plots/'+SPECIES+'/seasonal_mean_diurnal.png')
print('Done.')
print(cv_seas[0].mean())
print(mf_seas[0].mean())
