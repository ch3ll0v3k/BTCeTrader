#!/usr/bin/python
# -*- coding: utf-8 -*-
###################################################################################################
# BulitIn
import json, sys, time

# PyQt4
from PyQt4.QtCore import QTimer, SIGNAL, SLOT, Qt, QPointF, QPoint, QRectF, QRect
from PyQt4.QtGui import QMessageBox, QTextEdit, QDialog, QPolygonF,QPainter, QPen, QColor 
from PyQt4.QtGui import QBrush, QMainWindow,QWidget,QToolTip,QApplication, QFont,QIcon,QAction
from PyQt4.QtGui import QFrame,QListWidget,QComboBox,QCheckBox,QPushButton,QProgressBar,QLineEdit,QLabel
from PyQt4.QtGui import QTextBrowser, QCursor, qApp, QDesktopWidget
from PyQt4.QtGui import QGraphicsView, QGraphicsScene, QPicture, QPaintDevice, QStaticText

from PyQt4.QtGui import QCursor

###################################################################################################
class PlotterHoverLayer(QFrame):

    # =======================================================================
    def __init__(self, _SIZE, parent=None, _PARENT=None):

        # -------------------------------------------------------------------
        QFrame.__init__(self, parent);
        self.setGeometry( _SIZE[0], _SIZE[1], _SIZE[2], _SIZE[3] );
        self.PARENT                         = _PARENT;
        self.setStyleSheet("QFrame{ background-color: rgba(0,0,0, 127);}"); # background-image: url('./data/imgs/arrow_curr_pos.png'); }");
        # -------------------------------------------------------------------
        self.setMouseTracking(True);
        
        self.MOUSE_X                        = 0; 
        self.MOUSE_Y                        = 0; 
        
        self.MOUSE_STEP_REDUCTION           = True;
        # -------------------------------------------------------------------
        self.GRAPH_W                        = _SIZE[2];
        self.GRAPH_H                        = _SIZE[3];

        self.DRAW_CROSS                     = True;
        # -------------------------------------------------------------------

    # =======================================================================
    def mouseMoveEvent(self, event):
    
        # -------------------------------------------------------------------
        #event.globalPos();
        # event.x(), " -> ", event.y() | event.pos() | event.posF() |

        self.MOUSE_X = event.x()
        self.MOUSE_Y = event.y();

        self.update();
        # -------------------------------------------------------------------

    
    # =======================================================================
    def paintEvent(self, event):

        # -------------------------------------------------------------------
        Painter = QPainter()
        Painter.begin(self)
        
        # -------------------------------------------------------------------
        # Draw CROSS-MOUSE-POS
        if self.DRAW_CROSS:

            Painter.setPen( QPen( QColor(255,255,255, 255), 1, Qt.DashLine ) );
            Painter.drawPolyline( QPoint(self.MOUSE_X-600, self.MOUSE_Y), QPoint( self.MOUSE_X+600, self.MOUSE_Y) ); 
            Painter.drawPolyline( QPoint(self.MOUSE_X, self.MOUSE_Y-400), QPoint( self.MOUSE_X, self.MOUSE_Y+400) ); 

        # -------------------------------------------------------------------
        Painter.end();
        # -------------------------------------------------------------------

    # =======================================================================
