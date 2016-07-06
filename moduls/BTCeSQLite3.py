#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
import sqlite3
import sys, json
from time import time, sleep
from datetime import datetime
###################################################################################################
#db.isolation_level = None;
#db.isolation_level='DEFERRED';
#db.isolation_level='IMMEDIATE';
#db.isolation_level='EXCLUSIVE';

###################################################################################################
class DB(object):

    # =======================================================================
    def __init__(self, _CONF=None, _PARENT=None):

        # -------------------------------------------------------------------
        self.CONF                           = _CONF;
        self.AVAILABLE                      = False;

        self.PARENT                         = _PARENT;
        self.DBS                            = {};
        self.CURSOR                         = None;
        # -------------------------------------------------------------------
        if self.INIT():
            self.AVAILABLE = True;

        # -------------------------------------------------------------------

    # =======================================================================
    def ADD(self):

        # -------------------------------------------------------------------
        pass;
        """
        self.DB = sqlite3.connect( "../data/dbs/META_DB", isolation_level="DEFERRED");

        self.CURSOR = self.DB.cursor();

        for d in _DATA:

            D = json.loads(d);
            for MT in D:
                print(D[MT]["updated"]);

                #CREATE_TB_NAME = "CREATE TABLE IF NOT EXISTS "+MT+" ";
                #self.CURSOR.execute(CREATE_TB_NAME + "(updated INT, json BLOB) ");
            

                _SQL = 'INSERT INTO '+MT+' (updated, json) VALUES ('+str(D[MT]["updated"])+",'"+json.dumps(D[MT], separators=(',',':'))+"')";
                #self.CURSOR.execute(_SQL);
            #break;

        self.DB.commit();
        self.CURSOR.close();
        self.DB.close();
        """
        # -------------------------------------------------------------------

    # =======================================================================
    def INIT(self):

        # -------------------------------------------------------------------
        for DB_NAME in self.CONF["DBS"]["DB"]:

            try:
                # -------------------------------------------------------
                self.OPEN( DB_NAME );
                #print( DB_NAME );
                # -------------------------------------------------------
                if DB_NAME == "MAIN_DB":
                    pass;
               
                # -------------------------------------------------------
                if DB_NAME == "META_DB":

                    for table in self.CONF["API"]["ALL_PAIRS"]:
                        
                        _SQL = "CREATE TABLE IF NOT EXISTS "+table+" (updated INTEGER PRIMARY KEY, json BLOB);"
                        self.CURSOR.execute(_SQL);
                        current_unix_timestamp = time();

                        one_h = 3600;
                        _24H = one_h*24;
                        pattern = 0;

                        #--------------------------------------------------#
                        # SET - > TO ONE CANDLE                            #
                        #pattern =  current_unix_timestamp - (one_h*4);    # -(one_h*4) << LEFT ONE 2h's of TICKS over
                        #pattern =  current_unix_timestamp - (one_h*10);    # -(one_h*4) << LEFT ONE 1h's of TICKS over
                        #pattern =  1453293291+(880*15);    # -(one_h*4) << LEFT ONE 1h's of TICKS over
                        #--------------------------------------------------#

                    self.CURSOR.execute("DELETE FROM ltc_usd WHERE updated < "+str(pattern) );

                    # -----------------------------------------

                # -------------------------------------------------------
                elif DB_NAME == "BOOK_DB":

                    # -----------------------------------------
                    _SQL = """

                        CREATE TABLE IF NOT EXISTS _TB_NAME_ (
                            
                            /* ----------------------------- */
                            BKKPG_UID           INTEGER PRIMARY KEY,
                            completed           INT DEFAULT 0, 
                            started             INT DEFAULT 0, 

                            /* ----------------------------- */
                            buy_order_id        INTEGER,
                            buy_unix_time       REAL, 
                            buy_filled          INT DEFAULT 0, 
                            buy_amount          REAL, 
                            buy_at_price        REAL, 
                            buy_fee             REAL, 
                            buy_ttl             REAL, 
                            buy_grand_ttl       REAL,

                            /* ----------------------------- */
                            sell_order_id       INTEGER,
                            sell_unix_time      REAL, 
                            sell_filled         INT DEFAULT 0, 
                            sell_amount         REAL, 
                            sell_at_price       REAL, 
                            sell_fee            REAL, 
                            sell_ttl            REAL, 
                            sell_grand_ttl      REAL,

                            /* ----------------------------- */
                            profit_ttl          REAL /* sell_grand_ttl - buy_grand_ttl */

                            /* ----------------------------- */

                        );
                    """

                    for _TB_NAME_ in self.CONF["API"]["ALL_PAIRS"]:

                        self.CURSOR.execute(_SQL.replace("_TB_NAME_", _TB_NAME_));

                    # -----------------------------------------

                # -------------------------------------------------------
                elif DB_NAME == "HISTORY_DB":

                    # -----------------------------------------
                    # DB.FETCH("HISTORY_DB",_SQL, ALL=True);
                    # DB.FETCH("HISTORY_DB",_SQL, ALL=True);


                    _SQL = """

                        CREATE TABLE IF NOT EXISTS _TB_NAME_ (
                            
                            id INTEGER PRIMARY KEY,
                            order_id            INTEGER,
                            unix_time           REAL, /*  */
                            action              TEXT, /* bought/sold*/
                            filled              INT DEFAULT 0,  /* 1/0 */
                            amount              REAL, /*  */
                            at_price            REAL, /*  */ 
                            fee                 REAL, /*  */
                            ttl                 REAL, /*  */
                            grand_ttl           REAL  /*  */

                        );

                    """


                    for _TB_NAME_ in self.CONF["API"]["ALL_PAIRS"]:

                        self.CURSOR.execute(_SQL.replace("_TB_NAME_", _TB_NAME_));

                    # -----------------------------------------

                # -------------------------------------------------------
                elif DB_NAME == "ORDERS_DB":

                    # -----------------------------------------
                    _SQL = """

                        CREATE TABLE IF NOT EXISTS _TB_NAME_ (
                            
                            id INTEGER PRIMARY KEY,
                            order_id            INTEGER,
                            unix_time           REAL,
                            filled              INT, /* aka -> status */
                            at_price            REAL,
                            amount              REAL,
                            pair                TEXT,
                            type                TEXT

                        );

                    """

                    for _TB_NAME_ in self.CONF["API"]["ALL_PAIRS"]:

                        self.CURSOR.execute(_SQL.replace("_TB_NAME_", _TB_NAME_));

                    # -----------------------------------------

                # -------------------------------------------------------
                elif DB_NAME == "OFFICE_DB":

                    # -----------------------------------------
                    # Alarms

                    _SQL = """

                        CREATE TABLE IF NOT EXISTS alarms (
                            id INTEGER PRIMARY KEY,
                            action TEXT, 
                            pairs TEXT, 
                            this_price REAL, 
                            height TEXT
                        )

                    """

                    self.CURSOR.execute(_SQL);

                    # -----------------------------------------
                    # Auto-Trader

                    """

                    ACTIONS = [ "buy", "sell" ];

                    STRUCTURE = " this_price REAL "

                    for action in ACTIONS:
                        for curr in self.CONF["API"]["ALL_PAIRS"]:

                            curr = curr.split("_")[0];

                            _SQL = "CREATE TABLE IF NOT EXISTS "+action+"_"+curr+"_"+"if_lower ("+STRUCTURE+");"
                            #print(_SQL);
                            self.CURSOR.execute(_SQL);

                            _SQL = "CREATE TABLE IF NOT EXISTS "+action+"_"+curr+"_"+"if_higher ("+STRUCTURE+");"
                            #print(_SQL);
                            self.CURSOR.execute(_SQL);



                    """

                    # -----------------------------------------
                    # Balance

                    _SQL = """

                        CREATE TABLE IF NOT EXISTS balance (
                            ppc REAL, usd REAL, gbp REAL, xpm REAL, trc REAL, ltc REAL, ftc REAL, 
                            nvc REAL, nmc REAL, btc REAL, rur REAL, cnh REAL, eur REAL
                        )
                    """

                    self.CURSOR.execute(_SQL);


                    # -----------------------------------------

                # -------------------------------------------------------
                self.DBS[DB_NAME].commit();
                self.DBS[DB_NAME].close();
                # -------------------------------------------------------
            except Exception as _exception:

                self.PARENT.LOG["error"].append(str(_exception));
                print(_exception);
                return False;

        # -------------------------------------------------------------------
        # If all OKE ?
        return True;
        # -------------------------------------------------------------------

    # =======================================================================
    def FETCH(self, THIS_DB, SQL=False, ALL=False):

        # -------------------------------------------------------------------
        try:

            if SQL:

                if self.OPEN(THIS_DB):

                    self.CURSOR.execute(SQL);

                    if ALL:
                        data = self.CURSOR.fetchall();

                    else:
                        data = self.CURSOR.fetchone();

                    self.CLOSE( THIS_DB );
                    return data;

            else:
                raise Exception(" No SQL request! INSERT(SQL) ")

        except Exception as _exception:

            self.PARENT.LOG["error"].append(str(_exception));
            self.CLOSE( THIS_DB );
            print(_exception)
            return False;

        # -------------------------------------------------------------------

    # =======================================================================
    def INSERT(self, THIS_DB, SQL=False):

        # -------------------------------------------------------------------
        try:

            if SQL:
    
                if self.OPEN( THIS_DB ):
                
                    self.CURSOR.execute( SQL );
                    self.CLOSE( THIS_DB );

                    return True;
            
                else:
                    raise Exception(" Can't Open Data-Base ")

            else:
                raise Exception(" No SQL request! INSERT(SQL) ")

        except Exception as _exception:

            self.PARENT.LOG["error"].append(str(_exception));
            self.CLOSE( THIS_DB );
            print(_exception)
            return False;

        # -------------------------------------------------------------------

    # =======================================================================
    def EXEC(self, THIS_DB, SQL=False):

        # -------------------------------------------------------------------
        try:

            if SQL:
    
                if self.OPEN( THIS_DB ):
                
                    self.CURSOR.execute( SQL );
                    self.CLOSE( THIS_DB );

                    return True;
            
                else:
                    raise Exception(" Can't Open Data-Base ")

            else:
                raise Exception(" No SQL request! INSERT(SQL) ")

        except Exception as _exception:

            self.PARENT.LOG["error"].append(str(_exception));
            self.CLOSE( THIS_DB );
            print(_exception)
            return False;

        # -------------------------------------------------------------------

    # =======================================================================
    def OPEN(self, THIS_DB):

        # -------------------------------------------------------------------
        try:

            self.DBS[THIS_DB] = sqlite3.connect( 

                self.CONF["DBS"]["PATH"] + self.CONF["DBS"]["DB"][THIS_DB], 
                isolation_level=self.CONF["DBS"]["ISOLATION_LEVEL"][1]

            );

            self.CURSOR = self.DBS[THIS_DB].cursor();

            return True;

        except Exception as _exception:

            self.PARENT.LOG["error"].append(str(_exception));
            self.CLOSE( THIS_DB );
            print(_exception);
            return False;

        # -------------------------------------------------------------------

    # =======================================================================
    def CLOSE(self, THIS_DB):

        # -------------------------------------------------------------------
        try:
            self.DBS[THIS_DB].commit();
            self.CURSOR.close();
            self.DBS[THIS_DB].close();
            return True;

        except Exception as _exception:

            try:
                self.DBS[THIS_DB].close();
                self.PARENT.LOG["error"].append(str(_exception));
                print(_exception);

            except Exception as _FATAL:
                self.PARENT.LOG["error"].append(str(_exception));
                print(_FATAL);


            return False;

        # -------------------------------------------------------------------

    # =======================================================================

###################################################################################################
if __name__ == '__main__':
    
    pass;
    #_DB = DB();
    #_DB.ADD();



""" ------------------------------------------------------------------------------------
db = sqlite3.connect("_MD5_SQLite_db", isolation_level="DEFERRED");

cursor = db.cursor();
db.execute('BEGIN TRANSACTION');
"""

#sql = """CREATE TABLE `_"""+a+b+c+d+"""_` (
#      `id` int(11) NOT NULL AUTO_INCREMENT,
#      `hash` text NOT NULL,
#      `raw` text NOT NULL,
#      PRIMARY KEY (`id`)
#    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1"""

"""
cursor.execute(sql);

cursor.execute("COMMIT");
#cursor.execute("ROLLBACK");
#cursor.rollback();

db.commit();
db.close();
"""


""" ------------------------------------------------------------------------------------
From PyDoc

import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
"""

""" ------------------------------------------------------------------------------------
From PyDoc

# Never do this -- insecure!
symbol = 'RHAT'
c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

# Do this instead
t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
print c.fetchone()

# Larger example that inserts many records at a time
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

"""


""" ------------------------------------------------------------------------------------
From PyDoc

To retrieve data after executing a SELECT statement, you can either treat the cursor as an iterator, 
call the cursor’s fetchone() method to retrieve a single matching row, or 
call fetchall() to get a list of the matching rows.

This example uses the iterator form:

>>> for row in c.execute('SELECT * FROM stocks ORDER BY price'):
>>>     print row


(u'2006-01-05', u'BUY', u'RHAT', 100, 35.14)
(u'2006-03-28', u'BUY', u'IBM', 1000, 45.0)
(u'2006-04-06', u'SELL', u'IBM', 500, 53.0)
(u'2006-04-05', u'BUY', u'MSFT', 1000, 72.0)

or 

>>>  c.execute('SELECT * FROM stocks ORDER BY price'):

>>> print c.fetchone(); # to retrieve a single matching row

of 

>>> print c.fetchall(); # to get a list of the matching rows.





# example from SQLite wiki
con.execute("create virtual table recipe using fts3(name, ingredients)")
con.executescript('''
    insert into recipe (name, ingredients) values ('broccoli stew', 'broccoli peppers cheese tomatoes');
    insert into recipe (name, ingredients) values ('pumpkin stew', 'pumpkin onions garlic celery');
    insert into recipe (name, ingredients) values ('broccoli pie', 'broccoli cheese onions flour');
    insert into recipe (name, ingredients) values ('pumpkin pie', 'pumpkin sugar flour butter');
''')
for row in con.execute("select rowid, name, ingredients from recipe where name match 'pie'"):
    print row










"""
# ======================================================================
