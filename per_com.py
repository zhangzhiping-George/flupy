#!/usr/bin/env python
#coding: utf-8
'''
1, 2, 3, 4 四个数字生成数字不重复的三位数

for i in range(1, 5):
    for j in range(1, 5):
        for k in range(1, 5):
            if (i != k) and ( k != j) and (j != i):
                print(i,j,k)

per_com_list = [i*100 + j*10 + k for i in lnum for j in lnum for k in lnum if i != j != k != i ]
print per_com_list
'''
from itertools import permutations
lnum = [1, 2, 3, 4]
for i in permutations('1234', 3):
    val = '%s%s%s' % (i[0], i[1], i[2])
    print int(val)

