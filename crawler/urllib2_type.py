# import cookielib, urllib2
#
# url = "http://www.baidu.com"
#
# print 'first type'
#
# response1 = urllib2.urlopen(url)
# print response1.getcode()
# print len(response1.read())
#
# print 'second type'
# request = urllib2.Request(url)
# request.add_header("user-agent","Mozilla/5.0")
# response2 = urllib2.urlopen(request)
# print response2.getcode()
# print len(response2.read())
#
# print 'third type'
#
# cj = cookielib.CookieJar()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# urllib2.install_opener(opener)
# response3 = urllib2.urlopen(url)
# print response3.getcode()
# print cj
# print len(response3.read())


#coding:utf-8
import urllib2
import cookielib
url = "http://www.baidu.com"
print 'hehehe'
response1 = urllib2.urlopen(url)
print response1.getcode()
print len(response1.read())

print "hehehe"
request = urllib2.Request(url)
request.add_header("user-agent", "Mozilla/5.0")
response2 = urllib2.urlopen(request)
print response2.getcode()
print len(response2.read())

print "hehehe"
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
response3= urllib2.urlopen(url)
print response3.getcode()
print cj
print response3.read()
