# Note - this code must run in Python 2.x and you must download
# http://www.pythonlearn.com/code/BeautifulSoup.py
# Into the same folder as this program

import urllib
from BeautifulSoup import *

url = raw_input('Enter - ')
html = urllib.urlopen(url).read()

soup = BeautifulSoup(html)

# Retrieve all of the anchor tags
count  = 0;
Sum = 0;
tags = soup('span')
for tag in tags:
    # Look at the parts of a tag
    # print 'TAG:',tag
    # print 'URL:',tag.get('href', None)
    # print 'Contents:',tag.contents[0]
    count+=1
    Sum+=int(tag.contents[0])
print 'Count ', count
print 'Sum ', Sum
    #print 'Attrs:',tag.attr
