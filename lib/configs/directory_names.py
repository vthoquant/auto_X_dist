# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 13:55:45 2022

@author: vivin
"""

BASE_PATH = "C:\\Users\\vivin\\Documents\\strategy_backtest\\"
IB_API_LOGS_STORE = "{}logs\\".format(BASE_PATH)
LOCAL_INTRADAY_STORE_PATH = "{}bardata_store\\".format(BASE_PATH)
LD_STORE_PATH = "{}bardata_store\\index_ld\\".format(BASE_PATH)
YF_CACHE_PATH = "{}yf_cache\\".format(BASE_PATH)
BARDATA_STORE_PATH = "{}bardata_store\\".format(BASE_PATH)
INDIAVIX_STORE_PATH = "{}bardata_store\\^INDIAVIX\\".format(BASE_PATH)
ON_OBJECT_STATE_STORE = "{}on_object_state_store\\".format(BASE_PATH)

STRATEGY_RUN_BASE_PATHS = {
    'FUTURES_SPREAD_STATARB': "{}futures_spread\\".format(BASE_PATH),
    'INTRADAY_BREAKOUT_HILO': "{}intraday_bkout_hilo\\".format(BASE_PATH),
    'INTRADAY_BREAKOUT_CSTICK': "{}intraday_bkout_cstick\\".format(BASE_PATH),
    'INTRADAY_DBLBREAKOUT_CSTICK': "{}intraday_dblbkout_cstick\\".format(BASE_PATH),
    'INTRADAY_RANGE_BREAKOUT': "{}intraday_range_bkout\\".format(BASE_PATH),
    'INTRADAY_MA': "{}intraday_ma\\".format(BASE_PATH),
    'INTRADAY_MAC': "{}intraday_mac\\".format(BASE_PATH),
    'INTRADAY_MAC_2PERIOD': "{}intraday_mac_2p\\".format(BASE_PATH),
    'INTRADAY_MACD': "{}intraday_macd\\".format(BASE_PATH),
    'INTRADAY_MAC_SL': "{}intraday_mac_sl\\".format(BASE_PATH),
    'INTRADAY_MAC_MA': "{}intraday_mac_ma\\".format(BASE_PATH),
    'INTRADAY_MACD_TP_SL': "{}intraday_macd_tpsl\\".format(BASE_PATH),
    'INTRADAY_OVERTRADE_RSI': "{}intraday_overtrade_rsi\\".format(BASE_PATH),
    'INTRADAY_OVERTRADE_CUMUL_RSI': "{}intraday_overtrade_crsi\\".format(BASE_PATH),
    'INTRADAY_OVERTRADE_PRICE_LB': "{}intraday_overtrade_price_lb\\".format(BASE_PATH),
    'INTRADAY_OVERTRADE_BB': "{}intraday_overtrade_bb\\".format(BASE_PATH),
    'INTRADAY_OVERTRADE_RSI_CSTICK_REV': "{}intraday_overtrade_rsi_cstick_rev\\".format(BASE_PATH),
    'INTRADAY_HA_CCI': "{}intraday_ha_cci\\".format(BASE_PATH),
    'INTRADAY_PULLBACK': "{}intraday_pullback\\".format(BASE_PATH),
    'INTRADAY_PULLBACK_PRICE_LB': "{}intraday_pullback_lb\\".format(BASE_PATH),
    'INTRADAY_PULLBACK_CUMUL_RSI': "{}intraday_pullback_crsi\\".format(BASE_PATH),
    'INTRADAY_PULLBACK_PRICECHANGE': "{}intraday_pullback_pricechange\\".format(BASE_PATH),
    'INTRADAY_KELTNER_REVERSAL': "{}intraday_keltner_reversal\\".format(BASE_PATH),
    'INTRADAY_PULLBACK_BB': "{}intraday_pullback_bb\\".format(BASE_PATH),
    'INTRADAY_BB': "{}intraday_bb\\".format(BASE_PATH),
    'INTRADAY_BB_REVERSAL': "{}intraday_bb_reversal\\".format(BASE_PATH),
    'INTRADAY_BB_REVERSAL_V2': "{}intraday_bb_reversal_v2\\".format(BASE_PATH),
    'INTRADAY_PULLBACK_CSTICK_REV': "{}intraday_pullback_cstick_rev\\".format(BASE_PATH),
    'INTRADAY_BASE': "{}intraday_trend\\".format(BASE_PATH),
    'INTRADAY_TREND_CAPTURE': "{}intraday_trend\\".format(BASE_PATH),
    'INTRADAY_TREND_HEIKIN': "{}intraday_trend_heikin\\".format(BASE_PATH),
    'INTRADAY_TREND_HEIKIN_2': "{}intraday_trend_heikin_2\\".format(BASE_PATH),
    'INTRADAY_TREND_HEIKIN_3': "{}intraday_trend_heikin_3\\".format(BASE_PATH),
    'INTRADAY_CONTINUATION_HLDG': "{}intraday_cont_hldg\\".format(BASE_PATH),
    'INTRADAY_CONTINUATION_ATRTP': "{}intraday_cont_atrtp\\".format(BASE_PATH),
    'INTRADAY_CONTINUATION_ATRSLSHIFT': "{}intraday_cont_atrslshift\\".format(BASE_PATH),
    'INTRADAY_WILLR_BREAKOUT': "{}intraday_willr_bkout\\".format(BASE_PATH),
    'INTRADAY_FISHER_CROSSOVER': "{}intraday_fisher_crossover\\".format(BASE_PATH),
    'INTRADAY_KELTNER_BREAKOUT': "{}intraday_keltner_bkout\\".format(BASE_PATH),
    'MOMENTUM_REBAL_STRATEGY': "{}mom_rebal\\".format(BASE_PATH),
    'MULTICLASS_CLASSIFIER_REBAL': "{}multiclass_rebal\\".format(BASE_PATH)
}