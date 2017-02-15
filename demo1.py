# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 09:36:51 2017

@author: DaCheng
"""

import numpy as np
import matplotlib.pyplot as plt
#几何尺寸，空间步长及时间步长
M=1000
N=400
L1=0.5
L2=0.2
detax=L1/M
detay=L2/N
detat=1e-3
#材料属性设置
conductivity=4
specificheat=50
density=6.37e3
volumespecificheat=specificheat*density
#边界条件
T0=100
Tbound=4.2
#初始化
Tdis=np.array([T0]*M*N).reshape((N,M))
Kdish=np.array([conductivity]*(M+1)*N).reshape((N,M+1))
Kdisv=np.array([conductivity]*M*(N+1)).reshape((N+1,M))
#迭代计算
for t in np.linspace(0+detat,10.0,10.0/detat):
    Tdish=np.c_[Tdis[:,0],Tdis,Tdis[:,-1]]
    detaTh=Tdish[:,1:]-Tdish[:,:-1]
    Tdisv=np.r_[(np.ones_like(Tdis[0,:])*4.2).reshape(1,-1),Tdis,(np.ones_like(Tdis[0,:])*4.2).reshape(1,-1)]
    detaTv=Tdisv[1:,:]-Tdisv[:-1,:]   
    Qleft=Kdish[:,:-1]*detaTh[:,:-1] 
    Qright=Kdish[:,1:]*detaTh[:,1:]
    Qupper=Kdisv[:-1,:]*detaTv[:-1,:]
    Qdown=Kdisv[1:,:]*detaTv[1:,:]
    Tdistmp=Tdis+detat*(Qleft-Qright+Qdown-Qupper)/(volumespecificheat*detax*detay)
    Tdis=Tdistmp
    
print 'Calculation has been finished'
#绘制温度分布图
plt.contourf(Tdis,extent=(0,0.5,0,0.2))
plt.show()
#取中心线上的温度分布
mid=(Tdis[:,499]+Tdis[:,500])/2
    
