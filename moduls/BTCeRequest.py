#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
if __name__ == "__main__":

    exit();

else:

    #import _ssl
    #_ssl.PROTOCOL_SSLv23 = _ssl.PROTOCOL_TLSv1
    import httplib, urllib, json, hashlib, hmac
    import sys, os


    #import urllib3.contrib.pyopenssl
    #urllib3.contrib.pyopenssl.inject_into_urllib3()




###################################################################################################
"""
if incorrect user key pub/sic json response 
> {'success': 0, 'error': 'invalid sign'}

if nonce id incorrect json response
> {'success': 0, 'error': "invalid nonce parameter; on key:13, you sent:'13', you should send:14"}

next correct "nonce" = JSON["error"].split(":")[3]

by wrong key/sign  
>> {u'success': 0, u'error': u'invalid sign'}

"""
###################################################################################################
class Request(object):

    # =======================================================================
    def __init__(self, _CONF, _PARENT):

        # -------------------------------------------------------------------
        self.PARENT                             = _PARENT;
        self.CONF                               = _CONF;
        self.AVAILABLE                          = False;

        self.NONCE_FILE                         = self.CONF["USER"]["DIR"]+self.CONF["USER"]["NONCE_FILE"];
        self.NONCE                              = None;

        self.HMAC                               = None; 
        self.PARAMS                             = { };
        self.HEADERS                            = { };
        #self.API_METHODS                        = list(self.CONF["API_METHODS"]);
        # -------------------------------------------------------------------
        #self.PARENT.LOG["info"].append(" 200 ");
        self.INIT();
        # -------------------------------------------------------------------

    # =======================================================================
    def INIT(self):

        # -------------------------------------------------------------------
        self.CONF["API"]["KEY"]["PUB"] = str(self.CONF["API"]["KEY"]["PUB"]).strip();
        self.CONF["API"]["KEY"]["SEC"] = str(self.CONF["API"]["KEY"]["SEC"]).strip();

        """
        self.PARAMS = { "method" : "_METHOD_", "nonce": "_NONCE_" };
        self.HMAC = hmac.new(self.CONF["API"]["KEY"]["SEC"], digestmod=hashlib.sha512);

        self.HEADERS = {
            "Content-type"  : "application/x-www-form-urlencoded",
            "Key"           : self.CONF["API"]["KEY"]["PUB"],
            "Sign"          : "_SIGN_"
        };
        """        

        # -------------------------------------------------------------------
        #self.getInfo();                    # ok
        #self.Trade();                      # ?
        #self.ActiveOrders();               # ok
        #self.OrderInfo(936159769);         # ok
        #self.CancelOrder();                # ?
        #self.TradeHistory();               # EMPTY OK or with PARAMETERS
        #self.TransHistory();               # ? ALOT OF JSON
        #self.WithdrawCoin();               #
        #self.CreateCoupon();               #
        #self.RedeemCoupon();               #
        # -------------------------------------------------------------------
        self.AVAILABLE = True;
        # -------------------------------------------------------------------

    # =======================================================================
    def MK_REQ(self, _API_METHOD, _PARAMS=None):

        # -------------------------------------------------------------------
        try:

            #if _API_METHOD in self.API_METHODS:
            if _API_METHOD in self.CONF["API"]["METHODS"]:

                if self.UPDATE_NONCE():
                    
                    # -------------------------------------------------------
                    self.PARAMS = { "method" : "_METHOD_", "nonce": "_NONCE_" };

                    self.HMAC = hmac.new(self.CONF["API"]["KEY"]["SEC"], digestmod=hashlib.sha512);

                    self.HEADERS = {
                        "Content-type"  : "application/x-www-form-urlencoded",
                        "Key"           : self.CONF["API"]["KEY"]["PUB"],
                        "Sign"          : "_SIGN_"
                    };
                    
                    # -------------------------------------------------------
                    self.PARAMS["nonce"]    = self.NONCE;
                    self.PARAMS["method"]   = _API_METHOD;

                    if _PARAMS is not None:

                        i = 0;
                        while i < len(_PARAMS):
                            self.PARAMS[_PARAMS[i]] = _PARAMS[i+1];
                            i += 2;


                    tmp_params = urllib.urlencode(self.PARAMS);

                    # -------------------------------------------------------
                    self.HMAC.update(tmp_params);
                    SIGN = self.HMAC.hexdigest();
                    self.HEADERS["Sign"] = SIGN;

                    conn = httplib.HTTPSConnection(str(self.CONF["API"]["HOST"]));
                    conn.request("POST", str(self.CONF["API"]["URL"]["TAPI"]), tmp_params, self.HEADERS);
                    
                    res = conn.getresponse();

                     
                    # -------------------------------------------------------
                    JSON = json.load(res);
                    conn.close();

                    #print("-------------------------------------------------------------------");
                    #print(JSON);

                    if res.status == 200:
                        
                        if JSON["success"] == 1:
                            return JSON;
                        
                        else:

                            if JSON["error"] == "no orders":
                                return json.loads('{ "success" : 1, "return" : {} }');

                            else:
                                DATA = JSON["error"].split(":");
                                if DATA[0] == "invalid nonce parameter; on key":
                                    self.PARENT.LOG["notif"].append(" [MODULE:REQUEST]:<br/> Auto-Correcting data in AUTO-MODE!");
                                    self.NONCE = int(DATA[1].split(",")[0])+1;
                                else:
                                    self.PARENT.LOG["error"].append(" API-ERROR: <br/> "+str(JSON["error"]) );


                    else:

                        self.PARENT.LOG["error"].append("[MODULE:REQUEST]:<br/>"+str(res.status)+" :: "+str(res.reason));
                        
                        return json.loads( '{ "success" : 0, "error" : "'+str(res.status)+" :: "+str(res.reason)+'" }');
                    # -------------------------------------------------------

                else:
                    self.PARENT.LOG["error"].append(" [MODULE:REQUEST]:<br/> Can't Update NONCE. ");
                    return json.loads('{ "success" : 0, "error" : "Can\'t Update NONCE. " }');
            else:
                self.PARENT.LOG["error"].append(" [MODULE:REQUEST]:<br/> Unknown API-METHODS. ");
                return json.loads('{ "success" : 0, "error" : "Unknown API-METHODS. " }');

        except Exception as _exception:

            self.PARENT.LOG["error"].append(" [MODULE:REQUEST]:<br/> "+str(_exception));
            self.EXC_HANDLER(_exception);
            return False;

        # -------------------------------------------------------------------

    # =======================================================================
    def UPDATE_NONCE(self):

        # -------------------------------------------------------------------
        try:

            if self.NONCE is None:

                try:

                    FS = open( self.NONCE_FILE , "r");
                    self.NONCE = int(FS.readline().strip());
                    FS.close();

                except Exception as _exception:
                    
                    self.PARENT.LOG["error"].append( " [MODULE:REQUEST]:<br/> Can't READ from NONCE_FILE.\n" +str(_exception) );
                    raise Exception(" [MODULE:REQUEST]:<br/> Can't READ from NONCE_FILE.");
                
                try:

                    FS = open( self.NONCE_FILE , "w");
                    self.NONCE += 1;
                    FS.write(str(self.NONCE)+"\n");
                    FS.close();

                except Exception as _exception:

                    self.PARENT.LOG["error"].append( " [MODULE:REQUEST]:<br/> Can't READ from NONCE_FILE.\n" +str(_exception) );
                    raise Exception(" [MODULE:REQUEST]:<br/> Can't WRITE to NONCE_FILE.");

                return True;
            
            else:
                
                self.NONCE += 1;
                return True;

        except Exception as _exception:

            self.EXC_HANDLER( _exception );
            return False;
        # -------------------------------------------------------------------

    # =======================================================================
    def SAVE_NONCE(self):

        # -------------------------------------------------------------------
        try:

            if self.NONCE is None:
                return True;

            print("SAVING NONCE: "+str(self.NONCE))
            FS = open( self.NONCE_FILE , "w");
            self.NONCE += 1;
            FS.write(str(self.NONCE)+"\n");
            FS.close();
            return True;

        except Exception as _exception:

            print(_exception);
            print(" Cant' WRITE to NONCE_FILE.");
            raise Exception(" Can't WRITE to NONCE_FILE.");
            return False;
        # -------------------------------------------------------------------

    # =======================================================================
    def EXC_HANDLER(self, _exception):

        # -------------------------------------------------------------------
        '''
        if self.CONF["SYS"]["DEBUG"]:
            self._EXC_(_exception);
        '''
        
        self._EXC_(_exception);
        # -------------------------------------------------------------------

    # =======================================================================
    def _EXC_(self, _exception):

        # -------------------------------------------------------------------
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename

        print("----------------------------------------------------");
        print(" Exception: "+str(_exception));
        print(" File: "+str(filename));
        print(" LineNR: "+str(lineno));
        print("----------------------------------------------------");
        #print(" Error on line {}".format(sys.exc_info()[-1].tb_lineno));
        #print("----------------------------------------------------");

        # -------------------------------------------------------------------

    # END
    
    # =======================================================================
    # =======================================================================
    # =======================================================================

    #    >>>>>>>>>>>>>>>>>>>>>>>> API METHODS <<<<<<<<<<<<<<<<<<<<<<<<<<
    def getInfo(self, _PARAMS=None):
        # Parameters:None
        return self.MK_REQ( sys._getframe().f_code.co_name, _PARAMS);

    def Trade(self, _PARAMS=None):
        # Parameters: pair=ltc_usd&type=buy&rate=3.50&amount=2
        return self.MK_REQ( sys._getframe().f_code.co_name, _PARAMS);

    def OrderInfo(self, _PARAMS=None):
        # Parameters:
        _PARAMS = ["order_id", str(_PARAMS)];
        return self.MK_REQ( sys._getframe().f_code.co_name, _PARAMS);

    def ActiveOrders(self, _PARAMS=None):
        # Parameters:None
        return self.MK_REQ( sys._getframe().f_code.co_name, _PARAMS);

    def CancelOrder(self, _PARAMS=None):
        # Parameters:s§
        _PARAMS = ["order_id", str(_PARAMS)];
        return self.MK_REQ( sys._getframe().f_code.co_name, _PARAMS);

    def TradeHistory(self, _PARAMS=None):

        """
        Parameter   description                                 assumes value   standard value

        from        trade ID, from which the display starts     numerical       0
        count       the number of trades for display            numerical       1000
        from_id     trade ID, from which the display starts     numerical       0
        end_id      trade ID on which the display ends          numerical       ∞
        order       Sorting                                     ASC or DESC     DESC
        since       the time to start the display               UNIX time       0
        end         the time to end the display                 UNIX time       ∞
        pair        pair to be displayed                        btc_usd         all pairs
        """
        return self.MK_REQ( sys._getframe().f_code.co_name, _PARAMS);

    def TransHistory(self, _PARAMS=None):
        # Parameters:None
        return self.MK_REQ( sys._getframe().f_code.co_name, _PARAMS);

    def WithdrawCoin(self, _PARAMS=None):
        # Parameters:
        return self.MK_REQ( sys._getframe().f_code.co_name, _PARAMS);

    def CreateCoupon(self, _PARAMS=None):
        # Parameters:
        return self.MK_REQ( sys._getframe().f_code.co_name, _PARAMS);

    def RedeemCoupon(self, _PARAMS=None):
        # Parameters:
        return self.MK_REQ( sys._getframe().f_code.co_name, _PARAMS);

    # =======================================================================
    # =======================================================================
    # =======================================================================


###################################################################################################











