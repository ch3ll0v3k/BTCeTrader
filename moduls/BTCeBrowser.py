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
from PyQt4.QtCore import QTimer, SIGNAL, SLOT, Qt, QPointF, QPoint, QRectF, QRect, QThread,QString
from PyQt4.QtCore import pyqtSignal, pyqtSlot, QObject, QSize, QByteArray, QEvent, QUrl

from PyQt4.QtGui import QMessageBox, QTextEdit, QDialog, QPolygonF, QPainter, QPen, QColor, QImage
from PyQt4.QtGui import QBrush, QMainWindow, QWidget, QToolTip, QApplication, QFont, QIcon, QAction
from PyQt4.QtGui import QFrame, QListWidget, QComboBox, QCheckBox, QPushButton, QProgressBar, QLineEdit, QLabel
from PyQt4.QtGui import QTextBrowser, QCursor, qApp, QDesktopWidget, QGraphicsView, QGraphicsScene, QPicture
from PyQt4.QtGui import QSplashScreen, QPixmap, QTabWidget, QMovie, QPaintDevice, QSizePolicy

from PyQt4.QtGui import QDoubleValidator, QRadioButton, QButtonGroup, QHBoxLayout, QVBoxLayout
from PyQt4.QtGui import QLCDNumber, QStyleOptionTabWidgetFrame

#from PyQt4 import QtWebKit  
from PyQt4.QtWebKit import QWebView, QWebPage

###################################################################################################
class Browser(QFrame):

    # =======================================================================
    def __init__(self, parent=None, _PARENT=None):

        # -------------------------------------------------------------------
        QFrame.__init__(self, parent);

        _SIZE                               = [3, 5, 975, 585];

        self.setGeometry( _SIZE[0], _SIZE[1], _SIZE[2], _SIZE[3] );
        self.PARENT                         = _PARENT;
        self.CONF                           = _PARENT.CONF;

        self.setStyleSheet( "QFrame{ font: 12px 'monospace'; color: #000; background-color: transparent; background-image: url('./data/imgs/TAB_Browser.png'); }" );

        # -------------------------------------------------------------------
        self.BROWSER                    = QWebView(self);
        self.BROWSER.setGeometry(6, 83, 963, 500);
        self.BROWSER.page().setLinkDelegationPolicy( QWebPage.DelegateAllLinks );
        #self.BROWSER.loadFinished.connect( self.on_loadFinished );

        self.connect( self.BROWSER.page(), SIGNAL('linkClicked (QUrl)'), self.LINK_CLICKED );
        self.connect( self.BROWSER.page(), SIGNAL('loadProgress (int)'), self.PAGE_LOADPROGRESS );
        # void linkHovered (const QString&,const QString&,const QString&)
        self.connect( self.BROWSER.page(), SIGNAL('linkHovered (QString, QString, QString)'), self.LINK_HOVERED );


        #self.BROWSER.load(QUrl.fromUserInput(sys.argv[1]))

        # -------------------------------------------------------------------
        self.HISTORY                        = [];
        # -------------------------------------------------------------------
        # CONTROLS

        # BACK
        self.CONTROL_BACK_BTN               = QPushButton("", self);
        self.CONTROL_BACK_BTN.setGeometry(11, 15, 43, 34);
        self.CONTROL_BACK_BTN.setStyleSheet("QPushButton{ background-color: transparent; border-style: none; }")
        self.connect( self.CONTROL_BACK_BTN, SIGNAL('clicked()') , self.BROWSER.back );

        # STOP
        self.CONTROL_STOP_BTN               = QPushButton("", self);
        self.CONTROL_STOP_BTN.setGeometry(55, 15, 49, 34);
        self.CONTROL_STOP_BTN.setStyleSheet("QPushButton{ background-color: transparent; border-style: none; }")
        self.connect( self.CONTROL_STOP_BTN, SIGNAL('clicked()') , self.BROWSER.stop );

        # RELOAD
        self.CONTROL_RELOAD_BTN             = QPushButton("", self);
        self.CONTROL_RELOAD_BTN.setGeometry(105, 15, 52, 34);
        self.CONTROL_RELOAD_BTN.setStyleSheet("QPushButton{ background-color: transparent; border-style: none; }")
        self.connect( self.CONTROL_RELOAD_BTN, SIGNAL('clicked()') , self.BROWSER.reload );

        # FOREWARDE
        self.CONTROL_FOREWARDE_BTN          = QPushButton("", self);
        self.CONTROL_FOREWARDE_BTN.setGeometry(158, 15, 43, 34);
        self.CONTROL_FOREWARDE_BTN.setStyleSheet("QPushButton{ background-color: transparent; border-style: none; }")
        self.connect( self.CONTROL_FOREWARDE_BTN, SIGNAL('clicked()') , self.BROWSER.forward );
        
        # URL-BAR
        self.URL_BAR                        = QLineEdit("tradingview.com/chart/BNC1/BLX/YFDnalUh-The-Road-to-Obsolescence-A-Seven-Year-Cycle-in-Bitcoin/, https://www.bitstamp.net/, https://blockchain.info/charts/market-cap/", self); 
        self.URL_BAR.setGeometry(6, 55, 950, 27);
        self.URL_BAR.setPlaceholderText("bitstamp.net, blockchain.info/charts/market-cap/");
        self.URL_BAR.setStyleSheet("QLineEdit{ background-color: #222; color: #fff; padding-left: 10px; border-style: none; }");
        self.connect( self.URL_BAR, SIGNAL('returnPressed ()') , self.GO_TO );

        # CALENDER
        self.CONTROL_CALENDER_BTN           = QPushButton("", self);
        self.CONTROL_CALENDER_BTN.setGeometry(769, 15, 43, 34);
        self.CONTROL_CALENDER_BTN.setStyleSheet("QPushButton{ background-color: transparent; border-style: none; }")
        self.connect( self.CONTROL_CALENDER_BTN, SIGNAL('clicked()') , self.GET_CALENDER );

        # BC-E HOME
        self.BTCE_HOME_LNK                  = "https://btc-e.com/exchange/ltc_usd";
        self.CONTROL_BTCE_HOME_BTN          = QPushButton("", self);
        self.CONTROL_BTCE_HOME_BTN.setGeometry(812, 15, 49, 34);
        self.CONTROL_BTCE_HOME_BTN.setStyleSheet("QPushButton{ background-color: transparent; border-style: none; }")
        self.connect( self.CONTROL_BTCE_HOME_BTN, SIGNAL('clicked()') , lambda: self.BROWSER.load( QUrl( self.BTCE_HOME_LNK )) );

        # BLOCKCHAIN
        self.BLOCKCHAIN_LNK                 = "https://blockchain.info/charts/market-cap/?showDataPoints=true&timespan=30days&show_header=false&daysAverageString=7&scale=1&address="; 
        self.CONTROL_BLOCKCHAIN_BTN         = QPushButton("", self);
        self.CONTROL_BLOCKCHAIN_BTN.setGeometry(862, 15, 53, 34);
        self.CONTROL_BLOCKCHAIN_BTN.setStyleSheet("QPushButton{ background-color: transparent; border-style: none; }")
        self.connect( self.CONTROL_BLOCKCHAIN_BTN, SIGNAL('clicked()') , lambda: self.BROWSER.load( QUrl( self.BLOCKCHAIN_LNK )) );

        # GOOGLE
        self.GOOGLE_LNK                     = "https://google.com/";
        self.CONTROL_GOOGLE_BTN             = QPushButton("", self);
        self.CONTROL_GOOGLE_BTN.setGeometry(913, 15, 43, 34);
        self.CONTROL_GOOGLE_BTN.setStyleSheet("QPushButton{ background-color: transparent; border-style: none; }")
        self.connect( self.CONTROL_GOOGLE_BTN, SIGNAL('clicked()') , lambda: self.BROWSER.load( QUrl( self.GOOGLE_LNK )) );


        # STATUS-BAR
        self.STATUS_BAR                      = QLineEdit("status-bar", self); 
        self.STATUS_BAR.setGeometry(6, 585-27, 950, 27);
        self.STATUS_BAR.setStyleSheet("QLineEdit{ background-color: #333; color: #fff; padding-left: 10px; border-style: none; }");
        
        # -------------------------------------------------------------------
        self.setMouseTracking(True);
        
        self.MOUSE_X                        = 0; 
        self.MOUSE_Y                        = 0; 


        #self.load(QUrl('https://www.bitstamp.net/market/tradeview/'))
        #self.load(QUrl('https://www.bitstamp.net/'))
        #self.load(QUrl('https://btc-e.com/'))
        #self.BROWSER.load(QUrl('https://google.com/'))

        # -------------------------------------------------------------------
        self.INTI();
        # -------------------------------------------------------------------
        

    # =======================================================================
    def INTI(self):

        # -------------------------------------------------------------------
        #self.GET_CALENDER();
        pass;
        # -------------------------------------------------------------------


    # =======================================================================
    def PAGE_LOADPROGRESS(self, _int_pr):

        # -------------------------------------------------------------------
        #loadProgress (int)
        #print(_int_pr);
        pass;
        # -------------------------------------------------------------------

    # =======================================================================
    def LINK_HOVERED(self, _link):

        # -------------------------------------------------------------------
        self.STATUS_BAR.setText( _link );
        print(_link);
        # -------------------------------------------------------------------

    # =======================================================================
    def LINK_CLICKED(self, _link):

        # -------------------------------------------------------------------
        _link = str(_link.toString());
        self.HISTORY.append( _link );
        self.URL_BAR.setText( _link );
        # -------------------------------------------------------------------

    # =======================================================================
    def GET_CALENDER(self):

        # -------------------------------------------------------------------
        style = "ecoDayBackground=%23000000&"
        style += "defaultFont=%23333333&";
        style += "innerBorderColor=%2300FF00&";
        style += "borderColor=%23000000&";
        style += "ecoDayFontColor=%23FFFFFF&";

        self.MACRO_CALENDER_DATA = """
            <!DOCTYPE html>
            <html lang="en-US">
            <!-- =============================================================================== -->
            <head>

                <!-- ............................................. -->
                <meta charset="utf-8"/>
                <title>Экономический онлайн-календарь</title>

                <!--
                <link rel="stylesheet" type="text/css" href="css/ids.css">
                <script type="text/javascript" src="js/temax-main.js"></script>
                -->
                <script type="text/javascript">

                    window.addEventListener("load", function(){  

                        //alert("Yes we can");

                    });


                </script>

            </head>
            <!-- =============================================================================== -->
            <body>

                <iframe src="http://ec.ru.forexprostools.com?"""+style+"""columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&features=datepicker,timezone&countries=25,4,17,39,72,26,10,6,37,97,96,43,56,36,5,61,22,12,89,110,35&calType=week&timeZone=58&lang=7" width="943" height="450" frameborder="0" allowtransparency="true" marginwidth="0" marginheight="0"> <a href="http://google.com">GOOGLE</a> </iframe>
                <div class="poweredBy" style="font-family: Arial, Helvetica, sans-serif;">
                    <span style="font-size: 11px;color: #333333;text-decoration: none;">
                        <a href="http://ru.investing.com/" rel="nofollow" target="_blank" style="font-size: 11px;color: #06529D; font-weight: bold;" class="underline_link">Investing.com</a>
                    </span>
                </div>

            </body>
            <!-- =============================================================================== -->
            </html>
        """

        self.BROWSER.setHtml( self.MACRO_CALENDER_DATA );
        # -------------------------------------------------------------------

    # =======================================================================
    def AA(self):

        # -------------------------------------------------------------------
        self.BROWSER.stop();
        self.BROWSER.reload();
        #self.BROWSER.print();

        self.BROWSER.back();
        self.BROWSER.forward();
        #QWebHistory self.BROWSER.history();

        # -------------------------------------------------------------------
        self.BROWSER.history()
        # -------------------------------------------------------------------

    # =======================================================================
    def GO_TO(self):

        # -------------------------------------------------------------------
        self.BROWSER.load(QUrl( str(self.URL_BAR.text()).strip() ));
        self.update();
        # -------------------------------------------------------------------
        #print( self.BROWSER.history() );
        # -------------------------------------------------------------------
    # =======================================================================
    @pyqtSlot(str)  
    def showMessage(self, message):

        # -------------------------------------------------------------------
        print "Message from website:", message
        # -------------------------------------------------------------------

    # =======================================================================
    @pyqtSlot()
    def on_loadFinished(self):

        # -------------------------------------------------------------------
        pass;
        #self.page().mainFrame().evaluateJavaScript(getJsValue) 
        # -------------------------------------------------------------------

    # =======================================================================

###################################################################################################
