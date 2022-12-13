# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 22:12:21 2021

@author: vivin
"""

OPTIONS_COSTS_CONFIGS = {
    "NIFTY50": {'slippage_fixed': 0.1, 'slippage_perc': 0, 'options_config': {'ttm': 1/52, 'imp_vol': 0.2}},
    "BANKNIFTY": {'slippage_fixed': 0.3, 'slippage_perc': 0, 'options_config': {'ttm': 1/52, 'imp_vol': 0.25}},
    'default': {'slippage_fixed': 0, 'slippage_perc': 0.0002, 'options_config': {'ttm': 1/12, 'imp_vol': 0.3}, 'brokerage_fixed': 40.0, 'tax_perc': 0.0007}, #to be used for ss only + monthly
    'default_fx': {'slippage_fixed': 0.002, 'options_config': {'ttm': 1/52, 'imp_vol': 0.05}, 'brokerage_fixed': 20.0, 'tax_perc': 0.00035}
}

FUTURES_COSTS_CONFIGS = {
    "NIFTY50": {'slippage_fixed': 0.5, 'slippage_perc': 0}, #only monthly
    "BANKNIFTY": {'slippage_fixed': 1.0, 'slippage_perc': 0}, #only monthly
    'default': {'slippage_fixed': 0, 'slippage_perc': 0.0002, 'brokerage_fixed': 20.0, 'tax_perc': 0.0001}, #only to be used for ss
    'default_fx': {'slippage_fixed': 0.002, 'brokerage_fixed': 20.0, 'tax_perc': 0.00001} #only to be used for fx
}

SYNTHETIC_OPTIONS_CONFIGS = {
    'default': {'slippage_perc': 0.005, 'brokerage_fixed': 0.0}
    #'default': {'slippage_perc': 0.0002, 'brokerage_fixed': 0.0} #use this when using synthetic futures or shorting synthetic options
}