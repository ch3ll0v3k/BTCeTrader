#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# BulitIn
import json, sys, time, urllib2

from time import sleep

# PyQt4

from PyQt4.QtCore import QTimer, SIGNAL, SLOT, Qt, QPointF, QPoint, QRectF, QRect
from PyQt4.QtGui import QMessageBox, QTextEdit, QDialog, QPolygonF,QPainter, QPen, QColor 
from PyQt4.QtGui import QBrush, QMainWindow,QWidget,QToolTip,QApplication, QFont,QIcon,QAction
from PyQt4.QtGui import QFrame,QListWidget,QComboBox,QCheckBox,QPushButton,QProgressBar,QLineEdit,QLabel
from PyQt4.QtGui import QTextBrowser, QCursor, qApp, QDesktopWidget, QPixmap
from PyQt4.QtGui import QGraphicsView, QGraphicsScene, QPicture, QPaintDevice, QStaticText

from PyQt4.QtGui import QDoubleValidator, QRadioButton, QButtonGroup, QHBoxLayout, QVBoxLayout



from PyQt4.QtGui import QCursor

###################################################################################################
class PlotterQFrame(QFrame):

    # =======================================================================
    def __init__(self, parent=None, _PARENT=None):

        # -------------------------------------------------------------------
        QFrame.__init__(self, parent);

        _SIZE                               = [8, 276, 618, 301];

        self.setGeometry( _SIZE[0], _SIZE[1], _SIZE[2], _SIZE[3] );
        self.PARENT                         = _PARENT;
        self.CONF                           = _PARENT.CONF;
        # -------------------------------------------------------------------
        self.setMouseTracking(True);
        
        self.MOUSE_X                        = 0; 
        self.MOUSE_Y                        = 0; 
        
        self.MOUSE_STEP_REDUCTION           = True;
        # -------------------------------------------------------------------
        self.GRAPH_W                        = _SIZE[2];
        self.GRAPH_H                        = _SIZE[3];

        self.GRAPH_R_OFFSET                 = 30; # Right padding 
        self.GRAPH_B_OFFSET                 = 30; # Bottom padding for time displaying 

        # -------------------------------------------------------------------
        # CLASSIC CANDLES
        self.CANDLES                        = [];
        self.CANDLES_CLASSIC_DRAW           = True;

        self.CANDLES_MAX_NUM                = 48; # 48 == 24H
        self.CANDLE_W                       = 8.5;
        self.CANDLE_H                       = 8;
        self.CANDLE_G_COLOR                 = QColor( 0,225,0, 255 );
        self.CANDLE_R_COLOR                 = QColor( 225,0,0, 255 );

        # -------------------------------------------------------------------
        # CANDLES-POINTS
        self.CANDLES_POINTS_DRAW            = False;
        self.CANDLES_POINTS_DRAW_ON_TOP     = True;
        self.CANDLES_POINTS_OFFSET          = 0;
        self.CANDLES_POINTS                 = [];
        self.CANDLES_POINT_W                = 8;

        self.TICKS_FOR_ONE_CANDLE           = 120; # 120 == 00:30:00 
        self.IS_GROWING                     = False;
        # demoexchange.btc-e.org:443 30028792 eJ8iNDw1
        # demoexchange.btc-e.org:443
        # -------------------------------------------------------------------
        self.RAW_JSON_DATA                  = []; 
        self.BY_THIS_VALUE                  = "buy"; # Will be changed in he GUI / DONE
        # -------------------------------------------------------------------

        self.DRAW_GRID                      = True;
        self.GRID_SIZE                      = [ 46, 36 ]; # 46 == 12 H-L , 23 == 48 H-L
        self.GRID_LINE_SIZE                 = 1; 
        self.GRID_COLOR                     = QColor( 0,255,0,55 ); #QColor(0,255,0,70);
        self.DRAW_PICK_LINES                = True;

        self.DRAW_CROSS                     = False;
        # -------------------------------------------------------------------
        self.DRAW_MARKT_VOLUME              = False;
        self.MARKT_VOLUME                   = { }; 
        self.MARKT_VOLUME_JSON              = { }; 

        # -------------------------------------------------------------------
        self.DRAW_MIN_MAX_VALUE             = True;

        # -------------------------------------------------------------------
        self.Y_CENTER_OFFSET_SHIFTER_EXPR   = 200;
        self.Y_CENTER_OFFSET                = 50; # from notif
        self.Y_CENTER_OFFSET_SHIFTER        = 30;
        self.Y_CENTER_OFFSET_SHIFTER_STEP   = 2;
        self.X_OFFSET_CANDLE_TO_CANDLE      = 3;
        self.X_OFFSET_GLOBAL_CANDLE         = 0;

        self.Y_ZOOM                         = { 

                                                "btc_eur" : { "markt_volume_mul" : 10, "default" : 10,   "current" : 10,   "step" :  0.1  , "min_zoom" : 2   , "max_zoom" : 25   },
                                                "btc_usd" : { "markt_volume_mul" : 10, "default" : 10,   "current" : 10,   "step" :  0.1  , "min_zoom" : 2   , "max_zoom" : 25   },
                                                "btc_rur" : { "markt_volume_mul" : 1,  "default" : 4,    "current" : 4,    "step" :  0.1  , "min_zoom" : 2   , "max_zoom" : 12   },
                                                "eur_rur" : { "markt_volume_mul" : 1,  "default" : 600,  "current" : 600,  "step" :  10   , "min_zoom" : 120 , "max_zoom" : 120  },
                                                "eur_usd" : { "markt_volume_mul" : 1,  "default" : 4,    "current" : 4,    "step" :  0.1  , "min_zoom" : 120 , "max_zoom" : 120  },
                                                "ltc_btc" : { "markt_volume_mul" : 10, "default" : 4000, "current" : 4000, "step" :  100  , "min_zoom" : 120 , "max_zoom" : 1420 },
                                                "ltc_eur" : { "markt_volume_mul" : 1,  "default" : 600,  "current" : 600,  "step" :  10   , "min_zoom" : 120 , "max_zoom" : 1420 },
                                                "ltc_rur" : { "markt_volume_mul" : 1,  "default" : 80,   "current" : 80,   "step" :  4    , "min_zoom" : 120 , "max_zoom" : 1420 },
                                                "ltc_usd" : { "markt_volume_mul" : 1,  "default" : 800,  "current" : 800,  "step" :  25   , "min_zoom" : 120 , "max_zoom" : 1420 },
                                                "nmc_btc" : { "markt_volume_mul" : 10, "default" : 600,  "current" : 600,  "step" :  10   , "min_zoom" : 120 , "max_zoom" : 120  },
                                                "nmc_usd" : { "markt_volume_mul" : 1,  "default" : 600,  "current" : 600,  "step" :  10   , "min_zoom" : 120 , "max_zoom" : 120  },
                                                "nvc_btc" : { "markt_volume_mul" : 10, "default" : 600,  "current" : 600,  "step" :  10   , "min_zoom" : 120 , "max_zoom" : 120  },
                                                "nvc_usd" : { "markt_volume_mul" : 1,  "default" : 600,  "current" : 600,  "step" :  10   , "min_zoom" : 120 , "max_zoom" : 120  },
                                                "ppc_btc" : { "markt_volume_mul" : 10, "default" : 600,  "current" : 600,  "step" :  10   , "min_zoom" : 120 , "max_zoom" : 120  },
                                                "ppc_usd" : { "markt_volume_mul" : 1,  "default" : 600,  "current" : 600,  "step" :  10   , "min_zoom" : 120 , "max_zoom" : 120  },
                                                "usd_rur" : { "markt_volume_mul" : 1,  "default" : 600,  "current" : 600,  "step" :  10   , "min_zoom" : 120 , "max_zoom" : 120  }

                                            }

        #self.FRAME_GRAPH.Y_ZOOM["btc_usd"]["current"]
        #self.FRAME_GRAPH.Y_ZOOM["btc_usd"]["markt_volume_mul"] 
        #self.FRAME_GRAPH.MARKET_VOLUME_LIMIT = 120;

        # self.Y_ZOOM[ "ltc_usd" ]["deff"]
        # self.Y_ZOOM[ "btc_usd" ]["step"]

        self.P_FONT                         = QFont("monospace", 8);

        # -------------------------------------------------------------------
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Draw Candles or DotLines
        STL_GRAPH_OPTIONS_CANLES_WIDGET = "QWidget{ border-style: solid; border-width: 1px; border-color: #0F0; background-color: #333; color: #fff;  border-bottom-left-radius: 12px; border-bottom-right-radius: 12px; background-image: url('./data/imgs/GRAPH_OPTIONS_CANLES_WIDGET.png'); }";
        STL_RADIO_BUTTON = "QRadioButton{ background-image: url(''); background-color: transparent; border-color: transparent; }";
        STL_GRAPH_OPTIONS_SELL_BUY_WIDGET = "QWidget{ border-style: solid; border-width: 1px; border-color: #0F0; background-color: #333; color: #fff;  border-bottom-left-radius: 12px; border-bottom-right-radius: 12px; background-image: url('./data/imgs/GRAPH_OPTIONS_SELL_BUY_WIDGET.png'); }";
        STL_GRAPH_OPTIONS_DRAW_CROSS_WIDGET = "QWidget{ border-style: solid; border-width: 1px; border-color: #0F0; background-color: #333; color: #fff;  border-bottom-left-radius: 12px; border-bottom-right-radius: 12px; background-image: url('./data/imgs/GRAPH_OPTIONS_CROSS_WIDGET.png'); }";
        STL_CHECK_BOX = "QCheckBox{ background-image: url(''); background-color: transparent; border-color: transparent; }";



        self.GRAPH_OPTIONS_CANLES_WIDGET = QWidget(self);
        self.GRAPH_OPTIONS_CANLES_WIDGET.setGeometry(10, -4, 180, 32);
        self.GRAPH_OPTIONS_CANLES_WIDGET.setStyleSheet( STL_GRAPH_OPTIONS_CANLES_WIDGET );

        self.GRAPH_OPTIONS_CANLES_WIDGET_LAYOUT = QHBoxLayout();

        self.QCHECK_BOX_DRAW_CANDLES = QRadioButton("Cnd.", self);
        self.QCHECK_BOX_DRAW_CANDLES.setChecked( True );
        self.QCHECK_BOX_DRAW_CANDLES.setStyleSheet( STL_RADIO_BUTTON );
        self.GRAPH_OPTIONS_CANLES_WIDGET_LAYOUT.addWidget(self.QCHECK_BOX_DRAW_CANDLES);


        self.QCHECK_BOX_DRAW_CANDLES_POINTS = QRadioButton("Li.", self);
        self.QCHECK_BOX_DRAW_CANDLES_POINTS.setChecked( False );
        self.QCHECK_BOX_DRAW_CANDLES_POINTS.setStyleSheet( STL_RADIO_BUTTON );

        self.GRAPH_OPTIONS_CANLES_WIDGET_LAYOUT.addWidget(self.QCHECK_BOX_DRAW_CANDLES_POINTS);

        self.GRAPH_OPTIONS_CANLES_WIDGET.setLayout(self.GRAPH_OPTIONS_CANLES_WIDGET_LAYOUT);
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # DRAW GRAPH BASED ON BYT OR SELL


        self.GRAPH_OPTIONS_SELL_BUY_WIDGET = QWidget(self);
        self.GRAPH_OPTIONS_SELL_BUY_WIDGET.setGeometry(205, -4, 190, 32);
        self.GRAPH_OPTIONS_SELL_BUY_WIDGET.setStyleSheet( STL_GRAPH_OPTIONS_SELL_BUY_WIDGET );

        self.GRAPH_OPTIONS_SELL_BUY_WIDGET_LAYOUT = QHBoxLayout();

        self.QCHECK_BOX_BUY_CANDLES = QRadioButton("Buy", self);
        self.QCHECK_BOX_BUY_CANDLES.setChecked( True );
        self.QCHECK_BOX_BUY_CANDLES.setStyleSheet( STL_RADIO_BUTTON ); 
        self.GRAPH_OPTIONS_SELL_BUY_WIDGET_LAYOUT.addWidget(self.QCHECK_BOX_BUY_CANDLES);

        self.QCHECK_BOX_SELL_CANDLES = QRadioButton("Sell", self);
        self.QCHECK_BOX_SELL_CANDLES.setChecked( False );
        self.QCHECK_BOX_SELL_CANDLES.setStyleSheet( STL_RADIO_BUTTON );
        self.GRAPH_OPTIONS_SELL_BUY_WIDGET_LAYOUT.addWidget(self.QCHECK_BOX_SELL_CANDLES);

        self.GRAPH_OPTIONS_SELL_BUY_WIDGET.setLayout(self.GRAPH_OPTIONS_SELL_BUY_WIDGET_LAYOUT);
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # DRAW GRAPH CROSS CHECH_BOX


        self.GRAPH_OPTIONS_DRAW_CROSS_WIDGET = QWidget(self);
        self.GRAPH_OPTIONS_DRAW_CROSS_WIDGET.setGeometry(410, -4, 100, 32);
        self.GRAPH_OPTIONS_DRAW_CROSS_WIDGET.setStyleSheet( STL_GRAPH_OPTIONS_DRAW_CROSS_WIDGET );



        self.GRAPH_OPTIONS_DRAW_CROSS_CHECKBOX = QCheckBox("", self.GRAPH_OPTIONS_DRAW_CROSS_WIDGET);
        self.GRAPH_OPTIONS_DRAW_CROSS_CHECKBOX.setGeometry( 20, 10, 17, 17 );
        self.GRAPH_OPTIONS_DRAW_CROSS_CHECKBOX.setCheckState(Qt.Unchecked);
        self.GRAPH_OPTIONS_DRAW_CROSS_CHECKBOX.setStyleSheet( STL_CHECK_BOX );

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # ---------------------------------
        keyboard_sym        = u"⌨";
        start_b_sym         = u"★";
        start_w_sym         = u"☆";
        arrow_up_1_sym      = u"⇪";
        arrow_triangles_sym = u"▲△";
        a = u"⇩"; # d one  
        b = u"⇑";

        # ---------------------------------

        # GRAPH-ZOOM
        self.GRAPH_ZOOM_IN_BTN = QPushButton("&+", self);
        self.GRAPH_ZOOM_IN_BTN.setGeometry(547, 5, 28, 28);
        self.GRAPH_ZOOM_IN_BTN.setShortcut('CTRL++');

        self.GRAPH_ZOOM_OUT_BTN = QPushButton("&-", self);
        self.GRAPH_ZOOM_OUT_BTN.setGeometry(547, 47, 28, 28);
        self.GRAPH_ZOOM_OUT_BTN.setShortcut('CTRL+-');
        #self.GRAPH_ZOOM_OUT_BTN.setStyleSheet("QPushButton{ border-radius: 14px; }");

        # -----------------------------------
        # GRAPH-Y-SHIFTER

        self.GRAPH_UP_SHIFTER_BTN = QPushButton(u"&⇧", self);
        self.GRAPH_UP_SHIFTER_BTN.setGeometry(self.GRAPH_W-26, 5, 22, 32);
        self.GRAPH_UP_SHIFTER_BTN.setShortcut("CTRL+UP");
        self.GRAPH_UP_SHIFTER_BTN.setStyleSheet("QPushButton { font-size: 22px;}");
        #self.GRAPH_UP_SHIFTER_BTN.setEnabled( False );


        self.GRAPH_DOWN_SHIFTER_BTN = QPushButton(u"&⇩", self);
        self.GRAPH_DOWN_SHIFTER_BTN.setGeometry(self.GRAPH_W-26, 264, 22, 32);
        self.GRAPH_DOWN_SHIFTER_BTN.setShortcut("CTRL+DOWN");
        self.GRAPH_DOWN_SHIFTER_BTN.setStyleSheet("QPushButton { font-size: 22px;}");
        #self.GRAPH_DOWN_SHIFTER_BTN.setEnabled( False );

        # -----------------------------------
        # Display this widget if there is no data to PLOTT

        self.GRAPH_OVERLAY_WIDGET = QLabel("Loading ... \n It can take up to 5 minuts by first start!", self);
        self.GRAPH_OVERLAY_WIDGET.setGeometry(0, 0, _SIZE[2], _SIZE[3]);
        self.GRAPH_OVERLAY_WIDGET.setStyleSheet("QLabel{ background-color: #000; font-size: 16px; color: #aaa; }");
        self.GRAPH_OVERLAY_WIDGET.setAlignment( Qt.AlignCenter | Qt.AlignCenter );


        # -----------------------------------
        # GRAPH Floating chars info 
        self.MAX_VALUE_LABLE                = QLabel("", self);
        self.MAX_VALUE_LABLE.setStyleSheet("QLabel{ font: 12px 'monospace'; background-color: transparent; color: #FFF; }");
        self.MAX_VALUE_LABLE.setGeometry(0, 0, 100, 30);

        self.MIN_VALUE_LABLE                = QLabel("", self);
        self.MIN_VALUE_LABLE.setStyleSheet("QLabel{ font: 12px 'monospace'; background-color: transparent; color: #FFF; }");
        self.MIN_VALUE_LABLE.setGeometry(0, 0, 100, 30);

        self.CURR_VALUE_ARROW               = QLabel("", self);
        self.CURR_VALUE_ARROW.setStyleSheet("QLabel{ background-color: transparent; background-image: url('./data/imgs/arrow_curr_pos.png'); }");
        self.CURR_VALUE_ARROW.setGeometry( self.GRAPH_W - self.GRAPH_R_OFFSET, self.Y_CENTER_OFFSET-10, 21, 11);

        # -------------------------------------------------------------------
        self.PREV_CANDLE_EXIT_VALUE         = 0;
        self.MAX_VALUE                      = 0;
        self.MIN_VALUE                      = 99999;
        self.CURRENT_LAST_VALUE             = 0;

        self.UPDATE_RUNNING                 = False; 

        self.MAX_GLOBAL_VALUE               = 0;
        self.MIN_GLOBAL_VALUE               = 99999;

        # -------------------------------------------------------------------
        self.enter_val                      = 0;
        self.exit_val                       = 0;
        self.max_val                        = 0;
        self.min_val                        = 0;
        self.THIS_DATA                      = 0; #Will be ltc_usd, btc_usd, etc ...

        # -------------------------------------------------------------------
        self.FOUND_Y_OFFSET                 = False;
        self.CURRENT_Y_OFFSET               = 0;
        self.RESET_GLOBAL_VALUES            = False;

        # -------------------------------------------------------------------
        self.ONE_HOUR                       = 3600;

        # -------------------------------------------------------------------
        self.MOUSE_TRACKER_LABEL            = QLabel("", self);
        self.MOUSE_TRACKER_LABEL.setStyleSheet("QLabel{ font: 12px 'monospace'; background-color: rbga(51,51,51, 200); color: #fff; border-style: solid; border-width: 1px; border-color: #FFF; border-radius: 0px; }");

        self.PRICE_LABEL_W                  = 240;
        self.PRICE_LABEL_OFFSET             = 30;
        # -------------------------------------------------------------------
        self.JSON_GRAPH_LIMIT               = self.CANDLES_MAX_NUM * self.TICKS_FOR_ONE_CANDLE; # 120*48 == 5640

        self._LIMIT_                        = self.JSON_GRAPH_LIMIT - self.TICKS_FOR_ONE_CANDLE;
        # -------------------------------------------------------------------
        #self.TAKE_SCREENSHOT();
        # -------------------------------------------------------------------
        # indicators: FIBO

        self.FIBO_START                     = { "x":0, "y":0};
        self.FIBO_END                       = { "x":0, "y":0};
        self.FIBO_ENDET                     = False;
        self.FIBO_STARTED                   = False;
        self.FIBO_LINE_MEMORY               = [];
        self.FIBO_ALLOW                     = True;
        self.FIBO_LINE_L                    = 145;
        # -------------------------------------------------------------------


    # =======================================================================
    def TAKE_SCREENSHOT(self):


        # -------------------------------------------------------------------
        try:

            t = time.gmtime()
            PATH = self.CONF["USER"]["DIR"]+self.CONF["USER"]["SCR"];
            NAME = str(self.PARENT.Request.NONCE)+"|{0}.{1}.{2}-{3}:{4}.png".format(t.tm_mday, t.tm_mon, t.tm_year, t.tm_hour, t.tm_min);


            self.PARENT.LOG["notif"].append(" New screenshot saved:<br/>"+NAME);

            SCR = QPixmap.grabWidget( self, 0, 0, 618, 301);
            SCR.save( PATH+NAME, format="png", quality=100);

        except Exception as _exception:

            print(_exception);
        # -------------------------------------------------------------------

    # =======================================================================
    def CLEAN_META_DB(self):

        # -------------------------------------------------------------------
        try:

            self.TAKE_SCREENSHOT();

            t = time.gmtime()

            self.TIME = str(t.tm_hour)+":"+str(t.tm_min)+":"+str(t.tm_sec);

            self.PARENT.LOG["notif"].append(" DROP TABLE: @ "+self.TIME );

            self._LIMIT_ = self.JSON_GRAPH_LIMIT - (self.TICKS_FOR_ONE_CANDLE*2);

            _SQL_A = "SELECT updated, json FROM "+self.PARENT.CURR_PAIR+" order by updated DESC LIMIT "+str(self._LIMIT_);
            self.tmp_data = self.PARENT.DB.FETCH("META_DB",_SQL_A, ALL=True);

            _THIS_LIMIT_ = self.tmp_data[ len(self.tmp_data)-1 ][0];

            # TODO:
            # OR PASSING _THIS_LIMIT_ from self.PARENT.UPDATE_METADATA();

            _SQL_B = "DELETE FROM "+self.PARENT.CURR_PAIR+" WHERE updated < "+str( _THIS_LIMIT_ );
            self.PARENT.DB.EXEC("META_DB", _SQL_B);

            _SQL_C = "SELECT json from "+self.PARENT.CURR_PAIR+" order by updated ASC";
            self.RAW_JSON_DATA = self.PARENT.DB.FETCH("META_DB", _SQL_C, ALL=True);


        except Exception as _exception:
            print(_exception);
        # -------------------------------------------------------------------

    # =======================================================================
    def mousePressEvent(self, event):

        # -------------------------------------------------------------------
        if event.button() == 4: # 1 == left, 2 == right, 4 == middle
            return;
        

        self.FIBO_ALLOW = True;

        self.FIBO_START["x"] = event.x();
        self.FIBO_START["y"] = event.y();

        self.FIBO_STARTED = True;
        self.FIBO_ENDET = False;
        # -------------------------------------------------------------------

    # =======================================================================
    def mouseReleaseEvent(self, event):

        # -------------------------------------------------------------------
        if event.button() == 4: # 1 == left, 2 == right, 4 == middle

            self.FIBO_ALLOW = False;
            
            #self.FIBO_START = { "x":0, "y":0};
            #self.FIBO_END = { "x":0, "y":0};

            #self.FIBO_ENDET = False;
            #self.FIBO_STARTED = False;

            self.FIBO_LINE_MEMORY = [];

        self.FIBO_END["x"] = event.x();
        self.FIBO_END["y"] = event.y();
        # -------------------------------------------------------------------

        self.FIBO_STARTED = False;
        self.FIBO_ENDET = True;

        #self.LINE_MEMORY.append( [QPoint(self.START["x"],self.START["y"]), QPoint(self.END["x"],self.END["y"])] );
        self.FIBO_LINE_MEMORY.append( [self.FIBO_START["x"],self.FIBO_START["y"], self.FIBO_END["x"],self.FIBO_END["y"] ] );

        #self.START = { "x":0, "y":0};
        #self.END = { "x":0, "y":0};

        # -------------------------------------------------------------------

    # =======================================================================
    def mouseMoveEvent(self, event):
    
        # -------------------------------------------------------------------
        #event.globalPos();
        # event.x(), " -> ", event.y() | event.pos() | event.posF() |

        if self.FIBO_STARTED and not self.FIBO_ENDET:
            self.FIBO_END["x"] = event.x();
            self.FIBO_END["y"] = event.y();

        # -------------------------------------------------------------------
        if self.MOUSE_STEP_REDUCTION:
            self.MOUSE_STEP_REDUCTION = not self.MOUSE_STEP_REDUCTION;
            return;

        else:
            self.MOUSE_STEP_REDUCTION = not self.MOUSE_STEP_REDUCTION;

            self.MOUSE_X = event.x()
            self.MOUSE_Y = event.y();


            self.MOUSE_TRACKER_LABEL.hide();

            for x_offset, y_enter, y_exit, max_val, min_val, is_growing, enter_max, exit_max, max_v, min_v, _upd in self.CANDLES:

                # Mouse X-Pos -> Is in the candle
                if self.MOUSE_X >= x_offset and self.MOUSE_X <= x_offset+self.CANDLE_W:
                    
                    # REVENCED VALUES (if X more y_exit and less y_enter)
                    # Mouse X-Pos -> Is in the candle
                    if self.MOUSE_Y >= y_exit and self.MOUSE_Y <= y_enter or self.MOUSE_Y <= y_exit and self.MOUSE_Y >= y_enter:

                        self.MOUSE_TRACKER_LABEL.show();

                        if (self.MOUSE_X +self.PRICE_LABEL_OFFSET+ self.PRICE_LABEL_W) > self.GRAPH_W:
                            self.MOUSE_TRACKER_LABEL.setGeometry(self.MOUSE_X-self.PRICE_LABEL_OFFSET-self.PRICE_LABEL_W, self.MOUSE_Y-65, self.PRICE_LABEL_W, 40);

                        else: 
                            self.MOUSE_TRACKER_LABEL.setGeometry(self.MOUSE_X+self.PRICE_LABEL_OFFSET, self.MOUSE_Y-65, self.PRICE_LABEL_W, 40);

                        #UPD = time.strftime("%H:%M:%S", time.localtime(int(_upd)));
                        #self.MOUSE_TRACKER_LABEL.setText( "UPD: "+UPD+"\n En: "+str(enter_max)+" - Ex: "+str(exit_max)+"\n Min: "+str(min_v)+" - Max: "+str(max_v) );
                        
                        self.MOUSE_TRACKER_LABEL.setText( "En: "+str(enter_max)+" - Ex: "+str(exit_max)+"\n Min: "+str(min_v)+" - Max: "+str(max_v) );
                        break;

            self.update();
        # -------------------------------------------------------------------


    # =======================================================================
    def poly(self, _pts):
        
        # -------------------------------------------------------------------
        """ Clean up if needet
        for x in xrange(0, len(_pts)):
            if self._CANDELS[x][0] == None:
                self._CANDELS[x][0] = 0;
            if self._CANDELS[x][1] == None:
                self._CANDELS[x][1] = 0;
        """

        return QPolygonF(map(lambda p: QPointF(*p), _pts))
        # -------------------------------------------------------------------
    
    # =======================================================================
    def paintEvent(self, event):

        # -------------------------------------------------------------------
        #print("UPDATE: "+str(time.time()));
        # -------------------------------------------------------------------
        self.UPDATE_DATA();

        Painter = QPainter()
        Painter.begin(self)
        Painter.setFont(self.P_FONT);

        # -------------------------------------------------------------------
        if self.FIBO_ALLOW:

            A = 8;

            S_X = self.FIBO_START["x"];
            S_Y = self.FIBO_START["y"];
            E_X = self.FIBO_END["x"];
            E_Y = self.FIBO_END["y"];

            EX_SX = (E_X - S_X);
            EY_SY = (E_Y - S_Y);

            Painter.setBrush(QBrush(QColor(255, 255, 255))) # color
            Painter.setPen(QPen(QColor("#F00"), 1)) # circle border diameter

            Painter.drawEllipse(QRectF( S_X-(A/2), S_Y-(A/2), A, A ));
            Painter.drawPolyline( QPoint(S_X,S_Y), QPoint(E_X,E_Y) ); 
            Painter.drawPolyline( QPoint( S_X, S_Y ), QPoint( S_X-(E_X-S_X), S_Y-(E_Y-S_Y) ) ); 

            """ +150% """
            _50_X =  S_X - EX_SX/2;
            _50_Y =  S_Y - EY_SY/2;

            Painter.setPen(QPen(QColor("#FF0"), 1)) # circle border diameter
            Painter.drawPolyline( QPoint( _50_X, _50_Y ), QPoint( _50_X+self.FIBO_LINE_L, _50_Y ) ); 
            Painter.drawStaticText(QPointF( self.GRAPH_W-30, _50_Y), QStaticText('150%') );

            """ +138.2% """
            _50_X =  S_X - EX_SX*38.2/100;
            _50_Y =  S_Y - EY_SY*38.2/100;

            Painter.setPen(QPen(QColor("#FF0"), 1)) # circle border diameter
            Painter.drawPolyline( QPoint( _50_X, _50_Y ), QPoint( _50_X+self.FIBO_LINE_L, _50_Y ) ); 
            Painter.drawStaticText(QPointF( self.GRAPH_W-30, _50_Y), QStaticText('138.2%') );
            
            """ 100 % """
            Painter.setPen(QPen(QColor("#f00"), 1)) # circle border diameter
            Painter.drawPolyline( QPoint( S_X, S_Y ), QPoint( S_X+self.FIBO_LINE_L, S_Y ) ); 
            Painter.drawStaticText(QPointF( self.GRAPH_W-30, S_Y), QStaticText('100%') );

            """ +61.8% """
            _50_X =  S_X + EX_SX*38.2/100;
            _50_Y =  S_Y + EY_SY*38.2/100;

            Painter.setPen(QPen(QColor("#0ff"), 1)) # circle border diameter
            Painter.drawPolyline( QPoint( _50_X, _50_Y ), QPoint( _50_X+self.FIBO_LINE_L, _50_Y ) ); 
            Painter.drawStaticText(QPointF( self.GRAPH_W-30, _50_Y), QStaticText('61.8%') );

            """ +50% """
            _50_X =  S_X + EX_SX/2;
            _50_Y =  S_Y + EY_SY/2;

            Painter.setPen(QPen(QColor("#00f"), 1)) # circle border diameter
            Painter.drawPolyline( QPoint( _50_X, _50_Y ), QPoint( _50_X+self.FIBO_LINE_L, _50_Y ) ); 
            #Painter.drawStaticText(QPointF( self.GRAPH_W-30, _50_Y), QStaticText('50%') );

            """ +32.8% """

            _50_X =  S_X + EX_SX*61.8/100;
            _50_Y =  S_Y + EY_SY*61.8/100; 

            Painter.setPen(QPen(QColor("#0F0"), 1)) # circle border diameter
            Painter.drawPolyline( QPoint( _50_X, _50_Y ), QPoint( _50_X+self.FIBO_LINE_L, _50_Y ) ); 
            Painter.drawStaticText(QPointF( self.GRAPH_W-30, _50_Y), QStaticText('32.8%') );

            """ +0 % """
            Painter.setPen(QPen(QColor("#fff"), 1)) # circle border diameter
            Painter.drawPolyline( QPoint( E_X,E_Y ), QPoint( E_X+self.FIBO_LINE_L, E_Y ) ); 
            Painter.drawStaticText(QPointF( self.GRAPH_W-30, E_Y), QStaticText('0%') );

            """ -32.8 % 

            _50_X =  S_X + EX_SX*32.8/100;
            _50_Y =  S_Y + EY_SY*32.8/100; 

            Painter.setPen(QPen(QColor("#F00"), 1)) # circle border diameter
            Painter.drawPolyline( QPoint( E_X,E_Y ), QPoint( E_X+self.FIBO_LINE_L, E_Y ) ); 
            Painter.drawStaticText(QPointF( self.GRAPH_W-30, E_Y), QStaticText('-32.8%') );

            """

            """ " "" 
            for S_X, S_Y, E_X, E_Y in self.LINE_MEMORY:

                Painter.drawEllipse(QRectF( S_X-(A/2), S_Y-(A/2), A, A ));
                Painter.drawPolyline( QPoint(S_X,S_Y), QPoint(E_X,E_Y) ); 
                Painter.drawPolyline( QPoint( S_X, S_Y ), QPoint( S_X-(E_X-S_X)*2, S_Y-(E_Y-S_Y)*2 ) ); 
            "" " """ 

        # -------------------------------------------------------------------
        # Draw CROSS-MOUSE-POS
        if self.DRAW_CROSS:

            Painter.setPen( QPen( QColor(255,255,255, 255), 1, Qt.DashLine ) );
            Painter.drawPolyline( QPoint(self.MOUSE_X-600, self.MOUSE_Y), QPoint( self.MOUSE_X+600, self.MOUSE_Y) ); 
            Painter.drawPolyline( QPoint(self.MOUSE_X, self.MOUSE_Y-400), QPoint( self.MOUSE_X, self.MOUSE_Y+400) ); 

        # -------------------------------------------------------------------
        # Draw Grid & Time line

        if self.DRAW_GRID:
                        
            # ----------- draw VERTICAL grid lines ------------
            cur_x_pos = self.CANDLE_W+self.CANDLE_W;

            _time = int(str(time.time()).split(".")[0])-3600;

            _c = 16;

            try:

                while cur_x_pos < self.GRAPH_W-self.GRAPH_R_OFFSET: # right offset 30 px
                    
                    Painter.setPen(QPen(self.GRID_COLOR, self.GRID_LINE_SIZE));
                    #Painter.setPen(QPen( QColor(255,0,0), self.GRID_LINE_SIZE));
                    Painter.drawPolyline( QPoint(cur_x_pos, 0), QPoint(cur_x_pos, self.GRAPH_H-self.GRAPH_B_OFFSET)); 

                    # -----------------------------------------
                    # Hours
                    #_time = 14400;
                    
                    TT = _time-(7200*_c);

                    Painter.setPen(QPen( QColor("#F00"), 1 ));
                    Painter.drawStaticText(QPointF( cur_x_pos, self.GRAPH_H-self.GRAPH_B_OFFSET+4), QStaticText("|"+time.strftime("%H:%M", time.localtime( TT ))));
                    
                    _c -= 1;
                    # -----------------------------------------

                    cur_x_pos += self.GRID_SIZE[0];

            except Exception as _exception:
                print("2: "+str(_exception));


            # ----------- draw HORIZONTAL grid lines ------------
            try:

                cur_y_pos = self.GRID_SIZE[1];
                #Painter.setPen( QPen(self.GRID_COLOR, self.GRID_LINE_SIZE));
                qPen = QPen(QColor( 255,255,255, 30), 1, Qt.CustomDashLine );
                qPen.setDashPattern( [5, 8, 5, 8] )
                #qPen.setCosmetic(True);

                Painter.setPen( qPen );

                while cur_y_pos < self.GRAPH_H-self.GRAPH_B_OFFSET:
                
                    Painter.drawPolyline( QPoint(0, cur_y_pos), QPoint(self.GRAPH_W-self.GRAPH_R_OFFSET, cur_y_pos)); 
                    cur_y_pos += self.GRID_SIZE[1];

            except Exception as _exception:
                print("3: "+str(_exception));

            # ----------- draw RED SAMI/FRAME  ------------
            # DRAW RED BOTTOM & RIGHT SEPARETEN LINE

            Painter.setPen(QPen(QColor("#F00"), 2));
            Painter.drawPolyline( QPoint(0, self.GRAPH_H-self.GRAPH_B_OFFSET), QPoint(self.GRAPH_W-self.GRAPH_R_OFFSET, self.GRAPH_H-self.GRAPH_B_OFFSET)); 
            Painter.drawPolyline( QPoint(self.GRAPH_W-self.GRAPH_R_OFFSET, 0), QPoint(self.GRAPH_W-self.GRAPH_R_OFFSET, self.GRAPH_H-self.GRAPH_B_OFFSET)); 

        # -------------------------------------------------------------------        
        if self.DRAW_MIN_MAX_VALUE:
            try:

                # INIT CUSTOM PEN
                qPen = QPen( QColor(0,255,0, 225), 1, Qt.CustomDashLine );
                qPen.setDashPattern( [5, 8, 5, 8] )

                # MAX_VALUE
                Painter.setPen( qPen );
                Painter.drawPolyline( QPoint(0, self.GRAPH_H-int(self.MAX_VALUE)), QPoint(self.GRAPH_W, self.GRAPH_H-int(self.MAX_VALUE)) ); 

                # MIN_VALUE
                qPen.setColor( QColor(255,0,0, 225) );
                Painter.setPen( qPen );
                Painter.drawPolyline( QPoint(0, self.GRAPH_H-int(self.MIN_VALUE)), QPoint(self.GRAPH_W, self.GRAPH_H-int(self.MIN_VALUE)) ); 

                # CURR VALUE
                qPen.setColor( QColor(0,0,255, 225) );
                Painter.setPen( qPen );
                Painter.drawPolyline( QPoint(0, self.GRAPH_H-int(self.CURRENT_LAST_VALUE)), QPoint(self.GRAPH_W, self.GRAPH_H-int(self.CURRENT_LAST_VALUE)) ); 

                self.CURR_VALUE_ARROW.setGeometry( self.GRAPH_W - self.GRAPH_R_OFFSET, self.GRAPH_H-int(self.CURRENT_LAST_VALUE)-10, 11, 21);

            except Exception as _exception:
                print("4: "+str(_exception));
                # DRAW CURRENT LAST

        # -------------------------------------------------------------------
        if self.CANDLES_POINTS_DRAW:
            if self.CANDLES_POINTS_DRAW_ON_TOP:
                if self.CANDLES_CLASSIC_DRAW:
                    self.DRAW_CLASSIC_CANDLES(Painter);
        
                self.DRAW_CLASSIC_POINTS(Painter);
        
            else:

                self.DRAW_CLASSIC_CANDLES(Painter);

                if self.CANDLES_CLASSIC_DRAW:
                    self.DRAW_CLASSIC_CANDLES(Painter);
        
        elif self.CANDLES_CLASSIC_DRAW:
            
            self.DRAW_CLASSIC_CANDLES(Painter);

        # -------------------------------------------------------------------
        #print(self.MARKT_VOLUME_JSON);
        if self.DRAW_MARKT_VOLUME and self.PARENT.CURR_PAIR in self.MARKT_VOLUME_JSON:

            self.GET_MARKT_VOLUME( Painter );
        # -------------------------------------------------------------------
        Painter.end();
        # -------------------------------------------------------------------

    # =======================================================================
    def GET_MARKT_VOLUME(self, Painter):

        # -------------------------------------------------------------------
        #print("ENTER MARKT_VOLUME")
        # ----------------------------------------------------
        self.MARKT_VOLUME = {

            "ask" : [],
            "bid" : []

        };

        STEP = 0.01;

        # ----------------------------------------------------
        for pair in self.MARKT_VOLUME_JSON:

            # ---------------------------------------------------------------------------
            # ASKS

            skip_fs_step = True;
            curr_buy_index = 0;

            AX = str(self.MARKT_VOLUME_JSON[ pair ]["asks"][0][0]).split(".");
            SEARCH = float("{:.2f}".format( float(AX[0]+"."+AX[1][0:2]) ));
            self.MARKT_VOLUME["ask"].append( [ SEARCH, self.MARKT_VOLUME_JSON[ pair ]["asks"][0][1] ] );

            for i in xrange( 0, len(self.MARKT_VOLUME_JSON[ pair ]["asks"]) ):

                if skip_fs_step:
                    skip_fs_step = False;
                    continue;

                if float("{:.2f}".format( SEARCH + STEP )) < self.MARKT_VOLUME_JSON[ pair ]["asks"][i][0]:

                    SEARCH = float("{:.2f}".format( SEARCH + STEP ));

                    self.MARKT_VOLUME["ask"].append( [ SEARCH, self.MARKT_VOLUME_JSON[ pair ]["asks"][i][1] ] );
                    curr_buy_index += 1;

                else:

                    self.MARKT_VOLUME["ask"][ curr_buy_index ][1] += self.MARKT_VOLUME_JSON[ pair ]["asks"][i][1];

            # ---------------------------------------------------------------------------
            # BID

            skip_fs_step = True;
            curr_sell_index = 0;

            SEARCH = float("{:.2f}".format( self.MARKT_VOLUME_JSON[ pair ]["bids"][0][0]  ));
            self.MARKT_VOLUME["bid"].append( [ SEARCH, self.MARKT_VOLUME_JSON[ pair ]["bids"][0][1] ] );

            for i in xrange( 0, len(self.MARKT_VOLUME_JSON[ pair ]["bids"]) ):

                if skip_fs_step:
                    skip_fs_step = False;
                    continue;

                if float("{:.2f}".format( SEARCH-STEP)) > self.MARKT_VOLUME_JSON[ pair ]["bids"][i][0]:

                    SEARCH = float("{:.2f}".format( SEARCH - STEP ));

                    self.MARKT_VOLUME["bid"].append( [ SEARCH, self.MARKT_VOLUME_JSON[ pair ]["bids"][i][1] ] );
                    curr_sell_index += 1;

                else:

                    self.MARKT_VOLUME["bid"][ curr_sell_index ][1] += self.MARKT_VOLUME_JSON[ pair ]["bids"][i][1];




        # ----------------------------------------------------
        # DRAW MARKET VOLUME 
        _DEVIDER = 100;


        ST = 2500;
        MAX = 0;

        shifter = True;

        while MAX < 25000:

            if MAX == 0:
                MAX += ST;
                continue;

            X_P = MAX/_DEVIDER;



            if shifter:
                shifter = False;
                
                Painter.setPen( QPen(QColor(255,0,0, 225), 1));
                Painter.drawPolyline( QPoint( X_P, 37), QPoint( X_P, 43) );

                Painter.setPen( QPen(QColor(0,255,0, 225), 1));
                Painter.drawStaticText(QPointF( X_P+2, 35), QStaticText( "{:.2f}k".format(X_P/10) ));
            else:
                shifter = True;

                Painter.setPen( QPen(QColor(255,0,0, 225), 1));
                Painter.drawPolyline( QPoint( X_P, 47), QPoint( X_P, 53) );

                Painter.setPen( QPen(QColor(0,255,0, 225), 1));
                Painter.drawStaticText(QPointF( X_P+2, 45), QStaticText( "{:.2f}k".format(X_P/10) ));
            MAX += ST;

        # ----------------------------------------------------
        # ASK == PRICE_TO_BUY

        # TODO: DF must be calculated on the fly foreach currency 
        DF = 8;

        alpha_c = 180; 



        MUL = self.Y_ZOOM[ self.PARENT.CURR_PAIR ]["markt_volume_mul"];


        Painter.setBrush(QBrush( QColor(0,255,0,alpha_c) ));
        Painter.setPen(QPen( QColor(255,255,255,alpha_c), 1));

        for _vol_ in reversed(self.MARKT_VOLUME["ask"]):

            _V_ = self._GET_CONST_OFFSET(_vol_[0]);
            Painter.drawRect(0, self.GRAPH_H - _V_-DF-8 , _vol_[1]/_DEVIDER * MUL, DF);

        # ----------------------------------------------------
        #DF = (self.GRAPH_H - self._GET_CONST_OFFSET(self.MARKT_VOLUME["bid"][ len(self.MARKT_VOLUME["bid"])-1 ][0])) - (self.GRAPH_H - self.CURRENT_LAST_VALUE);
        #DF /= len(self.MARKT_VOLUME["bid"][0])
        #DF *= 0.8;


        Painter.setBrush(QBrush( QColor(255,0,0,alpha_c) ));
        Painter.setPen(QPen( QColor(255,255,255,alpha_c), 1));

        for _vol_ in self.MARKT_VOLUME["bid"]:
            _V_ = self._GET_CONST_OFFSET(_vol_[0]);
            Painter.drawRect(0, self.GRAPH_H - _V_ -DF, _vol_[1]/_DEVIDER * MUL, DF);
        # ----------------------------------------------------
        #self.MARKT_VOLUME_JSON = {};
        # ----------------------------------------------------

        # -------------------------------------------------------------------

    # =======================================================================
    def DRAW_CLASSIC_POINTS(self, Painter):

        # -------------------------------------------------------------------
        Painter.setPen( QPen( QColor("#FFF"), 2 ) );
        Painter.drawPolyline( self.poly( self.CANDLES_POINTS ) );

        Painter.setBrush(QBrush(QColor(255, 255, 255))) # color
        Painter.setPen(QPen(QColor("#F00"), 2)) # circle border diameter

        p = self.CANDLES_POINT_W;

        for x, y in self.CANDLES_POINTS:
            Painter.drawEllipse(QRectF(x - p/2, y - p/2, p, p));

        # -------------------------------------------------------------------

    # =======================================================================
    def DRAW_CLASSIC_CANDLES(self, Painter):

        # -------------------------------------------------------------------
        # CLASSIC CANDLES

        #Painter.setPen(QPen(QColor("#FFF"), 1, Qt.NoPen));
        Painter.setPen(QPen(QColor("#FFF"), 1));

        for x_offset, y_enter, y_exit, max_val, min_val, is_growing, e_1, e_2, e_3, e_4, _upd in self.CANDLES:

            try:
                
                # -------------------------------------------------------
                # LINES -> drawPolyline == from_x, from_y, to_x, to_y
                if self.DRAW_PICK_LINES:
                    Painter.drawPolyline( QPoint(x_offset+self.CANDLE_W/2, min_val), QPoint(x_offset+self.CANDLE_W/2, max_val) );

                # -------------------------------------------------------                    
                # CANDLES -> drawRect == from_x, from_y, length_x, length_y
                #Painter.setPen(QPen(QColor("#444"), 0));

                if is_growing:
                    Painter.setBrush( QBrush(self.CANDLE_G_COLOR) );
                else:
                    Painter.setBrush( QBrush(self.CANDLE_R_COLOR) );

                Painter.drawRect( x_offset, y_enter, self.CANDLE_W, y_exit-y_enter );

                # -------------------------------------------------------                    

            except Exception as _NoneTypeError:
                
                print(_NoneTypeError)
                print("x: "+str(x_offset)+" y: "+str(y_enter))
                Painter.end()
                exit();

        # -------------------------------------------------------------------

    # =======================================================================
    def _GET_CONST_OFFSET(self, _VAL):

        # -------------------------------------------------------------------
        #self.PARENT.LOG["info"].append(" _GET_CONST_OFFSET();");
        # -------------------------------------------------------------------
        # Search for correct Y offset to match viewport by data

        _curr_ = self.PARENT.CURR_PAIR;


        if not self.FOUND_Y_OFFSET:
            
            _SEARCH_STEP = 10;
            _VAL *= self.Y_ZOOM[ _curr_ ]["current"];

            T_H = self.GRAPH_H - self.Y_CENTER_OFFSET

            if _VAL > T_H+_SEARCH_STEP:
                
                while _VAL > T_H+_SEARCH_STEP:
                    self.CURRENT_Y_OFFSET += _SEARCH_STEP;
                    _VAL -= _SEARCH_STEP;

                self.FOUND_Y_OFFSET = True;

            elif _VAL < T_H-_SEARCH_STEP:
                while _VAL < T_H-_SEARCH_STEP:
                    self.CURRENT_Y_OFFSET -= _SEARCH_STEP;
                    _VAL += _SEARCH_STEP;
                self.FOUND_Y_OFFSET = True;

            # ---------------------------------------------------
            # return correct Y-OFFSET Value 
            _VAL = 90;
            _ret_val = (_VAL * self.Y_ZOOM[ _curr_ ]["current"]) - self.CURRENT_Y_OFFSET;

            if _ret_val is not None and _ret_val > 0:
                return _ret_val;
            else:
                return self.GRAPH_H / 2 - 50;
            # ---------------------------------------------------

        else:
            
            _ret_val = (_VAL * self.Y_ZOOM[ _curr_ ]["current"]) - self.CURRENT_Y_OFFSET;

            if _ret_val is not None and _ret_val > 0:
                return _ret_val;
            else:
                return self.GRAPH_H / 2 - 50;
        # -------------------------------------------------------------------

    # =======================================================================
    def UPDATE_DATA(self):
        
        # -------------------------------------------------------------------   
        if self.UPDATE_RUNNING:
            return;

        self.UPDATE_RUNNING = True;

        # -------------------------------------------------------------------
        self._LIMIT_ = self.JSON_GRAPH_LIMIT - self.TICKS_FOR_ONE_CANDLE;

        if len(self.RAW_JSON_DATA) >= self._LIMIT_:
            self.CLEAN_META_DB();

        else:
            pass;
            #self.PARENT.LOG["notif"].append("G_LIM: "+str(self.JSON_GRAPH_LIMIT)+" AVAIL: "+str(len(self.RAW_JSON_DATA))+" D_LIM: "+str(self._LIMIT_));

        # -------------------------------------------------------------------   
        self.CANDLES = [];

        self.FOUND_Y_OFFSET = False;
        self.CURRENT_Y_OFFSET = 0;
        self.X_OFFSET_GLOBAL_CANDLE = self.CANDLE_W+(self.CANDLE_W/2);

        self.MAX_GLOBAL_VALUE = 0;
        self.MIN_GLOBAL_VALUE = 99999;

        self.ENTER_VALUE = 0;
        self.MIN_VALUE   = 999999;
        self.MAX_VALUE   = 0;
        self.EXIT_VALUE  = 0;

        ITERATION_COUNTER = 1;

        self.MIN_MAX_VALUES_FOUND    = False;
        self.IS_CANDLE_COMPLITED     = False;
        self.HAS_AT_LEAST_ONE_CANDLE = False;

        self.CANDLES_POINTS = [];

        for JSON_LINE in self.RAW_JSON_DATA:

            # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            # All what we need is { "updated" : val, "buy" : val, "sell" : val }
            # Maybe more in the future ???

            JSD = json.loads( JSON_LINE[0] );
            self.THIS_DATA = JSD[ self.BY_THIS_VALUE ]; #  >>>> ["buy"];

            # -----------------------------------------------------
            # BEGIN CANDLE DATA COLLECTION
            if ITERATION_COUNTER == 1:
    
                UPDATED = JSD["updated"];
                self.ENTER_VALUE = self.THIS_DATA;    
                self.MAX_VALUE = self.THIS_DATA;
                self.MIN_VALUE = self.THIS_DATA;

                self.IS_CANDLE_COMPLITED = False;

            # GET MIN/MAX/AVG etc -> ticks/candle
            elif ITERATION_COUNTER < self.TICKS_FOR_ONE_CANDLE+1:

                if self.THIS_DATA > self.MAX_VALUE:
                    self.MAX_VALUE = self.THIS_DATA;

                if self.THIS_DATA < self.MIN_VALUE:
                    self.MIN_VALUE = self.THIS_DATA;

                if self.THIS_DATA > self.MAX_GLOBAL_VALUE:
                    self.MAX_GLOBAL_VALUE = self.THIS_DATA;

                if self.THIS_DATA < self.MIN_GLOBAL_VALUE:
                    self.MIN_GLOBAL_VALUE = self.THIS_DATA;

            # -----------------------------------------------------
            # PREPEAR ALL NEEDET DATA FOR QPainter [ GRAPH - PLOTTER]

            else:

                self.IS_CANDLE_COMPLITED = True;
                self.HAS_AT_LEAST_ONE_CANDLE = True;

                if self.THIS_DATA > self.MAX_VALUE:
                    self.MAX_VALUE = self.THIS_DATA;

                if self.THIS_DATA < self.MIN_VALUE:
                    self.MIN_VALUE = self.THIS_DATA;

                if self.THIS_DATA > self.MAX_GLOBAL_VALUE:
                    self.MAX_GLOBAL_VALUE = self.THIS_DATA;

                if self.THIS_DATA < self.MIN_GLOBAL_VALUE:
                    self.MIN_GLOBAL_VALUE = self.THIS_DATA;

                self.EXIT_VALUE = self.THIS_DATA;

                if self.PREV_CANDLE_EXIT_VALUE > self.EXIT_VALUE:
                    self.IS_GROWING = False;
                else:
                    self.IS_GROWING = True;

                self.PREV_CANDLE_EXIT_VALUE = self.EXIT_VALUE;


                self.CURRENT_LAST_VALUE = self._GET_CONST_OFFSET( self.THIS_DATA );

                self.enter_val = self._GET_CONST_OFFSET( self.ENTER_VALUE );
                self.exit_val = self._GET_CONST_OFFSET( self.EXIT_VALUE );
                self.max_val = self._GET_CONST_OFFSET( self.MAX_VALUE );
                self.min_val = self._GET_CONST_OFFSET( self.MIN_VALUE );

                # --------------------------------------------------------------------------------------
                # FOR GRAPH-PLOTTER To be able drawing only lines
                if self.CANDLES_POINTS_DRAW:
                    NEW_POINTS_DATA = [ self.X_OFFSET_GLOBAL_CANDLE + (self.CANDLE_W/2), ( self.GRAPH_H - self.exit_val)+self.CANDLES_POINTS_OFFSET ];
                    self.CANDLES_POINTS.append( NEW_POINTS_DATA );

                # --------------------------------------------------------------------------------------
                self.CANDLES.append([ 

                    self.X_OFFSET_GLOBAL_CANDLE,
                    self.GRAPH_H - self.enter_val, 
                    self.GRAPH_H - self.exit_val,
                    self.GRAPH_H - self.max_val,
                    self.GRAPH_H - self.min_val,
                    self.IS_GROWING,
                    self.ENTER_VALUE,
                    self.EXIT_VALUE,
                    self.MAX_VALUE,
                    self.MIN_VALUE,
                    UPDATED

                ]);

                self.X_OFFSET_GLOBAL_CANDLE += self.CANDLE_W + self.X_OFFSET_CANDLE_TO_CANDLE;

                ITERATION_COUNTER = 0; # >>> IMPORTANT (0) AFTER THIS AUTO > ++ so LOOP == 1;
            # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            ITERATION_COUNTER += 1;
            self.MIN_MAX_VALUES_FOUND = True;
            
            # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        # END for loop
        # -------------------------------------------------------------------
        # If last candle was not complited > add it manualy
        
        if not self.IS_CANDLE_COMPLITED: 

            if self.PREV_CANDLE_EXIT_VALUE > self.THIS_DATA:
                self.IS_GROWING = False;
            else:
                self.IS_GROWING = True;

            self.PREV_CANDLE_EXIT_VALUE = self.THIS_DATA;
            self.CURRENT_LAST_VALUE = self._GET_CONST_OFFSET( self.THIS_DATA );

            self.enter_val = self._GET_CONST_OFFSET( self.ENTER_VALUE );
            self.exit_val = self._GET_CONST_OFFSET( self.THIS_DATA );
            self.max_val = self._GET_CONST_OFFSET( self.MAX_VALUE );
            self.min_val = self._GET_CONST_OFFSET( self.MIN_VALUE );

            if self.CANDLES_POINTS_DRAW:
                NEW_POINTS_DATA = [ self.X_OFFSET_GLOBAL_CANDLE + (self.CANDLE_W/2), ( self.GRAPH_H - self.exit_val)+self.CANDLES_POINTS_OFFSET ];
                self.CANDLES_POINTS.append( NEW_POINTS_DATA );


            self.CANDLES.append([ 

                self.X_OFFSET_GLOBAL_CANDLE,
                self.GRAPH_H - self.enter_val, 
                self.GRAPH_H - self.exit_val,
                self.GRAPH_H - self.max_val,
                self.GRAPH_H - self.min_val,
                self.IS_GROWING,
                self.ENTER_VALUE,
                self.EXIT_VALUE,
                self.MAX_VALUE,
                self.MIN_VALUE,
                0

            ]);
        
        # -------------------------------------------------------------------
        try:

            if self.MIN_MAX_VALUES_FOUND:

                try:
                    
                    self.MIN_VALUE_LABLE.setText("min: "+str(self.MIN_GLOBAL_VALUE));
                    self.MIN_VALUE = self._GET_CONST_OFFSET(self.MIN_GLOBAL_VALUE);
                    self.MIN_VALUE_LABLE.setGeometry(10, self.GRAPH_H-int(self.MIN_VALUE)+2, 100, 24);

                    self.MAX_VALUE_LABLE.setText("max: "+str(self.MAX_GLOBAL_VALUE));
                    self.MAX_VALUE = self._GET_CONST_OFFSET(self.MAX_GLOBAL_VALUE);
                    self.MAX_VALUE_LABLE.setGeometry(10, self.GRAPH_H-int(self.MAX_VALUE)-25, 100, 24);
                    
                    self.GRAPH_OVERLAY_WIDGET.hide();

                except Exception as _exception:

                    self.GRAPH_OVERLAY_WIDGET.setText("[0:0] Loading ...");
                    self.GRAPH_OVERLAY_WIDGET.show();



        except Exception as _exception:

            self.GRAPH_OVERLAY_WIDGET.setText("[1:0] Loading ...");
            self.GRAPH_OVERLAY_WIDGET.show();
            print("ERROR: one time");

        # -------------------------------------------------------------------
        if True: #if self.HAS_AT_LEAST_ONE_CANDLE:

            self.GRAPH_OVERLAY_WIDGET.hide();

        else:

            self.GRAPH_OVERLAY_WIDGET.show();
            self.GRAPH_OVERLAY_WIDGET.setText("Loading ...\n Need to get ["+str(self.TICKS_FOR_ONE_CANDLE-len(self.RAW_JSON_DATA))+"] of ["+str(self.TICKS_FOR_ONE_CANDLE)+"] \n It can take up to 5 minuts by first start!");

        # -------------------------------------------------------------------
        # Try to CENTER GRAPH-DATA

        if self.GRAPH_H-self.MIN_VALUE < self.Y_CENTER_OFFSET_SHIFTER_EXPR - 5:

            #print("("+str(self.GRAPH_H - self.min_val)+")self.GRAPH_H - self.min_val > 190")

            self.Y_CENTER_OFFSET += self.Y_CENTER_OFFSET_SHIFTER_STEP; 
            self.UPDATE_RUNNING = False;
            self.update();


        elif self.GRAPH_H-self.MIN_VALUE > self.Y_CENTER_OFFSET_SHIFTER_EXPR + 5:

            #print("("+str(self.GRAPH_H - self.min_val)+")self.GRAPH_H - self.min_val < 180")

            self.Y_CENTER_OFFSET -= self.Y_CENTER_OFFSET_SHIFTER_STEP; 
            self.UPDATE_RUNNING = False;            
            self.update();
        else:
            pass;
            #print("self.GRAPH_H - self.min_val = "+str(self.GRAPH_H - self.min_val))
        # -------------------------------------------------------------------
        self.UPDATE_RUNNING = False;
        
        # -------------------------------------------------------------------
        """
        print("------------------------------------------------")
        print( "G_H: "+str(self.GRAPH_H) );
        print( "" );
        print( "min-max: ",self.min_val, self.max_val );
        print( "MIN-MAX: ",self.MIN_VALUE, self.MAX_VALUE );
        print( "" );
        print( "G_H-min: ",self.GRAPH_H-self.min_val );
        print( "G_H-max: ",self.GRAPH_H-self.max_val );
        print( "" );
        print( "G_H-MIN: ",self.GRAPH_H-self.MIN_VALUE );
        print( "G_H-MAX: ",self.GRAPH_H-self.MAX_VALUE );
        """

        """
        print("------------------------------------------------")
        #print(self.GRAPH_H - self.MAX_VALUE, self.Y_ZOOM[ self.PARENT.CURR_PAIR ]["current"])
        print(self.MAX_VALUE, self.Y_ZOOM[ self.PARENT.CURR_PAIR ]["current"])

        print( "G_H-MAX: ",self.GRAPH_H-self.MAX_VALUE );
        print( "G_H-MIN: ",self.GRAPH_H-self.MIN_VALUE );
        """
        # -------------------------------------------------------------------

    # =======================================================================

###################################################################################################