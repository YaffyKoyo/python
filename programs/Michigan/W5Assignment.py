import urllib
import xml.etree.ElementTree as ET

url = raw_input('Enter location: ')

print 'Retrieving ', url



urlstr = urllib.urlopen(url).read()
comments = ET.fromstring(urlstr)
lst = comments.findall('comments/comment')
Sum = 0
for item in lst:
    Sum+=int(item.find('count').text)

print 'Retrieved',len(urlstr),'characers'
print 'Count: ', len(lst)
print 'Sum: ', Sum
