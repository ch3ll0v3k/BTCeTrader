#!/usr/bin/python 
####################################################################################
import json, time, os, sys, urllib2
from datetime import datetime
####################################################################################

_headers = {
        "User-Agent": "Mozilla/5.0 (Win-32; rv:24.0) Gecko/20140723 Firefox/24.0 Iceweasel/24.7.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "http://from-here.com/",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0"
}

################################################################################
#print(datetime.datetime.fromtimestamp( int("1284101485") ).strftime('%Y-%m-%d %H:%M:%S') )
#print(datetime.datetime.utcfromtimestamp( int("1284101485") ).strftime('%Y-%m-%d %H:%M:%S')

_SERVER = "https://cex.io/api/price_stats/LTC/USD"
_POST_DATA   = "lastHours=240&maxRespArrSize=1000";



req = urllib2.Request(_SERVER, _POST_DATA, _headers)


JSON_DATA = json.loads(urllib2.urlopen(req).read());

for data in JSON_DATA:
    print(datetime.utcfromtimestamp( int(data["tmsp"]) ).strftime('%Y-%m-%d %H:%M:%S')+" : "+data["price"] )




####################################################################################
