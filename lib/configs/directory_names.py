# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 13:55:45 2022

@author: vivin
"""

BASE_PATH = "C:\\Users\\vivin\\Documents\\"
IB_API_LOGS_STORE = "C:\\Users\\vivin\\Downloads\\"
LOCAL_INTRADAY_STORE_PATH = "{}strategy_backtest\\bardata_store\\".format(BASE_PATH)
YF_CACHE_PATH = "{}strategy_backtest\\yf_cache\\".format(BASE_PATH)
BARDATA_STORE_PATH = "{}strategy_backtest\\bardata_store\\".format(BASE_PATH)
INDIAVIX_STORE_PATH = "{}strategy_backtest\\bardata_store\\^INDIAVIX\\".format(BASE_PATH)

STRATEGY_RUN_BASE_PATHS = {
    'FUTURES_SPREAD_STATARB': "{}strategy_backtest\\futures_spread\\".format(BASE_PATH),
    'INTRADAY_BREAKOUT_HILO': "{}strategy_backtest\\intraday_bkout_hilo\\".format(BASE_PATH),
    'INTRADAY_BREAKOUT_CSTICK': "{}strategy_backtest\\intraday_bkout_cstick\\".format(BASE_PATH),
    'INTRADAY_DBLBREAKOUT_CSTICK': "{}strategy_backtest\\intraday_dblbkout_cstick\\".format(BASE_PATH),
    'INTRADAY_MA': "{}strategy_backtest\\intraday_ma\\".format(BASE_PATH),
    'INTRADAY_MAC': "{}strategy_backtest\\intraday_mac\\".format(BASE_PATH),
    'INTRADAY_MACD': "{}strategy_backtest\\intraday_macd\\".format(BASE_PATH),
    'INTRADAY_MAC_SL': "{}strategy_backtest\\intraday_mac_sl\\".format(BASE_PATH),
    'INTRADAY_MAC_MA': "{}strategy_backtest\\intraday_mac_ma\\".format(BASE_PATH),
    'INTRADAY_MACD_TP_SL': "{}strategy_backtest\\intraday_macd_tpsl\\".format(BASE_PATH),
    'INTRADAY_OVERTRADE_RSI': "{}strategy_backtest\\intraday_overtrade_rsi\\".format(BASE_PATH),
    'INTRADAY_OVERTRADE_CUMUL_RSI': "{}strategy_backtest\\intraday_overtrade_crsi\\".format(BASE_PATH),
    'INTRADAY_OVERTRADE_PRICE_LB': "{}strategy_backtest\\intraday_overtrade_price_lb\\".format(BASE_PATH),
    'INTRADAY_OVERTRADE_BB': "{}strategy_backtest\\intraday_overtrade_bb\\".format(BASE_PATH),
    'INTRADAY_OVERTRADE_RSI_CSTICK_REV': "{}strategy_backtest\\intraday_overtrade_rsi_cstick_rev\\".format(BASE_PATH),
    'INTRADAY_HA_CCI': "{}strategy_backtest\\intraday_ha_cci\\".format(BASE_PATH),
    'INTRADAY_PULLBACK': "{}strategy_backtest\\intraday_pullback\\".format(BASE_PATH),
    'INTRADAY_PULLBACK_PRICE_LB': "{}strategy_backtest\\intraday_pullback_lb\\".format(BASE_PATH),
    'INTRADAY_PULLBACK_CUMUL_RSI': "{}strategy_backtest\\intraday_pullback_crsi\\".format(BASE_PATH),
    'INTRADAY_PULLBACK_BB': "{}strategy_backtest\\intraday_pullback_bb\\".format(BASE_PATH),
    'INTRADAY_BB': "{}strategy_backtest\\intraday_bb\\".format(BASE_PATH),
    'INTRADAY_PULLBACK_CSTICK_REV': "{}strategy_backtest\\intraday_pullback_cstick_rev\\".format(BASE_PATH),
    'INTRADAY_BASE': "{}strategy_backtest\\intraday_trend\\".format(BASE_PATH),
    'INTRADAY_TREND_CAPTURE': "{}strategy_backtest\\intraday_trend\\".format(BASE_PATH),
    'INTRADAY_TREND_HEIKIN': "{}strategy_backtest\\intraday_trend_heikin\\".format(BASE_PATH),
    'INTRADAY_TREND_HEIKIN_2': "{}strategy_backtest\\intraday_trend_heikin_2\\".format(BASE_PATH),
    'INTRADAY_TREND_HEIKIN_3': "{}strategy_backtest\\intraday_trend_heikin_3\\".format(BASE_PATH),
    'INTRADAY_CONTINUATION_HLDG': "{}strategy_backtest\\intraday_cont_hldg\\".format(BASE_PATH),
    'INTRADAY_CONTINUATION_ATRTP': "{}strategy_backtest\\intraday_cont_atrtp\\".format(BASE_PATH),
    'INTRADAY_CONTINUATION_ATRSLSHIFT': "{}strategy_backtest\\intraday_cont_atrslshift\\".format(BASE_PATH),
    'MOMENTUM_REBAL_STRATEGY': "{}QuantInsti\\project_data\\".format(BASE_PATH),
    'MULTICLASS_CLASSIFIER_REBAL': "{}QuantInsti\\project_data\\".format(BASE_PATH)
}