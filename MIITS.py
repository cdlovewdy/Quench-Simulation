# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 13:38:34 2017

@author: DaCheng
"""

import numpy as np
import material
from matplotlib import pyplot as plt
from scipy import integrate

#MIITS analysis
#input parameter:fcu,Acable
#output: MIITS to reach different temperature with different magnetfield

def NbTi_MIITs(Tend,fcu,acable,magnetfield,RRR):
    Tcs=9.2
    def Int(temp):
        res=(material.Copper_Cv(temp)*fcu+material.NbTi_Cv(temp)*(1-fcu))/material.Copper_Restivity(temp,RRR,magnetfield)
        return res
    MIITs=integrate.quad(Int,Tcs,Tend)[0]*fcu*acable**2/1e6
    return MIITs

def Nb3Sn_MIITs(Tend,fcu,acable,magnetfield,RRR):
    Tcs=16
    def Int(temp):
        res=(material.Copper_Cv(temp)*fcu+material.Nb3Sn_Cv(temp)*(1-fcu))/material.Copper_Restivity(temp,RRR,magnetfield)
        return res
    MIITs=integrate.quad(Int,Tcs,Tend)[0]*fcu*acable**2/1e6
    return MIITs

Tend=np.linspace(16,300,30)
MIITS0=[]
MIITS3=[]
MIITS6=[]
MIITS9=[]
MIITS12=[]
for temp in Tend:
    MIITS0.append(Nb3Sn_MIITs(temp,0.5,13.64e-6,12.473,200))
    MIITS3.append(Nb3Sn_MIITs(temp,0.5,9.1e-6,8.3913,200))
#    MIITS6.append(Nb3Sn_MIITs(temp,0.5,10.95e-6,6,200))
#    MIITS9.append(Nb3Sn_MIITs(temp,0.5,10.95e-6,9,200))
#    MIITS12.append(Nb3Sn_MIITs(temp,0.5,10.95e-6,12,200))
plt.figure(1)
plt.plot(MIITS0,Tend,'ro-')
plt.xlabel('MIITs')
plt.ylabel('Temperature')
plt.title('IHEPW4 MIITs curve(12.473 T)')
#plt.plot(MIITS3,Tend,'go-')
#plt.plot(MIITS6,Tend,'yo-')
#plt.plot(MIITS9,Tend,'bo-')
#plt.plot(MIITS12,Tend,'ko-')
plt.grid()
plt.show()
plt.figure(2)
plt.plot(MIITS3,Tend,'ro-')
plt.xlabel('MIITs')
plt.ylabel('Temperature')
plt.title('IHEPW5 MIITs curve(8.3913 T)')
#plt.plot(MIITS3,Tend,'go-')
#plt.plot(MIITS6,Tend,'yo-')
#plt.plot(MIITS9,Tend,'bo-')
#plt.plot(MIITS12,Tend,'ko-')
plt.grid()
plt.show()