# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import re

string = 'Why should you learn to write programs? 7746 12 1929 8827 Writing programs (or programming) is a very creative 7 and rewarding activity.  You can write programs for many reasons, ranging from making your living to solving8837 a difficult data analysis problem to having fun to helping 128someone else solve a problem.  This book assumes that everyone needs to know how to program ...'

kk = re.findall('[0-9]+',string)
sum = 0
for i in range(len(kk)):
    sum+=int(kk[i])
print sum