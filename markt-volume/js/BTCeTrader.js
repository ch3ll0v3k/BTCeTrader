// ================================================================================
var volume_box;
var JSON_DATA;
var MARKT_STEP = 0.01;
var CELL_H = 10;

var MARKT_DATA = {

    "buy" : [],
    "sell" : []

}

// ================================================================================
window.addEventListener("load", function(){
    
    volume_box = __byId("volume-box");
    volume_box.innerHTML = "";  

    draw_grid();

    //GET_MATADATA("ltc_usd", 10);

    UPDATE();
    //alert("YES");

});

// ================================================================================
var T;
var SPEED = 2000;

function UPDATE(){

    // ----------------------------------------------------
    clearTimeout(T);
    // ----------------------------------------------------

    console.log("dd");
    GET_MATADATA("ltc_usd", 10);

    // ----------------------------------------------------
    T = setTimeout(function(){ UPDATE(); }, SPEED);
    // ----------------------------------------------------
}

// ================================================================================
function draw_grid(){

    var grid = "";

    for (var i = 0; i < 160; i++)

        if(i>63 && i < 80)
            grid += '<div class="grid-box-cell" style="border-bottom: solid 2px #F00;"></div>';
        else if(i>79 && i < 96)
            grid += '<div class="grid-box-cell" style="border-top: solid 2px #0F0;"></div>';
        else
            grid += '<div class="grid-box-cell"></div>';

    __byId('grid-box').innerHTML = grid;


}
// ================================================================================
function DRAW_VOLUME(){

    OUT = "";

    MULL = 40;

    STP = 10
    POS = 240;


    for(var x=0; x<MARKT_DATA["buy"].length; x++){

        OUT += '<div class="volume-cell" style=" background-color: #0F0; margin-top: '+(POS)+'px; width: '+(MARKT_DATA["buy"][x][1]/MULL)+'px;"></div>';
        POS -=STP;
    }

    STP = 8
    POS = 250;

    for(var x=0; x<MARKT_DATA["sell"].length; x++){

        OUT += '<div class="volume-cell" style=" background-color: #F00; margin-top: '+(POS)+'px; width: '+(MARKT_DATA["sell"][x][1]/MULL)+'px;"></div>';
        POS +=STP;
    }


    volume_box.innerHTML = OUT;  
}

// ================================================================================
function GET_MATADATA(_pairs, _limit) {
    // -------------------------------------------
    var _AJAX_ = getXmlHttp();
    // -------------------------------------------
    _AJAX_.open('GET','./server.php?pairs='+_pairs+'&limit='+_limit, true); // false SYNC
    //_AJAX_.setRequestHeader('_status_', 'custom-data');
    // -------------------------------------------
    _AJAX_.onreadystatechange = function () {
        if(_AJAX_.readyState == 4 && _AJAX_.status == 200){
            // ---------------------------------------------------------

            JSON_DATA = JSON.parse(_AJAX_.responseText);

            // ---------------------------------------------------------
            // BUY
            var index = 0;
            var search = JSON_DATA["ltc_usd"]["asks"][0][0];

            MARKT_DATA["buy"][index] = [ search, JSON_DATA["ltc_usd"]["asks"][0][1]];

            for (var i = 0; i < JSON_DATA["ltc_usd"]["asks"].length; i++) {
                
                if( search+MARKT_STEP < JSON_DATA["ltc_usd"]["asks"][i][0]){

                    search += MARKT_STEP;
                    index++;                    
                    MARKT_DATA["buy"][index] = [ search, JSON_DATA["ltc_usd"]["asks"][i][1] ];

                }else{
                    MARKT_DATA["buy"][index][1] += JSON_DATA["ltc_usd"]["asks"][i][1];
                }
            };


            // ---------------------------------------------------------
            // SELL

            var index = 0;
            var search = JSON_DATA["ltc_usd"]["bids"][0][0];

            MARKT_DATA["sell"][index] = [ search, JSON_DATA["ltc_usd"]["bids"][0][1]];

            for (var i = 0; i < JSON_DATA["ltc_usd"]["bids"].length; i++) {
                
                if( search+MARKT_STEP > JSON_DATA["ltc_usd"]["bids"][i][0]){

                    search -= MARKT_STEP;
                    index++;                    
                    MARKT_DATA["sell"][index] = [ search, JSON_DATA["ltc_usd"]["bids"][i][1] ];

                }else{
                    MARKT_DATA["sell"][index][1] += JSON_DATA["ltc_usd"]["bids"][i][1];
                }
            };

            // ---------------------------------------------------------
            DRAW_VOLUME();
            // ---------------------------------------------------------
        }
    }
    // -------------------------------------------
    _AJAX_.send(null);
}
// ================================================================================


// ================================================================================
// ================================================================================
