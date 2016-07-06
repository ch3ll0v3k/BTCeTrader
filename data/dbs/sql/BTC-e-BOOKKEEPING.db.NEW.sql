BEGIN TRANSACTION;

/*  _TB_NAME_ == "ltc_usd, btc_usd, ..."  */
CREATE TABLE IF NOT EXISTS _TB_NAME_ (
    
    /* ----------------------------- */
    BKKPG_UID           INTEGER PRIMARY KEY,
    completed           INT DEFAULT 0, 
    started             INT DEFAULT 0, 

    /* ----------------------------- */
    buy_order_id        INTEGER,
    buy_unix_time       REAL, 
    buy_filled          INT DEFAULT 0, 
    buy_amount          REAL, 
    buy_at_price        REAL, 
    buy_fee             REAL, 
    buy_ttl             REAL, 
    buy_grand_ttl       REAL,

    /* ----------------------------- */
    sell_order_id       INTEGER,
    sell_unix_time      REAL, 
    sell_filled         INT DEFAULT 0, 
    sell_amount         REAL, 
    sell_at_price       REAL, 
    sell_fee            REAL, 
    sell_ttl            REAL, 
    sell_grand_ttl      REAL,

    /* ----------------------------- */
    profit_ttl          REAL /* sell_grand_ttl - buy_grand_ttl */

    /* ----------------------------- */

);

COMMIT;
// =====================================================================================


id, UID_SHA256, completed, started, buy_order_id,buy_unix_time, buy_filled, buy_amount, buy_at_price, 
buy_fee, buy_ttl, buy_grand_ttl,sell_order_id,sell_unix_time, sell_filled, sell_amount, 
sell_at_price, sell_fee, sell_ttl, sell_grand_ttl, profit_ttl








// =====================================================================================


buy 10 @ 3 <-> sell 10 @ 3.1


IF buy_filled = 1 AND sell_filled = 1; then SET completed = 1;












