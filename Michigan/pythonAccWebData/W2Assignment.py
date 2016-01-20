import re

cc = sum([int(i) for i in re.findall('[0-9]+',open('regex_sum_199166.txt').read())]);

kk = re.findall('[0-9]+',open('regex_sum_199166.txt').read())
sum = 0
number = 0
for i in range(len(kk)):
    sum+=int(kk[i])
    number+=1
print cc
