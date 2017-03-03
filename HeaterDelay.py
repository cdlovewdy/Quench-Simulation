# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 09:57:20 2017

@author: DaCheng
"""

import numpy as np
from material import *

width=50e-6
tCable=50e-6
tKapton=100e-6
tHeater=100e-6
tOkapton=50e-6
detax=10e-6
cusc=1.0
numx=np.int(width/detax)
numOkapton=np.int(tOkapton/detax)
numHeater=np.int(tHeater/detax)
numKapton=np.int(tKapton/detax)
numCable=np.int(tCable/detax)
numy=numCable+numHeater+numKapton+numOkapton
Tdis=np.ones(numx*numy).reshape((numy,numx))*4.2
detat=1e-10
def cond(Tdis):
    condOkapton=Kapton_Conductivity(Tdis[:numOkapton,:])
    condHeater=SS_Conductivity(Tdis[numOkapton:numOkapton+numHeater,:])
    condKapton=Kapton_Conductivity(Tdis[numOkapton+numHeater:numOkapton+numHeater+numKapton,:])
    condCable=Copper_Conductivity(Tdis[numOkapton+numHeater+numKapton:numy,:],np.ones_like(Tdis[numOkapton+numHeater+numKapton:numy,:])*200)
    cond=np.concatenate((condOkapton,condHeater,condKapton,condCable))
    return cond

def condUpgrade(Tdis):
    conduct0=cond(Tdis)
    conductl=conduct0[:,:-1]
    conductr=conduct0[:,1:]
    conducth=np.c_[detax/(detax/(2*conduct0[:,0])),detax/(detax/(2*conductl)+detax/(2*conductr)),detax/(detax/(2*conduct0[:,-1]))]
    conductu=conduct0[:-1,:]
    conductd=conduct0[1:,:]
    conductv=np.r_[detax/(detax/(2*conduct0[0,:])).reshape(1,-1),detax/(detax/(2*conductu)+detax/(2*conductd)),detax/(detax/(2*conduct0[-1,:])).reshape(1,-1)]
    return conducth,conductv

def cvUpgrade(Tdis):
    cvOkapton=Kapton_Cv(Tdis[:numOkapton,:])
    cvHeater=SS_Cv(Tdis[numOkapton:numOkapton+numHeater,:])
    cvKapton=Kapton_Cv(Tdis[numOkapton+numHeater:numOkapton+numHeater+numKapton,:])
    tempCable=Tdis[numOkapton+numHeater+numKapton:numy,:]
    cvCable=(1.0/(cusc+1))*Nb3Sn_Cv_sc(tempCable,12)+(cusc/(cusc+1))*Copper_Cv(tempCable)
    cv=np.concatenate((cvOkapton,cvHeater,cvKapton,cvCable))
    return cv

t=0
i=0
while t<0.05:
    tcable=Tdis[numOkapton+numHeater+numKapton:numy,:]
    theater=Tdis[numOkapton:numOkapton+numHeater,:]
    if i%1000==0:
        print 'Now time ',t
        print 'Nb3Sn maximum temperature ',tcable.max()
        print 'Heater maximum temperature ',theater.max()
#    print Tdis[49,0],Tdis[50,0],Tdis[51,0],Tdis[52,0]
        print'===================================================='
    if tcable.max()>12:
        break
    Kdish,Kdisv=condUpgrade(Tdis)
#    Tdish=np.c_[Tdis[:,0],Tdis,Tdis[:,-1]]
    detaTh=np.c_[np.zeros_like(Tdis[:,0]),Tdis[:,1:]-Tdis[:,:-1],np.zeros_like(Tdis[:,0])]
#    Tdisv=np.r_[(np.ones_like(Tdis[0,:])*4.2).reshape(1,-1),Tdis,(np.ones_like(Tdis[0,:])*4.2).reshape(1,-1)]
    detaTv=np.r_[Tdis[0,:]-(np.ones_like(Tdis[0,:]).reshape(1,-1))*4.2,Tdis[1:,:]-Tdis[:-1,:],np.zeros_like(Tdis[0,:]).reshape(1,-1)]  
    Qleft=Kdish[:,:-1]*detaTh[:,:-1] 
    Qright=Kdish[:,1:]*detaTh[:,1:]
    Qupper=Kdisv[:-1,:]*detaTv[:-1,:]
    Qdown=Kdisv[1:,:]*detaTv[1:,:]
    hgen=np.zeros_like(Tdis)
    hgen[numOkapton:numOkapton+numHeater,:]=1e10
    cv=cvUpgrade(Tdis)
    #adaptive timestep
    Ksum=Kdish[:,:-1]+Kdish[:,1:]+Kdisv[:-1,:]+Kdisv[1:,:]
    detat=0.99*(cv*detax*detax/Ksum).min()
    Q=-Qleft+Qright+Qdown-Qupper+hgen*detax*detax
    detaT=detat*Q/(cv*detax*detax)
    Tdis =Tdis+detaT
    t+=detat
    i+=1
    
