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

###################################################################################################
class NoteBook(QFrame):

    # =======================================================================
    def __init__(self, parent=None, _PARENT=None):

        # -------------------------------------------------------------------
        QFrame.__init__(self, parent);
        self.setGeometry(3, 5, 975, 548);
        # -------------------------------------------------------------------
        self.PARENT                         = _PARENT;
        self.CONF                           = _PARENT.CONF;

        self.DIR                            = self.CONF["USER"]["DIR"];
        self.NOTEBOOK_A_FILE                = self.DIR+"NOTE_A.file";
        self.NOTEBOOK_B_FILE                = self.DIR+"NOTE_B.file";

        _stl                                = " QTextEdit{ font: 12px 'monospace'; background-color: #444; color: #fff; background-image: url(); }";
        _MT                                 = 115;
        _ML                                 = 12;
        _W                                  = 470;
        _H                                  = 400;

        self.NOTEBOOK_A_WIDGET = QTextEdit("", self);
        self.NOTEBOOK_A_WIDGET.setGeometry(_ML, _MT, _W, _H);
        self.NOTEBOOK_A_WIDGET.setStyleSheet( _stl );
        self.NOTEBOOK_A_WIDGET.setDocumentTitle(" TTL A One test")
        self.NOTEBOOK_A_WIDGET.LineWrapMode( self.NOTEBOOK_A_WIDGET.WidgetWidth );
        #self.NOTEBOOK_A_WIDGET.setEditable(True);

        self.NOTEBOOK_B_WIDGET = QTextEdit("", self);
        self.NOTEBOOK_B_WIDGET.setGeometry(_W+(_ML*2), _MT, _W, _H);
        self.NOTEBOOK_B_WIDGET.setStyleSheet( _stl );
        self.NOTEBOOK_B_WIDGET.setDocumentTitle(" TTL B One test")
        self.NOTEBOOK_B_WIDGET.LineWrapMode( self.NOTEBOOK_B_WIDGET.WidgetWidth );
        #self.NOTEBOOK_B_WIDGET.setEditable(True);

        """
        self.SAVE_DATA_BTN = QPushButton("Save", self);
        self.SAVE_DATA_BTN.setGeometry(5, 5, 100, 30);
        self.connect( self.SAVE_DATA_BTN, SIGNAL('clicked()'), self.SAVE_DATA );
        """

        # -------------------------------------------------------------------
        self.INIT();
        # -------------------------------------------------------------------

    # =======================================================================
    def INIT(self):

        # -------------------------------------------------------------------
        try:

                
            # ---------------------------------------------------
            # A
            FS = open( self.NOTEBOOK_A_FILE, "r");
            lines = FS.readlines();
            FS.close();
            
            for line in lines:

                self.NOTEBOOK_A_WIDGET.append(line.strip());
                #self.NOTEBOOK_A_WIDGET.insertPlainText(line);
                #self.NOTEBOOK_A_WIDGET.insertHtml(line);

            # ---------------------------------------------------
            # B
            FS = open( self.NOTEBOOK_B_FILE, "r");
            lines = FS.readlines();
            FS.close();
            
            for line in lines:

                self.NOTEBOOK_B_WIDGET.append(line.strip());
                #self.NOTEBOOK_B_WIDGET.insertPlainText(line);
                #self.NOTEBOOK_B_WIDGET.insertHtml(line);
            # ---------------------------------------------------


        except Exception as _exception:
            print("-----------------------------------------------------");
            print(_exception);
        # -------------------------------------------------------------------

    # =======================================================================
    def SAVE_DATA(self):

        # -------------------------------------------------------------------
        try:

            # A
            FS = open( self.NOTEBOOK_A_FILE, "r");
            lines = FS.readlines();
            FS.close();
            
            for line in lines:

                self.NOTEBOOK_A_WIDGET.append(line.strip());
                #self.NOTEBOOK_A_WIDGET.insertPlainText(line);
                #self.NOTEBOOK_A_WIDGET.insertHtml(line);

            # ---------------------------------------------------
            # A
            FS = open( self.NOTEBOOK_A_FILE, "w");
            DATA = str(self.NOTEBOOK_A_WIDGET.toPlainText()).split("\n");
            for line in DATA:
                FS.write(line+"\n");
            FS.close();

            # ---------------------------------------------------
            # B
            FS = open( self.NOTEBOOK_B_FILE, "w");
            DATA = str(self.NOTEBOOK_B_WIDGET.toPlainText()).split("\n");
            for line in DATA:
                FS.write(line+"\n");
            FS.close();
            # ---------------------------------------------------


        except Exception as _exception:
            print("-----------------------------------------------------");
            print(_exception);
        # -------------------------------------------------------------------

    # =======================================================================

###################################################################################################