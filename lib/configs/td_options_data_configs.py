# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 14:08:27 2022

@author: vivin
"""

TICKER_MAPPER = {
    'NIFTY50': 'NIFTY'
}

OPTIONS_CHAINS_FILTERS = {
    'weeklyRegular': {
        'option_terms': ['W1'],
        'liq_filter': 0.7
    },
    
    'weeklyRegular;delta=0.3': {
        'option_terms': ['W1'],
        'liq_filter': 0.7,
        'delta': 0.3,
    }
}