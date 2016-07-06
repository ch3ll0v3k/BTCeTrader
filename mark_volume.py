#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# Built IN
import sys, json, time, os, math, subprocess
import httplib, urllib, urllib2, hashlib, hmac
from random import randint
from threading import Timer
from sys import stdout
from time import sleep
from datetime import datetime

###################################################################################################

PAIRS = ["ltc_usd"];

_URL = "https://btc-e.com/api/3/depth/|<>PAIRS<>|?limit=150".replace("|<>PAIRS<>|", PAIRS[0] );

req = urllib2.Request( _URL );

RAW_RESPONSE =urllib2.urlopen(req).read();


JSON = json.loads(RAW_RESPONSE);

#print(json.dumps( JSON , sort_keys=True, indent=4, separators=(',', ': ')));



STEP = 0.01;

MARKT_VOL = {

    "ask" : [],
    "bid" : []

};



print("JSON LEN: "+str(len(JSON["ltc_usd"]["asks"])));


for pair in JSON:

    # ---------------------------------------------------------------------------
    # ASKS

    skip_fs_step = True;
    curr_buy_index = 0;

    AX = str(JSON[ pair ]["asks"][0][0]).split(".");
    SEARCH = float("{:.2f}".format( float(AX[0]+"."+AX[1][0:2]) ));
    MARKT_VOL["ask"].append( [ SEARCH, JSON[ pair ]["asks"][0][1] ] );

    for i in xrange( 0, len(JSON[ pair ]["asks"]) ):

        if skip_fs_step:
            skip_fs_step = False;
            continue;

        if float("{:.2f}".format( SEARCH + STEP )) < JSON[ pair ]["asks"][i][0]:

            SEARCH = float("{:.2f}".format( SEARCH + STEP ))            
            MARKT_VOL["ask"].append( [ SEARCH, JSON[ pair ]["asks"][i][1] ] );
            curr_buy_index += 1;

        else:

            MARKT_VOL["ask"][ curr_buy_index ][1] += JSON[ pair ]["asks"][i][1];

    # ---------------------------------------------------------------------------
    # BID

    skip_fs_step = True;
    curr_sell_index = 0;

    SEARCH = float("{:.2f}".format( JSON[ pair ]["bids"][0][0]  ));
    MARKT_VOL["bid"].append( [ SEARCH, JSON[ pair ]["bids"][0][1] ] );


    for i in xrange( 0, len(JSON[ pair ]["bids"]) ):

        if skip_fs_step:
            skip_fs_step = False;
            continue;

        if float("{:.2f}".format( SEARCH-STEP)) > JSON[ pair ]["bids"][i][0]:

            SEARCH = float("{:.2f}".format( SEARCH - STEP ));
            MARKT_VOL["bid"].append( [ SEARCH, JSON[ pair ]["bids"][i][1] ] );
            curr_sell_index += 1;

        else:

            MARKT_VOL["bid"][ curr_sell_index ][1] += JSON[ pair ]["bids"][i][1];



###################################################################################################
print("----------------------------------------------");
LEN = len(MARKT_VOL["ask"]);
print(" MARKT_VOL (ASK) ->  TTL: "+str(LEN));

for i in xrange(0, LEN ):


    A = "{:7.8f}".format( MARKT_VOL["ask"][i][0] ).strip();
    B = "{:7.8f}".format( MARKT_VOL["ask"][i][1] ).strip();

    print(" @: [ {0:15} ] -> [ {1:15} ]".format( A, B ) );


print("----------------------------------------------");
LEN = len(MARKT_VOL["bid"]);
print(" MARKT_VOL (BID) ->  TTL: "+str(LEN));

for i in xrange(0, LEN ):

    A = "{:7.8f}".format( MARKT_VOL["bid"][i][0] ).strip();
    B = "{:7.8f}".format( MARKT_VOL["bid"][i][1] ).strip();

    print(" @: [ {0:15} ] -> [ {1:15} ]".format( A, B ) );

###################################################################################################
"""
 MARKT_VOL (ASK) ->  TTL: 9
 @: [ 3.10800000      ] -> [ 47.00570891     ]
 @: [ 3.11899700      ] -> [ 2,704.99269624  ]
 @: [ 3.12899700      ] -> [ 677.66089762    ]
 @: [ 3.13947000      ] -> [ 9,162.00053806  ]
 @: [ 3.14987600      ] -> [ 753.66517803    ]
 @: [ 3.15987600      ] -> [ 127.03738250    ]
 @: [ 3.17000000      ] -> [ 2,181.28455173  ]
 @: [ 3.18000000      ] -> [ 523.33477150    ]
 @: [ 3.19123200      ] -> [ 1,240.96200882  ]
----------------------------------------------
 MARKT_VOL (BID) ->  TTL: 8
 @: [ 3.09201000      ] -> [ 746.32887620    ]
 @: [ 3.08188200      ] -> [ 2,873.78543071  ]
 @: [ 3.07167100      ] -> [ 5,832.53330392  ]
 @: [ 3.06002000      ] -> [ 1,170.65029123  ]
 @: [ 3.05000000      ] -> [ 623.40391333    ]
 @: [ 3.03576400      ] -> [ 644.48371455    ]
 @: [ 3.02320000      ] -> [ 4,875.14522948  ]
 @: [ 3.01300000      ] -> [ 147.12622181    ]


"""
###################################################################################################

