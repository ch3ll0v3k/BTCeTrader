#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# BulitIn
import json, sys, time
import hashlib

from random import randint

# PyQt4
from PyQt4.QtGui import QMessageBox, QTextEdit, QDialog, QPolygonF,QPainter, QPen, QColor 
from PyQt4.QtGui import QBrush, QMainWindow,QWidget,QToolTip,QApplication, QFont,QIcon,QAction
from PyQt4.QtGui import QFrame,QListWidget, QListWidgetItem, QComboBox,QCheckBox,QPushButton
from PyQt4.QtGui import QProgressBar, QLineEdit, QLabel, QStyleOptionComboBox

from PyQt4.QtCore import QTimer, SIGNAL, SLOT, Qt, QPointF, QPoint, QRectF, QRect
from PyQt4.QtCore import pyqtSlot

###################################################################################################
class BookKeeping(QFrame):

    # =======================================================================
    def __init__(self, parent=None, _PARENT=None):

        # -------------------------------------------------------------------
        QFrame.__init__(self, parent);
        # -------------------------------------------------------------------
        self.PARENT                         = _PARENT;
        self.CONF                           = _PARENT.CONF;

        #self.SHA256                         = hashlib.sha256;
        #UID_SHA256 = self.SHA256( str(time.time()) ).hexdigest();
        self.SELECTED_BKKPG_UID             = None;

        # -------------------------------------------------------------------
        self.setGeometry( 3, 5, 975, 555 );
        self.setStyleSheet( "QFrame{ font: 12px 'monospace'; color: #000; background-color: transparent; background-image: url('./data/imgs/TAB_BookKeeping.png'); }" );

        self.PAIR_COMBO                     = QComboBox( self);
        self.PAIR_COMBO.setGeometry( 86, 20, 108, 44 ); 
        self.connect( self.PAIR_COMBO, SIGNAL('currentIndexChanged(int)'), self.CREATE_LISTS );
        #self.PAIR_COMBO.setStyleSheet( "QComboBox{ font: 16px 'monospace'; background-color: #333; color: #FFF; border-style: solid; border-width: 1px; border-color: #000; border-radius: none; }" );
        self.PAIR_COMBO.setEditable(False);

        """
        #self.PAIR_COMBO.setItemIcon( 0, QIcon("./data/imgs/500.png") );
        print(self.PAIR_COMBO.__len__());
        #set at tooltip
        combo.setItemData(0,"a tooltip",Qt.ToolTipRole)
        # set the Font Color
        combo.setItemData(0,QColor("#FF333D"), Qt.BackgroundColorRole)
        #set the font
        combo.setItemData(0, QtGui.QFont('Verdana', bold=True), Qt.FontRole)
        """

        # -------------------------------------------------------------------
        list_style                          = "QListWidget{ font: 10px 'monospace'; color: #fff;  background-color: #000; border-style: none; background-image: url('./data/imgs/TAB_BookKeeping_line.png'); }"; # ./data/imgs/BookKeeping_line.png
        lable_style                         = "QLabel{ font: 10px 'monospace'; color: #fff;  background-color: transparent; border-style: none; background-image: url(''); }"; 

        # -------------------------------------------------------------------
        self.DATA_TO_SEND                   = None;
        self._i_                            = "|"; # List delimiter
        self.CALCULATE_ONLY_COMPLETED       = True;
        self.DATA_TO_SEND_SELECTED          = False;
        
        # -------------------------------------------------------------------
        self.BOOKKEEPING_WIDGET             = QListWidget( self );
        self.BOOKKEEPING_WIDGET.setGeometry( 13, 144, 949, 259 );
        self.BOOKKEEPING_WIDGET.setStyleSheet( list_style );

        self.connect( self.BOOKKEEPING_WIDGET, SIGNAL('itemSelectionChanged()'), lambda: self.SEND_VALUES_TO_TRADE_TERMINAL("SOLD_WIDGET") );
        self.BOOKKEEPING_WIDGET.itemClicked.connect( lambda: self.SEND_VALUES_TO_TRADE_TERMINAL("SELECT_VALUES") );


        self.BOUGHT_TTL_LABLE               = QLabel("0.0", self);
        self.BOUGHT_TTL_LABLE.setGeometry( 304, 406, 85, 17 );
        #self.BOUGHT_TTL_LABLE.setEditable( False );
        self.BOUGHT_TTL_LABLE.setStyleSheet( lable_style );
        self.BOUGHT_TTL                     = 0;

        self.BOUGHT_TTL_PLUS_FEE_LABLE      = QLabel("0.0", self);
        self.BOUGHT_TTL_PLUS_FEE_LABLE.setGeometry( 396, 406, 85, 17 );
        #self.BOUGHT_TTL_PLUS_FEE_LABLE.setEditable( False );
        self.BOUGHT_TTL_PLUS_FEE_LABLE.setStyleSheet( lable_style );
        self.BOUGHT_TTL_PLUS_FEE            = 0;


        self.SOLD_TTL_LABLE                 = QLabel("0.0", self);
        self.SOLD_TTL_LABLE.setGeometry( 694, 406, 85, 17 );
        #self.SOLD_TTL_LABLE.setEditable( False );
        self.SOLD_TTL_LABLE.setStyleSheet( lable_style );
        self.SOLD_TTL                       = 0;

        self.SOLD_TTL_PLUS_FEE_LABLE        = QLabel("0.0", self);
        self.SOLD_TTL_PLUS_FEE_LABLE.setGeometry( 784, 406, 85, 17 );
        #self.SOLD_TTL_PLUS_FEE_LABLE.setEditable( False );
        self.SOLD_TTL_PLUS_FEE_LABLE.setStyleSheet( lable_style );
        self.SOLD_TTL_PLUS_FEE              = 0;

        self.PROFIT_TTL_LABLE               = QLabel("0.0", self);
        self.PROFIT_TTL_LABLE.setGeometry( 874, 406, 88, 17 );
        #self.PROFIT_TTL_LABLE.setEditable( False );
        self.PROFIT_TTL_LABLE.setStyleSheet( lable_style );
        self.PROFIT_TTL                     = 0;

        # -------------------------------------------------------------------
        self.SEND_ID_LABLE                  = QLabel("n/a", self);
        self.SEND_ID_LABLE.setGeometry( 18, 467, 43, 17 );
        self.SEND_ID_LABLE.setStyleSheet( lable_style );

        self.SEND_AMOUNT_LABLE              = QLabel("n/a", self);
        self.SEND_AMOUNT_LABLE.setGeometry( 66, 467, 85, 17 );
        self.SEND_AMOUNT_LABLE.setStyleSheet( lable_style );

        self.SEND_AT_PRICE_LABLE            = QLabel("n/a", self);
        self.SEND_AT_PRICE_LABLE.setGeometry( 156, 467, 43, 17 );
        self.SEND_AT_PRICE_LABLE.setStyleSheet( lable_style );

        self.SEND_VALUES_BTN                = QPushButton("", self); 
        self.SEND_VALUES_BTN.setGeometry( 60, 502, 131, 33 );
        self.SEND_VALUES_BTN.setStyleSheet( "QPushButton{ background-color: transparent; border-style: none; }" ); 
        self.connect( self.SEND_VALUES_BTN, SIGNAL('clicked()'), lambda: self.SEND_VALUES_TO_TRADE_TERMINAL("SEND_VALUES") );

        # -------------------------------------------------------------------
        self.ONLY_COMPLETED_CHECKBOX        = QCheckBox("", self);
        self.ONLY_COMPLETED_CHECKBOX.setGeometry( 665, 444, 17, 17 );
        self.ONLY_COMPLETED_CHECKBOX.setCheckState(Qt.Checked);
        #self.ONLY_COMPLETED_CHECKBOX.setEnabled(False);
        self.connect(self.ONLY_COMPLETED_CHECKBOX, SIGNAL('stateChanged(int)'), lambda: self.CHANGE_VALUES("only_completed") );

        # -------------------------------------------------------------------
        self.INIT();
        # -------------------------------------------------------------------

    # =======================================================================
    def INIT(self):

        # -------------------------------------------------------------------
        try:

            self.CREATE_PAIRS_SELECTOR();
            self.CREATE_LISTS();

        except Exception as _exception:

            print("-----------------------------------------------------");
            print("[INIT]"+str(_exception));
        # -------------------------------------------------------------------

    # =======================================================================
    def BKKPG_UID_ACTION(self, _ACTION, BKKPG_UID, _D):

        # -------------------------------------------------------------------
        #print("_ACTION: ", _ACTION, "BKKPG_UID: ", BKKPG_UID)
        # -------------------------------------------------------------------
        try:

            CURR_PAIR =  str(self.PAIR_COMBO.currentText()).lower().strip();

            order_id    = _D[0];
            unix_time   = _D[1];
            filled      = _D[2];
            amount      = _D[3];
            at_price    = _D[4];

            if _ACTION == "buy":

                # For CRYPTO
                ttl = amount;
                fee = ( ttl/100*self.PARENT.FEE );
            
            elif _ACTION == "sell":

                # For USD
                ttl = amount*at_price;
                fee = ( ttl/100*self.PARENT.FEE );

            grand_ttl = ttl-fee;

            # -------------------------------------------------------------------
            if BKKPG_UID == "": # Is New Record

                TPL = "buy_order_id, buy_unix_time, buy_filled, buy_amount, buy_at_price, buy_fee, buy_ttl, buy_grand_ttl, sell_order_id, sell_unix_time, sell_filled, sell_amount, sell_at_price, sell_fee, sell_ttl, sell_grand_ttl ";
                
                _SQL = "INSERT INTO "+CURR_PAIR+"( BKKPG_UID, completed, started, "+TPL+", profit_ttl ) ";

                if _ACTION == "buy":
                    _SQL += "VALUES( NULL,0,1,{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15}, 0 )".format( _D[0],_D[1],_D[2],_D[3],_D[4],fee, ttl, grand_ttl, 0, 0, 0, 0, 0, 0, 0, 0 );

                else:
                    _SQL += "VALUES( NULL,0,1,{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15}, 0 )".format( 0, 0, 0, 0, 0, 0, 0, 0, _D[0], _D[1],_D[2],_D[3],_D[4],fee, ttl, grand_ttl );


                self.PARENT.DB.EXEC("BOOK_DB", _SQL);

            else: # Existing Record

                # ------------------------------------------------
                if filled == 1:

                    completed = 1;

                    _SQL = "SELECT ACT_grand_ttl from "+CURR_PAIR+" WHERE BKKPG_UID="+BKKPG_UID;
                    
                    if _ACTION == "buy":

                        DATA = self.PARENT.DB.FETCH("BOOK_DB", _SQL.replace("ACT","sell"), ALL=False);
                        profit_ttl = DATA - grand_ttl;

                    else:

                        DATA = self.PARENT.DB.FETCH("BOOK_DB", _SQL.replace("ACT","buy"), ALL=False);
                        profit_ttl = grand_ttl - DATA;
                else:
                    profit_ttl = 0;
                    completed = 0;

                # ------------------------------------------------
                A = _ACTION;
                
                _SQL = "UPDATE "+CURR_PAIR+" SET completed={0}, "+A+"_order_id={1}, "+A+"_unix_time={2}, "+A+"_filled={3}, ";
                _SQL += A+"_amount={4}, "+A+"_at_price={5}, "+A+"_fee={6}, "+A+"_ttl={7}, "+A+"_grand_ttl={8}";
                _SQL += " WHERE BKKPG_UID="+BKKPG_UID;

                _SQL = _SQL.format( completed, order_id, unix_time, filled, amount, at_price, fee, ttl, grand_ttl );

                self.PARENT.DB.EXEC("BOOK_DB", _SQL);

        except Exception as _exception:

            print(" BOOKKEEPING[0:0]");
            print(_exception);
        # -------------------------------------------------------------------
        """
        BKKPG_UID, completed, started, 
        
        buy_order_id, buy_unix_time, buy_filled, buy_amount, buy_at_price, buy_fee, buy_ttl, buy_grand_ttl, 
        sell_order_id, sell_unix_time, sell_filled, sell_amount, sell_at_price, sell_fee, sell_ttl, sell_grand_ttl, 
        
        profit_ttl
        """
        # -------------------------------------------------------------------

    # =======================================================================
    def DELETE_ORDER(self, _order_id, _pair, _type):

        # -------------------------------------------------------------------

        _SQL = "SELECT buy_order_id, sell_order_id FROM "+_pair;
        _SQL += " WHERE buy_order_id="+str(_order_id)+" OR sell_order_id="+str(_order_id);

        DATA = self.PARENT.DB.FETCH("BOOK_DB", _SQL, ALL=False);

        if DATA is None:
            pass;

        if _type == "buy" and DATA[1] == 0:

            _SQL = "DELETE FROM "+_pair+" WHERE buy_order_id="+str(_order_id)+" OR sell_order_id="+str(_order_id);
            self.PARENT.DB.EXEC("BOOK_DB", _SQL);
            self.CREATE_LISTS();

        elif _type == "sell" and DATA[0] == 0:

            _SQL = "DELETE FROM "+_pair+" WHERE buy_order_id="+str(_order_id)+" OR sell_order_id="+str(_order_id);
            self.PARENT.DB.EXEC("BOOK_DB", _SQL);
            self.CREATE_LISTS();

        else:

            A = _type;

            _SQL = "UPDATE "+self.PARENT.CURR_PAIR+" SET ";
            _SQL += " completed=0, "+A+"_order_id=0, "+A+"_unix_time=0, "+A+"_filled=0, ";
            _SQL += A+"_amount=0, "+A+"_at_price=0, "+A+"_fee=0, "+A+"_ttl=0, "+A+"_grand_ttl=0 ";
            _SQL += "WHERE "+A+"_order_id="+str(_order_id);

            self.PARENT.DB.EXEC("BOOK_DB", _SQL);

        # -------------------------------------------------------------------

    # =======================================================================
    def CREATE_LISTS(self):

        # -------------------------------------------------------------------
        try:
            CURR_PAIR =  str(self.PAIR_COMBO.currentText()).lower();

            # -------------------------------------------------------------------
            self.BOOK = { "bought" : [], "sold" : [] };

            self.BOUGHT_TTL = 0;
            self.BOUGHT_TTL_PLUS_FEE = 0;

            self.SOLD_TTL = 0;
            self.SOLD_TTL_PLUS_FEE = 0;

            # -------------------------------------------------------------------
            #self.PARENT.DB.EXEC( "BOOK_DB", "DELETE FROM "+CURR_PAIR+" WHERE BKKPG_UID>7" );

            DATA = self.PARENT.DB.FETCH("BOOK_DB", "SELECT * FROM "+CURR_PAIR+" ORDER BY BKKPG_UID DESC", ALL=True);
            self.BOOKKEEPING_WIDGET.clear();

            for data in DATA:

                # ---------------------------------------------------------------
                """ " "" 
                print( data )
                for d in data:
                    print( d )
                exit();
                "" " """ 
                # ---------------------------------------------------------------
                # In-Memory DATA
                BKKPG_UID       = data[0]
                completed       = data[1]
                started         = data[2]

                buy_order_id    = data[3]
                buy_unix_time   = data[4]
                buy_filled      = data[5]
                buy_amount      = data[6]
                buy_at_price    = data[7]
                #buy_fee         = data[8]
                buy_ttl         = data[9]
                buy_grand_ttl   = data[10]

                sell_order_id   = data[11]
                sell_unix_time  = data[12]
                sell_filled     = data[13]
                sell_amount     = data[14]

                sell_at_price   = data[15]
                #sell_fee        = data[16]
                sell_ttl        = data[17]
                sell_grand_ttl  = data[18]

                profit_ttl      = data[19]

                # ---------------------------------------------------------------

                # ---------------------------------------------------------------
                """
                self.BOOK[ data[3] ].append( {
                                            
                                        BKKPG_UID,
                                        completed,
                                        started,

                                        buy_order_id,
                                        buy_unix_time,
                                        buy_filled,
                                        buy_amount,
                                        buy_at_price,
                                        buy_fee,
                                        buy_ttl,
                                        buy_grand_ttl,

                                        sell_order_id,
                                        sell_unix_time,
                                        sell_filled,
                                        sell_amount,
                                        sell_at_price,
                                        sell_fee,
                                        sell_ttl,
                                        sell_grand_ttl,

                                        profit_ttl

                                            } );

                """
                # ---------------------------------------------------------------
                if self.CALCULATE_ONLY_COMPLETED:

                    if buy_filled == 1 and sell_filled == 1:

                        self.BOUGHT_TTL += buy_ttl;
                        self.BOUGHT_TTL_PLUS_FEE += buy_grand_ttl*buy_at_price;

                        self.SOLD_TTL += sell_ttl;
                        self.SOLD_TTL_PLUS_FEE += sell_grand_ttl;

                else:

                    self.BOUGHT_TTL += buy_ttl;
                    self.BOUGHT_TTL_PLUS_FEE += buy_grand_ttl*buy_at_price;

                    self.SOLD_TTL += sell_ttl;
                    self.SOLD_TTL_PLUS_FEE += sell_grand_ttl;


                self.PROFIT_TTL_LABLE.setText( "{:10,.6f}".format(self.SOLD_TTL_PLUS_FEE - self.BOUGHT_TTL_PLUS_FEE) );


                # ---------------------------------------------------------------
                # Formating data to Display in BookKeeping Wodget

                item = "";

                item += "DEL{:7} ".format(str( BKKPG_UID )); # id

                # BUY / BOUGHT
                item += "#{:11} DEL".format( str(buy_order_id) ); # order_id
                item += "{:4} DEL".format( str(buy_filled) ); # filed
                item += "{:13} DEL".format( str("{:10,.6f}".format( float(buy_amount) )).strip() ); # Amount
                item += "{:13} DEL".format( str("{:10,.6f}".format( buy_at_price )).strip() ); # at_price
                #item += "{:13} DEL".format( str("{:10,.6f}".format( data[7] )).strip() ); # fee
                #item += "{:13} DEL".format( str("{:10,.6f}".format( buy_ttl )).strip() ); # ttl
                item += "{:14} ".format( str("{:10,.6f}".format( buy_grand_ttl )).strip() ); # grand_ttl

                # SELL / SOLD
                item += "#{:11} DEL".format( str(sell_order_id) ); # order_id
                item += "{:4} DEL".format( str(sell_filled) ); # filed
                item += "{:13} DEL".format( str("{:10,.6f}".format( sell_amount )).strip() ); # Amount
                item += "{:13} DEL".format( str("{:10,.6f}".format( sell_at_price )).strip() ); # at_price
                #item += "{:13} DEL".format( str("{:10,.6f}".format( data[7] )).strip() ); # fee
                #item += "{:13} DEL".format( str("{:10,.6f}".format( sell_ttl )).strip() ); # ttl
                item += "{:14} ".format( str("{:10,.6f}".format( sell_grand_ttl )).strip() ); # grand_ttl
                
                # PROFIT
                item += "{:13}".format( str("{:10,.6f}".format( profit_ttl )).strip() ); # grand_ttl

                newItem = QListWidgetItem( QIcon("./data/imgs/icon_filled_status_0.png"), item.replace("DEL", self._i_), self.BOOKKEEPING_WIDGET, 0);
                #newItemToolTip = "Order ID: #"+str()+" Created: "+time.ctime(int(data[2]));
                #newItem.setToolTip(newItemToolTip);

                # ---------------------------------------------------------------

            # / for
            # -------------------------------------------------------------------
            try: 
                self.BOUGHT_TTL_LABLE.setText( str("{:10,.6f}".format( self.BOUGHT_TTL ).strip()) );
                self.BOUGHT_TTL_PLUS_FEE_LABLE.setText( str("{:10,.6f}".format( self.BOUGHT_TTL_PLUS_FEE ).strip()) );

                self.SOLD_TTL_LABLE.setText( str("{:10,.6f}".format( self.SOLD_TTL ).strip()) );
                self.SOLD_TTL_PLUS_FEE_LABLE.setText( str("{:10,.6f}".format( self.SOLD_TTL_PLUS_FEE ).strip()) );

            except Exception as e:
                print("BOOKKEEPING[3:0]"+str(e))


        except Exception as _exception:

            print(" BOOKKEEPING[1:0]");
            print(_exception);
        # -------------------------------------------------------------------

    # =======================================================================
    def RESET_BKKPG_UID(self):

        # -------------------------------------------------------------------
        #CURR_PAIR =  str(self.PAIR_COMBO.currentText()).lower();
        self.PARENT.GUI.BKKPG_UID_VALUE.setText("");
        self.PARENT.GUI.CONTROL_TRADINGS_BTNS("buy", "show");
        self.PARENT.GUI.CONTROL_TRADINGS_BTNS("sell", "show");
        # -------------------------------------------------------------------

    # =======================================================================
    def CHANGE_VALUES(self, _this):

        # -------------------------------------------------------------------
        if _this == "only_completed":
            if self.ONLY_COMPLETED_CHECKBOX.isChecked():
                self.CALCULATE_ONLY_COMPLETED = True;
            else:
                self.CALCULATE_ONLY_COMPLETED = False;

        # -------------------------------------------------------------------
        self.CREATE_LISTS();
        # -------------------------------------------------------------------

    # =======================================================================
    def CREATE_PAIRS_SELECTOR(self, ALL=False):

        # -------------------------------------------------------------------
        if not ALL:
            for PAIR in self.CONF["API"]["PAIRS"]:
                self.PAIR_COMBO.addItem(PAIR.upper());

        else:
            for PAIR in self.CONF["API"]["ALL_PAIRS"]:
                self.PAIR_COMBO.addItem(PAIR.upper());

        for i in xrange(0, self.PAIR_COMBO.__len__()):

            self.PAIR_COMBO.setItemData( i, QColor("#333"),Qt.BackgroundRole );
            self.PAIR_COMBO.setItemData( i, QColor("#fff"),Qt.ForegroundRole );
            #self.PAIR_COMBO.setItemData( i, QFont('monospace', 16, -1, False), Qt.FontRole);
        # -------------------------------------------------------------------

    # =======================================================================
    def SEND_VALUES_TO_TRADE_TERMINAL(self, _action):

        # -------------------------------------------------------------------
        if _action == "SELECT_VALUES":

            self.DATA_TO_SEND_SELECTED = True;
            #self.DATA_TO_SEND = [ str(item).stip() for iten in str(self.BOOKKEEPING_WIDGET.currentItem().text()).strip().split("|")];
            self.DATA_TO_SEND = str(self.BOOKKEEPING_WIDGET.currentItem().text()).strip().split("|")[1].split("#")[0].strip();

        elif _action == "SEND_VALUES":

            if self.DATA_TO_SEND_SELECTED:

                _SQL = "SELECT buy_order_id, sell_order_id FROM "+self.PARENT.CURR_PAIR;
                _SQL += " WHERE BKKPG_UID="+self.DATA_TO_SEND;

                DATA = self.PARENT.DB.FETCH("BOOK_DB", _SQL, ALL=False);

                if DATA[0] != 0 and DATA[1] != 0:

                    self.PARENT.GUI.SHOW_QMESSAGE("info", "This UID is Full!<br> You can't add data to it enymore.<br>Bud You can delete sell and/or buy part<br/> and add new part.");
                    return;

                self.PARENT.GUI.BKKPG_UID_VALUE.setText( self.DATA_TO_SEND );

                self.PARENT.GUI.CONTROL_TRADINGS_BTNS("buy", "show");
                self.PARENT.GUI.CONTROL_TRADINGS_BTNS("sell", "show");

                self.DATA_TO_SEND_SELECTED = False;
                self.DATA_TO_SEND = None;

                # Clear Lables 
                self.SEND_ID_LABLE.setText( "n/a" );
                self.SEND_AMOUNT_LABLE.setText( "n/a" );
                self.SEND_AT_PRICE_LABLE.setText( "n/a" );


                if DATA[0] == 0:
                    self.PARENT.GUI.CONTROL_TRADINGS_BTNS("sell", "hide");

                else:
                    self.PARENT.GUI.CONTROL_TRADINGS_BTNS("buy", "hide");


                # Switch to Trader-Tab
                self.PARENT.GUI.MAIN_TABS.setCurrentIndex(0);

            else:

                self.PARENT.GUI.SHOW_QMESSAGE("info", " Select first item which one you would like<br/> send to the Trade-Terminal !");
                return; 
                
        # -------------------------------------------------------------------
        if self.DATA_TO_SEND is not None:
    
            self.SEND_ID_LABLE.setText( self.DATA_TO_SEND );

            #self.SEND_AMOUNT_LABLE.setText( self.DATA_TO_SEND[2] );
            #self.SEND_AT_PRICE_LABLE.setText( self.DATA_TO_SEND[3] );
 
        # -------------------------------------------------------------------

    # =======================================================================

###################################################################################################


