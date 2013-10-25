#!/usr/bin/python
##################################################################################
## plot tcoon salt03 data with timeseries toolkit
##
#################################################################################
##
## Author : Dharhas Pothina
## Created : 20091009
## Last Modified : 20091009
## Requires :
##     
##
#################################################################################

#################################################################################
# Import Required Modules 
import numpy as np #basic numerical functions
import pylab as plt #basic plotting functions
import datetime # datetime fns

#timeseries
import scikits.timeseries as ts
import scikits.timeseries.lib.plotlib as tpl
import numpy.ma as ma

dateconverter = lambda y, m : datetime.datetime(year=int(y.split('-')[2]),month=int(y.split('-')[0]),day=int(y.split('-')[1]),hour=int(m.split(':')[0]),minute=int(m.split(':')[1]))

#load only salinity data
salt03ts = ts.tsfromtxt('tcoon_salt03.txt', comments='#',missing='NA',datecols=(0,1),usecols=(0,1,2),dateconverter=dateconverter,freq='T')

#remove duplicated dates & fill missing 
salt03ts = ts.remove_duplicated_dates(salt03ts)
salt03ts = ts.fill_missing_dates(salt03ts)
salt03ts.sort_chronologically()

fig = tpl.tsfigure()
fsp = fig.add_tsplot(111)
fsp.tsplot(salt03ts,'c.')
fsp.grid()
fsp.set_ylim(0,45)
plt.title(site + ' Salinity')
plt.ylabel('Salinity (psu)')
plt.show()

#plots
freqs = ['H','D','W','M','A']
freqs = ['A']

for freq in freqs:
    
    tseries = salt03ts.convert(freq=freq,func=np.mean)
    fig = tpl.tsfigure()
    fsp = fig.add_tsplot(111)
    fsp.tsplot(tseries,'c.')
    fsp.grid()
    fsp.set_ylim(0,100)
    plt.title(site + ' Salinity')
    plt.ylabel('Salinity (psu)')
    plt.show()
#    plt.savefig('asd.png')
