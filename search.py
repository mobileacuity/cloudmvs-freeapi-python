#!/usr/bin/python
#
# A simple python script demonstrating how to search against Mobile Acuity's Free API Service with request signing
#
import binascii
import hashlib
import hmac
import json
import sys
import time
import urllib2
  
if len(sys.argv)!=3:
    print "Usage: search.py <dataset> <queryimage>"
    print "    <dataset> is the last part of the Search URL in your service settings."
else:
    query_image=open(sys.argv[2],"rb").read()
    IDENTITY="test"
    SECRET="testsecret"
    DATE=time.strftime("%a, %d %b %Y %H:%M:%S %z", time.gmtime())
    SIZE=len(query_image)
    STS=IDENTITY+"POSThttp://api.mobileacuity.net/v1/search/test/"+sys.argv[1]+DATE+str(SIZE)
    SIG=binascii.b2a_base64(hmac.new(SECRET,STS,hashlib.sha1).digest())[:-1]
    headers={"Content-Type" : "image/jpeg", "Accept" : "application/json", "Authorization" : "MAAPIv1 test "+SIG, "Date" : DATE}
    request=urllib2.Request("http://api.mobileacuity.net/v1/search/test/"+sys.argv[1],query_image,headers)
    response=urllib2.urlopen(request)
    result=json.loads(response.read())
    for r in result:
        print "Result:", r['r']
        print "    ID:", r['r0']
        print " Score:", r['s']
        print "Centre:", r['c']
