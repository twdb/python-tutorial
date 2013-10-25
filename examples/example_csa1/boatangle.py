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
files = glob.glob(csadir + '\CSA*.csv')

#define boat & depth sounder characteristics
boat_spd = 6 #in mph
boat_angle = 10 #in degrees
ping_freq = 1 # number of pings/second
epsilon = 0.1 
bank1 = 15.0 #distance from 1st bank before first measurement
bank2 = 10.0 #distance from 2nd bank before first measurement

files = ['crosssections\\CSA_LB09_upperlake.csv']
#loop through files in csadir
for csafile in files:
    print 'Reading in ' + csafile
    #read in cross sections
    x,z = np.genfromtxt(csafile,skiprows=1,delimiter=',',usecols=(1,2),unpack=True)

    tmp,lake,section = csafile.split('\\')[-1].split('.')[0].split('_')

    #convert elevations to depths
    z = z[0] - z

    #create new 'true' cross section with 0.001ft spacing for angle calc
    xt = np.arange(x[0],x[-1],0.01)
    zt = interp1d(x,z,kind='linear')(xt)

    #create new lower res 'true' cross section with 0.1ft spacing for graph and area calc
    xt_low = np.arange(x[0],x[-1],0.1)
    zt_low = interp1d(x,z,kind='linear')(xt_low)

    ####################################################
    #generate 'measured' cross sections
    boat_spd_fps = boat_spd * 1.466667
    dist = boat_spd_fps / ping_freq # distance travelled by boat between pings
    
    #left to right
    xm_lr = np.arange(0+bank1,xt[-1]-bank2,dist)
    zm_lr = np.zeros(xm_lr.size)
    #find intersection of angled measurement with bottom surface for each point in xm_lr
    print 'Calculating L-R'
    for i in range(xm_lr.size):
        xs = xt[xt>=xm_lr[i]] #find all points after current boat location
        zs = zt[xt>=xm_lr[i]]
        #found = 0
        for j in range(xs.size):
            #distance between (xm[i],0) and (xt[j],zt[j])
            xdist = xs[j]-xm_lr[i]
            theta = np.arctan(xdist/zs[j])*57.2957795 #convert angle to degrees
            #print i.__str__() + ' : theta,btangle = ', theta, boat_angle
            if (np.abs(theta-boat_angle) < epsilon): #compare with boat angle
                zm_lr[i] = np.sqrt(xdist**2 + zs[j]**2)
                #found = 1
                #print i.__str__() + ' boat angle found, z=', zm_lr[i]
                break
            if (theta > boat_angle):
                #print i.__str__() + ' boat angle not found'
                break

#        if (found==0):
#            print i.__str__() + ' boat angle not found'
            #break

    #exit(1)

            
    #right to left
    print 'Calculating R-L'
    xm_rl = np.arange(xt[-1]-bank1,0+bank2,-dist)
    #xm_rl = xm_rl[::-1]
    zm_rl = np.zeros(xm_rl.size)

    #reverse xt and zt
    xtr = xt[::-1]
    ztr = zt[::-1]
 
    #find intersection of angled measurement with bottom surface for each point in xm_lr
    for i in range(xm_rl.size):
        xs = xtr[xtr<=xm_rl[i]] #find all points before current boat location
        zs = ztr[xtr<=xm_rl[i]]
        for j in range(xs.size):
            xdist = xm_rl[i]-xs[j]
            theta = np.arctan(xdist/zs[j])*57.2957795 #convert angle to degrees
            #print i.__str__() + ' : theta,btangle = ', theta, boat_angle
            if (np.abs(theta-boat_angle) < epsilon): #compare with boat angle
                zm_rl[i] = np.sqrt(xdist**2 + zs[j]**2)
                #found = 1
                #print i.__str__() + ' : found, z=', zm_lr[i]
                break
            if (theta > boat_angle):
                break
            #distance between (xm[i],0) and (xt[j],zt[j])
            #h = np.sqrt((xm_rl[i]-xs[j])**2+zs[j]**2)
            #theta = np.arccos(zs[j]/h)*57.2957795 #convert angle to degrees
            #print i.__str__() + ' : theta', theta
            #if (np.abs(theta-boat_angle) < epsilon): #compare with boat angle
            #    zm_rl[i] = h
                #print i.__str__() + ' : found, z=', zs[j]
            #    break
    
    #reverse order of xm_rl,zm_rl
    xm_rl = xm_rl[::-1]
    zm_rl = zm_rl[::-1]

    #zm_lr[zm_lr==0.0] = np.nan #convert no data points to nan's
    #zm_rl[zm_rl==0.0] = np.nan 

    #calculate cross sectional areas using trapezoidal rule
    print 'calculating csa'
    csa_t = np.trapz(zt_low,xt_low)
    csa_lr = np.trapz(zm_lr,xm_lr)
    csa_rl = np.trapz(zm_rl,xm_rl)
    
    #area difference in%
    csa_lr_perc = (csa_lr-csa_t)/csa_t * 100.0
    csa_rl_perc = (csa_rl-csa_t)/csa_t * 100.0

    #plot cross sections
    plt.figure()
    plt.plot(xt_low,-zt_low,'k',label='exact, csa='+csa_t.__str__().split('.')[0]+'.'+csa_t.__str__().split('.')[1][0:2]+' ft^2')
    plt.plot(xm_lr,-zm_lr,'g',label='survey L-R, error='+csa_lr_perc.__str__().split('.')[0]+'.'+csa_lr_perc.__str__().split('.')[1][0:2]+' %')
    plt.plot(xm_rl,-zm_rl,'b',label='survey R-L, error='+csa_rl_perc.__str__().split('.')[0]+'.'+csa_rl_perc.__str__().split('.')[1][0:2]+' %')
    plt.xlabel('Distance Across Section (ft)')
    plt.ylabel('Depth (ft)')
    plt.title('Lake ' + lake + ' : Section=' + section + ', Spd='+ boat_spd.__str__() + 'mph, Angle=' + boat_angle.__str__())
    plt.legend(loc=0)
    filename = 'Lk'+lake+'_'+section+'_'+boat_spd.__str__()+'mph_'+boat_angle.__str__()+'deg.png'
    plt.savefig('figures/'+filename)

    

