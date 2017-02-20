# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 09:44:54 2017

@author: DaCheng
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
#几何尺寸，空间步长及时间步长
M=1000
N=400
L1=0.5
L2=0.2
detax=L1/M
detay=L2/N
detat=1e-3
lh1=0.1
lh2=0.2
#材料属性设置
def conductivity(T):
    T=np.select([T<4.2,T<100,T>=100],[2,38/95.8*(T-100)+40,40])
    return T

def specificheat(T):
    return 94/95.8*(T-100)+100
    

density=6.37e3

def volumespecificheat(T):
    return specificheat(T)*density

def conductivityUpgrad(Tdis,detax,detay):
    conduct0=conductivity(Tdis)
    conductl=conduct0[:,:-1]
    conductr=conduct0[:,1:]
    conducth=np.c_[detay/(detax/(2*conduct0[:,0])),detay/(detax/(2*conductl)+detax/(2*conductr)),detay/(detax/(2*conduct0[:,-1]))]
    conductu=conduct0[:-1,:]
    conductd=conduct0[1:,:]
    conductv=np.r_[detax/(detay/(2*conduct0[0,:])).reshape(1,-1),detax/(detay/(2*conductu)+detay/(2*conductd)),detax/(detay/(2*conduct0[-1,:])).reshape(1,-1)]
    return conducth,conductv
    
#边界条件
T0=4.2
Tbound=4.2
#初始化
Tdis=np.array([T0]*M*N).reshape((N,M))
i=0
a=[]
b=[]
#迭代计算
for t in np.linspace(0+detat,5.0,5.0/detat):
    Kdish,Kdisv=conductivityUpgrad(Tdis,detax,detay)
    Tdish=np.c_[Tdis[:,0],Tdis,Tdis[:,-1]]
    detaTh=Tdish[:,1:]-Tdish[:,:-1]
    Tdisv=np.r_[(np.ones_like(Tdis[0,:])*4.2).reshape(1,-1),Tdis,(np.ones_like(Tdis[0,:])*4.2).reshape(1,-1)]
    detaTv=Tdisv[1:,:]-Tdisv[:-1,:]   
    Qleft=Kdish[:,:-1]*detaTh[:,:-1] 
    Qright=Kdish[:,1:]*detaTh[:,1:]
    Qupper=Kdisv[:-1,:]*detaTv[:-1,:]
    Qdown=Kdisv[1:,:]*detaTv[1:,:]
    hgen=np.ones_like(Tdis)*1e6
    hgen[:,:int(lh1/detax)+1]=0
    #    hgen[:,-int(lh2/detax):]=1e6
    volspe=volumespecificheat(Tdis)
    Q=-Qleft+Qright+Qdown-Qupper+hgen*detax*detay
#    print Q[20,200],Q[20,201]
    detaT=detat*Q/(volspe*detax*detay)
#    print detaT[20,200],detaT[20,201]
    Tdistmp=Tdis+detaT
    if sum(sum((Tdis-Tdistmp)**2))<1e-4:
        print 'breaking time is ',t
        break
    Tdis=Tdistmp
    i+=1
    a.append(Tdis.max())
    b.append(Tdis.min())
#    print Tdis[20,200],Tdis[20,201]

#print 'Calculation has been finished'
##绘制温度分布图
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False
plt.contourf(Tdis,extent=(0,0.5,0,0.2))
plt.show()
##取中心线上的温度分布
#mid=(Tdis[:,499]+Tdis[:,500])/2
#plt.plot(mid,'r-',lw=2)
#plt.show()
#Kdish,Kdisv=conductivityUpgrad(Tdis,detax,detay)
#Tdish=np.c_[Tdis[:,0],Tdis,Tdis[:,-1]]
#detaTh=Tdish[:,1:]-Tdish[:,:-1]
#Tdisv=np.r_[(np.ones_like(Tdis[0,:])*4.2).reshape(1,-1),Tdis,(np.ones_like(Tdis[0,:])*4.2).reshape(1,-1)]
#detaTv=Tdisv[1:,:]-Tdisv[:-1,:]   
#Qleft=Kdish[:,:-1]*detaTh[:,:-1] 
#Qright=Kdish[:,1:]*detaTh[:,1:]
#Qupper=Kdisv[:-1,:]*detaTv[:-1,:]
#Qdown=Kdisv[1:,:]*detaTv[1:,:]
#hgen=np.ones_like(Tdis)*1e4
#hgen[:,:int(lh1/detax)+1]=0
##    hgen[:,-int(lh2/detax):]=1e6
#volspe=volumespecificheat(Tdis)
#Q=Qleft-Qright+Qdown-Qupper+hgen*detax*detay
#Tdistmp=Tdis+detat*Q/(volspe*detax*detay)
##    if sum(sum((Tdis-Tdistmp)**2))<1e-4:
##        print 'breaking time is ',t
##        break
#Tdis=Tdistmp
#print Q.max(),Tdis.max()
