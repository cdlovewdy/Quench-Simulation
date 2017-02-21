# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 15:43:37 2017

@author: DaCheng
"""

import numpy as np
from matplotlib import pyplot as plt


#copper properties, including mass density,electrical resistivity,thermal conducitiity and specific heat
#the property changes by the temperature,RRR and magnet field
#the function is from NIST and CUDI
 
#unit: kg/m^3  
def Copper_Density(temp):
    return 8960

#unit: ohm*m
def Copper_Restivity(temp,rrr,magnetfield=0):
    MR=0.5e-10
    resistivity=1e-8*pow(1.7/rrr+(2.32547e9/pow(temp,5)+9.57137e5/pow(temp,3)+1.62735e2/temp),-1)+MR*magnetfield
    return resistivity

#unit: W/mK    
def Copper_Conductivity(temp,rrr,magnetfield=0):
    beta=0.634/rrr
    betar=beta/0.0003
    P1=1.754e-8
    P2=2.763
    P3=1102
    P4=-0.165
    P5=70
    P6=1.756
    P7=0.838/pow(betar,0.1661)
    W0=beta/temp
    Wi=P1*pow(temp,P2)/(1+P1*P3*pow(temp,(P2+P4))*np.exp(-pow(P5/temp,P6)))
    Wi0=P7*Wi*W0/(Wi+W0)
    conductivity=1/(W0+Wi+Wi0)
    conductivity=conductivity*Copper_Restivity(temp,rrr,0)/Copper_Restivity(temp,rrr,magnetfield)
    return conductivity

#unit: J/m^3K    
def Copper_Cv(temp):
    a0=-1.91844
    a1=-0.15973
    a2=8.61013
    a3=-18.996
    a4=21.9661
    a5=-12.7328
    a6=3.54322
    a7=-0.3797
    cons=2.30258509299405
    N=a0+a1*np.log(temp)/cons+a2*pow(np.log(temp)/cons,2)+a3*pow(np.log(temp)/cons,3)+a4*pow(np.log(temp)/cons,4)+a5*pow(np.log(temp)/cons,5)+a6*pow(np.log(temp)/cons,6)+a7*pow(np.log(temp)/cons,7)
    specificheat=10**N
    return specificheat*8960

#Niobium-Titanium properties, including mass density,specific heat
#the property changes by the temperature
#the function is from NIST

#unit: kg/m^3 
def NbTi_Density(temp):
    return 6000

#unit: J/m^3K 
def NbTi_Cv(temp):
    beta=0.0023
    gamma=0.145
    if temp<31.9985:
        cp=beta*temp**3+gamma*temp
    elif temp<300:
        cp=(0.24*temp**3-160*temp**2+36149*temp-520779)/6000
    else:
        cp=(0.24*300**3-160*300**2+36149*300-520779)/6000
    return cp*6000

#Niobium-Tin properties, including mass density,specific heat
#the property changes by the temperature
#the function is from NIST

#unit: kg/m^3 
def Nb3Sn_Density(temp):
    return 8950
    
#unit: J/m^3K 
def Nb3Sn_Cv(temp,sc=0,magnetfield=0):
    gamma=0.139
    beta=0.001239
    if temp>20:
        a0=79.78547
        a1=-247.44839
        a2=305.01434
        a3=-186.90995
        a4=57.48133
        a5=-6.3977
        a6=-0.6827738
        a7=0.1662252
        cons=2.30258509299405
        N=a0+a1*np.log(temp)/cons+a2*pow(np.log(temp)/cons,2)+a3*pow(np.log(temp)/cons,3)+a4*pow(np.log(temp)/cons,4)+a5*pow(np.log(temp)/cons,5)+a6*pow(np.log(temp)/cons,6)+a7*pow(np.log(temp)/cons,7)
        specificheat=10**N
    elif sc==0:
        specificheat=beta*temp**3+gamma*temp
    else:
        Tc0=16
        Bc20=29.38
        specificheat=(beta+3*gamma/(Tc0*Tc0))*temp**3+gamma*(magnetfield/Bc20)*temp
    return specificheat*8950

#Kapton properties, including mass density,thermal conductivity,specific heat
#the property changes by the temperature
#the function is from NIST

#unit: kg/m^3 
def Kapton_Density(temp):
    return 1420

#unit: W/mK    
def Kapton_Conductivity(temp):
    if temp>=4:
        a0=5.73101
        a1=-39.5199
        a2=79.9313
        a3=-83.8572
        a4=50.9157
        a5=-17.9835
        a6=3.42413
        a7=-0.27133
        cons=2.30258509299405
        N=a0+a1*np.log(temp)/cons+a2*pow(np.log(temp)/cons,2)+a3*pow(np.log(temp)/cons,3)+a4*pow(np.log(temp)/cons,4)+a5*pow(np.log(temp)/cons,5)+a6*pow(np.log(temp)/cons,6)+a7*pow(np.log(temp)/cons,7)
        conductivity=10**N
    else:
        conductivity=0.00378+0.00161*temp
    return conductivity
 
#unit: J/m^3K    
def Kapton_Cv(temp):
    a0=-1.3684
    a1=0.65892
    a2=2.8719
    a3=0.42651
    a4=-3.0088
    a5=1.9558
    a6=-0.51998
    a7=0.051574
    cons=2.30258509299405
    N=a0+a1*np.log(temp)/cons+a2*pow(np.log(temp)/cons,2)+a3*pow(np.log(temp)/cons,3)+a4*pow(np.log(temp)/cons,4)+a5*pow(np.log(temp)/cons,5)+a6*pow(np.log(temp)/cons,6)+a7*pow(np.log(temp)/cons,7)
    specificheat=10**N
    return specificheat*1420     
  
#G10 properties, including mass density,thermal conductivity,specific heat
#the property changes by the temperature
#the function is from NIST

#unit: kg/m^3 
def G10_Density(temp):
    return 1800

#unit: W/mK    
def G10_Conductivity_normal(temp):
    a0=-4.1236
    a1=13.788
    a2=-26.068
    a3=26.272
    a4=-14.663
    a5=4.4954
    a6=-0.6905
    a7=0.0397
    cons=2.30258509299405
    N=a0+a1*np.log(temp)/cons+a2*pow(np.log(temp)/cons,2)+a3*pow(np.log(temp)/cons,3)+a4*pow(np.log(temp)/cons,4)+a5*pow(np.log(temp)/cons,5)+a6*pow(np.log(temp)/cons,6)+a7*pow(np.log(temp)/cons,7)
    conductivity=10**N
    return conductivity
 
#unit: W/mK    
def G10_Conductivity_parallel(temp):
    a0=-2.6487
    a1=8.80228
    a2=-24.8998
    a3=41.1625
    a4=-39.8754
    a5=23.1778
    a6=-7.95635
    a7=1.48806
    a8=-0.11701
    cons=2.30258509299405
    N=a0+a1*np.log(temp)/cons+a2*pow(np.log(temp)/cons,2)+a3*pow(np.log(temp)/cons,3)+a4*pow(np.log(temp)/cons,4)+a5*pow(np.log(temp)/cons,5)+a6*pow(np.log(temp)/cons,6)+a7*pow(np.log(temp)/cons,7)+a8*pow(np.log(temp)/cons,8)
    conductivity=10**N
    return conductivity
    
#unit: J/m^3K    
def G10_Cv(temp):
    a0=-2.4083
    a1=7.6006
    a2=-8.2982
    a3=7.3301
    a4=-4.2386
    a5=1.4294
    a6=-0.24396
    a7=0.015236
    cons=2.30258509299405
    N=a0+a1*np.log(temp)/cons+a2*pow(np.log(temp)/cons,2)+a3*pow(np.log(temp)/cons,3)+a4*pow(np.log(temp)/cons,4)+a5*pow(np.log(temp)/cons,5)+a6*pow(np.log(temp)/cons,6)+a7*pow(np.log(temp)/cons,7)
    specificheat=10**N
    return specificheat*1800     
#Test for the material function
if __name__=='__main__':
    RRR=100
    temp=np.linspace(4,300)
    cu_res=map(Copper_Restivity,temp,RRR*np.ones_like(temp))
    cu_con=map(Copper_Conductivity,temp,RRR*np.ones_like(temp))
    cu_cv=map(Copper_Cv,temp)
    nbti_cv=map(NbTi_Cv,temp)
    nb3sn_cv=map(Nb3Sn_Cv,temp)
    kapton_con=map(Kapton_Conductivity,temp)
    kapton_cv=map(Kapton_Cv,temp)
    g10_con_nor=map(G10_Conductivity_normal,temp)
    g10_con_par=map(G10_Conductivity_parallel,temp)
    g10_cv=map(G10_Cv,temp)
    plt.figure(1)
    plt.plot(temp,cu_res,'ro-')
    plt.title('Copper_Restivity')
    plt.xlabel('Temperture')
    plt.ylabel('Restivity')
    plt.grid()
    plt.show()
    plt.figure(2)
    plt.plot(temp,cu_con,'ro-')
    plt.title('Copper_Conductivity')
    plt.xlabel('Temperture')
    plt.ylabel('Conductivity')
    plt.grid()
    plt.show()      
    plt.figure(3)
    plt.plot(temp,cu_cv,'ro-')
    plt.title('Copper_Specific')
    plt.xlabel('Temperture')
    plt.ylabel('Cv')
    plt.grid()
    plt.show() 
    plt.figure(4)
    plt.plot(temp,nbti_cv,'ro-')
    plt.title('NbTi_Specific')
    plt.xlabel('Temperture')
    plt.ylabel('Cv')
    plt.grid()
    plt.show() 
    plt.figure(5)
    plt.plot(temp,nb3sn_cv,'ro-')
    plt.title('Nb3Sn_Specific')
    plt.xlabel('Temperture')
    plt.ylabel('Cv')
    plt.grid()
    plt.show() 
    plt.figure(6)
    plt.plot(temp,kapton_con,'ro-')
    plt.title('Kapton_Conductivity')
    plt.xlabel('Temperture')
    plt.ylabel('Conductivity')
    plt.grid()
    plt.show()
    plt.figure(7)
    plt.plot(temp,kapton_cv,'ro-')
    plt.title('Kapton_Specific')
    plt.xlabel('Temperture')
    plt.ylabel('Cv')
    plt.grid()
    plt.show()
    plt.figure(8)
    plt.plot(temp,g10_con_nor,'ro-',label='normal')
    plt.plot(temp,g10_con_par,'g*-',label='parallel')
    plt.legend(loc='lower right')
    plt.title('G10_Conductivity')
    plt.xlabel('Temperture')
    plt.ylabel('Conductivity')
    plt.grid()
    plt.show()
    plt.figure(8)
    plt.plot(temp,g10_cv,'ro-')
    plt.title('G10_Specific')
    plt.xlabel('Temperture')
    plt.ylabel('Cv')
    plt.grid()
    plt.show()