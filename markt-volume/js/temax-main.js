// ================================================================================
function __log(toLog){ console.log(toLog); }
// ----------------------------------------------------------------------------
function __dir(method){ console.log(console.dir(method)); }
// ----------------------------------------------------------------------------
function __byId(id){ return document.getElementById(id); }
// ----------------------------------------------------------------------------
function __byName(name){ return document.getElementsByName(name); }
// ----------------------------------------------------------------------------
function __byClass(className){ return document.getElementsByClassName(className); }
// ----------------------------------------------------------------------------
function __byTag(tagName){ return document.getElementsByTagName(tagName); }
// ----------------------------------------------------------------------------
function __newElem(type){ return document.createElement(type); }
// ----------------------------------------------------------------------------
function __grit(min, max){ return Math.floor(Math.random() * (max - min + 1)) + min; }
// ----------------------------------------------------------------------------
function __id(id){ return document.getElementById(id); }
// ----------------------------------------------------------------------------


// ================================================================================
function getXmlHttp(){
    var xmlHTTH;
    try{ xmlHTTH = new ActiveXObject("MSXML2.XMLHTTP");
    }catch (e){
        try { xmlHTTH = new ActiveXObject("Microsoft.XMLHTTP"); } 
        catch (e){ xmlHTTH = new XMLHttpRequest(); } 
    }return xmlHTTH;
}
// ================================================================================
function ajaxPOST(PostData){
    // -------------------------------------------
    var PostData = '';
        PostData += 'login=name';
        PostData += '&password=12345';

        //PostData = encodeURIComponent(PostData);
        //alert(encodeURIComponent(PostData));
        //alert(encodeURI(PostData));    
    // -------------------------------------------
    var _AJAX_ = getXmlHttp();
    // -------------------------------------------
    _AJAX_.open('POST',url, true); // false ASYNC         
    // -------------------------------------------
    //_AJAX_.setRequestHeader("Custom_name", "custom_data");
    //_AJAX_.setRequestHeader("Content-Type", "multipart/form-data");
    _AJAX_.setRequestHeader("Content-Type", "text/html");
    _AJAX_.setRequestHeader("Content-length", PostData.length);
    _AJAX_.setRequestHeader('Content-type','application/x-www-form-urlencoded');
    // -------------------------------------------
    _AJAX_.onreadystatechange = function () {
        if(_AJAX_.readyState == 4 && _AJAX_.status == 200){
            // ---------------------------------------------------------
            // var seconds = new Date().getTime() / 1000;
            // var time = new Date().getTime();

            // _AJAX_.getAllResponseHeaders();      // 
            // _AJAX_.getResponseHeader('name');    // 
            // _AJAX_.readyState                    // == 4
            // _AJAX_.status                        // == 200
            // _AJAX_.responseText                  // == text response
            // ---------------------------------------------------------
        }
    }
    // -------------------------------------------
    _AJAX_.send(PostData);
}
// ================================================================================
function ajaxGET(_pairs, _limit) {
    // -------------------------------------------
    var _AJAX_ = getXmlHttp();
    // -------------------------------------------
    _AJAX_.open('GET','./server.php?pairs='+_pairs+'&limit='+_limit, true); // false SYNC
    //_AJAX_.setRequestHeader('_status_', 'custom-data');
    // -------------------------------------------
    _AJAX_.onreadystatechange = function () {
        if(_AJAX_.readyState == 4 && _AJAX_.status == 200){
            // ---------------------------------------------------------

            console.log(_AJAX_.responseText);
            // var seconds = new Date().getTime() / 1000;
            // var time = new Date().getTime();

            // _AJAX_.getAllResponseHeaders();      // 
            // _AJAX_.getResponseHeader('name');    // 
            // _AJAX_.readyState                    // == 4
            // _AJAX_.status                        // == 200
            // _AJAX_.responseText                  // == text response
            // ---------------------------------------------------------
        }
    }
    // -------------------------------------------
    _AJAX_.send(null);
}
// ================================================================================