#!/usr/bin/python
##################################################################################
## plot tcoon salt03 data
## of a hydrographic survey line.
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

#try 1
#salt03 = np.genfromtxt('tcoon_salt03.txt')

#try 2
#salt03 = np.genfromtxt('tcoon_salt03.txt',dtype=None,names='date,time,T,S')

#try 3
salt03 = np.genfromtxt('tcoon_salt03.txt',dtype='S10,S10,<f8,<f8',names='date,time,T,S',missing='NA',comments='#',usemask=True)

dates = salt03['date']
times = salt03['time']
temp = salt03['T']
sal = salt03['S']

#make datetime
dt = []
for i in range(dates.size):
    mon,day,yr = dates[i].split('-')
    hr,mn = times[i].split(':')
    dt.append(datetime.datetime(int(yr),int(mon),int(day),int(hr),int(mn)))

dt = np.array(dt)

#plot
dt = plt.date2num(dt)

plt.plot_date(dt,sal,'r.',label='Salinity (ppt)',markersize=0.5)
plt.plot_date(dt,temp,'b.',label='Temperature (C)',markersize=0.5)
plt.legend(loc=0)
plt.title('SALT03 Data')
plt.show()

