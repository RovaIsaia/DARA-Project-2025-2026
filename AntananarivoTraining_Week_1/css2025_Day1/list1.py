#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 12:34:27 2025

@author: lget
"""

C2 = "M"
C3 = "M"
C4 = "F"
print(C2)
print(C3)
print(C4)

gender = ["M","M","F","M","F","F","F","M","M","F","M"]
print(gender[0])
print(gender[1])
print(gender[2])
print(gender[-1])


# country list
country = ["South Africa","Botswana","South Africa","South Africa","Kenya","Mozambique","Lesotho","Kenya","Kenya","Egypt","Sudan"]
print(country)
print(country[0])
print(country[5])


# Data Storage With Lists
my_list = [42, -2021, 6.283,"tau", "node"]
print(my_list)


# Data Storage With Lists
my_list = [42, -2021, 6.283,"tau", "node"]
print(my_list) 
print(my_list[:])

my_list.append("pi")
print(my_list)

my_list.insert(1,"pi2")
print(my_list)

my_list.remove("pi")
my_list.remove("pi2")
my_list.remove("tau")
print(my_list)
print(len(my_list))

# View a certain range of items:
print(my_list[0:3])