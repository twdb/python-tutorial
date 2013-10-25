#!/usr/bin/python
##################################################################################
## Analyse the effect of boat angle and speed on calculation of cross section area
## of a hydrographic survey line.
##
#################################################################################
##
## Author : Dharhas Pothina
## Created : 20090929
## Last Modified : 20090929
## Requires :
##     
##
#################################################################################

#################################################################################
# Import Required Modules 

import numpy as np #basic numerical functions
import glob #file search functions
import pylab as plt #basic plotting functions


#hardcoded directories
csadir = 'crosssections'
figdir = 'figures'
tabdir = 'tables'

#hardcoded values
elev0 = 429 #in ft

#get list of all cross section data files in csa dir
files = glob.glob(csadir + '\CSA*.csv')

table = []

for csafile in files:
    tmp,lake,section = csafile.split('\\')[-1].split('.')[0].split('_')
    if lake=='LB99':
        file_LB99 = csafile
        file_LB09 = csadir + '\\' + tmp + '_LB09_' + section + '.csv'
        print 'comparing section: ',section

        #read in cross sections
        x1,z1 = np.genfromtxt(file_LB99,skiprows=1,delimiter=',',usecols=(1,2),unpack=True)
        try:
            x2,z2 = np.genfromtxt(file_LB09,skiprows=1,delimiter=',',usecols=(1,2),unpack=True)
        except:
            print 'Matching LB09 section file not found for: ',csafile
        
        #convert elevations to depths
        z1 = z1 - elev0
        z2 = z2 - elev0
        #calculate cross sectional areas using trapezoidal rule
        csa1 = -np.trapz(z1,x1)
        csa2 = -np.trapz(z2,x2)
        csa_perc = (csa2-csa1)/csa1 * 100.0
        
        table.append([section,csa1,csa2,csa_perc])

        #plot cross sections
        plt.figure()
        plt.plot(x1,z1,'c.-',label='LBJ99, Area='+csa1.round(decimals=2).__str__() + ' ft^2')
        plt.plot(x2,z2,'g',label='LBJ09, Area='+csa2.round(decimals=2).__str__() + ' ft^2')
        plt.xlabel('Distance From Start of Section (ft)')
        plt.ylabel('Depth (ft)')
        plt.title('Comparison of Cross Sections at Section: '+section)
        leg = plt.legend(loc=0,title='change in area='+csa_perc.round(decimals=2).__str__()+' %')
        for t in leg.get_texts():
            t.set_fontsize('small') # change legend fontsizes
        filename = 'LB99_vs_LB09_Section-' + section + '.png'
        plt.savefig('figures/'+filename)


print 'Plots saved in figures directory'
#write summary data to file
print 'Cross section area and % change values stored in csa_compare.csv'
fid = open( 'csa_compare.csv' , 'w' )
fid.write( 'Section_Name,LB99_Area,LB09_Area,Perc_Change\n' )
np.savetxt(fid ,table, fmt='%s', delimiter=',')
fid.close()  

