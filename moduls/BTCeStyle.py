###################################################################################################
class STL(object):

    # =======================================================================
    """
    border-style: solid; border-width: 1px; border-color: #C0C0C0;
    

    """
    # =======================================================================
    PATH                                = "./data/imgs/";
    # --------------------------------------------------------
    MAIN_STYLE                          = "Macintosh";
    FONT_MAIN                           = "OldEnglish";
    FONT_MAIN_SIZE                      = 10;

    # =======================================================================
    # TAB Trader

    ICON_EXIT                           = PATH+"ExitIcon.png"
    WINDOWICON                          = PATH+"BTCeTraderIcon.png";
    FRAME_MAIN                          = "QFrame{ background-color: #333; color: #fff; background-image: url('"+PATH+"TAB_Trader.png') }";
    INFO_PANEL                          = "QWidget{ font: 12px 'monospace';  background-color: transparent; border-style: none; background-image: url('');  }";
    INFO_PANEL_LOG                      = "QTextEdit{ font: 12px 'monospace'; border-radius: 1px; color: #fff; background-color: #333; }";
    INFO_PANEL_LOG_CLEAR_BTN            = "QPushButton{ font: 14px 'monospace'; color: #fff; border-style: none; }"

    QTEXTEDIT                           = "QTextEdit{ }";

    PANEL_ASK_BID                       = "QListWidget{ font: 12px 'monospace'; background-color: transparent; background-image: url(''); border-style: solid; border-width: 1px; border-color: #666; }";
    PANEL_BUY_SELL                      = "QTextEdit{ font: 18px 'monospace'; background-color: transparent; font-size: 20px; background-image: url(''); border-style: none; color: #fff; }"; 
    ARROW_BUY_SELL                      = "QLabel{ background-color: transparent; background-image: url(''); }";

    PRICE_DIFFERENCE_GREEN              = "QLabel{ color: #0F0; font: 12px 'monospace'; font-weight: bold; border-style: none; border-radius: none; background-color: transparent; background-image: url('.asa.png'); }";
    PRICE_DIFFERENCE_RED                = "QLabel{ color: #F00; font: 12px 'monospace'; font-weight: bold; border-style: none; border-radius: none; background-color: transparent; background-image: url('.asa.png'); }";
    PRICE_DIFFERENCE_WHITE              = "QLabel{ color: #FFF; font: 12px 'monospace'; font-weight: bold; border-style: none; border-radius: none; background-color: transparent; background-image: url('.asa.png'); }";

    WATCH_DISPLAY                       = "QLabel{ background-color: transparent; color: #000; background-image: url(''); }";

    SELL_BUY_BTNS                       = "QPushButton{ background-color: transparent; color: transparent; border-style: none; }"
    PAIR_COMBO                          = "QComboBox{ }"; #background-image: url(""); background-color: #777; color: #fff; border-style: solid; border-width: 1px; border-color: #fff; }";

    USER_INPUT                          = "QLineEdit{ border-style: none; border-radius: none; background-color: #000; color: #fff; }";
    USER_INPUT_NO_EDIT                  = "QLineEdit{ border-style: none; border-radius: none; background-color: transparent; color: #fff; }";
    USER_INPUT_NO_EDIT_RED              = "QLineEdit{ border-style: none; border-radius: none; background-color: transparent; color: #F00; }";
    USER_INPUT_NO_EDIT_GREEN            = "QLineEdit{ border-style: none; border-radius: none; background-color: transparent; color: #0F0; }";

    BKKPG_UID_DISPLAY_WHITE             = "QLineEdit{ font: 12px 'monospace'; background-color: transparent; color: #fff; background-image: url(''); border-style: none; }";
    BKKPG_UID_DISPLAY_GREEN             = "QLineEdit{ font: 12px 'monospace'; background-color: transparent; color: #0F0; background-image: url(''); border-style: none; }";

    # --------------------------------------------------------
    FRAME_GRAPH                         = "QFrame{ background-color: #000; background-image: url(''); }";
    CALC_BTN                            = "QPushButton{ border-style: none; border-radius: 20px; color: transparent; background-color: transparent; }";


    GRAPH_OPTIONS_SELL_BUY_WIDGET       =  "QWidget{ border-style: solid; border-width: 1px; border-color: #0F0; background-color: #333; color: #fff;  border-bottom-left-radius: 12px; border-bottom-right-radius: 12px; background-image: url('./data/imgs/GRAPH_OPTIONS_SELL_BUY_WIDGET.png'); }";
    GRAPH_OPTIONS_DRAW_CROSS_WIDGET     =  "QWidget{ border-style: solid; border-width: 1px; border-color: #0F0; background-color: #333; color: #fff;  border-bottom-left-radius: 12px; border-bottom-right-radius: 12px; background-image: url('./data/imgs/GRAPH_OPTIONS_CROSS_WIDGET.png'); }";

    RADIO_BUTTON                        = "QRadioButton{ background-image: url(''); background-color: transparent; border-color: transparent; }";
    CHECK_BOX                           = "QCheckBox{ background-image: url(''); background-color: transparent; border-color: transparent; }";

    # --------------------------------------------------------
    TRANSPARENT_TOOLTIP                 = "QLabel{ background-color: transparent; background-image:url(''); }"

    # --------------------------------------------------------


    # =======================================================================
    # TAB Office
    FRAME_OFFICE                        = "QFrame{ color: #fff;  background-image: url('"+PATH+"TAB_Office.png'); }";
    
    BALANCE_WIDGET_LABLE                = "QLabel{ color: #000; background-color: transparent; background-image: url(''); } "
    BALANCE_WIDGET                      = "QTextEdit{ font: 16px 'monospace'; color: #ccc; padding-left: 16px; background-color: transparent; background-image: url(''); border-style: none; }"
    
    ALARMS_WIDGET_LABLE                 = "QLabel{ color: #000; background-color: transparent; background-image: url(''); } "
    ALARMS_WIDGET                       = "QWidget{ font: 16px 'monospace'; color: #ccc; padding-left: 16px; background-color: transparent; background-image: url(''); }";
    ALARMS_COMBO                        = "QWidget{ font: 16px 'monospace'; color: #000; }";
    ALARM_VALUE_INPUT                   = "QLineEdit{ font: 18px 'monospace'; padding-left: 6; color: #fff; border-style: none; background-color: #333; background-image: url(); }"

    ALARMS_LIST                         = "QListWidget{ font: 12px 'monospace'; background-color: transparent; color: #FFF; border-style: none; background-image: url(); }";


    # =======================================================================
    # FRAME_BOOKKEEPING
    FRAME_BOOKKEEPING                   = "QFrame{ font: 12px 'monospace'; color: #000; background-color: transparent;  background-image: url('"+PATH+"TAB_BookKeeping.png'); }" 

    # =======================================================================
    # FRAME_NOTEBOOK
    FRAME_NOTEBOOK                      = "QFrame{ font: 12px 'monospace'; color: #000; background-color: transparent;  background-image: url('"+PATH+"TAB_NoteBook.png'); }" 

    # =======================================================================
    # FRAME_SETTINGS
    FRAME_SETTINGS                      = "QFrame{ font: 12px 'monospace'; color: #000; background-color: transparent;  background-image: url('"+PATH+"TAB_Settings.png'); }" 

    # =======================================================================
    TRANS_MESSAGE_WIDGET                = "QWidget{ background-color: rgba(100, 100, 100, 127); }";
    TRANS_MESSAGE_LABEL                 = "QLabel{ background-color: #fff; border-style: solid; border-color: #222; border-width: 6px; border-radius: 12px; }";
    TRANS_MESSAGE_TEXT                  = "QTextEdit{ width: 400px; height: 100px; padding:20px; background-color: transparent; color: #000; font-size: 16px;  border-style: none; }";
    TRANS_MESSAGE_WIDGET_CLOSE_BTN      = "QPushButton{ background-image: url('"+PATH+"close.png'); background-color: transparent; border-style: none; }"; #border-style: solid; border-color: #000; border-width: 4px; border-radius: 20px; background-color: #FFF; font-size: 24px; color: #F00; }"

    # =======================================================================
        
###################################################################################################
class Colors(object):
    
    # =======================================================================
    #B                                   = "\033[01;30m";
    R                                   = "\033[01;31m";
    G                                   = "\033[01;32m";
    Y                                   = "\033[01;33m";
    B                                   = "\033[01;34m";
    P                                   = "\033[01;35m";
    C                                   = "\033[01;36m";
    W                                   = "\033[01;37m";

    EN                                  = "\033[0m";

    W_ON_G                              = "\033[01;40m\033[01;37m"
    d_arrow                             = "\342\207\212";
    u_arrow                             = "\342\207\210";

    # =======================================================================

###################################################################################################
