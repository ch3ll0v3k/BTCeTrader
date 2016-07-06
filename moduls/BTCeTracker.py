"https://api.coinbase.com/v2/prices/spot?currency=EUR"



"https://api.coinbase.com/v2/prices/buy"


"https://api.coinbase.com/v2/prices/buy/?currency=EUR"
"https://api.coinbase.com/v2/prices/sell/?currency=EUR"



# ================================================================================================
"""
BLOCKCHAIN - Market-Cap 

https://blockchain.info/charts/market-cap?showDataPoints=true&timespan=30days&show_header=true&daysAverageString=1&scale=0&format=json&address=

"""
# ================================================================================================


# ================================================================================================
 URL: https://blockchain.info/stats?format=json

No Parameters

Returns a JSON object containing the statistics seen on the stats page.
Response:

{
    "n_btc_mined": 780000000000,
    "market_cap": 96222279.58162625,
    "total_fees_btc": 2252128249,
    "total_btc_sent": 747456945221033,
    "minutes_between_blocks": 9.230769230769232,
    "market_price_usd": 9.857426146006336,
    "miners_operating_margin": 48,
    "electricity_cost_usd": 39755.97274663426,
    "hash_rate": 16989.731943006092,
    "estimated_transaction_volume_usd": 3744528.558883145,
    "miners_revenue_usd": 77104.78731406156,
    "blocks_size": 15503304,
    "n_blocks_total": 195228,
    "difficulty": 2190865.970102852,
    "timestamp": 1345681034495,
    "miners_revenue_btc": 7822,
    "n_blocks_mined": 156,
    "trade_volume_usd": 660214.3677100714,
    "electricity_consumption": 265039.81831089506,
    "estimated_btc_sent": 37986879165209,
    "n_tx": 37320,
    "trade_volume_btc": 66973.41726509096
}
# ================================================================================================
"""
https://data.btcchina.com/data/ticker?market=ltccny   <- ['btccny', 'ltccny','ltcbtc', 'all']

----------------------------------------------------------
single:
{
    "ticker": {
    "high": "2894.97",
    "low": "2850.08",
    "buy": "2876.92",
    "sell": "2883.80",
    "last": "2875.66",
    "vol": "4133.63800000",
    "date": 1396412995,
    "vwap": 2879.12,
    "prev_close": 2875.61,
    "open": 2880.01
  }
} 
----------------------------------------------------------
all:

{
    "ticker_btccny": {
    "high": "2894.97",
    "low": "2850.08",
    "buy": "2880.00",
    "sell": "2883.86",
    "last": "2880.00",
    "vol": "4164.41040000",
    "date": 1396412841,
    "vwap": 2879.12,
    "prev_close": 2875.61,
    "open": 2880.01
  },
    "ticker_ltccny": {
    "high": "78.80",
    "low": "77.50",
    "buy": "78.22",
    "sell": "78.35",
    "last": "78.35",
    "vol": "56443.71000000",
    "date": 1396412841,
    "vwap": 78.12,
    "prev_close": 78.61,
    "open": 78.62
  },
    "ticker_ltcbtc": {
    "high": "0.02800000",
    "low": "0.02710000",
    "buy": "0.02720000",
    "sell": "0.02730000",
    "last": "0.02720000",
    "vol": "7715.69400000",
    "date": 1396412841,
    "vwap": 0.0274,
    "prev_close": 0.0273,
    "open": 0.0272
  }
}
----------------------------------------------------------

"""


"""
https://data.btcchina.com/data/orderbook?market=ltccny&limit=10

asks/bids


"""




# ================================================================================================
