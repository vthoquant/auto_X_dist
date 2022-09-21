# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 00:59:08 2020

@author: vivin
"""
"""
MULTICLASS_TALIB_FEATURE_CONFIG = {
    'ROCP': {
        'name': 'ROCP',
        'data_cols': ['Close'],
        'kwargs': {'timeperiod': 1},
        'return': ['ROCP']
    },
    'SMA_S': {
        'name': 'SMA',
        'data_cols': ['Close'],
        'kwargs': {'timeperiod': 10},
        'return': ['SMA_S']
    },
    'SMA_L': {
        'name': 'SMA',
        'data_cols': ['Close'],
        'kwargs': {'timeperiod': 50},
        'return': ['SMA_L']
    },
    'ADX_S': {
        'name': 'ADX',
        'data_cols': ['High', 'Low', 'Close'],
        'kwargs': {'timeperiod': 10},
        'return': ['ADX_S']
    },
    'ADX_L': {
        'name': 'ADX',
        'data_cols': ['High', 'Low', 'Close'],
        'kwargs': {'timeperiod': 50},
        'return': ['ADX_L']
    },
}
"""
"""
MULTICLASS_TALIB_FEATURE_CONFIG = {
    'ROCP': {
        'name': 'ROCP',
        'data_cols': ['Close'],
        'kwargs': {'timeperiod': 1},
        'return': ['ROCP'],
        'is_feature': [False]
    },
    
    'MACD': {
        'name': 'MACD',
        'data_cols': ['Close'],
        'kwargs': {},
        'return': ['MACD', 'MACD_s', 'MACD_h'],
        'filter': [False, False, True],
    },
    'ADX': {
        'name': 'ADX',
        'data_cols': ['High', 'Low', 'Close'],
        'kwargs': {},
        'return': ['ADX']
    },
    'RSI': {
        'name': 'RSI',
        'data_cols': ['Close'],
        'kwargs': {},
        'return': ['RSI']
    },
    'ATR': {
        'name': 'ATR',
        'data_cols': ['High', 'Low', 'Close'],
        'kwargs': {},
        'return': ['ATR']
    },
}
"""

MULTICLASS_TALIB_FEATURE_CONFIG = {
    'ROCP': {
        'name': 'ROCP',
        'data_cols': ['Close'],
        'kwargs': {'timeperiod': 1},
        'return': ['ROCP'],
        'is_feature': [False]
    },
    
    'MACD': {
        'name': 'MACD',
        'data_cols': ['Close'],
        'kwargs': {},
        'return': ['MACD', 'MACD_s', 'MACD_h'],
        'filter': [False, False, True],
    },
    
    'ROCP_s': {
        'name': 'ROCP',
        'data_cols': ['Close'],
        'kwargs': {'timeperiod': 7},
        'return': ['ROCP_s'],
    },
    
    'RSI': {
        'name': 'RSI',
        'data_cols': ['Close'],
        'kwargs': {},
        'return': ['RSI'],
    },
}

PORTFOLIO_MOM_REBAL_TALIB_FEATURE_CONFIG = {
    'ADX_d': {
        'name': 'ADX',
        'data_cols': ['High', 'Low', 'Close'],
        'kwargs': {'timeperiod': 14},
        'return': ['ADX_def'],
    },
    
    'ADX_l': {
        'name': 'ADX',
        'data_cols': ['High', 'Low', 'Close'],
        'kwargs': {'timeperiod': 28},
        'return': ['ADX_long'],
    },
    
    'ADX_s': {
        'name': 'ADX',
        'data_cols': ['High', 'Low', 'Close'],
        'kwargs': {'timeperiod': 7},
        'return': ['ADX_short'],
    },
    
    'ADX_ss': {
        'name': 'ADX',
        'data_cols': ['High', 'Low', 'Close'],
        'kwargs': {'timeperiod': 2},
        'return': ['ADX_supershort'],
    },
}

TALIB_FEATURES_CONFIG_MAP = {
    'MULTICLASS_CLASSIFIER_REBAL': MULTICLASS_TALIB_FEATURE_CONFIG,
    'PORTFOLIO_TALIB_REBAL': PORTFOLIO_MOM_REBAL_TALIB_FEATURE_CONFIG
}