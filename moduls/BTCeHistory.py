#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# BulitIn
import json, sys, time
from random import randint
# PyQt4
from PyQt4.QtGui import QMessageBox, QTextEdit, QDialog, QPolygonF,QPainter, QPen, QColor 
from PyQt4.QtGui import QBrush, QMainWindow,QWidget,QToolTip,QApplication, QFont,QIcon,QAction
from PyQt4.QtGui import QFrame,QListWidget, QListWidgetItem, QComboBox,QCheckBox,QPushButton
from PyQt4.QtGui import QProgressBar, QLineEdit, QLabel, QStyleOptionComboBox

from PyQt4.QtCore import QTimer, SIGNAL, SLOT, Qt, QPointF, QPoint, QRectF, QRect
from PyQt4.QtCore import pyqtSlot

###################################################################################################
class History(QFrame):

    # =======================================================================
    def __init__(self, parent=None, _PARENT=None):

        # -------------------------------------------------------------------
        QFrame.__init__(self, parent);
        # -------------------------------------------------------------------
        self.PARENT                         = _PARENT;
        self.CONF                           = _PARENT.CONF;

        self.BOOK                           = { "bought" : [], "sold" : [] };

        # -------------------------------------------------------------------
        self.setGeometry( 3, 5, 975, 555 );
        self.setStyleSheet( "QFrame{ font: 12px 'monospace'; color: #000; background-color: transparent; background-image: url('./data/imgs/TAB_History.png'); }" );

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
        list_style                          = "QListWidget{ font: 10px 'monospace'; color: #fff;  background-color: #000; border-style: none; background-image: url('./data/imgs/TAB_History_line.png'); }"; # ./data/imgs/BookKeeping_line.png
        lable_style                         = "QLabel{ font: 10px 'monospace'; color: #fff;  background-color: transparent; border-style: none; background-image: url(''); }"; 
        # -------------------------------------------------------------------

        # Bought
        self.BOOKKEEPING_BOUGHT_WIDGET      = QListWidget( self );
        self.BOOKKEEPING_BOUGHT_WIDGET.setGeometry( 13, 144, 469, 400 );
        self.BOOKKEEPING_BOUGHT_WIDGET.setStyleSheet( list_style );

        self.connect( self.BOOKKEEPING_BOUGHT_WIDGET, SIGNAL('itemSelectionChanged()'), lambda: self.SEND_VALUES_TO_TRADE_TERMINAL("BOUGHT_WIDGET") );
        self.BOOKKEEPING_BOUGHT_WIDGET.itemClicked.connect( lambda: self.SEND_VALUES_TO_TRADE_TERMINAL("BOUGHT_WIDGET") );


        self.BOUGHT_TTL_LABLE               = QLabel("0.0", self);
        self.BOUGHT_TTL_LABLE.setGeometry( 272, 406, 85, 17 );
        #self.BOUGHT_TTL_LABLE.setEditable( False );
        self.BOUGHT_TTL_LABLE.setStyleSheet( lable_style );
        self.BOUGHT_TTL_LABLE.hide();
        self.BOUGHT_TTL                     = 0;

        self.BOUGHT_TTL_PLUS_FEE_LABLE      = QLabel("0.0", self);
        self.BOUGHT_TTL_PLUS_FEE_LABLE.setGeometry( 362, 406, 118, 17 );
        #self.BOUGHT_TTL_PLUS_FEE_LABLE.setEditable( False );
        self.BOUGHT_TTL_PLUS_FEE_LABLE.setStyleSheet( lable_style );
        self.BOUGHT_TTL_PLUS_FEE_LABLE.hide();
        self.BOUGHT_TTL_PLUS_FEE            = 0;

        # -------------------------------------------------------------------
        # Sold
        self.LAST_ACTIVE_WIDGET             = None; 

        self.BOOKKEEPING_SOLD_WIDGET        = QListWidget( self );
        self.BOOKKEEPING_SOLD_WIDGET.setGeometry( 493, 144, 469, 400 );
        self.BOOKKEEPING_SOLD_WIDGET.setStyleSheet( list_style );

        self.connect( self.BOOKKEEPING_SOLD_WIDGET, SIGNAL('itemSelectionChanged()'), lambda: self.SEND_VALUES_TO_TRADE_TERMINAL("SOLD_WIDGET") );
        self.BOOKKEEPING_SOLD_WIDGET.itemClicked.connect( lambda: self.SEND_VALUES_TO_TRADE_TERMINAL("SOLD_WIDGET") );

        self.SOLD_TTL_LABLE                 = QLabel("0.0", self);
        self.SOLD_TTL_LABLE.setGeometry( 752, 406, 85, 17 );
        #self.SOLD_TTL_LABLE.setEditable( False );
        self.SOLD_TTL_LABLE.setStyleSheet( lable_style );
        self.SOLD_TTL_LABLE.hide();
        self.SOLD_TTL                       = 0;

        self.SOLD_TTL_PLUS_FEE_LABLE        = QLabel("0.0", self);
        self.SOLD_TTL_PLUS_FEE_LABLE.setGeometry( 842, 406, 118, 17 );
        #self.SOLD_TTL_PLUS_FEE_LABLE.setEditable( False );
        self.SOLD_TTL_PLUS_FEE_LABLE.setStyleSheet( lable_style );
        self.SOLD_TTL_PLUS_FEE_LABLE.hide();
        self.SOLD_TTL_PLUS_FEE              = 0;

        # -------------------------------------------------------------------
        """
        self.DATA_TO_SEND                   = None;

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
        """

        # -------------------------------------------------------------------
        self._i_                            = "|"; # List delimiter

        # -------------------------------------------------------------------
        self.ONLY_FILLED_CHECKBOX           = QCheckBox("", self);
        self.ONLY_FILLED_CHECKBOX.setGeometry( 647, 444, 17, 17 );
        self.ONLY_FILLED_CHECKBOX.setCheckState(Qt.Checked);
        #self.ONLY_FILLED_CHECKBOX.setEnabled(False);
        self.connect(self.ONLY_FILLED_CHECKBOX, SIGNAL('stateChanged(int)'), lambda: self.CHANGE_VALUES("only_filled") );
        self.ONLY_FILLED_CHECKBOX.hide();

        self.CALCULATE_ONLY_FILLED          = True;
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
            print(_exception);
        # -------------------------------------------------------------------

    # =======================================================================
    def CREATE_LISTS(self):

        # -------------------------------------------------------------------
        CURR_PAIR =  str(self.PAIR_COMBO.currentText()).lower();

        # -------------------------------------------------------------------
        self.BOOK = { "bought" : [], "sold" : [] };

        self.BOUGHT_TTL = 0;
        self.BOUGHT_TTL_PLUS_FEE = 0;

        self.SOLD_TTL = 0;
        self.SOLD_TTL_PLUS_FEE = 0;

        # -------------------------------------------------------------------
        # Bought List
        # id, order_id, unix_time, action, filled, amount, at_price, fee, ttl, grand_ttl

        #self.PARENT.DB.EXEC( "HISTORY_DB", "DELETE FROM "+CURR_PAIR+" WHERE id>7" );


        DATA = self.PARENT.DB.FETCH("HISTORY_DB", "SELECT * FROM "+CURR_PAIR+" WHERE action='bought' ORDER BY id DESC", ALL=True);
        self.BOOKKEEPING_BOUGHT_WIDGET.clear();

        for data in DATA:

            # ---------------------------------------------------------------
            # In-Memory DATA

            self.BOOK[ data[3] ].append( {
                                        
                                            "id"        : data[0] , 
                                            "order_id"  : data[1] , 
                                            "unix_time" : data[2] , 
                                            "action"    : data[3] , 
                                            "filled"    : data[4] , 
                                            "amount"    : data[5] , 
                                            "at_price"  : data[6] , 
                                            "fee"       : data[7] , 
                                            "ttl"       : data[8] , 
                                            "grand_ttl" : data[9]


                                        } );

            if self.CALCULATE_ONLY_FILLED:
                if data[4] == 1:
                    self.BOUGHT_TTL += data[8];
                    self.BOUGHT_TTL_PLUS_FEE += data[9];

            else:
                self.BOUGHT_TTL += data[8];
                self.BOUGHT_TTL_PLUS_FEE += data[9];

            # ---------------------------------------------------------------
            # Formatinf data to Display in BookKeeping Wodget

            item = "";

            item += "DEL{:6} DEL".format(str( data[0] )); # id
            #item += "{:11} DEL".format( data[1] ); # order_id
            #item += "{:11} DEL".format( data[2] ); # unix_time
            #item += "{:11} DEL".format( data[3] ); # action
            #item += "{:11} DEL".format( data[4] ); # filed
            item += "{:13} DEL".format( str("{:10,.6f}".format( data[5] )).strip() ); # Amount
            item += "{:13} DEL".format( str("{:10,.6f}".format( data[6] )).strip() ); # at_price
            #item += "{:13} DEL".format( str("{:10,.6f}".format( data[7] )).strip() ); # fee
            item += "{:13} DEL".format( str("{:10,.6f}".format( data[8] )).strip() ); # ttl
            item += "{:13}".format( str("{:10,.6f}".format( data[9] )).strip() ); # grand_ttl
            
            #self.BOOKKEEPING_BOUGHT_WIDGET.addItem( item.replace("DEL", self._i_) );
            newItem = QListWidgetItem( QIcon("./data/imgs/icon_filled_status_"+str(data[4])+".png"), item.replace("DEL", self._i_), self.BOOKKEEPING_BOUGHT_WIDGET, 0);
            newItemToolTip = "Order ID: #"+str(data[1])+" Created: "+time.ctime(int(data[2]));


            newItem.setToolTip(newItemToolTip);


            # ---------------------------------------------------------------
        # / for
        # -------------------------------------------------------------------
        self.BOUGHT_TTL_LABLE.setText( str("{:10,.6f}".format( self.BOUGHT_TTL ).strip()) );
        self.BOUGHT_TTL_PLUS_FEE_LABLE.setText( str("{:10,.6f}".format( self.BOUGHT_TTL_PLUS_FEE ).strip()) );

        # -------------------------------------------------------------------
        # Sold List
        # id, order_id, unix_time, action, filled, amount, at_price, fee, ttl, grand_ttl

        DATA = self.PARENT.DB.FETCH("HISTORY_DB", "SELECT * FROM "+CURR_PAIR+" WHERE action='sold' ORDER BY id DESC", ALL=True);
        self.BOOKKEEPING_SOLD_WIDGET.clear();

        for data in DATA:

            # ---------------------------------------------------------------
            # In-Memory DATA

            self.BOOK[ data[3] ].append( {
                                        
                                            "id"        : data[0] , 
                                            "order_id"  : data[1] , 
                                            "unix_time" : data[2] , 
                                            "action"    : data[3] , 
                                            "filled"    : data[4] , 
                                            "amount"    : data[5] , 
                                            "at_price"  : data[6] , 
                                            "fee"       : data[7] , 
                                            "ttl"       : data[8] , 
                                            "grand_ttl" : data[9]


                                        } );

            if self.CALCULATE_ONLY_FILLED:
                if data[4] == 1:
                    self.SOLD_TTL += data[8];
                    self.SOLD_TTL_PLUS_FEE += data[9];

            else:
                self.SOLD_TTL += data[8];
                self.SOLD_TTL_PLUS_FEE += data[9];

            # ---------------------------------------------------------------
            # Formatinf data to Display in BookKeeping Wodget

            item = "";

            item += "DEL{:6} DEL".format(str( data[0] )); # id
            #item += "{:11} DEL".format( data[1] ); # order_id
            #item += "{:11} DEL".format( data[2] ); # unix_time
            #item += "{:11} DEL".format( data[3] ); # action
            #item += "{:11} DEL".format( data[4] ); # filed
            item += "{:13} DEL".format( str("{:10,.6f}".format( data[5] )).strip() ); # Amount
            item += "{:13} DEL".format( str("{:10,.6f}".format( data[6] )).strip() ); # at_price
            #item += "{:13} DEL".format( str("{:10,.6f}".format( data[7] )).strip() ); # fee
            item += "{:13} DEL".format( str("{:10,.6f}".format( data[8] )).strip() ); # ttl
            item += "{:13}".format( str("{:10,.6f}".format( data[9] )).strip() ); # grand_ttl

            #self.BOOKKEEPING_SOLD_WIDGET.addItem( item.replace("DEL", self._i_) );
            newItem = QListWidgetItem( QIcon("./data/imgs/icon_filled_status_"+str(data[4])+".png"), item.replace("DEL", self._i_), self.BOOKKEEPING_SOLD_WIDGET, 0);
            
            newItemToolTip = "Order ID: #"+str(data[1])+" Created: "+time.ctime(int(data[2]));

            newItem.setToolTip(newItemToolTip);
            # ---------------------------------------------------------------
        # / for
        # -------------------------------------------------------------------
        self.SOLD_TTL_LABLE.setText( str("{:10,.6f}".format( self.SOLD_TTL ).strip()) );
        self.SOLD_TTL_PLUS_FEE_LABLE.setText( str("{:10,.6f}".format( self.SOLD_TTL_PLUS_FEE ).strip()) );

        # -------------------------------------------------------------------

    # =======================================================================
    def CHANGE_VALUES(self, _this):

        # -------------------------------------------------------------------
        if _this == "only_filled":
            if self.ONLY_FILLED_CHECKBOX.isChecked():
                self.CALCULATE_ONLY_FILLED = True;
            else:
                self.CALCULATE_ONLY_FILLED = False;

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
        if _action == "BOUGHT_WIDGET":

            self.LAST_ACTIVE_WIDGET = "BOUGHT_WIDGET";
            self.DATA_TO_SEND = str(self.BOOKKEEPING_BOUGHT_WIDGET.currentItem().text()).strip().split("|");  

            #self.SEND_ID_LABLE.setFocus();          

        elif _action == "SOLD_WIDGET":

            self.LAST_ACTIVE_WIDGET = "SOLD_WIDGET";
            self.DATA_TO_SEND = str(self.BOOKKEEPING_SOLD_WIDGET.currentItem().text()).strip().split("|");
        
            #self.SEND_ID_LABLE.setFocus();          

        elif _action == "SEND_VALUES":

            if self.LAST_ACTIVE_WIDGET is not None:

                self.PARENT.GUI.USER_SELL_AMOUNT.setText( self.DATA_TO_SEND[2].strip() );
                self.PARENT.GUI.USER_SELL_AT_PRICE.setText( self.DATA_TO_SEND[3].strip() );

                self.PARENT.GUI.USER_BUY_AMOUNT.setText( self.DATA_TO_SEND[2].strip() );
                self.PARENT.GUI.USER_BUY_AT_PRICE.setText( self.DATA_TO_SEND[3].strip() );

                self.LAST_ACTIVE_WIDGET = None;
                self.DATA_TO_SEND = None;

                # Show Tradeer Tab
                self.PARENT.GUI.MAIN_TABS.setCurrentIndex(0);

                # Clear Lables 
                self.SEND_ID_LABLE.setText( "n/a" );
                self.SEND_AMOUNT_LABLE.setText( "n/a" );
                self.SEND_AT_PRICE_LABLE.setText( "n/a" );

            else:

                self.PARENT.GUI.SHOW_QMESSAGE("info", " Select first item which one you would like<br/> send to the Trade-Terminal !");
                return; 
                
        # -------------------------------------------------------------------
        if self.DATA_TO_SEND is not None:
    
            self.SEND_ID_LABLE.setText( self.DATA_TO_SEND[1] );
            self.SEND_AMOUNT_LABLE.setText( self.DATA_TO_SEND[2] );
            self.SEND_AT_PRICE_LABLE.setText( self.DATA_TO_SEND[3] );

        # -------------------------------------------------------------------

    # =======================================================================
    def DELETE_ORDER(self, _order_id, _pair, _type):

        # ------------------------------------------------------------------
        self.PARENT.DB.EXEC("HISTORY_DB", "DELETE FROM "+_pair+" WHERE order_id="+str(_order_id));

        # ------------------------------------------------------------------

    # =======================================================================

###################################################################################################


