#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:00:39 2020

@author: marc
"""

import numpy as np

f = open("input-day01", 'r')
nbrs = np.asarray(f.read().splitlines(), dtype='int')

for c1, n in enumerate(nbrs):
    for c2, m in enumerate(nbrs[c1:]):
        for k in nbrs[c1+c2:]:
            if (n+m+k == 2020):
                print('Numbers are', n, m, k, 'with product:', n*m*k)

f.close()    
