#!/usr/bin/python
##################################################################################
## Analyse the effect of boat angle and speed on calculation of cross section area
## of a hydrographic survey line.
##
#################################################################################
##
## Author : Dharhas Pothina
## Created : 20090925
## Last Modified : 20090925
## Requires :
##     
##
#################################################################################

#################################################################################
# Import Required Modules 

import numpy as np #basic numerical functions
import glob #file search functions
import pylab as plt #basic plotting functions
from scipy.interpolate import interp1d #1d interp function

#hardcoded directories
csadir = 'crosssections'
figdir = 'figures'
tabdir = 'tables'

#get list of all cross section data files in csa dir
file1 = 'crosssections\\CSA_LB99_1.csv'
file2 = 'crosssections\\CSA_LB09_1.csv'

#read in cross sections
x1,z1 = np.genfromtxt(file1,skiprows=1,delimiter=',',usecols=(1,2),unpack=True)
x2,z2 = np.genfromtxt(file2,skiprows=1,delimiter=',',usecols=(1,2),unpack=True)

#convert elevations to depths
z1 = z1 - 429
z2 = z2 - 429
#calculate cross sectional areas using trapezoidal rule
csa1 = -np.trapz(z1,x1)
csa2 = -np.trapz(z2,x2)

csa_perc = (csa2-csa1)/csa1 * 100.0
#plot cross sections
plt.figure()
plt.plot(x1,z1,'b',label='LBJ99, csa='+csa1.__str__())
plt.plot(x2,z2,'g',label='LBJ09, csa='+csa2.__str__()+',perc change='+csa_perc.__str__())
plt.xlabel('distance (ft)')
plt.ylabel('depth (ft)')
plt.legend(loc=0)
plt.show()


    

