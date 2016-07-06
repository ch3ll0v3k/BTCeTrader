#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# Built IN
import json, sys, time
from datetime import datetime

# PyQt4
from PyQt4.QtCore import QTimer, SIGNAL, SLOT, Qt, QPointF, QPoint, QRectF, QRect
from PyQt4.QtGui import QMessageBox, QTextEdit, QDialog, QPolygonF,QPainter, QPen, QColor 
from PyQt4.QtGui import QBrush, QMainWindow,QWidget,QToolTip,QApplication, QFont,QIcon,QAction
from PyQt4.QtGui import QFrame,QComboBox,QCheckBox,QPushButton,QProgressBar,QLineEdit,QLabel
from PyQt4.QtGui import QTextBrowser, QCursor, qApp, QDesktopWidget, QScrollArea, QVBoxLayout
from PyQt4.QtGui import QGraphicsView, QGraphicsScene, QPicture, QPaintDevice, QStaticText

from PyQt4.QtGui import QListWidget, QListWidgetItem, QListView


from PyQt4.QtGui import  QDoubleValidator

###################################################################################################
class OrdersWidget(QFrame):

    # =======================================================================
    def __init__(self, parent=None, _PARENT=None):

        # -------------------------------------------------------------------
        QFrame.__init__(self, parent);
        # -------------------------------------------------------------------
        self.setGeometry( 3, 5, 968, 555 );
        self.setStyleSheet("QFrame{ color: #fff;  background-image: url('./data/imgs/TAB_Orders.png'); }" );

        # -------------------------------------------------------------------
        self.PARENT                         = _PARENT;
        self.CONF                           = _PARENT.CONF;
        self.ORDER_ID_TO_CANCEL             = False;
        self.ORDER_TYPE_TO_CANCEL           = False; # buy/sell to be able delete records from bookkeeping separatly

        self.ORDERS_FROM_DB                 = {};

        # -------------------------------------------------------------------
        WIDGETS_W = 469;
        WIDGETS_H = 325;
        WIDGETS_ML = 13;
        WIDGETS_MT = 144;

        list_style                          = "QListWidget{ font: 10px 'monospace'; color: #fff;  background-color: #000; border-style: none; background-image: url('./data/imgs/TAB_Orders_line.png'); }";

        # BUY
        self.ORDERS_LIST_BUY = QListWidget(self);
        self.ORDERS_LIST_BUY.setGeometry( WIDGETS_ML, WIDGETS_MT, WIDGETS_W, WIDGETS_H );
        self.ORDERS_LIST_BUY.setStyleSheet( list_style );
        self.ORDERS_LIST_BUY.setViewMode( QListView.ListMode );

        self.connect( self.ORDERS_LIST_BUY, SIGNAL('itemSelectionChanged()'), lambda: self.SELECT_ORDER_ID("buy") );
        self.ORDERS_LIST_BUY.itemClicked.connect( lambda: self.SELECT_ORDER_ID("buy") )

        # SELL
        self.ORDERS_LIST_SELL = QListWidget(self);
        self.ORDERS_LIST_SELL.setGeometry( WIDGETS_W+(WIDGETS_ML*2 )-1, WIDGETS_MT, WIDGETS_W-1, WIDGETS_H );
        self.ORDERS_LIST_SELL.setStyleSheet( list_style );

        self.connect( self.ORDERS_LIST_SELL, SIGNAL('itemSelectionChanged()'), lambda: self.SELECT_ORDER_ID("sell") );
        self.ORDERS_LIST_SELL.itemClicked.connect( lambda: self.SELECT_ORDER_ID("sell") )
        # -------------------------------------------------------------------
        self.CANCEL_ORDER_BTN = QPushButton("Apply", self);
        self.CANCEL_ORDER_BTN.setGeometry( 555, 506, 80, 30 );

        self._i_                            = "|"; # List delimiter

        # -------------------------------------------------------------------
        self.INIT();
        # -------------------------------------------------------------------

    # =======================================================================
    def INIT(self):

        # -------------------------------------------------------------------
        self.GET_ORDERS_FROM_DB();
        # -------------------------------------------------------------------

    # =======================================================================
    def SELECT_ORDER_ID(self, _type):

        # -------------------------------------------------------------------
        try:

            self.ORDER_TYPE_TO_CANCEL = _type;

            if _type == "sell":
                self.ORDER_ID_TO_CANCEL = str(self.ORDERS_LIST_SELL.currentItem().text()).split("|")[0].strip()[1:];

            elif _type == "buy":
                self.ORDER_ID_TO_CANCEL = str(self.ORDERS_LIST_BUY.currentItem().text()).split("|")[0].strip()[1:];


        except Exception as _exception:
            print(_exception);
        # -------------------------------------------------------------------

    # =======================================================================
    def CREATE_LISTS(self):

        # -------------------------------------------------------------------
        try:

            self.ORDERS_LIST_SELL.clear();
            self.ORDERS_LIST_BUY.clear();

            for ID in self.ORDERS_FROM_DB:

                item = "";

                item += "#{:11} DEL".format( str(ID) ); # order_id
                item += "{:7} DEL".format( self.ORDERS_FROM_DB[ID]["pair"] ); # type
                item += "{:13} DEL".format( str("{:10,.6f}".format( self.ORDERS_FROM_DB[ID]["amount"] )).strip() ); # Amount
                item += "{:13} DEL".format( str("{:10,.6f}".format( self.ORDERS_FROM_DB[ID]["at_price"] )).strip() ); # at_price

                newItemToolTip = "Order ID: #"+str(ID)+" Created: "+time.ctime( self.ORDERS_FROM_DB[ID]["unix_time"] );
                
                if self.ORDERS_FROM_DB[ID]["type"] == "buy":

                    ttl = self.ORDERS_FROM_DB[ID]["amount"] - (self.ORDERS_FROM_DB[ID]["amount"]/100*self.PARENT.FEE);

                    item += "{:13}".format( str("{:10,.6f}".format( ttl )).strip() ); # ttl_usd
                    newItem = QListWidgetItem( QIcon("./data/imgs/icon_filled_status_0.png"), item.replace("DEL", self._i_), self.ORDERS_LIST_BUY, 0);
                    newItem.setToolTip(newItemToolTip);

                elif self.ORDERS_FROM_DB[ID]["type"] == "sell":

                    ttl = self.ORDERS_FROM_DB[ID]["at_price"]*self.ORDERS_FROM_DB[ID]["amount"];
                    ttl -= (ttl/100*self.PARENT.FEE);
                    
                    item += "{:13}".format( str("{:10,.6f}".format( ttl )).strip() ); # ttl_usd
                    newItem = QListWidgetItem( QIcon("./data/imgs/icon_filled_status_0.png"), item.replace("DEL", self._i_), self.ORDERS_LIST_SELL, 0);
                    newItem.setToolTip(newItemToolTip);

        except Exception as _exception:
            print("FRAME_ORDER.CREATE_LISTS: "+str(_exception));

        # -------------------------------------------------------------------

    # =======================================================================
    def DELETE_ORDER(self, _order_id, _pair, _type):

        # ------------------------------------------------------------------
        _SQL = "DELETE FROM "+_pair+" WHERE order_id="+str(_order_id);
        self.PARENT.DB.EXEC("ORDERS_DB", _SQL );

        # ------------------------------------------------------------------

    # =======================================================================
    def UPDATE_ACTIVE_ORDERS(self):

        # ------------------------------------------------------------------
        pass;
        # ------------------------------------------------------------------
 
    # =======================================================================
    def GET_ORDERS_FROM_DB(self):

        # ------------------------------------------------------------------
        #del self.ORDERS_FROM_DB;
        #self.ORDERS_FROM_DB = {};
        # ------------------------------------------------------------------
        for PAIR in self.CONF["API"]["ALL_PAIRS"]:

            THIS_FIELDS = "order_id, unix_time, filled, at_price, amount, pair, type";

            DATA = self.PARENT.DB.FETCH("ORDERS_DB", "SELECT "+THIS_FIELDS+" FROM "+PAIR+" WHERE filled=0", ALL=True);

            _len = len(DATA);

            for order_id, unix_time, filled, at_price, amount, pair, _type in DATA:
                self.ORDERS_FROM_DB[ order_id ] = { "order_id":order_id, "unix_time":unix_time, "filled":filled, "at_price":at_price, "amount":amount, "pair":pair, "type":_type };

            """
            if _len > 0:
                #print(order_id, "->", self.ORDERS_FROM_DB[ order_id ])
                print(self.ORDERS_FROM_DB)
            exit();
            """ 
        # ------------------------------------------------------------------

    # =======================================================================

###################################################################################################