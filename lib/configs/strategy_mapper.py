# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 08:31:11 2020

@author: vivin
"""

prefix = 'lib.strategies'

STRATEGY_MAP_TEMP = {
    #classname to filename mapping for strategies
    "MULTICLASS_CLASSIFIER_REBAL": "multi_class_rebal",
    "MOMENTUM_REBAL_STRATEGY": "momentum_rebal",
    "PORTFOLIO_MOM_REBAL": "pfolio_mom_rebal",
    "PORTFOLIO_TALIB_REBAL": "pfolio_mom_rebal",
    "PORTFOLIO_STATIC_REBAL": "portfolio_static",
    "PORTFOLIO_STATIC": "portfolio_static",
    'INTRADAY_TREND_CAPTURE': 'intraday_trend_capture',
    'INTRADAY_TREND_HEIKIN': 'intraday_trend_capture',
    'INTRADAY_TREND_HEIKIN_2': 'intraday_trend_capture',
    'INTRADAY_TREND_HEIKIN_3': 'intraday_trend_capture',
    'INTRADAY_MA': 'intraday_ma',
    'INTRADAY_MAC': 'intraday_ma',
    'INTRADAY_MACD': 'intraday_ma',
    'INTRADAY_MACD_TP_SL': 'intraday_ma',
    'INTRADAY_MAC_SL': 'intraday_ma',
    'INTRADAY_MAC_MA': 'intraday_ma',
    'INTRADAY_PULLBACK': 'intraday_pullback',
    'INTRADAY_PULLBACK_PRICE_LB': 'intraday_pullback',
    'INTRADAY_PULLBACK_CUMUL_RSI': 'intraday_pullback',
    'INTRADAY_PULLBACK_BB': 'intraday_pullback',
    'INTRADAY_PULLBACK_CSTICK_REV': 'intraday_pullback',
    'INTRADAY_OVERTRADE_RSI': 'intraday_overtrade',
    'INTRADAY_OVERTRADE_CUMUL_RSI': 'intraday_overtrade',
    'INTRADAY_OVERTRADE_RSI_CSTICK_REV': 'intraday_overtrade',
    'INTRADAY_OVERTRADE_PRICE_LB': 'intraday_overtrade',
    'INTRADAY_OVERTRADE_BB': 'intraday_overtrade',
    'INTRADAY_CONTINUATION_HLDG': 'intraday_trend_continuation',
    'INTRADAY_CONTINUATION_ATRTP': 'intraday_trend_continuation',
    'INTRADAY_CONTINUATION_ATRSLSHIFT': 'intraday_trend_continuation',
    'INTRADAY_BB': 'intraday_pullback',
    'INTRADAY_HA_CCI': 'intraday_overtrade',
    'INTRADAY_BREAKOUT_HILO': 'intraday_breakout',
    'INTRADAY_BREAKOUT_CSTICK': 'intraday_breakout',
    'INTRADAY_DBLBREAKOUT_CSTICK': 'intraday_breakout',
    'INTRADAY_RANGE_BREAKOUT': 'intraday_breakout',
    'INTRADAY_WILLR_BREAKOUT': 'intraday_breakout',
    'FUTURES_SPREAD_STATARB': 'futures_spread_statarb'
}

STRATEGY_MAP = {k:'{}.{}'.format(prefix,v) for k,v in STRATEGY_MAP_TEMP.items()}