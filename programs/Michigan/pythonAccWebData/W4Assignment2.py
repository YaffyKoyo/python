# Note - this code must run in Python 2.x and you must download
# http://www.pythonlearn.com/code/BeautifulSoup.py
# Into the same folder as this program

import urllib
from BeautifulSoup import *

url = raw_input('Enter URL- ')
count = int(raw_input('Enter Count - '))
position = int(raw_input('Enter position - '))
print url

for i in range(count):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)

    tags = soup('a')
    tempPos = position
    for tag in tags:
        if(tempPos==1):
            if (i==count-1):
                print 'Last Url: ', tag.get('href', None)
            else: print 'Retrieving: ', tag.get('href', None)
            url = tag.get('href', None)
            break;
        tempPos-=1
