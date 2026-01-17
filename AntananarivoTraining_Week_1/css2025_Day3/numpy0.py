#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 09:46:35 2025

@author: lget
"""
import numpy as np
x = np.arange(-0.1,0.5,0.007)
print(x)


x1 = np.linspace(0,10.0,30)
print(x1)

a = [1,2,3]
aa=np.array(a)
print(aa)

b = [[1,2,3],[4,5,6],[7,8,-1]]
bb=np.array(b)
print(bb)

#Now, if you want to find the inverse matrix of bb, first check if its possible:
cc = np.linalg.inv(bb)
print(cc)

#Numpy arithmetic
p=np.array([1,2,3])
q=np.array([-3,-4,-5])
r=p+q
s=p-q
print(r) 
print(s)
print(p.size)
print(p.shape)
print(p.ndim)

p2d=np.reshape(p,[1,3])
print(p2d)