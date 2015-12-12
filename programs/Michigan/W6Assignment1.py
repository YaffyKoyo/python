import json
import urllib

url = raw_input('Enter location: ')

print 'Retrieving ', url



urlstr = urllib.urlopen(url).read()

info = json.loads(urlstr)
print 'Retrieved ', len(urlstr), 'characters'

Sum = 0
for item in info['comments']:
     Sum+=item["count"]
#     # print 'Name', item['name']
#     # print 'Id', item['id']
#     # print 'Attribute', item['x']
#
print 'Count: ', len(info['comments'])
print 'Sum: ', Sum
