# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 20:34:39 2022

@author: vivin
"""

NIFTY_OPT_CONFIG = {
    'imp_vol': 0.15,
    'rr': 0.03,
    'strike_gap': 50
}

BANKNIFTY_OPT_CONFIG = {
    'imp_vol': 0.18,
    'rr': 0.03,
    'strike_gap': 100
}

RELIANCE_OPT_CONFIG = {
    'imp_vol': 0.22,
    'rr': 0.03,
    'strike_gap': 20
}

HDFC_OPT_CONFIG = {
    'imp_vol': 0.2,
    'rr': 0.03,
    'strike_gap': 20
}

INFY_OPT_CONFIG = {
    'imp_vol': 0.22,
    'rr': 0.03,
    'strike_gap': 20
}

TCS_OPT_CONFIG = {
    'imp_vol': 0.2,
    'rr': 0.03,
    'strike_gap': 20
}

SBIN_OPT_CONFIG = {
    'imp_vol': 0.25,
    'rr': 0.03,
    'strike_gap': 5
}

MARUTI_OPT_CONFIG = {
    'imp_vol': 0.25,
    'rr': 0.03,
    'strike_gap': 100
}

DEFAULT_OPT_CHOICE = {
    'imp_vol_mult': 1,
    'vol_premium': 0.1,
    'max_lev_alloc': 0.05,
    'strike_gap_mult': -4,
    'short_options_or_fut': False,
    'is_fut': True,
    'short_option_lev': 5
}

TICKER_TO_OPT_CONFIG = {
    'NIFTY50': NIFTY_OPT_CONFIG,
    'BANKNIFTY': BANKNIFTY_OPT_CONFIG,
    'RELIANCE': RELIANCE_OPT_CONFIG,
    'HDFC': HDFC_OPT_CONFIG,
    'INFY': INFY_OPT_CONFIG,
    'TCS': TCS_OPT_CONFIG,
    'SBIN': SBIN_OPT_CONFIG,
    'MARUTI': MARUTI_OPT_CONFIG
}

OPTION_TRADE_CHOICES = {
    'default': DEFAULT_OPT_CHOICE
}