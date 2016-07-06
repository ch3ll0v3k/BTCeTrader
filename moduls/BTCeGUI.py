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

# OyQt
from PyQt4.QtCore import QTimer, SIGNAL, SLOT, Qt, QPointF, QPoint, QRectF, QRect, QThread, QString
from PyQt4.QtCore import pyqtSignal, pyqtSlot, QObject, QSize, QByteArray, QEvent

from PyQt4.QtGui import QMessageBox, QTextEdit, QDialog, QPolygonF, QPainter, QPen, QColor, QImage
from PyQt4.QtGui import QBrush, QMainWindow, QWidget, QToolTip, QApplication, QFont, QIcon, QAction
from PyQt4.QtGui import QFrame, QListWidget, QComboBox, QCheckBox, QPushButton, QProgressBar, QLineEdit, QLabel
from PyQt4.QtGui import QTextBrowser, QCursor, qApp, QDesktopWidget, QGraphicsView, QGraphicsScene, QPicture
from PyQt4.QtGui import QSplashScreen, QPixmap, QTabWidget, QMovie, QPaintDevice, QSizePolicy

from PyQt4.QtGui import QDoubleValidator, QRadioButton, QButtonGroup, QHBoxLayout, QVBoxLayout
from PyQt4.QtGui import QLCDNumber, QStyleOptionTabWidgetFrame

# BTCeTrader modules
from BTCeStyle import STL
from BTCePloter import PlotterQFrame
from BTCeOrdersWidget import OrdersWidget
from BTCeSound import Sound
from BTCeNoteBook import NoteBook
from BTCeBookKeeping import BookKeeping
from BTCeHistory import History
from BTCeChat import Chat
from BTCePlotterHoverLayer import PlotterHoverLayer
from BTCeBrowser import Browser


###################################################################################################
class GUI(QMainWindow, QWidget):

    # =======================================================================
    def __init__(self, _CONF, _REQUEST, parent=None):

        # -------------------------------------------------------------------
        QMainWindow.__init__(self, parent=None);
        QWidget.__init__(self, parent=None);

        # -------------------------------------------------------------------
        self.AVAILABLE                          = False;
        self.CONF                               = _CONF;
        self.PARENT                             = parent;
        self.Request                            = _REQUEST;

        self.LOG_MANAGER_TIMER                  = QTimer()

        self.LOG_MANAGER_UPD_DELAY              = 1000;
        self.ALLOW_DISPLAY_LOG                  = False;
        self.ALLOW_UPD_METADATA                 = False;

        # -------------------------------------------------------------------
        self.Sound                              = Sound(parent);
        #self.Sound.SOUND_TEST();
        #if self.CONF["SYS"]["ALLOW_SOUND"]: self.Sound.RING( _type=1 );
        # -------------------------------------------------------------------
        if self.CONF["SYS"]["GUI"]["SPLASH"]["SHOW"]:

            _Splash = Splash(
                _msg=" Please wait. Loading ...  ", 
                _app=self.CONF["INFO"]["NAME"], 
                _ver=self.CONF["INFO"]["VERSION"], 
                _link=self.CONF["INFO"]["LINK"], 
                _author=self.CONF["INFO"]["AUTHOR"]  
            );

        # -------------------------------------------------------------------
        self.DESKTOP                            = QDesktopWidget();
        self.SCREEN                             = self.DESKTOP.screenGeometry();
        self.SCREEN_W                           = self.SCREEN.width();
        self.SCREEN_H                           = self.SCREEN.height();

        # -------------------------------------------------------------------
        self.MARKET_VOLUME_LIMIT                = 60;
        # -------------------------------------------------------------------
        QToolTip.setFont(QFont(STL.FONT_MAIN, STL.FONT_MAIN_SIZE));
        
        self.setGeometry(
            self.CONF["SYS"]["GUI"]["ML"], self.CONF["SYS"]["GUI"]["MT"], 
            self.CONF["SYS"]["GUI"]["W"], self.CONF["SYS"]["GUI"]["H"]
        );
        
        self.setWindowTitle(
            self.CONF["INFO"]["NAME"]+' - '+self.CONF["INFO"]["VERSION"]+' - by: '+ 
            self.CONF["INFO"]["AUTHOR"]+' - '+self.CONF["INFO"]["LICENS"]
        );
        
        self.setWindowIcon( QIcon(STL.WINDOWICON) );
        self.setFixedSize( self.geometry().width(), self.geometry().height() );
        #self.WindowFlags = [Qt.Drawer, Qt.SplashScreen, Qt.FramelessWindowHint, Qt.Tool,Qt.Desktop,Qt.Widget,Qt.Window, Qt.Dialog];
        #self.setWindowFlags(Qt.Dialog & Qt.WindowMinimizeButtonHint);
        #self.setWindowFlags(self.windowFlags() | Qt.Window | Qt.WindowMinimizeButtonHint);
        #self.setWindowFlags(Qt.WindowMaximizeButtonHint);
        # -------------------------------------------------------------------
        qApp.setStyle("Windowsxp"); # "Windows", "Motif", "Cde", "Plastique", "Windowsxp", "Macintosh"
        self.DESKTOP                        = QDesktopWidget();
        self.SCREEN                         = self.DESKTOP.screenGeometry();

        #self.setEnabled(False);
        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
        # MENU-BAR

        # Menu bar 
        #self.MENU_BAR = self.menuBar();
        #self.MENU_BAR.setEnabled(True);

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
        # MENUS 

        # File
        #self.MENU_File = self.MENU_BAR.addMenu('&File');

        # Tools
        #self.MENU_Tools = self.MENU_BAR.addMenu('&Tools');

        # help
        #self.MENU_Help = self.MENU_BAR.addMenu('&Help');

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
        # SUB-MENUS

        """
        self.SUB_MENU_exit = QAction(QIcon(STL.ICON_EXIT), 'Exit', self);
        self.SUB_MENU_exit.setShortcut('Ctrl+Q');
        self.SUB_MENU_exit.setStatusTip('Exit application');
        self.connect(self.SUB_MENU_exit, SIGNAL('triggered()'), self.GUI_EXIT);
        self.MENU_File.addAction(self.SUB_MENU_exit);
        """

        """
        self.SUB_MENU_open = QAction(QIcon(STL.ICON_EXIT), 'Open', self);
        self.SUB_MENU_open.setShortcut('Ctrl+O');
        self.SUB_MENU_open.setStatusTip('Open new File');
        self.connect(self.SUB_MENU_open, SIGNAL('triggered()'), SLOT('close()'));
        self.MENU_File.addAction(self.SUB_MENU_open);
        """

        """
        self.TEST_ACTION = QAction(QIcon(STL.ICON_EXIT), 'Open', self);
        self.TEST_ACTION.setShortcut('Ctrl+P');
        self.TEST_ACTION.setStatusTip('CTRL+P');
        self.connect(self.TEST_ACTION, SIGNAL('triggered()'), self.TEST_METHOD);
        self.MENU_Tools.addAction(self.TEST_ACTION);
        """

        ####################################################################
        # TABS-TAB-BEGIN QTabWidget
        ####################################################################
        self.MAIN_TABS = QTabWidget(self);
        self.MAIN_TABS.setGeometry( 5, 0, 985, 630 ); # (5, 35, 985, 595) 
        #self.MAIN_TABS.setTabShape(self.MAIN_TABS.Rounded);
        self.MAIN_TABS.setStyleSheet('QTabBar { font: 16px "monospace"; color: #333; background-color: transparent; padding-top: 5px; padding-bottom: 5px; font-weight: bold;  }');
        
        """
        TAB_STYLE = QStyleOptionTabWidgetFrame();
        TAB_STYLE.tabBarSize = QSize(60, 60);
        TAB_STYLE.leftCornerWidgetSize = QSize(60, 60);
        TAB_STYLE.rightCornerWidgetSize = QSize(1, 1);

        QSize leftCornerWidgetSize
        int lineWidth
        int midLineWidth
        QSize rightCornerWidgetSize
        QTabBar.Shape shape
        QSize tabBarSize
        self.MAIN_TABS.initStyleOption( TAB_STYLE );
        """




        ####################################################################
        # TABS-TAB Trader

        self.TAB_Trader = QWidget();

        self.FRAME_MAIN = QFrame(self.TAB_Trader);

        self.FRAME_MAIN.setGeometry(3, 5, 975, 590);
        self.FRAME_MAIN.setStyleSheet(STL.FRAME_MAIN);
        self.FRAME_MAIN.setEnabled(True);
        self.FRAME_MAIN.show();
        #self.FRAME_MAIN.NAME = "QFrame: on self.TAB_Trader. "

        # ----------------------------------------------------
        self.ARROW_U = QPixmap("data/imgs/arrow_u_20px.png");
        self.ARROW_D = QPixmap("data/imgs/arrow_d_20px.png");
        self.ARROW_N = QPixmap("data/imgs/arrow_n_20px.png");

        self.CALC_PIX = QPixmap("data/imgs/calc_58px.png");

        self.INIT_VALUE_0 = "0.0000000";
        self.INIT_VALUE_1 = "1.0000000";
        QDouble         = [0, 1, 7]; # Input Validation QdoubleValidation
        
        PRICES_SIZE     = [180, 40];
        BTNS_SIZE       = [81, 42];
        INPUT_SIZE      = [125, 21];

        # ----------------------------------------------------
        PANELS_SIZE     = [201, 189];
        PANELS_MT       = 50;

        # BID PANEL
        self.PANEL_BUY_ORDERS = QListWidget(self.FRAME_MAIN);
        self.PANEL_BUY_ORDERS.setGeometry(767, PANELS_MT, PANELS_SIZE[0], PANELS_SIZE[1]);
        self.PANEL_BUY_ORDERS.setStyleSheet(STL.PANEL_ASK_BID)
        self.PANEL_BUY_ORDERS.itemClicked.connect( lambda: self.ORDERS_PANEL_ACTION("buy") );
        self.connect( self.PANEL_BUY_ORDERS, SIGNAL('itemSelectionChanged()'), lambda: self.ORDERS_PANEL_ACTION("buy") );

        self.PANEL_BUY_ORDERS_TOOLTIP = QLabel(self.FRAME_MAIN);
        self.PANEL_BUY_ORDERS_TOOLTIP.setGeometry(942, 8, 30, 30);
        self.PANEL_BUY_ORDERS_TOOLTIP.setStyleSheet(STL.TRANSPARENT_TOOLTIP);
        self.PANEL_BUY_ORDERS_TOOLTIP.setToolTip('Latest price: Buy Orders! ');


        # ASK PANEL
        self.PANEL_SELL_ORDERS = QListWidget(self.FRAME_MAIN);
        self.PANEL_SELL_ORDERS.setGeometry(7, PANELS_MT, PANELS_SIZE[0], PANELS_SIZE[1]);
        self.PANEL_SELL_ORDERS.setStyleSheet(STL.PANEL_ASK_BID)
        self.PANEL_SELL_ORDERS.itemClicked.connect( lambda: self.ORDERS_PANEL_ACTION("sell")  );
        self.connect( self.PANEL_SELL_ORDERS, SIGNAL('itemSelectionChanged()'), lambda: self.ORDERS_PANEL_ACTION("sell") );

        self.PANEL_SELL_ORDERS_TOOLTIP = QLabel(self.FRAME_MAIN);
        self.PANEL_SELL_ORDERS_TOOLTIP.setGeometry(184, 8, 30, 30);
        self.PANEL_SELL_ORDERS_TOOLTIP.setStyleSheet(STL.TRANSPARENT_TOOLTIP);
        self.PANEL_SELL_ORDERS_TOOLTIP.setToolTip(' Latest price: Sell Orders! ');

        # ----------------------------------------------------
        # BUYING PRICE PANEL
        self.BUYING_PRICE = QTextEdit( self.INIT_VALUE_0, self);
        self.BUYING_PRICE.setGeometry(265, 42, PRICES_SIZE[0], PRICES_SIZE[1]); # OK
        self.BUYING_PRICE.setStyleSheet(STL.PANEL_BUY_SELL);
        self.BUYING_PRICE.setReadOnly(True);

        # BUYING LAST PRICE DIFFERENCE PANEL
        self.BUYING_PRICE_DIFFERENCE = QLabel( self.INIT_VALUE_0, self.FRAME_MAIN);
        self.BUYING_PRICE_DIFFERENCE.setGeometry( 265, 34, 140, 29 );
        self.BUYING_PRICE_DIFFERENCE.setStyleSheet( STL.PRICE_DIFFERENCE_WHITE );

        # BUYING LAST PRICE PANEL
        self.BUYING_LAST_PRICE = QTextEdit( self.INIT_VALUE_0, self.FRAME_MAIN);
        self.BUYING_LAST_PRICE.setGeometry(255, 57, PRICES_SIZE[0], PRICES_SIZE[1]); # OK
        self.BUYING_LAST_PRICE.setStyleSheet( STL.PANEL_BUY_SELL );
        self.BUYING_LAST_PRICE.setReadOnly(True);

        # BUYING ARROW
        self.BUYING_ARROW = QLabel("", self);
        self.BUYING_ARROW.setGeometry(238, 62, 20, 20); # OK
        self.BUYING_ARROW.setStyleSheet(STL.ARROW_BUY_SELL)
        self.BUYING_ARROW.setPixmap(self.ARROW_D);
        self.BUYING_ARROW.setMask(self.ARROW_D.mask());

        # ----------------------------------------------------
        # SELLING PRICE PANEL
        self.SELLING_PRICE = QTextEdit( self.INIT_VALUE_0, self);
        self.SELLING_PRICE.setGeometry(596, 42, PRICES_SIZE[0], PRICES_SIZE[1]); # OK
        self.SELLING_PRICE.setStyleSheet(STL.PANEL_BUY_SELL);
        self.SELLING_PRICE.setReadOnly(True);

        # BUYING LAST PRICE DIFFERENCE PANEL
        self.SELLING_PRICE_DIFFERENCE = QLabel( self.INIT_VALUE_0, self.FRAME_MAIN );
        self.SELLING_PRICE_DIFFERENCE.setGeometry( 595, 34, 140, 29 );
        self.SELLING_PRICE_DIFFERENCE.setStyleSheet( STL.PRICE_DIFFERENCE_WHITE );

        # SELLING LAST PRICE PANEL
        self.SELLING_LAST_PRICE = QTextEdit( self.INIT_VALUE_0, self.FRAME_MAIN);
        self.SELLING_LAST_PRICE.setGeometry(586, 57, PRICES_SIZE[0], PRICES_SIZE[1]); # OK
        self.SELLING_LAST_PRICE.setStyleSheet(STL.PANEL_BUY_SELL);
        self.SELLING_LAST_PRICE.setReadOnly(True);

        # SELLING ARROW
        self.SELLING_ARROW = QLabel("", self);
        self.SELLING_ARROW.setGeometry(570, 62, 20, 20);
        self.SELLING_ARROW.setStyleSheet(STL.ARROW_BUY_SELL);
        self.SELLING_ARROW.setPixmap(self.ARROW_U); # OK
        self.SELLING_ARROW.setMask(self.ARROW_U.mask());


        self.WATCH_DISPLAY = QLCDNumber( self );
        self.WATCH_DISPLAY.setDigitCount(5);
        self.WATCH_DISPLAY.setStyleSheet("QLCDNumber { font: 12px 'monospace';  background-color: #333; color: red;  background-image: url(''); }");
        self.WATCH_DISPLAY.setGeometry(466, 51, 60, 30);
        self.WATCH_DISPLAY.SegmentStyle(QLCDNumber.Filled);
        self.WATCH_DISPLAY.show();

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
        # USER INPUT

        # BUY
        self.USER_BUY_AMOUNT = QLineEdit( self.INIT_VALUE_1, self.FRAME_MAIN); 
        self.USER_BUY_AMOUNT.setGeometry( 345, 93, INPUT_SIZE[0], 19 );
        self.USER_BUY_AMOUNT.setValidator(QDoubleValidator( QDouble[0], QDouble[1], QDouble[2] )) 
        self.USER_BUY_AMOUNT.setStyleSheet(STL.USER_INPUT);
        self.connect( self.USER_BUY_AMOUNT , SIGNAL("textChanged(QString)"), lambda: self.CALCULATE("buy", "1") );

        self.USER_BUY_AMOUNT_PURE = QLineEdit( self.INIT_VALUE_1, self.FRAME_MAIN); 
        self.USER_BUY_AMOUNT_PURE.setGeometry( 345, 110, INPUT_SIZE[0], 15 );
        self.USER_BUY_AMOUNT_PURE.setReadOnly( True );
        self.USER_BUY_AMOUNT_PURE.setStyleSheet(STL.USER_INPUT_NO_EDIT);


        self.USER_BUY_AT_PRICE = QLineEdit(self.INIT_VALUE_0, self.FRAME_MAIN); 
        self.USER_BUY_AT_PRICE.setGeometry( 345, 129, INPUT_SIZE[0], INPUT_SIZE[1] );
        self.USER_BUY_AT_PRICE.setValidator(QDoubleValidator( QDouble[0], QDouble[1], QDouble[2] )) 
        self.USER_BUY_AT_PRICE.setStyleSheet(STL.USER_INPUT);
        self.connect( self.USER_BUY_AT_PRICE , SIGNAL("textChanged(QString)"), lambda: self.CALCULATE("buy", "1") );

        self.USER_BUY_AVAIL = QLineEdit(self.INIT_VALUE_0, self.FRAME_MAIN); 
        self.USER_BUY_AVAIL.setGeometry( 345, 154, INPUT_SIZE[0], INPUT_SIZE[1] );
        self.USER_BUY_AVAIL.setValidator(QDoubleValidator( QDouble[0], QDouble[1], QDouble[2] ));
        self.USER_BUY_AVAIL.setStyleSheet( STL.USER_INPUT_NO_EDIT ); #"QLineEdit{ background-color: transparent; color: #fff; }");
        self.USER_BUY_AVAIL.setReadOnly(True);

        self.USER_BUY_PLUS_FEE_COAST = QLineEdit(self.INIT_VALUE_0, self.FRAME_MAIN); 
        self.USER_BUY_PLUS_FEE_COAST.setGeometry( 345, 180, INPUT_SIZE[0]+24, INPUT_SIZE[1] );
        self.USER_BUY_PLUS_FEE_COAST.setStyleSheet( STL.USER_INPUT_NO_EDIT ); #"QLineEdit{ background-color: transparent; color: #fff; }");
        self.USER_BUY_PLUS_FEE_COAST.setReadOnly(True);

        """
        ---------------------------------------------------------------
        # BUY CALC BUTTON
        """
        self.USER_BUY_CALC_LAYOUT = QVBoxLayout();
        self.USER_BUY_CALC_WIDGET = QWidget(self.FRAME_MAIN);
        self.USER_BUY_CALC_WIDGET.setGeometry(271, 105, 36, 73);
        self.USER_BUY_CALC_WIDGET.setStyleSheet( "QWidget{ font-size: 24px; background-color: transparent; }" );

        self.CALC_BUY_1 = QRadioButton('', self.USER_BUY_CALC_WIDGET);
        self.connect(self.CALC_BUY_1, SIGNAL('clicked()'), lambda: self.CALCULATE("buy", "1") );
        self.USER_BUY_CALC_LAYOUT.addWidget(self.CALC_BUY_1);
        
        self.CALC_BUY_2 = QRadioButton('', self.USER_BUY_CALC_WIDGET);
        self.connect(self.CALC_BUY_2, SIGNAL('clicked()'), lambda: self.CALCULATE("buy", "2") );
        self.USER_BUY_CALC_LAYOUT.addWidget(self.CALC_BUY_2);
        self.CALC_BUY_2.setEnabled(False);

        self.CALC_BUY_3 = QRadioButton('', self.USER_BUY_CALC_WIDGET); 
        self.connect(self.CALC_BUY_3, SIGNAL('clicked()'), lambda: self.CALCULATE("buy", "3") );
        self.USER_BUY_CALC_LAYOUT.addWidget(self.CALC_BUY_3);
        self.USER_BUY_CALC_WIDGET.setLayout(self.USER_BUY_CALC_LAYOUT);
        """
        ---------------------------------------------------------------
        """

        self.BUY_CALC_BTN = QPushButton("&Q", self.FRAME_MAIN);
        self.BUY_CALC_BTN.setGeometry(227, 116, 50, 48);
        self.connect(self.BUY_CALC_BTN, SIGNAL('clicked()'), lambda: self.SET_NEW_TRADE_DATA("buy"));
        self.BUY_CALC_BTN.setStyleSheet(STL.CALC_BTN);
        self.BUY_CALC_BTN.setToolTip( " Init fields with latest MetaData");

        # BUY BUTTON
        self.BUY_BTN = QPushButton("", self.FRAME_MAIN);
        self.BUY_BTN.setShortcut('Ctrl+B');
        self.BUY_BTN.setGeometry(218, 190, BTNS_SIZE[0], BTNS_SIZE[1] );
        self.connect(self.BUY_BTN, SIGNAL('clicked()'), lambda: self.TRADE_ACTION(_action="buy") );
        self.BUY_BTN.setStyleSheet(STL.SELL_BUY_BTNS);
        self.BUY_BTN.setEnabled(True);
        self.BUY_BTN.setToolTip( " Create new BUY Order.");
        #self.BUY_BTN.hide();

        self.BUY_BTN_COVER = QLabel("", self.FRAME_MAIN);
        self.BUY_BTN_COVER.setGeometry(213, 185, BTNS_SIZE[0]+10, BTNS_SIZE[1]+10);
        self.BUY_BTN_COVER.setStyleSheet( "QLabel{ background-color: rbga(51, 51, 51, 150); background-image: url(''); }" );
        self.BUY_BTN_COVER.setToolTip( " Complite Binded ORDER delete BKKPG-UID.");
        self.BUY_BTN_COVER.hide();

        # ------------------ >>>>>>>
        # SELL
        self.USER_SELL_AMOUNT = QLineEdit(str(float(self.INIT_VALUE_0)+1), self.FRAME_MAIN); 
        self.USER_SELL_AMOUNT.setGeometry( 537, 103, INPUT_SIZE[0], INPUT_SIZE[1] ); # OK
        self.USER_SELL_AMOUNT.setValidator(QDoubleValidator( QDouble[0], QDouble[1], QDouble[2] )) 
        self.USER_SELL_AMOUNT.setStyleSheet(STL.USER_INPUT);
        self.connect( self.USER_SELL_AMOUNT , SIGNAL("textChanged(QString)"), lambda: self.CALCULATE("sell", "1") );

        self.USER_SELL_AT_PRICE = QLineEdit(self.INIT_VALUE_0, self.FRAME_MAIN); 
        self.USER_SELL_AT_PRICE.setGeometry( 537, 129, INPUT_SIZE[0], INPUT_SIZE[1] );
        self.USER_SELL_AT_PRICE.setValidator(QDoubleValidator( QDouble[0], QDouble[1], QDouble[2] )) 
        self.USER_SELL_AT_PRICE.setStyleSheet(STL.USER_INPUT);
        self.connect( self.USER_SELL_AT_PRICE , SIGNAL("textChanged(QString)"), lambda: self.CALCULATE("sell", "1") );

        self.USER_SELL_AVAIL = QLineEdit(self.INIT_VALUE_0, self.FRAME_MAIN); 
        self.USER_SELL_AVAIL.setGeometry( 537, 154, INPUT_SIZE[0], INPUT_SIZE[1] );
        self.USER_SELL_AVAIL.setValidator(QDoubleValidator( QDouble[0], QDouble[1], QDouble[2] )) 
        self.USER_SELL_AVAIL.setStyleSheet( STL.USER_INPUT_NO_EDIT ); #"QLineEdit{ background-color: transparent; color: #fff; }");
        self.USER_SELL_AVAIL.setReadOnly(True);

        self.USER_SELL_PLUS_FEE_COAST = QLineEdit(self.INIT_VALUE_0, self.FRAME_MAIN); 
        self.USER_SELL_PLUS_FEE_COAST.setGeometry( 537, 180, INPUT_SIZE[0]+24, INPUT_SIZE[1] );
        self.USER_SELL_PLUS_FEE_COAST.setStyleSheet( STL.USER_INPUT_NO_EDIT ); #"QLineEdit{ background-color: transparent; color: #fff; }");
        self.USER_SELL_PLUS_FEE_COAST.setReadOnly(True);

        """
        ---------------------------------------------------------------
        # SELL CALC BUTTON
        """
        self.USER_SELL_CALC_LAYOUT = QVBoxLayout();
        self.USER_SELL_CALC_WIDGET = QWidget(self.FRAME_MAIN);
        self.USER_SELL_CALC_WIDGET.setGeometry(664, 105, 36, 73);
        self.USER_SELL_CALC_WIDGET.setStyleSheet( "QWidget{ font-size: 24px; background-color: transparent; }" );

        self.CALC_SELL_1 = QRadioButton('', self.USER_SELL_CALC_WIDGET);
        self.connect(self.CALC_SELL_1, SIGNAL('clicked()'), lambda: self.CALCULATE("sell", "1") );
        self.USER_SELL_CALC_LAYOUT.addWidget(self.CALC_SELL_1);
        
        self.CALC_SELL_2 = QRadioButton('', self.USER_SELL_CALC_WIDGET);
        self.connect(self.CALC_SELL_2, SIGNAL('clicked()'), lambda: self.CALCULATE("sell", "2") );
        self.USER_SELL_CALC_LAYOUT.addWidget(self.CALC_SELL_2);
        self.CALC_SELL_2.setEnabled(False);

        self.CALC_SELL_3 = QRadioButton('', self.USER_SELL_CALC_WIDGET); 
        self.connect(self.CALC_SELL_3, SIGNAL('clicked()'), lambda: self.CALCULATE("sell", "3") );
        self.USER_SELL_CALC_LAYOUT.addWidget(self.CALC_SELL_3);
        self.USER_SELL_CALC_WIDGET.setLayout(self.USER_SELL_CALC_LAYOUT);
        """
        ---------------------------------------------------------------
        """

        self.SELL_CALC_BTN = QPushButton("&N", self.FRAME_MAIN);
        self.SELL_CALC_BTN.setGeometry(695, 116, 50, 48); # OK
        self.connect(self.SELL_CALC_BTN, SIGNAL('clicked()'), lambda: self.SET_NEW_TRADE_DATA("sell"));
        self.SELL_CALC_BTN.setStyleSheet(STL.CALC_BTN);
        self.SELL_CALC_BTN.setToolTip( " Init fields with latest MetaData");


        # SELL BUTTON
        self.SELL_BTN = QPushButton("", self.FRAME_MAIN);
        self.SELL_BTN.setShortcut('Ctrl+S');
        self.SELL_BTN.setGeometry(675, 190, BTNS_SIZE[0], BTNS_SIZE[1]);  # OK
        self.connect(self.SELL_BTN, SIGNAL('clicked()'), lambda: self.TRADE_ACTION(_action="sell"));
        self.SELL_BTN.setStyleSheet(STL.SELL_BUY_BTNS);
        self.SELL_BTN.setEnabled(True);
        self.SELL_BTN.setToolTip( " Create new SELL Ordeder.");

        self.SELL_BTN_COVER = QLabel("", self.FRAME_MAIN);
        self.SELL_BTN_COVER.setGeometry(670, 185, BTNS_SIZE[0]+10, BTNS_SIZE[1]+10);
        self.SELL_BTN_COVER.setStyleSheet( "QLabel{ background-color: rbga(51, 51, 51, 150); background-image: url(''); }" );
        self.SELL_BTN_COVER.setToolTip( " Complite Binded ORDER delete BKKPG-UID.");
        self.SELL_BTN_COVER.hide();


        self.USER_SELL_BUY_DIFFERENCE = QLineEdit(self.INIT_VALUE_0, self.FRAME_MAIN); 
        self.USER_SELL_BUY_DIFFERENCE.setGeometry( 431, 211, 125, 20 );
        self.USER_SELL_BUY_DIFFERENCE.setStyleSheet( STL.USER_INPUT_NO_EDIT );
        self.USER_SELL_BUY_DIFFERENCE.setReadOnly(True);

        self.BKKPG_UID_VALUE = QLineEdit( "", self.FRAME_MAIN); 
        self.BKKPG_UID_VALUE.setGeometry( 431, 246, 125, 20 );
        self.BKKPG_UID_VALUE.setStyleSheet( STL.BKKPG_UID_DISPLAY_WHITE ); 
        self.BKKPG_UID_VALUE.setPlaceholderText("BKKPG-UID:");
        self.BKKPG_UID_VALUE.setReadOnly(True);

        self.BKKPG_UID_DEL_BTN = QPushButton("", self.FRAME_MAIN);
        self.BKKPG_UID_DEL_BTN.setGeometry(560, 245, 24, 24);
        self.BKKPG_UID_DEL_BTN.setStyleSheet(STL.SELL_BUY_BTNS);
        self.BKKPG_UID_DEL_BTN.setToolTip( " Delete this BKKPG-UID: To create new stand allown BKKPG-UID. ");
        self.connect(self.BKKPG_UID_DEL_BTN, SIGNAL('clicked()'), lambda: self.FRAME_BOOKKEEPING.RESET_BKKPG_UID( ) );

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
        # PAIR SELECTOR ( QComboBox)

        self.FRAME_MAIN.PAIR_COMBO = QComboBox( self.FRAME_MAIN);
        self.FRAME_MAIN.PAIR_COMBO.setGeometry(440, 55, 98, 30); 
        self.FRAME_MAIN.PAIR_COMBO.currentIndexChanged.connect(self.SELECT_PAIR);
        self.FRAME_MAIN.PAIR_COMBO.setStyleSheet(STL.PAIR_COMBO);
        self.FRAME_MAIN.PAIR_COMBO.setEditable(False);
        self.FRAME_MAIN.PAIR_COMBO.clear()

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
        # GRAPH

        self.FRAME_GRAPH = PlotterQFrame( parent=self.FRAME_MAIN, _PARENT=self.PARENT );
        self.FRAME_GRAPH.setStyleSheet( STL.FRAME_GRAPH );

        self.connect(self.FRAME_GRAPH.QCHECK_BOX_DRAW_CANDLES, SIGNAL('clicked()'), lambda: self.CHANGE_GRAPH_PLOT_STYLE_OPTIONS("CANDLES"));
        self.connect(self.FRAME_GRAPH.QCHECK_BOX_DRAW_CANDLES_POINTS, SIGNAL('clicked()'), lambda: self.CHANGE_GRAPH_PLOT_STYLE_OPTIONS("CANDLES_POINTS"));
        self.connect(self.FRAME_GRAPH.QCHECK_BOX_BUY_CANDLES, SIGNAL('clicked()'), lambda: self.CHANGE_GRAPH_PLOT_VALUE_OPTIONS("buy"));
        self.connect(self.FRAME_GRAPH.QCHECK_BOX_SELL_CANDLES, SIGNAL('clicked()'), lambda: self.CHANGE_GRAPH_PLOT_VALUE_OPTIONS("sell"));
        self.connect(self.FRAME_GRAPH.GRAPH_OPTIONS_DRAW_CROSS_CHECKBOX, SIGNAL('stateChanged(int)'), lambda: self.CHANGE_GRAPH_PLOT_VALUE_OPTIONS("cross"));
        self.connect(self.FRAME_GRAPH.GRAPH_ZOOM_IN_BTN, SIGNAL('clicked()'), lambda: self.GRAPH_Y_ZOOMER('+') );
        self.connect(self.FRAME_GRAPH.GRAPH_ZOOM_OUT_BTN, SIGNAL('clicked()'), lambda: self.GRAPH_Y_ZOOMER('-') );
        self.connect(self.FRAME_GRAPH.GRAPH_UP_SHIFTER_BTN, SIGNAL('clicked()'), lambda: self.GRAPH_Y_SHIFTER("+"));
        self.connect(self.FRAME_GRAPH.GRAPH_DOWN_SHIFTER_BTN, SIGNAL('clicked()'), lambda: self.GRAPH_Y_SHIFTER("-"));


        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
        # INFO_PANEL

        self.INFO_PANEL = QWidget(self.FRAME_MAIN);
        self.INFO_PANEL.setGeometry(634, 275, 334, 303);
        self.INFO_PANEL.setStyleSheet(STL.INFO_PANEL);
        #self.INFO_PANEL.hide();

        self.INFO_PANEL_LOG = QTextEdit("", self.INFO_PANEL);
        self.INFO_PANEL_LOG.setGeometry(7, 7, 320, 265);
        self.INFO_PANEL_LOG.setAlignment( Qt.AlignTop | Qt.AlignLeft );
        self.INFO_PANEL_LOG.setStyleSheet(STL.INFO_PANEL_LOG)
        self.INFO_PANEL_LOG.setEnabled(True);
        self.INFO_PANEL_LOG.setReadOnly(True);

        self.INFO_PANEL_LOG_CLEAR_BTN = QPushButton( "&Cl.", self.INFO_PANEL );
        self.INFO_PANEL_LOG_CLEAR_BTN.setGeometry( 2, 275, 53, 23 );
        self.INFO_PANEL_LOG_CLEAR_BTN.setStyleSheet( STL.INFO_PANEL_LOG_CLEAR_BTN );
        self.connect(self.INFO_PANEL_LOG_CLEAR_BTN, SIGNAL('clicked()'), lambda: self.INFO_PANEL_LOG.setText("") );
        self.INFO_PANEL_LOG_CLEAR_BTN.setToolTip( " Clear Console.");

        self.INFO_PANEL_CONSOLE = QLineEdit("", self.INFO_PANEL);
        self.INFO_PANEL_CONSOLE.setPlaceholderText(" Console: ");
        self.INFO_PANEL_CONSOLE.setGeometry(90, 275, 237, 23);
        self.INFO_PANEL_CONSOLE.setStyleSheet( "QLineEdit{ background-image: url(); background-color: #333; color: #fff; border-style: none; border-radius: 2px; }" );
        self.connect(self.INFO_PANEL_CONSOLE, SIGNAL('returnPressed()'), self.CONSOLE_ACTION );

        self.MAIN_TABS.addTab(self.TAB_Trader, "Trader");
        self.MAIN_TABS.setTabIcon(0, QIcon("./data/imgs/TAB_Trader_icon.png"));
        self.MAIN_TABS.setTabToolTip(0, "Trade Terminal.");

        ####################################################################
        # TABS-TAB Orders

        self.TAB_Orders = QWidget();

        self.FRAME_ORDERS = OrdersWidget( parent=self.TAB_Orders, _PARENT=self.PARENT );
        self.connect( self.FRAME_ORDERS.CANCEL_ORDER_BTN, SIGNAL('clicked()'), lambda: self.API_CANCEL_ORDERS( self.FRAME_ORDERS.ORDER_ID_TO_CANCEL, self.FRAME_ORDERS.ORDER_TYPE_TO_CANCEL ) );

        self.MAIN_TABS.addTab(self.TAB_Orders, "Orders");
        self.MAIN_TABS.setTabIcon(1, QIcon("./data/imgs/TAB_Orders_icon.png"));
        self.MAIN_TABS.setTabToolTip(1, "Orders state/settins.");
        ####################################################################
        # TABS-TAB BookKeeping

        self.TAB_BookKeeping = QWidget();
        self.FRAME_BOOKKEEPING = BookKeeping( parent=self.TAB_BookKeeping, _PARENT=self.PARENT );


        self.MAIN_TABS.addTab(self.TAB_BookKeeping, "BookKeeping");
        self.MAIN_TABS.setTabIcon(2, QIcon("./data/imgs/TAB_BookKeeping_icon.png"));
        self.MAIN_TABS.setTabToolTip(2, "Account BookKeeping.");
        ####################################################################
        # TABS-TAB History

        self.TAB_History = QWidget();
        self.FRAME_HISTORY = History( parent=self.TAB_History, _PARENT=self.PARENT );


        self.MAIN_TABS.addTab(self.TAB_History, "History");
        self.MAIN_TABS.setTabIcon(3, QIcon("./data/imgs/TAB_History_icon.png"));
        self.MAIN_TABS.setTabToolTip(3, "Account History.");
        ####################################################################
        # TABS-TAB OFFICE

        self.TAB_Office = QWidget();
        self.FRAME_OFFICE = QFrame( self.TAB_Office );
        self.FRAME_OFFICE.setGeometry( 3, 5, 975, 555 );
        self.FRAME_OFFICE.setStyleSheet( STL.FRAME_OFFICE );

        # ALARMS

        self.ALARMS_DATA = { 
            "buy": {
                "lower": [], "higher" : []
            },
            "sell": {
                "lower": [], "higher" : []
            }
        };

        self.ALARMS_WIDGET = QWidget( self.FRAME_OFFICE );
        self.ALARMS_WIDGET.setGeometry( 10, 98, 665, 447 );
        self.ALARMS_WIDGET.setStyleSheet( STL.ALARMS_WIDGET );

        self.CURRENCY_ACTION_COMBO = QComboBox( self.FRAME_OFFICE );
        self.CURRENCY_ACTION_COMBO.setGeometry( 24, 107, 76, 29 ); 
        self.CURRENCY_ACTION_COMBO.setStyleSheet( STL.ALARMS_COMBO );
        self.CURRENCY_ACTION_COMBO.setEditable( False );
        self.CURRENCY_ACTION_COMBO.addItem("BUY");
        self.CURRENCY_ACTION_COMBO.addItem("SELL");

        self.CURRENCY_COMBO = QComboBox( self.FRAME_OFFICE );
        self.CURRENCY_COMBO.setGeometry( 174, 107, 112, 29 ); 
        self.CURRENCY_COMBO.setStyleSheet( STL.ALARMS_COMBO );
        self.CURRENCY_COMBO.setEditable( False );

        for PAIR in self.CONF["API"]["PAIRS"]:
            self.CURRENCY_COMBO.addItem(PAIR.upper());

        self.IF_CURRENCY_COMBO = QComboBox( self.FRAME_OFFICE );
        self.IF_CURRENCY_COMBO.setGeometry( 324, 107, 103, 29 ); 
        self.IF_CURRENCY_COMBO.setStyleSheet( STL.ALARMS_COMBO );
        self.IF_CURRENCY_COMBO.setEditable( False );

        self.IF_CURRENCY_COMBO.addItem("LOWER");
        self.IF_CURRENCY_COMBO.addItem("HIGHER");

        self.ALARM_VALUE_INPUT = QLineEdit(self.FRAME_OFFICE);
        self.ALARM_VALUE_INPUT.setStyleSheet( STL.ALARM_VALUE_INPUT );
        self.ALARM_VALUE_INPUT.setGeometry( 451, 107, 165, 29 ); 

        self.ALARM_VALUE_INPUT.setValidator( QDoubleValidator(0, 1, 7) ) 
        self.ALARM_VALUE_INPUT.setText("0.0"); 

        self.ALARMS_WIDGET_ADD_BTN = QPushButton( "", self.FRAME_OFFICE );
        self.ALARMS_WIDGET_ADD_BTN.setGeometry( 626, 104, 36, 36 ); 
        self.ALARMS_WIDGET_ADD_BTN.setStyleSheet( "QPushButton{ background-color: transparent; border-style: none; }" ); 
        self.connect( self.ALARMS_WIDGET_ADD_BTN, SIGNAL("clicked()"), lambda: self.ALARMS_ACTION("add") );

        # ALARMS_LIST
        self.ALARMS_LIST_TO_BUY = QListWidget(self.FRAME_OFFICE);
        self.ALARMS_LIST_TO_BUY.setGeometry( 24, 174, 308, 305 );
        self.ALARMS_LIST_TO_BUY.setStyleSheet( STL.ALARMS_LIST  );
        self.connect( self.ALARMS_LIST_TO_BUY, SIGNAL('itemSelectionChanged()'), lambda: self.ALARMS_ACTION("item_changed", "buy") );

        self.ALARMS_LIST_TO_SELL = QListWidget(self.FRAME_OFFICE);
        self.ALARMS_LIST_TO_SELL.setGeometry( 348, 174, 308, 305 );
        self.ALARMS_LIST_TO_SELL.setStyleSheet( STL.ALARMS_LIST  );
        self.connect( self.ALARMS_LIST_TO_SELL, SIGNAL('itemSelectionChanged()'), lambda: self.ALARMS_ACTION("item_changed", "sell") );

        self.ALARMS_WIDGET_DELETE_BTN = QPushButton( "", self.FRAME_OFFICE );
        self.ALARMS_WIDGET_DELETE_BTN.setGeometry( 242, 499, 194, 43 ); 
        self.ALARMS_WIDGET_DELETE_BTN.setStyleSheet( "QPushButton{ border-style: none; background-color: none;}"  );
        self.connect( self.ALARMS_WIDGET_DELETE_BTN, SIGNAL("clicked()"), lambda: self.ALARMS_ACTION("delete") );

        self.ALARMS_CURRENT_LIST_SELECTOR = None;
        # ------------------------

        # BALANCE
        """
        self.BALANCE_WIDGET_LABLE = QLabel("Account balance:", self.FRAME_OFFICE);
        self.BALANCE_WIDGET_LABLE.setGeometry(730, 62, 300, 30);
        self.BALANCE_WIDGET_LABLE.setStyleSheet(STL.BALANCE_WIDGET_LABLE);
        """

        self.BALANCE_WIDGET = QTextEdit("", self.FRAME_OFFICE);
        self.BALANCE_WIDGET.setGeometry(721, 98, 240, 290);
        self.BALANCE_WIDGET.setStyleSheet(STL.BALANCE_WIDGET);
        self.BALANCE_WIDGET.setEnabled(True);
        self.BALANCE_WIDGET.setReadOnly(True);

        self.BALANCE_WIDGET_UPDATE_BTN = QPushButton(" Update", self.FRAME_OFFICE);
        self.BALANCE_WIDGET_UPDATE_BTN.setGeometry(730, 401, 223, 28);
        self.connect(self.BALANCE_WIDGET_UPDATE_BTN, SIGNAL("clicked()"), self.SET_NEW_TRADE_DATA);


        self.MAIN_TABS.addTab(self.TAB_Office, "Office");
        self.MAIN_TABS.setTabIcon(4, QIcon("./data/imgs/TAB_Office_icon.png"));
        self.MAIN_TABS.setTabToolTip(4, "Account Asisstance.");
        ####################################################################
        # TABS-TAB NoteBook

        self.TAB_NoteBook = QWidget();
        
        self.FRAME_NOTEBOOK = NoteBook( parent=self.TAB_NoteBook, _PARENT=self.PARENT );
        self.FRAME_NOTEBOOK.setStyleSheet( STL.FRAME_NOTEBOOK );



        self.MAIN_TABS.addTab(self.TAB_NoteBook, "NoteBook");
        self.MAIN_TABS.setTabIcon(5, QIcon("./data/imgs/TAB_NoteBook_icon.png"));
        self.MAIN_TABS.setTabToolTip(5, "User notes.");
        ####################################################################
        # TABS-TAB Settings
        
        self.TAB_Settings = QWidget();
        self.FRAME_SETTINGS = QFrame(self.TAB_Settings);
        self.FRAME_SETTINGS.setGeometry(3, 5, 975, 548);
        self.FRAME_SETTINGS.setStyleSheet(STL.FRAME_SETTINGS);



        self.MAIN_TABS.addTab(self.TAB_Settings, "Settings");
        self.MAIN_TABS.setTabIcon(6, QIcon("./data/imgs/TAB_Settings_icon.png"));
        self.MAIN_TABS.setTabToolTip(6, "Account settings.");
        ####################################################################
        # TABS-TAB Chat
        
        self.TAB_Chat = QWidget();
        self.FRAME_CHAT = Chat(parent=self.TAB_Chat, _PARENT=self.PARENT );


        self.MAIN_TABS.addTab(self.TAB_Chat, "Chat");
        self.MAIN_TABS.setTabIcon(7, QIcon("./data/imgs/TAB_Chat_icon.png"));
        self.MAIN_TABS.setTabToolTip(7, "BTC-e Chat.");
        ####################################################################
        # TABS-TAB Browser
        
        self.TAB_Browser = QWidget();
        self.FRAME_BROWSER = Browser(parent=self.TAB_Browser, _PARENT=self.PARENT  );
        #self.FRAME_BROWSER.show();


        self.MAIN_TABS.addTab(self.TAB_Browser, "B");
        self.MAIN_TABS.setTabIcon(8, QIcon("./data/imgs/TAB_Browser_icon.png"));
        self.MAIN_TABS.setTabToolTip(8, "Browser");
        ####################################################################
        # TABS-TAB-END / END
        ####################################################################
        # >>>>>>>>>>>>>> TRANSPARENT (WAIT-LOADING) OVERLAY <<<<<<<<<<<<<<<< 
        # INFO_PANEL

        self.TRANS_MESSAGE_WIDGET_ALPHA = QWidget(self);
        self.TRANS_MESSAGE_WIDGET_ALPHA.setGeometry(5, 35, 990, 620);
        self.TRANS_MESSAGE_WIDGET_ALPHA.setStyleSheet(STL.TRANS_MESSAGE_WIDGET);
        self.TRANS_MESSAGE_WIDGET_ALPHA.LOCKED = False;

        self.TRANS_MESSAGE_TIMER = QTimer();
        self.TRANS_MESSAGE_TIMER.setSingleShot(True);

        self.TRANS_MESSAGE_BOX = QLabel(self.TRANS_MESSAGE_WIDGET_ALPHA);
        self.TRANS_MESSAGE_BOX.setGeometry(300, 100, 400, 300);
        self.TRANS_MESSAGE_BOX.setStyleSheet(STL.TRANS_MESSAGE_LABEL); #  STL.TRANSPARENT=rbga(0, 0, 0, 255);;
        self.TRANS_MESSAGE_BOX.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding);
        self.TRANS_MESSAGE_BOX.setAlignment(Qt.AlignCenter);

        self.TRANS_MESSAGE_WIDGET_CLOSE_BTN = QPushButton('', self.TRANS_MESSAGE_BOX);
        self.TRANS_MESSAGE_WIDGET_CLOSE_BTN.setGeometry(350, 20, 30, 30);
        self.connect(self.TRANS_MESSAGE_WIDGET_CLOSE_BTN, SIGNAL('clicked()'), self.TRANS_MESSAGE_WIDGET_RELEAS_LOCK);
        self.TRANS_MESSAGE_WIDGET_CLOSE_BTN.setStyleSheet(STL.TRANS_MESSAGE_WIDGET_CLOSE_BTN);
        self.TRANS_MESSAGE_WIDGET_CLOSE_BTN.hide();

        self.TRANS_MESSAGE_TEXT_AREA = QTextEdit("", self.TRANS_MESSAGE_BOX);
        self.TRANS_MESSAGE_TEXT_AREA.setGeometry(60, 70, 300, 100);
        #self.TRANS_MESSAGE_TEXT_AREA.setAlignment(Qt.AlignCenter );
        self.TRANS_MESSAGE_TEXT_AREA.setStyleSheet(STL.TRANS_MESSAGE_TEXT)
        self.TRANS_MESSAGE_TEXT_AREA.setReadOnly(True);

        self.TRANS_MESSAGE_LOADING_ANIM = QMovie("./data/imgs/progress_bar.gif", QByteArray(), self);
        self.TRANS_MESSAGE_LOADING_ANIM.setCacheMode(QMovie.CacheAll);
        self.TRANS_MESSAGE_LOADING_ANIM.setSpeed(250);
        self.TRANS_MESSAGE_BOX.setMovie(self.TRANS_MESSAGE_LOADING_ANIM);

        ####################################################################
        #                            STATUS_BAR  
        ####################################################################
        self.TRANS_MESSAGE(_action="show", _loading=True, _msg=" Initializing ... ");
        #self.TRANS_MESSAGE(_action="hide");
        
        self.TO_STATUSBAR(" BTCeTrader Loaded. Status: Ready!");
        self.PARENT.LOG["success"].append(" BTCeTrader Loaded. Status: Ready!");

        ####################################################################
        #                        __init__ / END  
        ####################################################################

        if self.CONF["SYS"]["GUI"]["SPLASH"]["SHOW"]: _Splash.Screen.hide();

        self.AVAILABLE = True;
        self.ALLOW_DISPLAY_LOG = True;
        self.setEnabled(True);

        for PAIR in self.CONF["API"]["PAIRS"]:
            self.FRAME_MAIN.PAIR_COMBO.addItem(PAIR.upper());


        self.connect(self.LOG_MANAGER_TIMER, SIGNAL("timeout()"), self.LOG_MANAGER);
        self.LOG_MANAGER_TIMER.start(self.LOG_MANAGER_UPD_DELAY);

        # ------------------------------------------------------------------
        self.TRADE_TERMINAL_HAS_ACTION = False; # Maybe beeter place for this variable ???
        # ------------------------------------------------------------------
        self.UPD_WATCH_COUNTER = self.CONF["SYS"]["UPD_DELAY"];
        # ------------------------------------------------------------------

        self.UPD_WATCH_TIMER = QTimer();
        self.connect(self.UPD_WATCH_TIMER, SIGNAL("timeout()"), self.UPDATE_WATCH_DISPLAY);
        self.UPD_WATCH_TIMER.start(1000);

        #self.UPDATE_WATCH_DISPLAY();
        
        # ------------------------------------------------------------------
        self.TRANS_MESSAGE(_action="show", _loading=True, _msg="Loading ...", _close=False, _lock=True);
        # ------------------------------------------------------------------
        # FOR TEST ONLY
        self.API_GET_ORDERS_LIST();
        # ------------------------------------------------------------------
        self.NEWS_LINE_TIMER = QTimer();
        self.NEWS_LINE_TIMER.singleShot(3000, self.NEWS_LINE_UPDATER);

        self.NEWS_LINE_DATA = "";
        self.NEWS_LINE_DATA_L = 0;
        self.NEWS_LINE_DATA_C = 0;

        # ------------------------------------------------------------------
        self.ONCE_T = QTimer();
        self.ONCE_T.singleShot(3000, self.SET_NEW_TRADE_DATA);

        self.ALARMS_ACTION("update");
        # ------------------------------------------------------------------

    # =======================================================================
    def CONTROL_TRADINGS_BTNS(self, _btn, _action):

        # ------------------------------------------------------------------
        if _btn == "sell":
            if _action == "show":
                self.SELL_BTN_COVER.hide();
                self.SELL_BTN.show();
            else:
                self.SELL_BTN_COVER.show();
                self.SELL_BTN.hide();
        
        else: 
            if _action == "show":
                self.BUY_BTN_COVER.hide();
                self.BUY_BTN.show();
            else:
                self.BUY_BTN_COVER.show();
                self.BUY_BTN.hide();

        # ------------------------------------------------------------------

    # =======================================================================
    def CONSOLE_ACTION(self):

        # ------------------------------------------------------------------
        try:
            # --------------------------------------------
            HELP = [
                ["screenshot: " , "Take screenshot of Graph-Plotter"],
                ["_c: " , "To clean up consol"],
                ["1+1 or 2*2 or" , "Perform arithmetic operations"],
            ]
            # --------------------------------------------
            expression = str(self.INFO_PANEL_CONSOLE.text()).strip();
            
            if expression == "help":
                self.INFO_PANEL_LOG.clear();

                for _h in HELP:
                    self.INFO_PANEL_LOG.append(_h[0]+" : "+_h[1]+"<br/>");

            elif expression == "screenshot":
                self.FRAME_GRAPH.TAKE_SCREENSHOT();

            elif expression == "_c":
                self.INFO_PANEL_LOG.clear();

            else:

                expression_1 = "self.INFO_PANEL_LOG.append('CMD: '+str( "+expression+" ));"

                try:
                    exec(expression_1);

                except Exception as _exception:
                    exec(expression);


                #self.INFO_PANEL_LOG.append(str(  ));

            #self.INFO_PANEL_CONSOLE.setText("");
            #self.PARENT.LOG["notif"].append("CMD - OK");
            # --------------------------------------------

        except Exception as _exception:
            self.PARENT.LOG["error"].append(" CONSOLE: <br/>"+str(_exception));

        # ------------------------------------------------------------------

    # =======================================================================
    def CHANGE_GRAPH_PLOT_STYLE_OPTIONS(self, _action):
        
        # ------------------------------------------------------------------
        if _action == "CANDLES":
            self.FRAME_GRAPH.CANDLES_CLASSIC_DRAW = True;
            self.FRAME_GRAPH.CANDLES_POINTS_DRAW = False;

        elif _action == "CANDLES_POINTS":
            self.FRAME_GRAPH.CANDLES_CLASSIC_DRAW = False;
            self.FRAME_GRAPH.CANDLES_POINTS_DRAW = True;

        # ------------------------------------------------------------------
        self.FRAME_GRAPH.update();
        # ------------------------------------------------------------------
 
    # =======================================================================
    def CHANGE_GRAPH_PLOT_VALUE_OPTIONS(self, _value):
        
        # ------------------------------------------------------------------
        if _value == "cross":
            self.FRAME_GRAPH.DRAW_CROSS = not self.FRAME_GRAPH.DRAW_CROSS;

        else:
            self.FRAME_GRAPH.BY_THIS_VALUE = _value;

        # ------------------------------------------------------------------
        self.FRAME_GRAPH.update();
        # ------------------------------------------------------------------
 
    # =======================================================================
    def ORDERS_PANEL_ACTION(self, _type):

        if _type == "sell":
            

            # TODO: Wrong calculations !!!!!!

            res = str( self.PANEL_SELL_ORDERS.currentItem().text() ).split("|")[0].strip();
            self.USER_BUY_AT_PRICE.setText(res);
            
        elif _type == "buy":

            res = str(self.PANEL_BUY_ORDERS.currentItem().text() ).split("|")[0].strip();
            self.USER_SELL_AT_PRICE.setText(res);

        # ------------------------------------------------------------------

    # =======================================================================
    def CALCULATE(self, _type, _option):

        # ------------------------------------------------------------------
        # 1: AMOUNT
        # 2: PRICE
        # 3: AVAIL
        # ------------------------------------------------------------------
        # https://btc-e.com/api/2/ltc_usd/fee 
        # > {"trade":0.2}
        # self.PARENT.FEE = 
        # ------------------------------------------------------------------
        if _type == "buy":

            # --------------------------------------------------------------
            try:
                if _option == "1":
                    

                    """
                    price = float(self.USER_BUY_AMOUNT.text()) * float(self.USER_BUY_AT_PRICE.text());
                    OLD CALCULATIONS FOR USD PRICE + FEE

                    _COAST_PLUS_FEE_ = price + (price/100*self.PARENT.FEE);

                    if _COAST_PLUS_FEE_ > float(self.USER_BUY_AVAIL.text()):
                        self.USER_BUY_PLUS_FEE_COAST.setStyleSheet(STL.USER_INPUT_NO_EDIT_RED);
                    else:
                        self.USER_BUY_PLUS_FEE_COAST.setStyleSheet(STL.USER_INPUT_NO_EDIT_GREEN);

                    self.USER_BUY_PLUS_FEE_COAST.setText( "{0:,.7f}".format(_COAST_PLUS_FEE_) ); 
                    """

                    amount = float(self.USER_BUY_AMOUNT.text());
                    at_price = float(self.USER_BUY_AT_PRICE.text());

                    price = amount * at_price;
                    fee = (amount/100*self.PARENT.FEE);

                    if price > float(self.USER_BUY_AVAIL.text()):
                        self.USER_BUY_PLUS_FEE_COAST.setStyleSheet(STL.USER_INPUT_NO_EDIT_RED);
                    else:
                        self.USER_BUY_PLUS_FEE_COAST.setStyleSheet(STL.USER_INPUT_NO_EDIT_GREEN);

                    self.USER_BUY_PLUS_FEE_COAST.setText( "{0:,.7f}".format( price ) ); 
                    self.USER_BUY_AMOUNT_PURE.setText( "{0:,.7f}".format( amount-fee ) );


                elif _option == "2":
                    pass;

                elif _option == "3":

                    avail_no_fee = float(self.USER_BUY_AVAIL.text());
                    avail_plus_fee = avail_no_fee - (avail_no_fee/100*self.PARENT.FEE);

                    ttl_coins = avail_plus_fee / float(self.USER_BUY_AT_PRICE.text());
                    price = ttl_coins * float(self.USER_BUY_AT_PRICE.text());

                    self.USER_BUY_PLUS_FEE_COAST.setText( "{0:,.7f}".format( price ) ); 
                    self.USER_BUY_AMOUNT.setText( "{0:,.7f}".format( ttl_coins ) );

            except Exception as _exception:
                print(_exception)

            # --------------------------------------------------------------

        # ------------------------------------------------------------------
        elif _type == "sell":

            try:

                if _option == "1":
                    
                    sell_amount = float( self.USER_SELL_AMOUNT.text() );
                    
                    price = sell_amount * float(self.USER_SELL_AT_PRICE.text());

                    if sell_amount > float(self.USER_SELL_AVAIL.text()):
                        self.USER_SELL_AVAIL.setStyleSheet( STL.USER_INPUT_NO_EDIT_RED );
                        self.USER_SELL_PLUS_FEE_COAST.setStyleSheet( STL.USER_INPUT_NO_EDIT_RED );
                    else:
                        self.USER_SELL_AVAIL.setStyleSheet( STL.USER_INPUT_NO_EDIT_GREEN );
                        self.USER_SELL_PLUS_FEE_COAST.setStyleSheet( STL.USER_INPUT_NO_EDIT_GREEN );

                    _COAST_PLUS_FEE_ = price - (price/100*self.PARENT.FEE);
                    self.USER_SELL_PLUS_FEE_COAST.setText( "{0:,.7f}".format(_COAST_PLUS_FEE_) ); 


                elif _option == "2":
                    pass;

                elif _option == "3":

                    ttl_coins = float(self.USER_SELL_AVAIL.text());
                    self.USER_SELL_AMOUNT.setText( "{0:,.7f}".format(ttl_coins) );

                    price = ttl_coins * float(self.USER_SELL_AT_PRICE.text());
                    
                    _COAST_PLUS_FEE_ = price - (price/100*self.PARENT.FEE);
                    self.USER_SELL_PLUS_FEE_COAST.setText( "{0:,.7f}".format(_COAST_PLUS_FEE_) ); 


            except Exception as _exception:
                print(_exception)

        # ------------------------------------------------------------------
        try:

            # TODO

            sell_plus_fee = str(self.USER_SELL_PLUS_FEE_COAST.text()).replace(",", "");
            buy_plus_fee = str(self.USER_BUY_PLUS_FEE_COAST.text()).replace(",", "");

            diff = float( sell_plus_fee ) - float( buy_plus_fee );

            if diff > 0:
                self.USER_SELL_BUY_DIFFERENCE.setStyleSheet( STL.USER_INPUT_NO_EDIT_GREEN );
                self.USER_SELL_BUY_DIFFERENCE.setText(" +{0:,.7f}".format( diff ));

            else:
                self.USER_SELL_BUY_DIFFERENCE.setStyleSheet( STL.USER_INPUT_NO_EDIT_RED );
                self.USER_SELL_BUY_DIFFERENCE.setText(" {0:,.7f}".format( diff ));

        except Exception as _exception:
            self.PARENT.LOG["error"].append(" CLC_ERR[0:0]: <br/>"+str(_exception));

        # ------------------------------------------------------------------

    # =======================================================================
    def G_SC_SELECT(self, _value):
        
        # ------------------------------------------------------------------
        # if 1 candle is 01:00:00h -> 3600 sec / UPDATE_DELAY(15sec) == 240 ticks / 1 candle  
        # if 1 candle is 00:30:00h -> 1800 sec / UPDATE_DELAY(15sec) == 120 ticks / 1 candle  
        # if 1 candle is 00:15:00h ->  900 sec / UPDATE_DELAY(15sec) == 60  ticks / 1 candle  
        # if 1 candle is 00:10:00h ->  600 sec / UPDATE_DELAY(15sec) == 40  ticks / 1 candle  
        # if 1 candle is 00:05:00h ->  300 sec / UPDATE_DELAY(15sec) == 20  ticks / 1 candle  
        # ------------------------------------------------------------------
        """
        self.FRAME_GRAPH.TICKS_FOR_ONE_CANDLE = _value;
        self.PARENT.JSON_GRAPH_LIMIT = (self.FRAME_GRAPH.CANDLES_MAX_NUM - 1)* self.FRAME_GRAPH.TICKS_FOR_ONE_CANDLE;
        self.FRAME_GRAPH.update();

        if _value == 240:
            self.FRAME_GRAPH.GRID_SIZE[0] = 6;
        elif _value == 120:
            self.G_SC_4.setChecked(True);
            self.FRAME_GRAPH.GRID_SIZE[0] = 36;
        elif _value == 60:
            self.G_SC_3.setChecked(True);
            self.FRAME_GRAPH.GRID_SIZE[0] = 84;
        elif _value == 40:
            self.G_SC_2.setChecked(True);
            self.FRAME_GRAPH.GRID_SIZE[0] = 132;
        elif _value == 20:
            self.FRAME_GRAPH.GRID_SIZE[0] = 336;

        """
        # -------------------------------------------------------------------
        self.PARENT.LOG["info"].append( str(self.FRAME_GRAPH.GRID_SIZE) );
        # -------------------------------------------------------------------

    # =======================================================================
    def GRAPH_Y_SHIFTER(self, _action):

        # -------------------------------------------------------------------
        #print(_action);

        if _action == "+":
            self.FRAME_GRAPH.Y_CENTER_OFFSET_SHIFTER_EXPR += self.FRAME_GRAPH.Y_CENTER_OFFSET_SHIFTER_STEP;
        
        elif _action == "-":
            self.FRAME_GRAPH.Y_CENTER_OFFSET_SHIFTER_EXPR -= self.FRAME_GRAPH.Y_CENTER_OFFSET_SHIFTER_STEP;


        """
        if _action == "+":
            self.FRAME_GRAPH.Y_CENTER_OFFSET += self.FRAME_GRAPH.Y_CENTER_OFFSET_SHIFTER_STEP;
        
        elif _action == "-":
            self.FRAME_GRAPH.Y_CENTER_OFFSET -= self.FRAME_GRAPH.Y_CENTER_OFFSET_SHIFTER_STEP;
        """
            
        self.PARENT.LOG["notif"].append(self.FRAME_GRAPH.Y_CENTER_OFFSET);
        # -------------------------------------------------------------------
        self.FRAME_GRAPH.update();
        # -------------------------------------------------------------------

    # =======================================================================
    def GRAPH_Y_ZOOMER(self, _action):

        # -------------------------------------------------------------------
        _curr_ = self.PARENT.CURR_PAIR;

        if _action == "+":

            if self.FRAME_GRAPH.GRAPH_H-self.FRAME_GRAPH.MAX_VALUE < 60:
                return;

            self.FRAME_GRAPH.Y_ZOOM[ _curr_ ]["current"] += self.FRAME_GRAPH.Y_ZOOM[ _curr_ ]["step"];

        elif _action == "-":

            self.FRAME_GRAPH.Y_ZOOM[ _curr_ ]["current"] -= self.FRAME_GRAPH.Y_ZOOM[ _curr_ ]["step"];

            # Do not Allow To ZOOM in reverce ( max value must stay on top)
            if self.FRAME_GRAPH.Y_ZOOM[ _curr_ ]["current"] < self.FRAME_GRAPH.Y_ZOOM[ _curr_ ]["min_zoom"]:
                self.FRAME_GRAPH.Y_ZOOM[ _curr_ ]["current"] = self.FRAME_GRAPH.Y_ZOOM[ _curr_ ]["min_zoom"];

        elif _action == "reset":
        
            self.FRAME_GRAPH.Y_ZOOM[ _curr_ ]["current"] -= self.FRAME_GRAPH.Y_ZOOM[ _curr_ ]["default"];

        else:

            print("GRAPH_Y_ZOOMER: Unknown _action: ["+str(_action)+"]")
            return;

        # -------------------------------------------------------------------
        #self.PARENT.LOG["notif"].append(self.FRAME_GRAPH.Y_ZOOM);
        # -------------------------------------------------------------------
        self.FRAME_GRAPH.update();
        # -------------------------------------------------------------------

    # =======================================================================
    def UPDATE_WATCH_DISPLAY(self):

        # -------------------------------------------------------------------
        try:

            left = self.UPD_WATCH_COUNTER/1000; 

            self.WATCH_DISPLAY.display( "00:"+str(left if left > 9 else "0"+str(left)) );
            self.UPD_WATCH_COUNTER -= 1000;

            if self.TRADE_TERMINAL_HAS_ACTION:
                self.TRADE_TERMINAL_HAS_ACTION = False;
                self.SET_NEW_TRADE_DATA();

        except Exception as _exception:

            msg = " Watch error: Enabling Auto-Correction. <br>"+str(_exception);
            self.PARENT.LOG["info"].append(msg);

        # -------------------------------------------------------------------

    # =======================================================================
    # OFFICE-METHODS

    def ALARMS_ACTION(self, _action, _params=None):
        
        # -------------------------------------------------------------------
        # 41.27
        # New ORDER: #0 buy 3.249 ltc_usd @ 13.393
        # -------------------------------------------------------------------
        if _action == "item_changed":

            if _params == "buy":
                self.ALARMS_CURRENT_LIST_SELECTOR = "buy";
            else:
                self.ALARMS_CURRENT_LIST_SELECTOR = "sell";

        elif _action == "add":
            
            try:
                if float(self.ALARM_VALUE_INPUT.text()) < 0.0000001:
                    self.SHOW_QMESSAGE("info", "Value can't be less 0.0000001");
                    return;

                else:

                    actions = str(self.CURRENCY_ACTION_COMBO.currentText());
                    pairs = str(self.CURRENCY_COMBO.currentText());
                    height = str(self.IF_CURRENCY_COMBO.currentText());
                    price = float(self.ALARM_VALUE_INPUT.text());

                    self.PARENT.LOG["info"].append(" New Alarm: <br/> [Ring if "+str(pairs)+" is "+str(height)+" > "+str(price)+"]");

                    _SQL = "INSERT INTO alarms ( id, action, pairs, height, this_price )";
                    _SQL += " VALUES( NULL, '{0}', '{1}', '{2}', {3} )".format( actions, pairs, height, price );

                    self.PARENT.DB.EXEC("OFFICE_DB", _SQL);
                    self.ALARM_VALUE_INPUT.setText("0");
                    if self.CONF["SYS"]["ALLOW_SOUND"]: self.Sound.RING( _type=0 );

                self.ALARMS_ACTION("update");

            except Exception as _exception:

                msg = " Could't set new Alarm: <br/> "+str(_exception);
                self.PARENT.LOG["error"].append(msg);


        elif _action == "delete":

            try:

                ID = None;

                if self.ALARMS_CURRENT_LIST_SELECTOR == "buy":
                    if self.ALARMS_LIST_TO_BUY.currentItem() is not None:
                        ID = str(self.ALARMS_LIST_TO_BUY.currentItem().text()).split("|")[0].split(":")[1];
                    else:
                        return;

                elif self.ALARMS_CURRENT_LIST_SELECTOR == "sell":
                    if self.ALARMS_LIST_TO_SELL.currentItem() is not None:
                        ID = str(self.ALARMS_LIST_TO_SELL.currentItem().text()).split("|")[0].split(":")[1];
                    else:
                        return;
                if ID is not None:

                    self.PARENT.DB.EXEC("OFFICE_DB", "DELETE FROM alarms  WHERE id="+str(ID) );
                    self.ALARMS_ACTION("update");

                    if self.CONF["SYS"]["ALLOW_SOUND"]: self.Sound.RING( _type=4 );

            except Exception as _exception:
                msg = " Could't DELETE Alarm: <br/> "+str(_exception);
                self.PARENT.LOG["error"].append(msg);

        elif _action == "update":
    
            try:

                # Append alarms from db
                _ALARMS = self.PARENT.DB.FETCH("OFFICE_DB", "SELECT * FROM alarms", ALL=True);
                
                self.ALARMS_LIST_TO_BUY.clear(  );
                self.ALARMS_LIST_TO_SELL.clear(  );


                self.ALARMS_DATA = { 
                    "buy": {
                        "lower": [], "higher" : []
                    },
                    "sell": {
                        "lower": [], "higher" : []
                    }
                };


                for row in _ALARMS:

                    # print( "0", row[0]); |> id
                    # print( "1", row[1]); |> action
                    # print( "2", row[2]); |> pairs
                    # print( "3", row[3]); |> this_price
                    # print( "4", row[4]); |> height

                    # ( id, action, pairs, this_price, height )
                    action = str(row[1]).lower();
                    height = str(row[4]).lower();

                    self.ALARMS_DATA[ action ][ height ].append( [ row[0], row[1], row[2], row[3], row[4] ] );
                    
                    _alarm = "ID: "+str(str(row[0])+" | "+str(row[1].upper())+" "+str(row[2])+" if "+str(row[4])+" > "+str(row[3]));

                    if action == "buy":
                        self.ALARMS_LIST_TO_BUY.addItem( _alarm );

                    else:
                        self.ALARMS_LIST_TO_SELL.addItem( _alarm );

            except Exception as _exception:
                msg = " Could't UPDATE Alarms: <br/> "+str(_exception);
                self.PARENT.LOG["error"].append(msg);

        elif _action == "check":


            try:
                # [1, 'BUY', 'LTC_USD', 2.0, 'LOWER'] == alarm
                _buy, _sell, _pair = _params;

                # BUY
                for alarm in self.ALARMS_DATA["buy"]["lower"]:

                    if alarm[2].lower() == _pair.lower():
                        if float(_buy) <= float(alarm[3]):
                            #print(float(_buy), "<=", float(alarm[3]));
                            if self.CONF["SYS"]["ALLOW_SOUND"]: self.Sound.RING( _type=2 );
                            self.SHOW_QMESSAGE("info", "Alarm ID: ["+str(alarm[0])+"]<br> BUY if ['"+str(alarm[2])+"'] is LOWER > "+str(float(alarm[3]))+"<br> Current ['BUY'] price is: "+str(float(_buy)));

                for alarm in self.ALARMS_DATA["buy"]["higher"]:

                    if alarm[2].lower() == _pair.lower():
                        if float(_buy) >= float(alarm[3]):
                            #print(float(_buy), ">=", float(alarm[3]));
                            if self.CONF["SYS"]["ALLOW_SOUND"]: self.Sound.RING( _type=2 );
                            self.SHOW_QMESSAGE("info", "Alarm ID: ["+str(alarm[0])+"]<br> BUY if ['"+str(alarm[2])+"'] is HIGHER > "+str(float(alarm[3]))+"<br> Current ['BUY'] price is: "+str(float(_buy)));

                # SELL
                for alarm in self.ALARMS_DATA["sell"]["lower"]:

                    if alarm[2].lower() == _pair.lower():
                        if float(_sell) <= float(alarm[3]):
                            #print(float(_sell), "<=", float(alarm[3]));
                            if self.CONF["SYS"]["ALLOW_SOUND"]: self.Sound.RING( _type=2 );
                            self.SHOW_QMESSAGE("info", "Alarm ID: ["+str(alarm[0])+"]<br> SELL if ['"+str(alarm[2])+"'] is LOWER > "+str(float(alarm[3]))+"<br> Current ['BUY'] price is: "+str(float(_buy)));


                for alarm in self.ALARMS_DATA["sell"]["higher"]:

                    if alarm[2].lower() == _pair.lower():
                        if float(_sell) >= float(alarm[3]):
                            #print(float(_sell), ">=", float(alarm[3]));
                            if self.CONF["SYS"]["ALLOW_SOUND"]: self.Sound.RING( _type=2 );
                            self.SHOW_QMESSAGE("info", "Alarm ID: ["+str(alarm[0])+"]<br> SELL if ['"+str(alarm[2])+"'] is HIGHER > "+str(float(alarm[3]))+"<br> Current ['BUY'] price is: "+str(float(_buy)));

            except Exception as _exception:
                msg = " Could't CHECK Alarms: <br/> "+str(_exception);
                self.PARENT.LOG["error"].append(msg);

        # -------------------------------------------------------------------


    # =======================================================================
    def TEST_METHOD(self):

        self.PARENT.LOG["info"].append( "TEST_METHOD trigered !" );

    # =======================================================================
    # CLASS METHOD's >>>

    #@pyqtSlot()
    def LOG_MANAGER(self): # AUTO UPDATE EACH (self.LOG_MANAGER_UPD_DELAY) MillSecs

        # -------------------------------------------------------------------
        #self.PARENT.LOG["notif"].append( str(self.FRAME_GRAPH.GRID_SIZE) );
        # -------------------------------------------------------------------
        try:

            if self.ALLOW_UPD_METADATA:
                self.ALLOW_UPD_METADATA = False;
                self.UPDATE_METADATA();

            if self.ALLOW_DISPLAY_LOG:

                # ---------------------------------------------------
                for _data in self.PARENT.LOG["info"]: # (PRIORITY = 4) 
                    self.INFO_PANEL_LOG.append('<i style="color: #00F;"> Info</i>: <i>'+str(_data)+'</i>');

                self.PARENT.LOG["info"] = []; # Clear out

                # ---------------------------------------------------
                for _data in self.PARENT.LOG["notif"]: # (PRIORITY = 3) 
                    self.INFO_PANEL_LOG.append('<i style="color: #FF0;"> Notif</i>: <i>'+str(_data)+'</i>');

                self.PARENT.LOG["notif"] = []; # Clear out

                # ---------------------------------------------------
                for _data in self.PARENT.LOG["success"]: # (PRIORITY = 2) 
                    self.INFO_PANEL_LOG.append('<i style="color: #0F0;"> Success</i>: <i>'+str(_data)+'</i>');

                self.PARENT.LOG["success"] = []; # Clear out

                # ---------------------------------------------------
                for _data in self.PARENT.LOG["error"]: # (PRIORITY = 1) 
                    self.INFO_PANEL_LOG.append('<i style="color: #F00; "> Error</i>: <i>'+str(_data)+'</i>');

                self.PARENT.LOG["error"] = []; # Clear out

                # ---------------------------------------------------
                for _data in self.PARENT.LOG["status-bar"]: # (PRIORITY = 0)
                    self.TO_STATUSBAR(_data);

                self.PARENT.LOG["status-bar"] = []; # Clear out

                # ---------------------------------------------------
            #self.update();

        except Exception as _exception:

            self.PARENT.LOG["error"].append(" LOG_MANAGER: "+str(_exception));
        # ------------------------------------------------------------------

    # =======================================================================
    def UPDATE_METADATA(self):

        # ------------------------------------------------------------------
        if self.CONF["SYS"]["ALLOW_UPD"]:

            buy = self.PARENT.JSON_META_DATA[self.PARENT.CURR_PAIR]["buy"];
            last_buy = self.PARENT.LAST_JSON_META_DATA[self.PARENT.CURR_PAIR]["buy"];
            
            sell = self.PARENT.JSON_META_DATA[self.PARENT.CURR_PAIR]["sell"];
            last_sell = self.PARENT.LAST_JSON_META_DATA[self.PARENT.CURR_PAIR]["sell"];

            for pair in self.PARENT.JSON_META_DATA:
                self.ALARMS_ACTION(_action="check", _params=[ buy, sell, pair ]);


            self.BUYING_PRICE.value = buy;
            self.BUYING_PRICE.setText(str(buy));
            self.BUYING_LAST_PRICE.setText(str(last_buy));

            self.SELLING_PRICE.value = sell;
            self.SELLING_PRICE.setText(str(sell));
            self.SELLING_LAST_PRICE.setText(str(last_sell));

            # -------------------------------------------------------
            if last_buy > buy:
                self.BUYING_ARROW.setPixmap(self.ARROW_D);
                self.BUYING_ARROW.setMask(self.ARROW_D.mask());
                buy_sym = u"↓";

                self.BUYING_PRICE_DIFFERENCE.setText( "-{:10,.7f}".format(last_buy-buy) );
                self.BUYING_PRICE_DIFFERENCE.setStyleSheet( STL.PRICE_DIFFERENCE_RED );


            elif last_buy < buy:
                self.BUYING_ARROW.setPixmap(self.ARROW_U);
                self.BUYING_ARROW.setMask(self.ARROW_U.mask());
                buy_sym = u"↑";

                self.BUYING_PRICE_DIFFERENCE.setText( "+{:10,.7f}".format( buy-last_buy  ) );
                self.BUYING_PRICE_DIFFERENCE.setStyleSheet( STL.PRICE_DIFFERENCE_GREEN );

            else:
                self.BUYING_ARROW.setPixmap(self.ARROW_N);
                self.BUYING_ARROW.setMask(self.ARROW_N.mask());
                buy_sym = "=";

                self.BUYING_PRICE_DIFFERENCE.setStyleSheet( STL.PRICE_DIFFERENCE_WHITE );
                self.BUYING_PRICE_DIFFERENCE.setText( "= "+self.INIT_VALUE_0 );

            # -------------------------------------------------------
            if last_sell > sell:
                self.SELLING_ARROW.setPixmap(self.ARROW_D);
                self.SELLING_ARROW.setMask(self.ARROW_D.mask());
                sell_sym = u"↓";

                self.SELLING_PRICE_DIFFERENCE.setText( "-{:10,.7f}".format(last_sell-sell) );
                self.SELLING_PRICE_DIFFERENCE.setStyleSheet( STL.PRICE_DIFFERENCE_RED );

            elif last_sell < sell:
                self.SELLING_ARROW.setPixmap(self.ARROW_U);
                self.SELLING_ARROW.setMask(self.ARROW_U.mask());
                sell_sym = u"↑";

                self.SELLING_PRICE_DIFFERENCE.setText( "+{:10,.7f}".format( sell-last_sell ) );
                self.SELLING_PRICE_DIFFERENCE.setStyleSheet( STL.PRICE_DIFFERENCE_GREEN );


            else:
                self.SELLING_ARROW.setPixmap(self.ARROW_N);
                self.SELLING_ARROW.setMask(self.ARROW_N.mask());
                sell_sym = "=";

                self.SELLING_PRICE_DIFFERENCE.setStyleSheet( STL.PRICE_DIFFERENCE_WHITE );
                self.SELLING_PRICE_DIFFERENCE.setText( "= "+self.INIT_VALUE_0 );


            # -------------------------------------------------------
            templ = "[ {0} H: {1}, L: {2}, B:"+buy_sym+" {3}, S:"+sell_sym+" {4} ] ";
            OUT = "";

            JSD = self.PARENT.JSON_META_DATA;

            for P in JSD:

                OUT += templ.format( P.replace("_", "/").upper(), JSD[P]["high"], JSD[P]["low"], JSD[P]["buy"], JSD[P]["sell"] );

            self.NEWS_LINE_DATA = OUT;

            # -------------------------------------------------------
            # 

            if self.CONF["SYS"]["GUI"]["SHOW_MSG_AS_WIN_TITLE"]:
                self.setWindowTitle('['+buy_sym+str(buy)[0:6]+'|'+sell_sym+str(sell)[0:6]+']');

            # -------------------------------------------------------
            self.PANEL_BUY_ORDERS.clear();
            bids = self.PARENT.RAW_ASK_BID_META_DATA[self.PARENT.CURR_PAIR]["bids"];
            for bid in bids:

                self.PANEL_BUY_ORDERS.addItem(" {0:.7f}  | {1:.7f}".format( bid[0], bid[1] ) );

            self.PANEL_SELL_ORDERS.clear();
            asks = self.PARENT.RAW_ASK_BID_META_DATA[self.PARENT.CURR_PAIR]["asks"];

            for ask in asks:

                self.PANEL_SELL_ORDERS.addItem( " {0:.7f}  | {1:.7f}".format( ask[0], ask[1] ) );

            # ------------------------------------------------------------------
            self.API_GET_ORDERS_LIST();
            # ------------------------------------------------------------------
            self.update();
            self.TRANS_MESSAGE(_action="hide");
            

        else:
            self.PARENT.LOG["info"].append(" UPDATE: Is DISABLED[0:0]");
        # ------------------------------------------------------------------

    # ======================================================================
    def NEWS_LINE_UPDATER(self):

        # ------------------------------------------------------------------

        self.NEWS_LINE_DATA_L = len(self.NEWS_LINE_DATA);
        #self.NEWS_LINE_DATA_C = 0;

        self.NEWS_LINE_DATA_C += 1;
        if self.NEWS_LINE_DATA_C > self.NEWS_LINE_DATA_L-1:
            self.NEWS_LINE_DATA_C = 0;


        #if self.CONF["SYS"]["GUI"]["SHOW_MSG_AS_WIN_TITLE"]:
        #    self.setWindowTitle('['+buy_sym+str(buy)[0:6]+'|'+sell_sym+str(sell)[0:6]+']');

        OUT = self.NEWS_LINE_DATA[self.NEWS_LINE_DATA_C:] + self.NEWS_LINE_DATA[:self.NEWS_LINE_DATA_C]                

        #print(OUT[0:50]);

        self.TO_STATUSBAR( OUT );
        #self.setWindowTitle( OUT );
        #self.setWindowTitle('['+buy_sym+str(buy)[0:6]+'|'+sell_sym+str(sell)[0:6]+']');




        self.NEWS_LINE_TIMER = QTimer();
        self.NEWS_LINE_TIMER.singleShot( 250, self.NEWS_LINE_UPDATER );
        # ------------------------------------------------------------------

    # ======================================================================
    def SHOW_QMESSAGE(self, _type="info", _msg="None"):

        # ------------------------------------------------------------------
        try:

            _msg = '<center><b style="color: #000; font-color: 16px;">'+_msg+'</b></center>'

            if _type == "info":
                _out = '<b style="font-color: 22px; color: #009;">Notification!</b>';
                reply = QMessageBox.information(self, self.CONF["INFO"]["NAME"], _out+_msg, QMessageBox.Yes, QMessageBox.No)

            elif _type == "warning":
                _out = '<B style="font-color: 22px; color: #900;">Warning!</b>';
                reply = QMessageBox.warning(self, self.CONF["INFO"]["NAME"], _out+_msg, QMessageBox.Yes, QMessageBox.No)

            elif _type == "question":
                _out = '<b style="font-color: 22px; color: #009;">Question!</b><br/>';
                reply = QMessageBox.question(self, self.CONF["INFO"]["NAME"], _out+_msg, QMessageBox.Yes, QMessageBox.No)

            elif _type == "critical":
                _out = '<b style="font-color: 22px; color: #F00;">Critical!</b><br/>';
                reply = QMessageBox.critical(self, self.CONF["INFO"]["NAME"], _out+_msg, QMessageBox.Yes, QMessageBox.No)

            else:
                self.PARENT.LOG["error"].append(" Unknown QMessageBox[type]");
                return;

            # --------------------------------------------------------------
            # 16384 == yes / 65536 == no
            if reply == QMessageBox.Yes:
                return True;
            else:
                return False;

        except Exception as _exception:

            self.PARENT.LOG["error"].append(" Last action error: "+str(_exception));
            return False;
        # ------------------------------------------------------------------

    # =======================================================================
    def SELECT_PAIR(self):

        # ------------------------------------------------------------------
        try:

            self.FRAME_GRAPH.GRAPH_OVERLAY_WIDGET.show();

            self.PARENT.CURR_PAIR = str(self.FRAME_MAIN.PAIR_COMBO.currentText()).lower();
            self.FRAME_GRAPH.CURR_PAIR = self.PARENT.CURR_PAIR;
            
            self.PARENT.IS_FIRST_UPDATE = True;
            _msg = " Changing Trading Pairs to: "+str(self.PARENT.CURR_PAIR.upper());

            self.PARENT.LOG["info"].append(_msg);
            self.TRANS_MESSAGE(_action="show", _loading=True, _msg=_msg);

            self.FRAME_GRAPH.RESET_GLOBAL_VALUES = True;

        except Exception as _exception:
            _msg = " Selecting pair error: "+str(_exception);
            print(_msg);
            self.PARENT.LOG["error"].append(_msg);
        # ------------------------------------------------------------------

    # =======================================================================
    def TRADE_ACTION(self, _action="None"):

        # ------------------------------------------------------------------
        try:
        # ------------------------------------------------------------------
            if self.SHOW_QMESSAGE(_type="info", _msg=" Are you sure ?"):

                # ----------------------------------------------------------------------
                while not self.PARENT.TRADE_MANAGER_ACTION_FINISHED:
                    pass;

                # ----------------------------------------------------------------------
                if _action == "sell":
    
                    self.PARENT.TRADE_MANAGER_DATA["SELL"]["CURR_TYPE"].append(self.PARENT.CURR_PAIR);
                    self.PARENT.TRADE_MANAGER_DATA["SELL"]["AMOUNT"].append(float( str(self.USER_SELL_AMOUNT.text()).strip() ));
                    self.PARENT.TRADE_MANAGER_DATA["SELL"]["AT_PRICE"].append(float( str(self.USER_SELL_AT_PRICE.text()).strip() ));

                    self.PARENT.TRADE_MANAGER_ACTION_REQUIRED = True;

                    self.USER_SELL_AMOUNT.setText( self.INIT_VALUE_1 );
                    self.USER_SELL_AT_PRICE.setText( self.INIT_VALUE_0 );

                elif _action == "buy":

                    self.PARENT.TRADE_MANAGER_DATA["BUY"]["CURR_TYPE"].append( self.PARENT.CURR_PAIR );
                    self.PARENT.TRADE_MANAGER_DATA["BUY"]["AMOUNT"].append(float( str(self.USER_BUY_AMOUNT.text()).strip() ));
                    self.PARENT.TRADE_MANAGER_DATA["BUY"]["AT_PRICE"].append(float( str(self.USER_BUY_AT_PRICE.text()).strip() ));

                    self.PARENT.TRADE_MANAGER_ACTION_REQUIRED = True;

                    self.USER_BUY_AMOUNT.setText( self.INIT_VALUE_1 );
                    self.USER_BUY_AT_PRICE.setText( self.INIT_VALUE_0 );

                # ----------------------------------------------------------------------
                #self.PARENT.GUI.BUY_BTN.setEnabled(True);
                #self.PARENT.GUI.SELL_BTN.setEnabled(True);

                if self.CONF["SYS"]["ALLOW_SOUND"]: self.Sound.RING( _type=0 );
                # ----------------------------------------------------------------------

            else:
                self.PARENT.LOG["info"].append(" Action: Canceled!");
        
        # ------------------------------------------------------------------
        except Exception as _exception:
            self.PARENT.LOG["error"].append(_exception);
        # ------------------------------------------------------------------

    # =======================================================================
    # =======================================================================
    # =======================================================================
    # self.API_* Methods

    def API_UPDATE_BALANCE(self):

        # ------------------------------------------------------------------
        if self.CONF["SYS"]["ALLOW_UPD"]:

            # ------------------------------------------------------------------
            self.TRANS_MESSAGE(_action="show", _loading=True, _msg="Updating ...", _lock=True, _close=False);
            # ------------------------------------------------------------------
            try:

                JSON = self.Request.getInfo();

                if JSON["success"] == 1:

                    self.PARENT.USER_BALANCE = JSON["return"];
                    self.BALANCE_WIDGET.setText("");

                    for key in self.PARENT.USER_BALANCE["funds"]:

                        balance_line =  "{0:5} {1}".format( key.upper(), str(self.PARENT.USER_BALANCE["funds"][key]) );

                        self.BALANCE_WIDGET.append(balance_line);

                else:
                    
                    self.PARENT.LOG["error"].append(" "+JSON["error"]);
                    #print( json.dump(JSON, sort_keys=True, indent=4, separators=(',', ': ')) );

            except Exception as _exception:
                self.PARENT.LOG["error"].append(" Could't get account balance !");
                print(_exception);

            # ------------------------------------------------------------------
            self.TRANS_MESSAGE_WIDGET_RELEAS_LOCK();
            # ------------------------------------------------------------------

        else:
            pass;
        # ------------------------------------------------------------------

    # =======================================================================
    def API_CANCEL_ORDERS(self, _order_id, _type):

        # ------------------------------------------------------------------
        if self.FRAME_ORDERS.ORDER_ID_TO_CANCEL:

            if self.SHOW_QMESSAGE(_type="info", _msg=" Do you want CANCEL order ID\n"+str(_order_id)+" ?"):
                
                # ----------------------------------------------
                # Get info about order wich will be canceled


                JSON = self.Request.OrderInfo( _order_id );


                if JSON["success"] == 1:

                    _PAIR_ = JSON["return"][_order_id]["pair"];
                    _TYPE_ = JSON["return"][_order_id]["type"];

                # ----------------------------------------------
                # Cancel this order

                JSON = self.Request.CancelOrder( _order_id );

                if JSON["success"] == 1:

                    # ------------------------------------------------------
                    JSON = JSON["return"];
                    self.PARENT.LOG["success"].append(" ORDER: "+str(_order_id)+" Was canceled! ");

                    if self.CONF["SYS"]["ALLOW_SOUND"]: self.Sound.RING( _type=4 );

                    # ------------------------------------------------------
                    try:

                        if self.FRAME_ORDERS.ORDER_TYPE_TO_CANCEL:

                            # ------------------------------------------------------
                            # FRAME_ORDERS

                            self.FRAME_ORDERS.DELETE_ORDER( _order_id, _PAIR_, _TYPE_ );
                            del self.FRAME_ORDERS.ORDERS_FROM_DB[ int(_order_id) ];
                            self.FRAME_ORDERS.CREATE_LISTS();

                            # ------------------------------------------------------
                            # FRAME_HISTIRY
                            #self.FRAME_HISTORY.DELETE_ORDER( _order_id, _PAIR_, _TYPE_ );
                            #self.FRAME_HISTORY.CREATE_LISTS();

                            # ------------------------------------------------------
                            # FRAME_BOOKKEEPING
                            self.FRAME_BOOKKEEPING.DELETE_ORDER( _order_id, _PAIR_, _TYPE_  );
                            self.FRAME_BOOKKEEPING.CREATE_LISTS();

                            # ------------------------------------------------------
                            self.API_GET_ORDERS_LIST();

                            # ------------------------------------------------------
                            # Clean UP some garbadge

                            self.FRAME_ORDERS.ORDER_ID_TO_CANCEL = False;
                            self.FRAME_ORDERS.ORDER_TYPE_TO_CANCEL = False;
                            # ------------------------------------------------------

                        else:

                            print(" NO 'self.FRAME_ORDERS.ORDER_TYPE_TO_CANCEL' ");


                    except Exception as _exception:
                        
                        print(_exception);
                        self.PARENT.LOG["error"].append(str(_exception));
                    # ------------------------------------------------------

                else:

                    self.SHOW_QMESSAGE(_type="warning", _msg="ORDER: "+str(_order_id)+"<br> Was't CANCELED<br> Maybe Wrong ID ? ");

                    self.PARENT.LOG["error"].append("ORDER: "+str(_order_id)+" Was't CANCELED! Maybe Wrong ID ? ");
                    self.PARENT.LOG["error"].append("ORDER: "+str(_order_id)+" -> "+JSON["error"]);

        else:

            print("You can't access this method direct! ");
        # ------------------------------------------------------------------

    # =======================================================================
    def API_GET_ORDERS_LIST(self):


        # ------------------------------------------------------------------
        if self.CONF["SYS"]["ALLOW_UPD"]:

            # ------------------------------------------------------------------
            #self.TRANS_MESSAGE(_action="show", _loading=True, _msg="Updating ...", _lock=True, _close=False);
            # ------------------------------------------------------------------
            try:

                JSON = self.Request.ActiveOrders();

                if JSON["success"] == 1:

                    JSON_FROM_SERVER = JSON["return"];

                    '''
                    print( json.dumps( JSON , separators=(',', ': ')) );
                    print( json.dumps( JSON , indent=4, separators=(',', ': ')) );
                    '''

                    # ====================================================================
                    if True:

                        # -------------------------------------------------------------
                        # Check for complited orders
                        MSG = "";

                        ORDERS_TO_DEL = [];

                        for ORDER_ID_FROM_DB in self.FRAME_ORDERS.ORDERS_FROM_DB:

                            ORDER_ID_FROM_DB = str(ORDER_ID_FROM_DB);

                            if ORDER_ID_FROM_DB not in JSON_FROM_SERVER: # Then it's complited

                                if self.CONF["SYS"]["ALLOW_SOUND"]: self.Sound.RING( _type=1 );

                                # -----------------------------------------------------
                                self.PARENT.LOG["success"].append("Order ID: "+str(ORDER_ID_FROM_DB)+" Complited!");
                                MSG += "Order ID: "+str(ORDER_ID_FROM_DB)+" Complited! <br/>";

                                # -----------------------------------------------------
                                _type = self.FRAME_ORDERS.ORDERS_FROM_DB[ int(ORDER_ID_FROM_DB) ]["type"];
                                _pair = self.FRAME_ORDERS.ORDERS_FROM_DB[ int(ORDER_ID_FROM_DB) ]["pair"];

                                # -----------------------------------------------------
                                # BOOKKEEPING_DB
                                _SQL = "UPDATE "+_pair+" SET "+_type+"_filled=1"+" WHERE "+_type+"_order_id="+str(ORDER_ID_FROM_DB);
                                self.PARENT.DB.EXEC("BOOK_DB", _SQL);

                                # -----------------------------------------------------
                                # HISTORY_DB

                                _SQL = "UPDATE "+_pair+" SET filled=1 WHERE order_id="+str(ORDER_ID_FROM_DB);
                                self.PARENT.DB.EXEC("HISTORY_DB", _SQL);
                                self.FRAME_HISTORY.CREATE_LISTS();

                                # -----------------------------------------------------
                                # ORDERS_DB
                                _SQL = "UPDATE "+_pair+" SET filled=1 WHERE order_id="+str(ORDER_ID_FROM_DB);
                                self.PARENT.DB.EXEC("ORDERS_DB", _SQL);

                                ORDERS_TO_DEL.append(int(ORDER_ID_FROM_DB));

                                # -----------------------------------------------------
                            """
                            else:
                                print("this order is IN DB: "+ORDER_ID_FROM_DB);
                        
                            """
                        # -------------------------------------------------------------
                        for order in ORDERS_TO_DEL:
                            del self.FRAME_ORDERS.ORDERS_FROM_DB[ int(order) ];

                        self.FRAME_ORDERS.GET_ORDERS_FROM_DB();
                        self.FRAME_ORDERS.CREATE_LISTS();

                        # -------------------------------------------------------------
                        # Display info about complited Orders
                        if MSG != "":
                            self.TRANS_MESSAGE(_action="show", _loading=False, _msg=MSG, _lock=True);

                        # ====================================================================

                else: # JSON["success"] == 0:
                    
                    self.PARENT.LOG["error"].append(" Could't get ACTIVE orders! \n "+JSON["error"]);

            except Exception as _exception:
                
                if not str(_exception) == "'NoneType' object has no attribute '__getitem__'":
                    self.PARENT.LOG["error"].append(" Order list update error[0:0]: "+str(_exception));

                print("ERR: [12:0]"+str(_exception));

            # ------------------------------------------------------------------
            #self.TRANS_MESSAGE_WIDGET_RELEAS_LOCK();
            # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        else:

            print("API_GET_ORDERS_LIST: ALLOW_UPD == False;")
        # ------------------------------------------------------------------

    # =======================================================================
    # =======================================================================
    # =======================================================================
    def SET_NEW_TRADE_DATA(self, _action="None"):

        # ------------------------------------------------------------------
        self.API_UPDATE_BALANCE();# <<< has own try{ }catch(){}
        # ------------------------------------------------------------------
        try:

            sell_avail = "{0:,.7f}".format( self.PARENT.USER_BALANCE["funds"][self.PARENT.CURR_PAIR.split("_")[0]]);
            self.USER_SELL_AVAIL.setText( sell_avail );

            buy_avail = "{0:,.7f}".format( self.PARENT.USER_BALANCE["funds"][self.PARENT.CURR_PAIR.split("_")[1]]);
            self.USER_BUY_AVAIL.setText( buy_avail );

            self.USER_SELL_AT_PRICE.setText(str(self.PARENT.RAW_ASK_BID_META_DATA[self.PARENT.CURR_PAIR]["bids"][0][0]));
            self.USER_BUY_AT_PRICE.setText(str(self.PARENT.RAW_ASK_BID_META_DATA[self.PARENT.CURR_PAIR]["asks"][0][0]));

        except Exception as _exception:

            #self.PARENT.LOG["error"].append(" Data Error: \n "+str(_exception));
            print(_exception);
        # ------------------------------------------------------------------

    # =======================================================================
    def closeEvent(self, _event):
        
        # ------------------------------------------------------------------
        if self.GUI_EXIT():
            pass;
        
        else:
            _event.ignore();
            #self.setWindowState(Qt.WindowMinimized);
        # ------------------------------------------------------------------

    # =======================================================================
    def GUI_EXIT(self):

        # ------------------------------------------------------------------
        if self.SHOW_QMESSAGE(_type="info", _msg=" Do you want exit ?"):
            if self.CONF["SYS"]["ALLOW_SOUND"]: self.Sound.RING( _type=4 );
            # -----------------------------------------------------------
            self.CONF["SYS"]["ALLOW_UPD"] = False;
            print("self.GUI.exit(): Accepted! ")
            self.AVAILABLE = False;
            
            self.hide();

            # -----------------------------------------------------------
            if self.CONF["SYS"]["GUI"]["SPLASH"]["SHOW"]:

                _Splash = Splash(
                    _msg=" Saving & Exit !  ", 
                    _app=self.CONF["INFO"]["NAME"], 
                    _ver=self.CONF["INFO"]["VERSION"], 
                    _link=self.CONF["INFO"]["LINK"], 
                    _author=self.CONF["INFO"]["AUTHOR"]  
                );
                
                self.CONF["SYS"]["ALLOW_UPD"] = False;
                if self.PARENT.SAVE_DATA():
                    self.CONF["SYS"]["ALLOW_UPD"] = False;
                    #self.FRAME_ORDERS.SAVE_ACTIVE_ORDERS();

                    _Splash.hide();
                    exit();

                else:
                    print(" ERROR: Could't Save data! BTCeGUI.GUI_EXIT();");

            # -----------------------------------------------------------
            if self.PARENT.SAVE_DATA():
                self.FRAME_NOTEBOOK.SAVE_DATA();
                exit();

            else:
                print(" ERROR: Could't Save data! BTCeGUI.GUI_EXIT();");

            # -----------------------------------------------------------
            return True; #  (if return False: closeEvent.ignore() == True )
            # -----------------------------------------------------------

        else:
            return False;
        # ------------------------------------------------------------------
    
    # =======================================================================
    def REINIT(self, _CONF):

        # ------------------------------------------------------------------
        self.CONF = _CONF;
        # ------------------------------------------------------------------

    # =======================================================================
    def SET_OPACITY(self, _OPAS=1.0):

        # ------------------------------------------------------------------
        #self.DESKTOP.setWindowOpacity(0.5);
        #self.setWindowOpacity(_OPAS);
        pass;
        # ------------------------------------------------------------------

    # =======================================================================
    def TO_STATUSBAR(self, _msg):

        # ------------------------------------------------------------------
        self.statusBar().showMessage(_msg); #.setEnabled(False);

        # ------------------------------------------------------------------

    # =======================================================================
    def TRANS_MESSAGE_WIDGET_RELEAS_LOCK(self):

        # ------------------------------------------------------------------
        self.TRANS_MESSAGE_WIDGET_ALPHA.LOCKED = False;
        self.TRANS_MESSAGE_WIDGET_CLOSE_BTN.hide();
        self.TRANS_MESSAGE(_action="hide");

        # ------------------------------------------------------------------

    # =======================================================================
    def TRANS_MESSAGE(self, _action="hide", _loading=False, _msg="System Message:", _delay=None, _lock=False, _close=True):

        # ------------------------------------------------------------------
        """
        self.TRANS_MESSAGE(_action="show", _loading=True, _msg="LOCKED", _lock=True);
        self.TRANS_MESSAGE(_action="show", _loading=True, _msg="_delay=1000", _delay=1000);
        self.TRANS_MESSAGE(_action="show", _loading=True, _msg="Updating ...", _lock=True, _close=False);
        self.TRANS_MESSAGE_WIDGET_RELEAS_LOCK();

        """
        # ------------------------------------------------------------------
        if _action == "show":

            try:

                if self.TRANS_MESSAGE_WIDGET_ALPHA.LOCKED:
                    #self.PARENT.LOG["info"].append(" System message: Action required ! @ "+self.PARENT.TIME);
                    return;

                if _lock:

                    self.TRANS_MESSAGE_WIDGET_ALPHA.LOCKED = True;

                    if _close:
                        self.TRANS_MESSAGE_WIDGET_CLOSE_BTN.show();

                
                self.TRANS_MESSAGE_WIDGET_ALPHA.show();
                self.TRANS_MESSAGE_TEXT_AREA.setHtml(_msg);

                if _loading:
                    self.TRANS_MESSAGE_LOADING_ANIM.start();
                
                if _delay is not None:
                    self.TRANS_MESSAGE_TIMER.singleShot(_delay, self.TRANS_MESSAGE);
    
            except Exception as _exception:
                self.PARENT.LOG["error"].append(" Notification Window: Error ");
                self.PARENT.LOG["error"].append(_exception);
                print(_exception);

        else:

            if self.TRANS_MESSAGE_WIDGET_ALPHA.LOCKED:
                #self.PARENT.LOG["info"].append(" System message: Action required ! @ "+self.PARENT.TIME);
                return;
    
            try:
                if not self.TRANS_MESSAGE_WIDGET_ALPHA.LOCKED:
                    self.TRANS_MESSAGE_WIDGET_ALPHA.hide();
                    self.TRANS_MESSAGE_LOADING_ANIM.stop();
                    self.TRANS_MESSAGE_WIDGET_CLOSE_BTN.hide();

            except Exception as _exception:

                self.PARENT.LOG["error"].append(_exception);

        # ------------------------------------------------------------------

    # =======================================================================

###################################################################################################
class Splash(object):

    # =======================================================================
    def __init__(self, _msg="None", _app="None", _ver="None", _link="None", _author="None"):

        # ------------------------------------------------------------------
        self.BG = QPixmap("data/imgs/splash.png");

        self.Screen = QSplashScreen(self.BG, Qt.WindowStaysOnTopHint)
        self.Screen.setAttribute(Qt.WA_TranslucentBackground, True);
        self.Screen.setMask(self.BG.mask());

        self.Screen.setAttribute(Qt.WA_DeleteOnClose);

        font = QFont(self.Screen.font())
        font.setPointSize(font.pointSize() + 5)
        self.Screen.setFont(font)
        self.Screen.show();
        qApp.processEvents();

        # ------------------------------------------------------------------
        self.app = QLabel(_app, self.Screen);
        self.app.setGeometry(250, 55, 200, 45);
        self.app.setStyleSheet("QLabel{ color: #222; font-size: 22px; border: none; background-color: transparent; }")
        self.app.show();

        self.ver = QLabel(_ver, self.Screen);
        self.ver.setGeometry(250, 80, 200, 45);
        self.ver.setStyleSheet("QLabel{ color: #333; font-size: 14px; border: none; background-color: transparent; }")
        self.ver.show();

        self.author = QLabel("by: "+_author, self.Screen);
        self.author.setGeometry(480, 205, 120, 35);
        self.author.setStyleSheet("QLabel{ color: #333; font-size: 14px; border: none; background-color: transparent; }")
        self.author.show();

        """
        self.link = QLabel(_link, self.Screen);
        self.link.setGeometry(380, 55, 120, 35);
        self.link.setStyleSheet("QLabel{ color: #333; font-size: 16px; border: none; background-color: transparent; }")
        self.link.show();
        """


        self.msg = QLabel(_msg, self.Screen);
        self.msg.setGeometry(270, 205, 200, 35);
        self.msg.setStyleSheet("QLabel{ color: #333; font-size: 16px; border: none; background-color: transparent; }")
        self.msg.show();
        # ------------------------------------------------------------------
        self.Screen.update()
        self.Screen.repaint();
        time.sleep(2);
        
        # ------------------------------------------------------------------
    # =======================================================================
    def paintEvent(self, event=None):
 
        # ------------------------------------------------------------------
        #print(" paint event")
        painter = QPainter(self.Screen)

        painter.setPen(QPen(QColor(0,90,0, 255)));
        painter.drawPixmap(self.Screen.rect(), self.BG);
        painter.drawText(aTextRect, itsAlignment, itsMessage);
        # ------------------------------------------------------------------

    # =======================================================================
    def hide(self):

        # ------------------------------------------------------------------
        self.Screen.hide();
        # ------------------------------------------------------------------

    # =======================================================================
    def finish(self, _widget):

        # ------------------------------------------------------------------
        self.Screen.show();
        time.sleep(1);
        self.Screen.finish(_widget);
        # ------------------------------------------------------------------
    # =======================================================================

        
###################################################################################################
