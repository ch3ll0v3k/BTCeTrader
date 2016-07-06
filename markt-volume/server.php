<?php
// =================================================================================================

$pairs = "ltc_usd";
$limit = "200";

if(isset($_GET["pairs"]))

    $pairs = $_GET["pairs"];

if(isset($_GET["limit"]))
    $limmit = $_GET["limit"];


$url = "https://btc-e.com/api/3/depth/$pairs?limit=".$limit;

echo file_get_contents($url);





// =================================================================================================
/*
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
*/



?>