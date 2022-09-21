# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 22:55:06 2021

@author: vivin
"""

prefix = 'lib.order_placers'

OPLACERS_MAP_TEMP = {
    #classname to filename mapping for order placers
    "FUTURES_SPREAD_ORDER": "futures_spread",
    "FUTURES_SPREAD_MONITOR_ORDER": "futures_spread",
    "OPTIONS_BSK_ORDER": "options_basket",
    "OPTIONS_BSK_BIDASK_DYNAMIC": "options_basket",
    "OPTIONS_BSK_ORDER_DEPTH": "options_basket",
    "OPTIONS_HEDGE_BIDASK_DYNAMIC_ORDER": "futures_bidask",
    "CALLPUT_IV_ARB_ORDER": "callput_iv_arb",
    "CAL_IV_STATARB_ORDER": "cal_iv_statarb",
    "FUTURES_HEDGE_BIDASK_DYNAMIC_ORDER": "futures_bidask",
    "FUTURES_BSK_BIDASK_DYNAMIC_ORDER": "futures_bidask"
}

OPLACERS_MAP = {k:'{}.{}'.format(prefix,v) for k,v in OPLACERS_MAP_TEMP.items()}