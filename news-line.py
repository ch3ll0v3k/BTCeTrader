#!/usr/bin/python
# =========================================================================
from sys import stdout
from threading import Timer
from time import sleep

# =========================================================================
NWS = "[ LTC/USD: HIGH 3.12323, LOW 3.10323, BUY 3.23123, SELL 3.2324 ], [ BTC/USD: HIGH 323.2323, LOW 324.0323, BUY 333.23123, SELL 3.2324 ], [ BTC/LTC: HIGH 0.008323, LOW 0.008023, BUY 0.082123, SELL 0.08224 ] ";
NWS = "[ LTC/USD: HIGH 3.12323, LOW 3.10323, BUY 3.23123, SELL 3.2324 ]";

L = len(NWS);
c = 0;
print(L);

while True:
    stdout.write( NWS[c:] + NWS[:c] +"\r");
    stdout.flush();
    c += 1;
    sleep(0.075);
    if c > L-1:
        c = 0;
        #NWS += "Z";
        #L += 1;

# =========================================================================
