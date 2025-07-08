#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 10:36:28 2025

@author: lget
"""

import numpy as np
x = np.arange(0,10.1,0.1)
y1=x*x
y2=x**2*np.sin(x) # note that ** raises each element to a power, in this case 2.
#just for fun, lets plot y1 and y2 relative to x using matplotlib (we’ll do more on that later)
import matplotlib.pyplot as plt
plt.plot(x,y1,"r*")
plt.plot(x,y2,"g")
plt.show()