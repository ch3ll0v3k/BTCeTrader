#!/usr/bin/python
######################################################################################
import urllib2
import time
import sys, os, json


from BeautifulSoup import BeautifulSoup

######################################################################################
HEADERS = {
    "User-Agent"        : "Mozilla/5.0 (Win-32; rv:24.0) Gecko/20140723 Firefox/24.0 Iceweasel/24.7.0",
    "Accept"            : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language"   : "en-US,en;q=0.5",
    "Referer"           : "https://btc-e.com/",
    "Connection"        : "keep-alive",
    "Cache-Control"     : "max-age=0",
    "Cookie"            : ""
}

sys.argv.remove(__file__);
args = sys.argv;

URL  = "https://btc-e.com/"

CHAT_LANGS = [ "en", "ru", "cn" ];

HEADERS["Cookie"] = "chatRefresh=1; locale="+CHAT_LANGS[1]+";"

################################################################################
req = urllib2.Request(URL, headers=HEADERS);
RAW_RESPONSE = urllib2.urlopen(req).read();

t = time.gmtime();
TIME = str(t.tm_mday)+"-"+str(t.tm_mon)+"-"+str(t.tm_year)+" / "+str(t.tm_hour)+":"+str(t.tm_min)+":"+str(t.tm_sec);

######################################################################################
parsed_html = BeautifulSoup( RAW_RESPONSE );

# pure text NO-TAGS
#print parsed_html.body.find('div', attrs={'id':'nChat'}).text

# Pretty-HTML
#print parsed_html.body.find('div', attrs={'id':'nChat'}).prettify();

#print parsed_html.body.find('div', attrs={'id':'nChat'}).find(id="chatmessage");
CHAT = parsed_html.body.find('div', attrs={'id':'nChat'});
for data in CHAT:
    print("--------------------------------------------------")
    print(data["id"]+" :: "+data.a["title"]+" :: "+data.a.string); 
    print(data.span.string); 


# cat data/config/BTCeTrader.json | python -m json.tool
# python -m json.tool data/config/BTCeTrader.json


######################################################################################
