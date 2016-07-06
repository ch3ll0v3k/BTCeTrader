# ------------------------------------------------------------------------------------
@getInfo

Parameters:None

_200 = {
    'return': {
        'funds': {
                'ppc': 0, 'usd': 0.00634755, 'gbp': 0, 'xpm': 0, 'trc': 0, 'ltc': 2.24268601, 
                'ftc': 0, 'nvc': 0, 'nmc': 0, 'btc': 0, 'rur': 0, 'cnh': 0, 'eur': 0.00995544
            }, 
            'open_orders': 1, 'server_time': 1451110454, 'transaction_count': 0, 
            'rights': {
                    'info': 1, 'withdraw': 0, 'trade': 1
            }
        },
    'success': 1
}

_500 = {}

# ------------------------------------------------------------------------------------
@Trade

"""
Parameters:

Parameter       description                             assumes value
pair            pair                                    btc_usd (example)
type            order type                              buy or sell
rate            the rate at which you need to buy/sell  numerical
amount          the amount you need to buy / sell       numerical


------------------------------------------------------------------------
pair=ltc_usd&type=buy&rate=3.50&amount=2
------------------------------------------------------------------------

"""

_200 = {
    "success":1,
    "return":{
        "received":0.1,
        "remains":0,
        "order_id":0,
        "funds":{
            "usd":325,
            "btc":2.498,
            "ltc":0,
            ...
        }
    }
}

_500 = {}

# ------------------------------------------------------------------------------------
@ActiveOrders

Parameters:None

_200 = {
    'return': {
        '936159769': {
            'timestamp_created': 1451102172, 'status': 0, 
            'rate': 3.65, 'amount': 2.0, 'pair': 'ltc_usd', 'type': 'sell'
        }
    }, 
    'success': 1
}

_500 = {}
# ------------------------------------------------------------------------------------
@OrderInfo

_200 = {
    'return': {
        '936159769': {
            'timestamp_created': 1451102172, 'status': 0, 'rate': 3.65, 'amount': 2.0, 
            'pair': 'ltc_usd', 'start_amount': 2.0, 'type': 'sell'
        }
    }, 
    'success': 1
}

_500 = {'success': 0, 'error': 'invalid parameter: order_id'}

# ------------------------------------------------------------------------------------
@CancelOrder

"""
Parameter       description     assumes value
order_id        order ID        numerical
"""

_200 = {
    "success":1,
    "return":{
        "order_id":343154,
        "funds":{
            "usd":325,
            "btc":24.998,
            "ltc":0,
            ...
        }
    }
}
 
_500 = {}

# ------------------------------------------------------------------------------------
@TradeHistory
"""
Parameter   description                                 assumes value   standard value

from        trade ID, from which the display starts     numerical       0
count       the number of trades for display            numerical       1000
from_id     trade ID, from which the display starts     numerical       0
end_id      trade ID on which the display ends          numerical       ∞
order       Sorting                                     ASC or DESC     DESC
since       the time to start the display               UNIX time       0
end         the time to end the display                 UNIX time       ∞
pair        pair to be displayed                        btc_usd         all pairs
"""


_200 = {
    'return': {
        '65612187': {
            'order_id': 927563993, 'timestamp': 1450334461, 'rate': 3.373, 'amount': 0.631524, 'is_your_order': 1, 'pair': 'ltc_eur', 'type': 'buy'
        }, 
        '65612186': {
            'order_id': 927464871, 'timestamp': 1450334460, 'rate': 3.373, 'amount': 0.132, 'is_your_order': 0, 'pair': 'ltc_eur', 'type': 'buy'
        }, 
        '65862229': {
            'order_id': 935587738, 'timestamp': 1451044448, 'rate': 3.53239, 'amount': 0.1046, 'is_your_order': 0, 'pair': 'ltc_usd', 'type': 'buy'
        }, 
        '65617598': {
            'order_id': 927700133, 'timestamp': 1450346187, 'rate': 3.66791, 'amount': 0.186057, 'is_your_order': 0, 'pair': 'ltc_usd', 'type': 'sell'
        }, 
        '65862230': {
            'order_id': 935587562, 'timestamp': 1451044448, 'rate': 3.53266, 'amount': 1.9524, 'is_your_order': 0, 'pair': 'ltc_usd', 'type': 'buy'
        }, 
        '65729590': {
            'order_id': 930879017, 'timestamp': 1450660439, 'rate': 3.223, 'amount': 0.1, 'is_your_order': 0, 'pair': 'ltc_eur', 'type': 'buy'
        }, 
        '65830965': {
            'order_id': 934209297, 'timestamp': 1450929363, 'rate': 1.08211, 'amount': 6.6336, 'is_your_order': 0, 'pair': 'eur_usd', 'type': 'sell'
        }, 
        '65609701': {
            'order_id': 927468922, 'timestamp': 1450325515, 'rate': 3.367, 'amount': 1, 'is_your_order': 1, 'pair': 'ltc_eur', 'type': 'sell'
        }, 
        '65612184': {
            'order_id': 927563891, 'timestamp': 1450334460, 'rate': 3.37, 'amount': 0.100476, 'is_your_order': 0, 'pair': 'ltc_eur', 'type': 'buy'
        }, 
        '65711186': {
            'order_id': 928060633, 'timestamp': 1450634781, 'rate': 3.45, 'amount': 4, 'is_your_order': 1, 'pair': 'ltc_usd', 'type': 'buy'
        }, 
        '65611739': {
            'order_id': 927536873, 'timestamp': 1450331600, 'rate': 3.36, 'amount': 0.1, 'is_your_order': 1, 'pair': 'ltc_eur', 'type': 'sell'
        }, 
        '65617599': {
            'order_id': 927699940, 'timestamp': 1450346187, 'rate': 3.6676, 'amount': 0.00019891, 'is_your_order': 0, 'pair': 'ltc_usd', 'type': 'sell'
        }, 
        '65617603': {
            'order_id': 927700371, 'timestamp': 1450346195, 'rate': 3.6676, 'amount': 0.1569, 'is_your_order': 1, 'pair': 'ltc_usd', 'type': 'sell'
        }, 
        '65830397': {
            'order_id': 934193408, 'timestamp': 1450927898, 'rate': 3.328, 'amount': 2, 'is_your_order': 1, 'pair': 'ltc_eur', 'type': 'sell'
        }, 
        '65617605': {
            'order_id': 927700371, 'timestamp': 1450346199, 'rate': 3.6676, 'amount': 3.45684, 'is_your_order': 1, 'pair': 'ltc_usd', 'type': 'sell'
        }, 
        '65612185': {
            'order_id': 927484309, 'timestamp': 1450334460, 'rate': 3.371, 'amount': 0.136, 'is_your_order': 0, 'pair': 'ltc_eur', 'type': 'buy'
        }
    }, 
    'success': 1
}

_500 = {}

# ------------------------------------------------------------------------------------
@TransHistory

_200 = {
        'return': {
            '1978893176': {
                'status': 2, 'timestamp': 1451102159, 'currency': 'LTC', 'amount': 2.12135, 'type': 4, 'desc': 'Cancel order :order:935974459:'
            }, 
            '1961077092': {
                'status': 2, 'timestamp': 1450325027, 'currency': 'LTC', 'amount': 4.0, 'type': 4, 'desc': 'Cancel order :order:927452016:'
            }, 
            '1961087845': {
                'status': 2, 'timestamp': 1450325515, 'currency': 'EUR', 'amount': 3.360266, 'type': 4, 'desc': 'Bought 1 LTC from your order :order:927468922: by price 3.367 EUR total 3.367 EUR (-0.2%)'}, '1961129330': {'status': 2, 'timestamp': 1450327491, 'currency': 'EUR', 'amount': 3.3, 'type': 5, 'desc': 'In payment for a warrant :order:927492887:'}, '1961079408': {'status': 2, 'timestamp': 1450325128, 'currency': 'LTC', 'amount': 4.0, 'type': 5, 'desc': 'In payment for a warrant :order:927468408:'}, '1977729043': {'status': 2, 'timestamp': 1451044448, 'currency': 'USD', 'amount': 6.89716147, 'type': 5, 'desc': 'Buy 1.9524 LTC (-0.2%) from order :order:935587562: by price 3.532658 USD'}, '1977729041': {'status': 2, 'timestamp': 1451044448, 'currency': 'USD', 'amount': 0.36948747, 'type': 5, 'desc': 'Buy 0.1046 LTC (-0.2%) from order :order:935587738: by price 3.532385 USD'}, '1978893489': {'status': 2, 'timestamp': 1451102172, 'currency': 'LTC', 'amount': 2.0, 'type': 5, 'desc': 'In payment for a warrant :order:936159769:'}, '1961274945': {'status': 2, 'timestamp': 1450334460, 'currency': 'EUR', 'amount': 0.33860438, 'type': 5, 'desc': 'Buy 0.10047608 LTC (-0.2%) from order :order:927563891: by price 3.37 EUR'}, '1974888323': {'status': 2, 'timestamp': 1450927898, 'currency': 'EUR', 'amount': 6.642688, 'type': 4, 'desc': 'Bought 2 LTC from your order :order:934193408: by price 3.328 EUR total 6.656 EUR (-0.2%)'}, '1961079122': {'status': 2, 'timestamp': 1450325115, 'currency': 'LTC', 'amount': 4.0, 'type': 4, 'desc': 'Cancel order :order:927467571:'}, '1961270770': {'status': 2, 'timestamp': 1450334223, 'currency': 'LTC', 'amount': 0.1, 'type': 4, 'desc': 'Cancel order :order:927537597:'}, '1961126422': {'status': 2, 'timestamp': 1450327320, 'currency': 'EUR', 'amount': 3.3, 'type': 4, 'desc': 'Cancel order :order:927482189:'}, '1974888304': {'status': 2, 'timestamp': 1450927897, 'currency': 'LTC', 'amount': 2.0, 'type': 5, 'desc': 'In payment for a warrant :order:934193408:'}, '1961326434': {'status': 2, 'timestamp': 1450336883, 'currency': 'LTC', 'amount': 3.89, 'type': 5, 'desc': 'In payment for a warrant :order:927589347:'}, '1967330285': {'status': 2, 'timestamp': 1450634781, 'currency': 'LTC', 'amount': 3.992, 'type': 4, 'desc': 'Buy 4 LTC (-0.2%) from your order :order:928060633: by price 3.45 USD'}, '1961274963': {'status': 2, 'timestamp': 1450334461, 'currency': 'LTC', 'amount': 0.63026088, 'type': 4, 'desc': 'Buy 0.63152392 LTC (-0.2%) from your order :order:927563993: by price 3.373 EUR'}, '1961274948': {'status': 2, 'timestamp': 1450334460, 'currency': 'EUR', 'amount': 0.458456, 'type': 5, 'desc': 'Buy 0.136 LTC (-0.2%) from order :order:927484309: by price 3.371 EUR'}, '1978347139': {'status': 2, 'timestamp': 1451077372, 'currency': 'LTC', 'amount': 2.24268601, 'type': 4, 'desc': 'Cancel order :order:935640542:'}, '1978347084': {'status': 2, 'timestamp': 1451077369, 'currency': 'LTC', 'amount': 2.0, 'type': 4, 'desc': 'Cancel order :order:935641798:'}, '1975091390': {'status': 2, 'timestamp': 1450935996, 'currency': 'LTC', 'amount': 2.0, 'type': 4, 'desc': 'Cancel order :order:934191951:'}, '1961323133': {'status': 2, 'timestamp': 1450336739, 'currency': 'LTC', 'amount': 3.89800001, 'type': 4, 'desc': 'Cancel order :order:927568077:'}, '1961220677': {'status': 2, 'timestamp': 1450331637, 'currency': 'LTC', 'amount': 0.1, 'type': 5, 'desc': 'In payment for a warrant :order:927537261:'}, '1962297468': {'status': 2, 'timestamp': 1450383588, 'currency': 'USD', 'amount': 13.8, 'type': 4, 'desc': 'Cancel order :order:927738473:'}, '1961221352': {'status': 2, 'timestamp': 1450331670, 'currency': 'LTC', 'amount': 0.1, 'type': 5, 'desc': 'In payment for a warrant :order:927537597:'}, '1961270776': {'status': 2, 'timestamp': 1450334224, 'currency': 'LTC', 'amount': 1.0, 'type': 4, 'desc': 'Cancel order :order:927509484:'}, '1961556438': {'status': 2, 'timestamp': 1450346187, 'currency': 'USD', 'amount': 0.68107619, 'type': 4, 'desc': 'Sell 0.186057 LTC from order :order:927700133: by price 3.667914 USD total 0.68244107 USD (-0.2%)'}, '1960984222': {'status': 2, 'timestamp': 1450320721, 'currency': 'LTC', 'amount': 4.0, 'type': 1, 'desc': 'LTC payment'}, '1961080446': {'status': 2, 'timestamp': 1450325178, 'currency': 'LTC', 'amount': 1.0, 'type': 5, 'desc': 'In payment for a warrant :order:927468922:'}, '1974885354': {'status': 2, 'timestamp': 1450927790, 'currency': 'LTC', 'amount': 2.0, 'type': 5, 'desc': 'In payment for a warrant :order:934191951:'}, '1974759171': {'status': 2, 'timestamp': 1450923697, 'currency': 'LTC', 'amount': 2.0, 'type': 4, 'desc': 'Cancel order :order:930734805:'}, '1961556661': {'status': 2, 'timestamp': 1450346199, 'currency': 'USD', 'amount': 12.6529682, 'type': 4, 'desc': 'Bought 3.45684409 LTC from your order :order:927700371: by price 3.667601 USD total 12.67832484 USD (-0.2%)'}, '1961107428': {'status': 2, 'timestamp': 1450326387, 'currency': 'EUR', 'amount': 3.3, 'type': 5, 'desc': 'In payment for a warrant :order:927482189:'}, '1961556601': {'status': 2, 'timestamp': 1450346195, 'currency': 'USD', 'amount': 0.5742957, 'type': 4, 'desc': 'Bought 0.1569 LTC from your order :order:927700371: by price 3.667601 USD total 0.57544659 USD (-0.2%)'}, '1961270247': {'status': 2, 'timestamp': 1450334184, 'currency': 'EUR', 'amount': 3.3, 'type': 4, 'desc': 'Cancel order :order:927492887:'}, '1977836322': {'status': 2, 'timestamp': 1451049203, 'currency': 'LTC', 'amount': 2.24268601, 'type': 5, 'desc': 'In payment for a warrant :order:935640542:'}, '1961219889': {'status': 2, 'timestamp': 1450331599, 'currency': 'LTC', 'amount': 0.1, 'type': 5, 'desc': 'In payment for a warrant :order:927536873:'}, '1967797441': {'status': 2, 'timestamp': 1450649532, 'currency': 'LTC', 'amount': 2.0, 'type': 5, 'desc': 'In payment for a warrant :order:930734805:'}, '1977838940': {'status': 2, 'timestamp': 1451049307, 'currency': 'LTC', 'amount': 2.0, 'type': 5, 'desc': 'In payment for a warrant :order:935641798:'}, '1977709931': {'status': 2, 'timestamp': 1451043476, 'currency': 'USD', 'amount': 7.21, 'type': 4, 'desc': 'Cancel order :order:935578254:'}, '1968098022': {'status': 2, 'timestamp': 1450660439, 'currency': 'EUR', 'amount': 0.3223, 'type': 5, 'desc': 'Buy 0.1 LTC (-0.2%) from order :order:930879017: by price 3.223 EUR'}, '1961274954': {'status': 2, 'timestamp': 1450334460, 'currency': 'EUR', 'amount': 2.13013018, 'type': 5, 'desc': 'In payment for a warrant :order:927563993:'}, '1961635536': {'status': 2, 'timestamp': 1450350280, 'currency': 'USD', 'amount': 13.8, 'type': 5, 'desc': 'In payment for a warrant :order:927738473:'}, '1961080061': {'status': 2, 'timestamp': 1450325159, 'currency': 'LTC', 'amount': 4.0, 'type': 4, 'desc': 'Cancel order :order:927468408:'}, '1967799038': {'status': 2, 'timestamp': 1450649618, 'currency': 'LTC', 'amount': 2.0, 'type': 5, 'desc': 'In payment for a warrant :order:930735623:'}, '1961046131': {'status': 2, 'timestamp': 1450323582, 'currency': 'LTC', 'amount': 4.0, 'type': 5, 'desc': 'In payment for a warrant :order:927452016:'}, '1961128195': {'status': 2, 'timestamp': 1450327436, 'currency': 'EUR', 'amount': 3.34, 'type': 4, 'desc': 'Cancel order :order:927491901:'}, '1961077735': {'status': 2, 'timestamp': 1450325052, 'currency': 'LTC', 'amount': 4.0, 'type': 5, 'desc': 'In payment for a warrant :order:927467571:'}, '1961127341': {'status': 2, 'timestamp': 1450327381, 'currency': 'EUR', 'amount': 3.34, 'type': 5, 'desc': 'In payment for a warrant :order:927491901:'}, '1977712325': {'status': 2, 'timestamp': 1451043578, 'currency': 'USD', 'amount': 7.2512103, 'type': 5, 'desc': 'In payment for a warrant :order:935579709:'}, '1961283176': {'status': 2, 'timestamp': 1450334879, 'currency': 'LTC', 'amount': 3.89800001, 'type': 5, 'desc': 'In payment for a warrant :order:927568077:'}, '1961270831': {'status': 2, 'timestamp': 1450334227, 'currency': 'LTC', 'amount': 0.1, 'type': 4, 'desc': 'Cancel order :order:927537261:'}, '1961274951': {'status': 2, 'timestamp': 1450334460, 'currency': 'EUR', 'amount': 0.445236, 'type': 5, 'desc': 'Buy 0.132 LTC (-0.2%) from order :order:927464871: by price 3.373 EUR'}, '1961219913': {'status': 2, 'timestamp': 1450331600, 'currency': 'EUR', 'amount': 0.335328, 'type': 4, 'desc': 'Bought 0.1 LTC from your order :order:927536873: by price 3.36 EUR total 0.336 EUR (-0.2%)'}, '1974924997': {'status': 2, 'timestamp': 1450929363, 'currency': 'USD', 'amount': 7.16392833, 'type': 4, 'desc': 'Sell 6.6336 EUR from order :order:934209297: by price 1.08211 USD total 7.17828489 USD (-0.2%)'}, '1978516263': {'status': 2, 'timestamp': 1451086327, 'currency': 'LTC', 'amount': 2.12135, 'type': 5, 'desc': 'In payment for a warrant :order:935974459:'}, '1962299070': {'status': 2, 'timestamp': 1450383672, 'currency': 'USD', 'amount': 13.8, 'type': 5, 'desc': 'In payment for a warrant :order:928060633:'}, '1961163207': {'status': 2, 'timestamp': 1450329148, 'currency': 'LTC', 'amount': 1.0, 'type': 5, 'desc': 'In payment for a warrant :order:927509484:'}, '1961404695': {'status': 2, 'timestamp': 1450340252, 'currency': 'LTC', 'amount': 3.89, 'type': 4, 'desc': 'Cancel order :order:927589347:'}, '1977727222': {'status': 2, 'timestamp': 1451044348, 'currency': 'USD', 'amount': 7.2512103, 'type': 4, 'desc': 'Cancel order :order:935579709:'}, '1977709316': {'status': 2, 'timestamp': 1451043432, 'currency': 'USD', 'amount': 7.21, 'type': 5, 'desc': 'In payment for a warrant :order:935578254:'}, '1961556442': {'status': 2, 'timestamp': 1450346187, 'currency': 'LTC', 'amount': 3.61374409, 'type': 5, 'desc': 'In payment for a warrant :order:927700371:'}, '1961556440': {'status': 2, 'timestamp': 1450346187, 'currency': 'USD', 'amount': 0.00072807, 'type': 4, 'desc': 'Sell 0.00019891 LTC from order :order:927699940: by price 3.667604 USD total 0.00072952 USD (-0.2%)'}, '1974803161': {'status': 2, 'timestamp': 1450925242, 'currency': 'LTC', 'amount': 2.0, 'type': 4, 'desc': 'Cancel order :order:930735623:'}
    }, 
    'success': 1
}

_500 = {}

# ------------------------------------------------------------------------------------
@WithdrawCoin

"""
Please note: 
    You need to have the privilege of the Withdraw key to be able to use this method. 
    You can make a request for enabling this privilege by submitting a ticket to Support.
"""

"""
You need to create the API key that you are going to use for this method in advance. 
Please provide the first 8 characters of the key (e.g. HKG82W66) in your ticket to support. 
We'll enable the Withdraw privilege for this key.

When using this method, there will be no additional confirmations of withdrawal. 
Please note that you are fully responsible for keeping the secret of the API key safe after 
we have enabled the Withdraw privilege for it.
"""

"""
Parameter           Description             Assumes value
coinName            currency                BTC, LTC (example)
amount              withdrawal amount       numeric
address             withdrawal address      address
"""

{
    "success":1,
    "return":{
        "tId":37832629,     // tId: Transaction ID.
        "amountSent":0.009, // amountSent: The amount sent including commission.
        "funds":{           // funds: Balance after the request.

            "usd":325,
            "btc":24.998,
            "ltc":0,
            ...
        }
    }
}

# ------------------------------------------------------------------------------------
@CreateCoupon

"""
Please note: 
    You need to have the privilege of the Withdraw key to be able to use this method. 
    You can make a request for enabling this privilege by submitting a ticket to Support.
"""

_200 = {}
_500 = {}

# ------------------------------------------------------------------------------------
@RedeemCoupon

"""
Please note: 
    You need to have the privilege of the Withdraw key to be able to use this method. 
    You can make a request for enabling this privilege by submitting a ticket to Support.
"""

_200 = {}
_500 = {}



