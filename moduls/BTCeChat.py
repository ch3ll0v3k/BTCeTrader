#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# BulitIn
import json, sys, time, urllib2
import hashlib

from BeautifulSoup import BeautifulSoup
from random import randint

# PyQt4
from PyQt4.QtGui import QWidget,QToolTip, QFont, QIcon, QAction
from PyQt4.QtGui import QFrame, QListWidget, QListWidgetItem, QComboBox, QCheckBox, QPushButton
from PyQt4.QtGui import QLineEdit, QLabel, QTextEdit, QColor

from PyQt4.QtCore import QTimer, SIGNAL, SLOT, Qt

###################################################################################################
class Chat(QFrame):

    # =======================================================================
    def __init__(self, parent=None, _PARENT=None):

        # -------------------------------------------------------------------
        QFrame.__init__(self, parent);
        # -------------------------------------------------------------------
        self.PARENT                         = _PARENT;
        self.CONF                           = _PARENT.CONF;

        self.setGeometry(3, 5, 975, 548);
        self.setStyleSheet( "QFrame{ font: 12px 'monospace'; color: #000; background-color: transparent; background-image: url('./data/imgs/TAB_Chat.png'); }" );

        # -------------------------------------------------------------------
        self.CHAT_URL                       = "https://btc-e.com/";
        self.CHAT_DATA                      = [];
        self.CHAT_LANG                      = self.CONF["USER"]["CHAT_LANG"];

        self.CHAT_HEADERS = {
            "User-Agent"        : "Mozilla/5.0 (Win-32; rv:24.0) Gecko/20140723 Firefox/24.0 Iceweasel/24.7.0",
            "Accept"            : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language"   : "en-US,en;q=0.5",
            "Referer"           : "https://btc-e.com/",
            "Connection"        : "keep-alive",
            "Cache-Control"     : "max-age=0",
            "Cookie"            : ""
        }

        self.CHAT_TIMER                     = QTimer();
        #self.CHAT_BG_COLOR                  = "#555";
        self.CHAT_BG_COLOR                  = "#0F0";
        self.CHAT_ALLOW_UPD                 = False;
        # -------------------------------------------------------------------
        self.CHAT_WIDGET                    = QTextEdit( self );
        self.CHAT_WIDGET.setGeometry( 13, 116, 690, 388 );
        self.CHAT_WIDGET.setStyleSheet( "QTextEdit{ background-color: transparent; color: #fff; background-image: url(''); }" );
        self.CHAT_WIDGET.setReadOnly( True );

        self.LANG_COMBO                     = QComboBox( self);
        self.LANG_COMBO.setGeometry( 86, 20, 108, 44 ); 
        self.connect( self.LANG_COMBO, SIGNAL('currentIndexChanged(int)'), self.CHANGE_CHAT_LANG );
        self.LANG_COMBO.setEditable(False);
        

        self.NEW_MSG                    = QLineEdit("", self);
        self.NEW_MSG.setGeometry( 20, 510, 500, 30 );
        self.NEW_MSG.setStyleSheet(" QLineEdit{ border-style: none; background-color: #333; color: #fff; background-image: url(''); }");
        self.NEW_MSG.setPlaceholderText(" Enter message:");



        self.SEND                       = QPushButton(" Send", self); 
        self.SEND.setGeometry( 593, 510, 90, 30 );
        #self.SEND.setStyleSheet( "QPushButton{ background-color: transparent; border-style: none; }" ); 
        #self.connect( self.SEND, SIGNAL('clicked()'), lambda: self.SEND_VALUES_TO_TRADE_TERMINAL("SEND_VALUES") );

        # -------------------------------------------------------------------
        self.ALLOW_UPDATE_CHECKBOX        = QCheckBox("", self);
        self.ALLOW_UPDATE_CHECKBOX.setGeometry( 335, 83, 17, 17 );
        self.ALLOW_UPDATE_CHECKBOX.setCheckState(Qt.Unchecked);
        self.connect(self.ALLOW_UPDATE_CHECKBOX, SIGNAL('stateChanged(int)'), self.CHANGE_VALUES );


        self.UPDATE_NOW_BTN               = QPushButton("Update Now!", self);
        self.UPDATE_NOW_BTN.setGeometry( 360, 74, 94, 24 );
        self.connect( self.UPDATE_NOW_BTN, SIGNAL('clicked()'), self.UPDATE_NOW );

        # -------------------------------------------------------------------
        self.INIT();
        # -------------------------------------------------------------------

    # =======================================================================
    def INIT(self):

        # -------------------------------------------------------------------
        try:
            self.INIT_CHAT_COMBO();
            self.UPDATE();

        except Exception as _exception:

            print("-----------------------------------------------------");
            print("[INIT]"+str(_exception));
        # -------------------------------------------------------------------

    # =======================================================================
    def UPDATE_NOW(self):

        # -------------------------------------------------------------------
        self.CHAT_ALLOW_UPD = True;

        self.UPDATE();

        self.CHAT_ALLOW_UPD = False;
        # -------------------------------------------------------------------

    # =======================================================================
    def UPDATE(self):

        # -------------------------------------------------------------------
        #print("UPDATE:")
        # -------------------------------------------------------------------
        try:

            if self.CHAT_ALLOW_UPD:

                self.GET_DATA();
                self.CHAT_WIDGET.clear();

                for msg in self.CHAT_DATA:

                    # ---------------------------------------------------------------
                    """
                    print(msg["time"]);
                    print(msg["nick"]);
                    print(msg["msg"]);
                    """

                    # ---------------------------------------------------------------
                    item = '<p style="background-color: #555;">';                
                    item += "[<span style='color: #000;'>"+msg["time"].split(" ")[1]+"</span>] : ";

                    if msg["nick"] == "admin":
                        item += "[<span style='color: #f00; font-weight: bold;'>"+msg["nick"]+"</span>]<br/><br/>";
                    else:
                        item += "[<span style='color: #000; font-weight: bold;'>"+msg["nick"]+"</span>]<br/><br/>";

                    item += msg["msg"]+"<br/>";
                    item += "</p>";

                    self.CHAT_WIDGET.append(item);


                    # ---------------------------------------------------------------

            self.CHAT_TIMER.singleShot( self.CONF["SYS"]["UPD_DELAY"], self.UPDATE );

        except Exception as e:
            
            print("CHAT[0:0]"+str(e))
            self.CHAT_TIMER.singleShot( self.CONF["SYS"]["UPD_DELAY"], self.UPDATE );

        # -------------------------------------------------------------------

    # =======================================================================
    def CHANGE_VALUES(self):

        # -------------------------------------------------------------------
        if self.ALLOW_UPDATE_CHECKBOX.isChecked():
            self.CHAT_ALLOW_UPD = True;

        else:
            self.CHAT_ALLOW_UPD = False;

        # -------------------------------------------------------------------

    # =======================================================================
    def GET_DATA(self):
        
        # -------------------------------------------------------------------
        try:

            self.CHAT_HEADERS["Cookie"] = "chatRefresh=1; locale="+self.CHAT_LANG+";"

            req = urllib2.Request(self.CHAT_URL, headers=self.CHAT_HEADERS);
            resp = urllib2.urlopen(req).read();

            CHAT = BeautifulSoup( resp ).body.find('div', attrs={'id':'nChat'});

            self.CHAT_DATA = [];

            for data in CHAT:

                self.CHAT_DATA.append( { "msg_id": data["id"], "nick":data.a.string, "time": data.a["title"], "msg": data.span.string } );


        except Exception as e:
            
            print("CHAT[0:1]"+str(e))
        # -------------------------------------------------------------------

    # =======================================================================
    def CHANGE_CHAT_LANG(self):

        # -------------------------------------------------------------------
        self.CHAT_LANG = str(self.LANG_COMBO.currentText()).lower().strip();
        #print(self.CHAT_LANG);
        # -------------------------------------------------------------------

    # =======================================================================
    def INIT_CHAT_COMBO(self):

        # -------------------------------------------------------------------
        for LANG in self.CONF["USER"]["CHAT_LANGS"]:
            self.LANG_COMBO.addItem(LANG.upper());

        for i in xrange(0, self.LANG_COMBO.__len__()):

            self.LANG_COMBO.setItemData( i, QColor("#333"),Qt.BackgroundRole );
            self.LANG_COMBO.setItemData( i, QColor("#fff"),Qt.ForegroundRole );
            #self.LANG_COMBO.setItemData( i, QFont('monospace', 16, -1, False), Qt.FontRole);
        # -------------------------------------------------------------------

    # =======================================================================

###################################################################################################


