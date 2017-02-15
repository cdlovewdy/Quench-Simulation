# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 10:00:56 2017

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
#材料属性设置
def conductivity(T):
    return 38/95.8*(T-100)+40

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
T0=100
Tbound=4.2
#初始化
Tdis=np.array([T0]*M*N).reshape((N,M))
#迭代计算
for t in np.linspace(0+detat,10.0,10.0/detat):
    Kdish,Kdisv=conductivityUpgrad(Tdis,detax,detay)
    Tdish=np.c_[Tdis[:,0],Tdis,Tdis[:,-1]]
    detaTh=Tdish[:,1:]-Tdish[:,:-1]
    Tdisv=np.r_[(np.ones_like(Tdis[0,:])*4.2).reshape(1,-1),Tdis,(np.ones_like(Tdis[0,:])*4.2).reshape(1,-1)]
    detaTv=Tdisv[1:,:]-Tdisv[:-1,:]   
    Qleft=Kdish[:,:-1]*detaTh[:,:-1] 
    Qright=Kdish[:,1:]*detaTh[:,1:]
    Qupper=Kdisv[:-1,:]*detaTv[:-1,:]
    Qdown=Kdisv[1:,:]*detaTv[1:,:]
    volspe=volumespecificheat(Tdis)
    Tdistmp=Tdis+detat*(Qleft-Qright+Qdown-Qupper)/(volspe*detax*detay)
    Tdis=Tdistmp

print 'Calculation has been finished'
#绘制温度分布图
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False
plt.contourf(Tdis,extent=(0,0.5,0,0.2))
plt.show()
#取中心线上的温度分布
mid=(Tdis[:,499]+Tdis[:,500])/2
plt.plot(mid,'r-',lw=2)
plt.show()

