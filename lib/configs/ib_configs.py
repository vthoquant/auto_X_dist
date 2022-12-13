# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 18:44:46 2021

@author: vivin
"""
from lib.configs.ib_fno_configs import IB_FNO_CONFIG

IB_OPTIONS_CONFIG = IB_FNO_CONFIG

INTDY_MACD_EURINR = {
    'strategy_name': 'INTRADAY_MACD',
    'params':{        
        'rescale_shorts': False,
        'window_short': 50,
        'long_window_mult': 2,
        'signal_window_mult': 1,
        'restrict_trade_time': True,
        'add_transaction_costs': True,
        'inst_delta': 1.0
    },
    'api_attrs': {
        'historical_data_offset': 86400 * 9,
        'client_id': 114,
        'order_config': {
            'inst': 'FUT', # can be OPT, FUT, STK
            'order_type': 'MKT',
            'algo_attrs': {
                'algoStrategy': 'Adaptive',
                'algoParams': {'adaptivePriority': 'Normal'}
            }
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '15 mins',
        'durationStr': '7 D'
    },
    
    'event_wait_time': 1
}

FUTURES_SPREAD_EURINR_TEST = {
    'strategy_name': 'FUTURES_SPREAD_STATARB',
    'params':{},
    'api_attrs': {
        'historical_data_offset': 86400,
        'client_id': 115,
        'order_config': {
            'inst': 'FUT',
            'order_type': 'MTL'
        },
    },

    'api_data_config': {
        'barSizeSetting': '30 secs'
    },

    'event_wait_time': 1
}

INTDY_OTRADE_RSI_CSTICK_IB_PARAMS_OPT_TEST_W_BANKNIFTY_multi = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-otrade-cstick-bnifty-long-1',
            'strategy_name': 'INTRADAY_OVERTRADE_RSI_CSTICK_REV',
            'params':{        
                'rescale_shorts': False,
                'rsi_period': 3, 
                'rsi_entry': (25, 75),
                'rsi_exit': (55, 45),
                'max_holding': None,
                'trend_baseline_long': None,
                'trend_baseline_short':10,
                'cstick_modes': '1,2,5',
                'side_restriction': 1,
                'restrict_trade_time': False,
                'add_transaction_costs': True,
                'inst_delta': 0.5
            },
        },
        {
            'run_name': 'intraday-otrade-cstick-bnifty-short-1',
            'strategy_name': 'INTRADAY_OVERTRADE_RSI_CSTICK_REV',
            'params':{        
                'rescale_shorts': False,
                'rsi_period': 3, 
                'rsi_entry': (25, 75),
                'rsi_exit': (55, 45),
                'max_holding': 5,
                'trend_baseline_long': None,
                'trend_baseline_short':10,
                'cstick_modes': '2',
                'side_restriction': -1,
                'restrict_trade_time': False,
                'add_transaction_costs': True,
                'inst_delta': 0.5
            },
        },
        {
            'run_name': 'intraday-otrade-cstick-bnifty-short-2',
            'strategy_name': 'INTRADAY_OVERTRADE_RSI_CSTICK_REV',
            'params':{        
                'rescale_shorts': False,
                'rsi_period': 10, 
                'rsi_entry': (25, 75),
                'rsi_exit': (55, 45),
                'max_holding': None,
                'trend_baseline_long': None,
                'trend_baseline_short':10,
                'cstick_modes': '3',
                'side_restriction': -1,
                'restrict_trade_time': False,
                'add_transaction_costs': True,
                'inst_delta': 0.5
            },
        },
        {
            'run_name': 'intraday-otrade-cstick-bnifty-short-3',
            'strategy_name': 'INTRADAY_OVERTRADE_RSI_CSTICK_REV',
            'params':{        
                'rescale_shorts': False,
                'rsi_period': 2, 
                'rsi_entry': (10, 90),
                'rsi_exit': (55, 45),
                'max_holding': 5,
                'trend_baseline_long': None,
                'trend_baseline_short':10,
                'cstick_modes': '5',
                'side_restriction': -1,
                'restrict_trade_time': False,
                'add_transaction_costs': True,
                'inst_delta': 0.5
            },
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 5,
        'client_id': 142,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '3 D'
    },
    
    'event_wait_time': 1
}

INTDY_OTRADE_RSI_CSTICK_IB_PARAMS_OPT_TEST_W_NIFTY_multi = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-otrade-cstick-nifty-long-1',
            'strategy_name': 'INTRADAY_OVERTRADE_RSI_CSTICK_REV',
            'params':{        
                'rescale_shorts': False,
                'rsi_period': 2, 
                'rsi_entry': (10, 90),
                'rsi_exit': (55, 45),
                'max_holding': None,
                'trend_baseline_long': None,
                'trend_baseline_short':10,
                'cstick_modes': '1,5',
                'side_restriction': 1,
                'restrict_trade_time': False,
                'add_transaction_costs': True,
                'inst_delta': 0.5
            },
        },
        {
            'run_name': 'intraday-otrade-cstick-nifty-short-1',
            'strategy_name': 'INTRADAY_OVERTRADE_RSI_CSTICK_REV',
            'params':{        
                'rescale_shorts': False,
                'rsi_period': 2, 
                'rsi_entry': (10, 90),
                'rsi_exit': (55, 45),
                'max_holding': 5,
                'trend_baseline_long': None,
                'trend_baseline_short':10,
                'cstick_modes': '2',
                'side_restriction': -1,
                'restrict_trade_time': False,
                'add_transaction_costs': True,
                'inst_delta': 0.5
            },
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 5,
        'client_id': 145,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '3 D'
    },
    
    'event_wait_time': 1
}

INTDY_PBACK_RSI_CSTICK_IB_PARAMS_OPT_TEST_W_BANKNIFTY_multi = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-pback-cstick-bnifty-long-1',
            'strategy_name': 'INTRADAY_PULLBACK_CSTICK_REV',
            'params':{        
                'rescale_shorts': False,
                'rsi_period': 3, 
                'rsi_entry': (25, 75),
                'rsi_exit': (40, 60),
                'max_holding': 5,
                'trend_baseline': 100,
                'cstick_modes': '1,5',
                'side_restriction': 1,
                'restrict_trade_time': False,
                'add_transaction_costs': True,
                'inst_delta': 0.5
            },
        },
        {
            'run_name': 'intraday-pback-cstick-bnifty-short-1',
            'strategy_name': 'INTRADAY_PULLBACK_CSTICK_REV',
            'params':{        
                'rescale_shorts': False,
                'rsi_period': 3, 
                'rsi_entry': (25, 75),
                'rsi_exit': (40, 60),
                'max_holding': 5,
                'trend_baseline': 100,
                'cstick_modes': '5',
                'side_restriction': -1,
                'restrict_trade_time': False,
                'add_transaction_costs': True,
                'inst_delta': 0.5
            },
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 5,
        'client_id': 143,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '3 D'
    },
    
    'event_wait_time': 1
}

INTDY_PBACK_RSI_CSTICK_IB_PARAMS_OPT_TEST_W_NIFTY_multi = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-pback-cstick-nifty-long-1',
            'strategy_name': 'INTRADAY_PULLBACK_CSTICK_REV',
            'params':{        
                'rescale_shorts': False,
                'rsi_period': 3, 
                'rsi_entry': (25, 75),
                'rsi_exit': (40, 60),
                'max_holding': 5,
                'trend_baseline': 100,
                'cstick_modes': '1,3,5',
                'side_restriction': 1,
                'restrict_trade_time': False,
                'add_transaction_costs': True,
                'inst_delta': 0.5
            },
        },
        {
            'run_name': 'intraday-pback-cstick-nifty-short-1',
            'strategy_name': 'INTRADAY_PULLBACK_CSTICK_REV',
            'params':{        
                'rescale_shorts': False,
                'rsi_period': 3, 
                'rsi_entry': (25, 75),
                'rsi_exit': (40, 60),
                'max_holding': 5,
                'trend_baseline': 100,
                'cstick_modes': '2,4',
                'side_restriction': -1,
                'restrict_trade_time': False,
                'add_transaction_costs': True,
                'inst_delta': 0.5
            },
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 5,
        'client_id': 144,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '3 D'
    },
    
    'event_wait_time': 1
}

INTDY_MREV_IB_PARAMS_OPT_TEST_W_BANKNIFTY_multi_5m = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-pback-rsi-bnifty-5m',
            'strategy_name': 'INTRADAY_PULLBACK',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 2, 
                'rsi_entry': (5, 95),
                'rsi_exit': (40, 60),
                'max_holding': 3,
                'trend_baseline': 100,
                'side_restriction': None,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-otrade-rsi-bnifty-long-5m',
            'strategy_name': 'INTRADAY_OVERTRADE_RSI',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 2, 
                'rsi_entry': (5, 95),
                'rsi_exit': (40, 60),
                'max_holding': 5,
                'trend_baseline_long': None,
                'trend_baseline_short': 10,
                'side_restriction': 1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-otrade-rsi-bnifty-short-5m',
            'strategy_name': 'INTRADAY_OVERTRADE_RSI',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 5, 
                'rsi_entry': (5, 95),
                'rsi_exit': (55, 45),
                'max_holding': 5,
                'trend_baseline_long': None,
                'trend_baseline_short': 10,
                'side_restriction': -1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 5,
        'client_id': 146,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '3 D'
    },
    
    'event_wait_time': 1
}

INTDY_MREV_IB_PARAMS_OPT_TEST_W_BANKNIFTY_multi_15m = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-pback-crsi-bnifty-short-15m',
            'strategy_name': 'INTRADAY_PULLBACK_CUMUL_RSI',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 2,
                'cumul_rsi_period': 2,
                'rsi_entry': (5, 95),
                'rsi_exit': (55, 45),
                'max_holding': 3,
                'trend_baseline': 100,
                'side_restriction': -1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-pback-crsi-bnifty-long-15m',
            'strategy_name': 'INTRADAY_PULLBACK_CUMUL_RSI',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 2,
                'cumul_rsi_period': 3,
                'rsi_entry': (10, 90),
                'rsi_exit': (55, 45),
                'max_holding': 1,
                'trend_baseline': 100,
                'side_restriction': 1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-otrade-rsi-bnifty-long-15m',
            'strategy_name': 'INTRADAY_OVERTRADE_RSI',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 3, 
                'rsi_entry': (10, 90),
                'rsi_exit': (55, 45),
                'max_holding': 3,
                'trend_baseline_long': 100,
                'trend_baseline_short': 10,
                'side_restriction': 1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-otrade-rsi-bnifty-short-15m',
            'strategy_name': 'INTRADAY_OVERTRADE_RSI',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 5, 
                'rsi_entry': (10, 90),
                'rsi_exit': (55, 45),
                'max_holding': 1,
                'trend_baseline_long': 100,
                'trend_baseline_short': 10,
                'side_restriction': -1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 9,
        'client_id': 148,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '15 mins',
        'durationStr': '7 D'
    },
    
    'event_wait_time': 1
}

INTDY_MREV_IB_PARAMS_OPT_TEST_W_NIFTY_multi_5m = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-pback-crsi-nifty-5m',
            'strategy_name': 'INTRADAY_PULLBACK_CUMUL_RSI',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 2,
                'cumul_rsi_period': 2,
                'rsi_entry': (10, 90),
                'rsi_exit': (55, 45),
                'max_holding': 3,
                'trend_baseline': 100,
                'side_restriction': None,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-otrade-crsi-nifty-long-5m',
            'strategy_name': 'INTRADAY_OVERTRADE_CUMUL_RSI',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 3,
                'cumul_rsi_period': 2,
                'rsi_entry': (10, 90),
                'rsi_exit': (55, 45),
                'side_restriction': 1,
                'max_holding': 3,
                'trend_baseline_long': 100,
                'trend_baseline_short': 10,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 5,
        'client_id': 147,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '3 D'
    },
    
    'event_wait_time': 1
}

INTDY_MREV_IB_PARAMS_OPT_TEST_W_NIFTY_multi_15m = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-pback-crsi-nifty-15m',
            'strategy_name': 'INTRADAY_PULLBACK_CUMUL_RSI',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 2,
                'cumul_rsi_period': 2,
                'rsi_entry': (5, 95),
                'rsi_exit': (40, 60),
                'max_holding': 3,
                'trend_baseline': 100,
                'side_restriction': None,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-otrade-crsi-nifty-long-15m',
            'strategy_name': 'INTRADAY_OVERTRADE_CUMUL_RSI',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 2,
                'cumul_rsi_period': 2,
                'rsi_entry': (5, 95),
                'rsi_exit': (55, 45),
                'side_restriction': 1,
                'max_holding': 1,
                'trend_baseline_long': None,
                'trend_baseline_short': 10,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 9,
        'client_id': 149,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '15 mins',
        'durationStr': '7 D'
    },
    
    'event_wait_time': 1
}

INTDY_TREND_IB_PARAMS_OPT_TEST_W_BANKNIFTY_multi_5m = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-cont-hldg-bnifty-long-1-5m',
            'strategy_name': 'INTRADAY_CONTINUATION_HLDG',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 5, 
                'rsi_entry': (75, 25),
                'max_holding': None,
                'cstick_modes': '3,6,7,8',
                'trend_baseline': 50,
                'side_restriction': 1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-cont-hldg-bnifty-short-1-5m',
            'strategy_name': 'INTRADAY_CONTINUATION_HLDG',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 5, 
                'rsi_entry': (75, 25),
                'max_holding': None,
                'cstick_modes': '2,3',
                'trend_baseline': 50,
                'side_restriction': -1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 5,
        'client_id': 150,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'SELL', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '3 D'
    },
    
    'event_wait_time': 1
}

INTDY_TREND_IB_PARAMS_OPT_TEST_W_BANKNIFTY_multi_15m = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-cont-hldg-bnifty-long-1-15m',
            'strategy_name': 'INTRADAY_CONTINUATION_HLDG',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 2, 
                'rsi_entry': (90, 10),
                'max_holding': 3,
                'cstick_modes': '2,3',
                'trend_baseline': 10,
                'side_restriction': 1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-cont-hldg-bnifty-long-2-15m',
            'strategy_name': 'INTRADAY_CONTINUATION_HLDG',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 2, 
                'rsi_entry': (95, 5),
                'max_holding': 5,
                'cstick_modes': '6',
                'trend_baseline': 10,
                'side_restriction': 1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-cont-hldg-bnifty-short-1-15m',
            'strategy_name': 'INTRADAY_CONTINUATION_HLDG',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 5, 
                'rsi_entry': (75, 25),
                'max_holding': 3,
                'cstick_modes': '7,8',
                'trend_baseline': 10,
                'side_restriction': -1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-cont-hldg-bnifty-short-2-15m',
            'strategy_name': 'INTRADAY_CONTINUATION_HLDG',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 5, 
                'rsi_entry': (75, 25),
                'max_holding': 5,
                'cstick_modes': '2,3',
                'trend_baseline': 10,
                'side_restriction': -1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 9,
        'client_id': 152,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'SELL', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '15 mins',
        'durationStr': '7 D'
    },
    
    'event_wait_time': 1
}

INTDY_TREND_IB_PARAMS_OPT_TEST_W_NIFTY_multi_5m = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-cont-hldg-nifty-long-1-5m',
            'strategy_name': 'INTRADAY_CONTINUATION_HLDG',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 10, 
                'rsi_entry': (55, 45),
                'max_holding': 5,
                'cstick_modes': '2,3',
                'trend_baseline': 20,
                'side_restriction': 1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-cont-hldg-nifty-long-2-5m',
            'strategy_name': 'INTRADAY_CONTINUATION_HLDG',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 10, 
                'rsi_entry': (55, 45),
                'max_holding': None,
                'cstick_modes': '7,8',
                'trend_baseline': 20,
                'side_restriction': 1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-cont-hldg-nifty-short-1-5m',
            'strategy_name': 'INTRADAY_CONTINUATION_HLDG',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 5, 
                'rsi_entry': (75, 25),
                'max_holding': None,
                'cstick_modes': '2,6,7,8',
                'trend_baseline': 50,
                'side_restriction': -1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 5,
        'client_id': 151,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'SELL', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '3 D'
    },
    
    'event_wait_time': 1
}

INTDY_TREND_IB_PARAMS_OPT_TEST_W_NIFTY_multi_15m = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-cont-hldg-nifty-long-1-15m',
            'strategy_name': 'INTRADAY_CONTINUATION_HLDG',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 3, 
                'rsi_entry': (10, 90),
                'max_holding': 5,
                'cstick_modes': '7,8',
                'trend_baseline': 10,
                'side_restriction': 1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
        {
            'run_name': 'intraday-cont-hldg-nifty-short-1-15m',
            'strategy_name': 'INTRADAY_CONTINUATION_HLDG',
            'params': {
                'rescale_shorts': False,
                'rsi_period': 3, 
                'rsi_entry': (75, 25),
                'max_holding': 5,
                'cstick_modes': '2,7,8',
                'trend_baseline': 10,
                'side_restriction': -1,
                'add_transaction_costs': True,
                'restrict_trade_time': False,
                'inst_delta': 0.5
            }
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 9,
        'client_id': 153,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'SELL', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '15 mins',
        'durationStr': '7 D'
    },
    
    'event_wait_time': 1
}

INTDY_BKOUT_CSTICK_NIFTY = {
    'strategy_name': 'INTRADAY_BREAKOUT_CSTICK',
    'params': {
        'rescale_shorts': False,
        'sl_atr': 1,
        'tp_atr': 10,
        'is_trailing_sl': True,
        'trail_scale': 0.5,
        'lookback_period': 70,
        'add_transaction_costs': False,
        'inst_delta': 1.0
    },
    'api_attrs': {
        'historical_data_offset': 86400 * 9,
        'client_id': 154,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'otm',
            'gap_multiplier': 2,
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '3 D'
    },
    
    'event_wait_time': 1
}

INTDY_BKOUT_CSTICK_RELIANCE = {
    'strategy_name': 'INTRADAY_BREAKOUT_CSTICK',
    'params': {
        'rescale_shorts': False,
        'sl_atr': 0.1,
        'tp_atr': 10,
        'is_trailing_sl': False,
        'lookback_period': 10,
        'add_transaction_costs': False,
        'inst_delta': 1.0
    },
    'api_attrs': {
        'historical_data_offset': 86400 * 9,
        'client_id': 179,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MKT',
            'strike_mode': 'otm',
            'gap_multiplier': 4,
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '15 mins',
        'durationStr': '3 D'
    },
    
    'event_wait_time': 1
}

INTDY_BKOUT_CSTICK_SBIN = {
    'strategy_name': 'INTRADAY_BREAKOUT_CSTICK',
    'params': {
        'rescale_shorts': False,
        'sl_atr': 0.1,
        'tp_atr': 10,
        'is_trailing_sl': False,
        'lookback_period': 10,
        'add_transaction_costs': False,
        'inst_delta': 1.0
    },
    'api_attrs': {
        'historical_data_offset': 86400 * 9,
        'client_id': 180,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MKT',
            'strike_mode': 'otm',
            'gap_multiplier': 2, #we've doubled the strike gap for sbin so only need 2 instead of 4
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '15 mins',
        'durationStr': '3 D'
    },
    
    'event_wait_time': 1
}

INTDY_BKOUT_CSTICK_BANKNIFTY = {
    'strategy_name': 'INTRADAY_BREAKOUT_CSTICK',
    'params': {
        'rescale_shorts': False,
        'sl_atr': 1,
        'tp_atr': 10,
        'is_trailing_sl': True,
        'trail_scale': 0.5,
        'lookback_period': 70,
        'add_transaction_costs': False,
        'inst_delta': 1.0
    },
    'api_attrs': {
        'historical_data_offset': 86400 * 9,
        'client_id': 201,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'otm',
            'gap_multiplier': 4,
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '3 D'
    },
    
    'event_wait_time': 1
}

INTDY_WILLR_BKOUT_BNIFTY_SELLOPT = {
    'strategy_name': 'INTRADAY_WILLR_BREAKOUT',
    'params': {
        'rescale_shorts': False,
        'willr_buy': -20, 
        'willr_sell': -80,
        'willr_period': 30, 
        'entry_scale': 0, 
        'exit_scale': 0.618, 
        'eod_squareoff': False,
        'add_transaction_costs': False,
        'inst_delta': 0.5
    },
    'api_attrs': {
        'historical_data_offset': 86400 * 4,
        'client_id': 157,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'SELL', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '2 D'
    },
    
    'event_wait_time': 1
}

INTDY_WILLR_BKOUT_BNIFTY_BUYOPT = {
    'strategy_name': 'INTRADAY_WILLR_BREAKOUT',
    'params': {
        'rescale_shorts': False,
        'willr_buy': -20, 
        'willr_sell': -80,
        'willr_period': 30, 
        'entry_scale': 0, 
        'exit_scale': 0.618, 
        'eod_squareoff': False,
        'add_transaction_costs': False,
        'inst_delta': 0.5
    },
    'api_attrs': {
        'historical_data_offset': 86400 * 4,
        'client_id': 158,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '2 D'
    },
    
    'event_wait_time': 1
}

INTDY_WILLR_BKOUT_BNIFTY_FUT = {
    'strategy_name': 'INTRADAY_WILLR_BREAKOUT',
    'params': {
        'rescale_shorts': False,
        'willr_buy': -20, 
        'willr_sell': -80,
        'willr_period': 30, 
        'entry_scale': 0, 
        'exit_scale': 0.618, 
        'eod_squareoff': False,
        'add_transaction_costs': False,
        'inst_delta': 1.0
    },
    'api_attrs': {
        'historical_data_offset': 86400 * 4,
        'client_id': 159,
        'order_config': {
            'inst': 'FUT', # can be OPT, FUT, STK
            'order_type': 'MTL',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '2 D'
    },
    
    'event_wait_time': 1
}

INTDY_WILLR_BKOUT_NIFTY_SELLOPT = {
    'strategy_name': 'INTRADAY_WILLR_BREAKOUT',
    'params': {
        'rescale_shorts': False,
        'willr_buy': -10, 
        'willr_sell': -70,
        'willr_period': 14, 
        'entry_scale': 0, 
        'exit_scale': 1, 
        'eod_squareoff': False,
        'add_transaction_costs': False,
        'inst_delta': 0.5
    },
    'api_attrs': {
        'historical_data_offset': 86400 * 4,
        'client_id': 160,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'SELL', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '2 D'
    },
    
    'event_wait_time': 1
}

INTDY_WILLR_BKOUT_NIFTY_BUYOPT = {
    'strategy_name': 'INTRADAY_WILLR_BREAKOUT',
    'params': {
        'rescale_shorts': False,
        'willr_buy': -10, 
        'willr_sell': -70,
        'willr_period': 14, 
        'entry_scale': 0, 
        'exit_scale': 1, 
        'eod_squareoff': False,
        'add_transaction_costs': False,
        'inst_delta': 0.5
    },
    'api_attrs': {
        'historical_data_offset': 86400 * 4,
        'client_id': 161,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '2 D'
    },
    
    'event_wait_time': 1
}

INTDY_WILLR_BKOUT_NIFTY_FUT = {
    'strategy_name': 'INTRADAY_WILLR_BREAKOUT',
    'params': {
        'rescale_shorts': False,
        'willr_buy': -10, 
        'willr_sell': -70,
        'willr_period': 14, 
        'entry_scale': 0, 
        'exit_scale': 1, 
        'eod_squareoff': False,
        'add_transaction_costs': False,
        'inst_delta': 1.0
    },
    'api_attrs': {
        'historical_data_offset': 86400 * 4,
        'client_id': 162,
        'order_config': {
            'inst': 'FUT', # can be OPT, FUT, STK
            'order_type': 'MTL',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '5 mins',
        'durationStr': '2 D'
    },
    
    'event_wait_time': 1
}

INTDY_HA_CCI_IB_PARAMS_OPT_TEST_W_BNIFTY_multi_15m = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-ha-cci-bnifty-short-30m',
            'strategy_name': 'INTRADAY_HA_CCI',
            'params': {
                'rescale_shorts': False,
                'cci_period': 50,
                'cci_entry': (-125, 125),
                'cci_exit': (50, -50),
                'sl_atr': 1,
                'tp_atr': 2,
                'side_restriction': -1,
                'is_trailing_sl': False,
                'add_transaction_costs': False,
                'inst_delta': 1.0
            }
        },
        {
            'run_name': 'intraday-ha-cci-bnifty-long-30m',
            'strategy_name': 'INTRADAY_HA_CCI',
            'params': {
                'rescale_shorts': False,
                'cci_period': 30,
                'cci_entry': (-75, 75),
                'cci_exit': (125, -125),
                'sl_atr': 5,
                'tp_atr': 2,
                'side_restriction': 1,
                'is_trailing_sl': False,
                'add_transaction_costs': False,
                'inst_delta': 1.0
            }
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 9,
        'client_id': 155,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'BUY', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '30 mins',
        'durationStr': '7 D'
    },
    
    'event_wait_time': 1
}

INTDY_HA_CCI_IB_PARAMS_OPT_TEST_W_BNIFTY_SELL_multi_15m = {
    'multi_strategy_params': [
        {
            'run_name': 'intraday-ha-cci-bnifty-sell-short-30m',
            'strategy_name': 'INTRADAY_HA_CCI',
            'params': {
                'rescale_shorts': False,
                'cci_period': 50,
                'cci_entry': (-125, 125),
                'cci_exit': (50, -50),
                'sl_atr': 1,
                'tp_atr': 2,
                'side_restriction': -1,
                'is_trailing_sl': False,
                'add_transaction_costs': False,
                'inst_delta': 1.0
            }
        },
        {
            'run_name': 'intraday-ha-cci-bnifty-sell-long-30m',
            'strategy_name': 'INTRADAY_HA_CCI',
            'params': {
                'rescale_shorts': False,
                'cci_period': 30,
                'cci_entry': (-75, 75),
                'cci_exit': (125, -125),
                'sl_atr': 5,
                'tp_atr': 2,
                'side_restriction': 1,
                'is_trailing_sl': False,
                'add_transaction_costs': False,
                'inst_delta': 1.0
            }
        },
    ],
    'api_attrs': {
        'historical_data_offset': 86400 * 9,
        'client_id': 156,
        'order_config': {
            'inst': 'OPT', # can be OPT, FUT, STK
            'dir': 'SELL', # only applicable for OPT. can be BUY or SELL
            'exp': 'weekly', #only applicable for OPT. can be weekly or monthly
            'order_type': 'MTL',
            'strike_mode': 'atm_minus',
        },
    },
    
    'api_data_config': {
        'barSizeSetting': '30 mins',
        'durationStr': '7 D'
    },
    
    'event_wait_time': 1
}

STRATEGY_IB_CONFIG_MAP = {
    'intraday-pback-cstick-bnifty-multi': INTDY_PBACK_RSI_CSTICK_IB_PARAMS_OPT_TEST_W_BANKNIFTY_multi,
    'intraday-pback-cstick-nifty-multi': INTDY_PBACK_RSI_CSTICK_IB_PARAMS_OPT_TEST_W_NIFTY_multi,
    'intraday-otrade-cstick-bnifty-multi': INTDY_OTRADE_RSI_CSTICK_IB_PARAMS_OPT_TEST_W_BANKNIFTY_multi,
    'intraday-otrade-cstick-nifty-multi': INTDY_OTRADE_RSI_CSTICK_IB_PARAMS_OPT_TEST_W_NIFTY_multi,
    'intraday-mrev-bnifty-multi-5m': INTDY_MREV_IB_PARAMS_OPT_TEST_W_BANKNIFTY_multi_5m,
    'intraday-mrev-nifty-multi-5m': INTDY_MREV_IB_PARAMS_OPT_TEST_W_NIFTY_multi_5m,
    'intraday-mrev-bnifty-multi-15m': INTDY_MREV_IB_PARAMS_OPT_TEST_W_BANKNIFTY_multi_15m,
    'intraday-mrev-nifty-multi-15m': INTDY_MREV_IB_PARAMS_OPT_TEST_W_NIFTY_multi_15m,
    'intraday-trend-bnifty-multi-5m': INTDY_TREND_IB_PARAMS_OPT_TEST_W_BANKNIFTY_multi_5m,
    'intraday-trend-nifty-multi-5m': INTDY_TREND_IB_PARAMS_OPT_TEST_W_NIFTY_multi_5m,
    'intraday-trend-bnifty-multi-15m': INTDY_TREND_IB_PARAMS_OPT_TEST_W_BANKNIFTY_multi_15m,
    'intraday-trend-nifty-multi-15m': INTDY_TREND_IB_PARAMS_OPT_TEST_W_NIFTY_multi_15m,
    'intraday-bkout-cstick-nifty-15m': INTDY_BKOUT_CSTICK_NIFTY,
    'intraday-bkout-cstick-bnifty-15m': INTDY_BKOUT_CSTICK_BANKNIFTY,
    'intraday-bkout-cstick-reliance-15m': INTDY_BKOUT_CSTICK_RELIANCE,
    'intraday-bkout-cstick-sbin-15m': INTDY_BKOUT_CSTICK_SBIN,
    'intraday-ha-cci-bnifty-multi-30m': INTDY_HA_CCI_IB_PARAMS_OPT_TEST_W_BNIFTY_multi_15m,
    'intraday-ha-cci-bnifty-sell-multi-30m': INTDY_HA_CCI_IB_PARAMS_OPT_TEST_W_BNIFTY_SELL_multi_15m,
    'intraday-willr-bkout-nifty-sellopt': INTDY_WILLR_BKOUT_NIFTY_SELLOPT,
    'intraday-willr-bkout-nifty-buyopt': INTDY_WILLR_BKOUT_NIFTY_BUYOPT,
    'intraday-willr-bkout-nifty-fut': INTDY_WILLR_BKOUT_NIFTY_FUT,
    'intraday-willr-bkout-bnifty-sellopt': INTDY_WILLR_BKOUT_BNIFTY_SELLOPT,
    'intraday-willr-bkout-bnifty-buyopt': INTDY_WILLR_BKOUT_BNIFTY_BUYOPT,
    'intraday-willr-bkout-bnifty-fut': INTDY_WILLR_BKOUT_BNIFTY_FUT,
}

NSE_EQ_HOLIDAYS = ["2022-01-26", "2022-03-01", "2022-03-18", "2022-04-14", "2022-04-15", "2022-05-03", "2022-08-09", "2022-08-15", "2022-08-31", "2022-10-05", "2022-10-24", "2022-10-26", "2022-11-08"]
NSE_FX_HOLIDAYS = ["2022-01-26", "2022-02-07", "2022-03-01", "2022-03-18", "2022-04-01", "2022-04-14", "2022-04-15", "2022-05-03", "2022-05-16", "2022-08-09", "2022-08-15", "2022-08-16", "2022-08-31", "2022-10-05", "2022-10-24", "2022-10-26", "2022-11-08"]

OPLACE_FUTURES_SPD_REL_PARAMS = {
    'oplacer_name': 'FUTURES_SPREAD_ORDER',
    'event_wait_time': 2,
    'api_attrs': {
        'client_id': 163,
        'order_config': {
            'inst': 'FUT', # can be OPT, FUT, STK
            'order_type': 'REL',
        },
    },
}

OPLACE_FUTURES_SPD_ADAPT_PARAMS = {
    'oplacer_name': 'FUTURES_SPREAD_ORDER',
    'event_wait_time': 2,
    'api_attrs': {
        'client_id': 164,
        'order_config': {
            'inst': 'FUT',
            'order_type': 'MKT',
            'algo_attrs': {
                'algoStrategy': 'Adaptive',
                'algoParams': {'adaptivePriority': 'Urgent'}
            }
        }
    }
}

OPLACE_FUTURES_SPD_ADAPT_LMT_PARAMS = {
    'oplacer_name': 'FUTURES_SPREAD_ORDER',
    'event_wait_time': 2,
    'api_attrs': {
        'client_id': 165,
        'order_config': {
            'inst': 'FUT',
            'order_type': 'LMT',
            'lmt_offset': 0.05,
            'algo_attrs': {
                'algoStrategy': 'Adaptive',
                'algoParams': {'adaptivePriority': 'Urgent'}
            }
        }
    }
}

OPLACE_FUTURES_SPD_ADAPT_MID_PARAMS = {
    'oplacer_name': 'FUTURES_SPREAD_ORDER',
    'event_wait_time': 2,
    'api_attrs': {
        'client_id': 166,
        'order_config': {
            'inst': 'FUT',
            'order_type': 'LMT',
            'lmt_offset': 'MID',
            'algo_attrs': {
                'algoStrategy': 'Adaptive',
                'algoParams': {'adaptivePriority': 'Urgent'}
            }
        }
    }
}

OPLACE_OPT_BSK_MID_PARAMS_1 = {
    'oplacer_name': 'OPTIONS_BSK_ORDER',
    'event_wait_time': 2,
    'api_attrs': {
        'client_id': 1671,
        'order_config': {
            'inst': 'OPT',
            'order_type': 'LMT',
            'lmt_offset': 'MID',
        }
    }
}

OPLACE_OPT_BSK_MID_PARAMS_2 = {
    'oplacer_name': 'OPTIONS_BSK_ORDER',
    'event_wait_time': 2,
    'api_attrs': {
        'client_id': 1672,
        'order_config': {
            'inst': 'OPT',
            'order_type': 'LMT',
            'lmt_offset': 'MID',
        }
    }
}

OPLACE_OPT_BSK_MID_PARAMS_3 = {
    'oplacer_name': 'OPTIONS_BSK_ORDER',
    'event_wait_time': 2,
    'api_attrs': {
        'client_id': 1673,
        'order_config': {
            'inst': 'OPT',
            'order_type': 'LMT',
            'lmt_offset': 'MID',
        }
    }
}

OPLACE_OPT_BSK_DEPTH_PARAMS_TEST_1 = {
    'oplacer_name': 'OPTIONS_BSK_ORDER_DEPTH',
    'event_wait_time': 2,
    'api_attrs': {
        'client_id': 1674,
        'order_config': {
            'inst': 'OPT',
            'order_type': 'LMT',
            'lmt_offset': 3,
        }
    }
}

OPLACE_OPT_BSK_DEPTH_PARAMS_TEST_2 = {
    'oplacer_name': 'OPTIONS_BSK_ORDER_DEPTH',
    'event_wait_time': 2,
    'api_attrs': {
        'client_id': 1675,
        'order_config': {
            'inst': 'OPT',
            'order_type': 'LMT',
            'lmt_offset': 2,
        }
    }
}

OPLACE_OPT_BSK_DEPTH_PARAMS_TEST_3 = {
    'oplacer_name': 'OPTIONS_BSK_ORDER_DEPTH',
    'event_wait_time': 2,
    'api_attrs': {
        'client_id': 1676,
        'order_config': {
            'inst': 'OPT',
            'order_type': 'LMT',
            'lmt_offset': 3,
        }
    }
}

OPLACE_FUTURES_SPD_MONITOR_ADAPT_PARAMS = {
    'oplacer_name': 'FUTURES_SPREAD_MONITOR_ORDER',
    'event_wait_time': 30,
    'api_attrs': {
        'client_id': 168,
        'order_config': {
            'inst': 'FUT',
            'order_type': 'MKT',
            'algo_attrs': {
                'algoStrategy': 'Adaptive',
                'algoParams': {'adaptivePriority': 'Urgent'}
            }
        }
    }
}

OPLACE_CALLPUT_IV_ARB_MIDADAPT_PARAMS = {
    'oplacer_name': 'CALLPUT_IV_ARB_ORDER',
    'event_wait_time': 30,
    'api_attrs': {
        'client_id': 169,
        'order_config': {
            'order_type_fut': 'MKT',
            'algo_attrs_fut': {
                'algoStrategy': 'Adaptive',
                'algoParams': {'adaptivePriority': 'Urgent'}
            },
            'order_type_opt': 'LMT',
            'lmt_offset_opt': 'MID',
        }
    }
}

OPLACE_CALLPUT_IV_ARB_MIDADAPT_PARAMS_2 = {
    'oplacer_name': 'CALLPUT_IV_ARB_ORDER',
    'event_wait_time': 30,
    'api_attrs': {
        'client_id': 170,
        'order_config': {
            'order_type_fut': 'MKT',
            'algo_attrs_fut': {
                'algoStrategy': 'Adaptive',
                'algoParams': {'adaptivePriority': 'Urgent'}
            },
            'order_type_opt': 'LMT',
            'lmt_offset_opt': 'MID',
        }
    }
}

OPLACE_CAL_IV_STATARB_MID_PARAMS = {
    'oplacer_name': 'CAL_IV_STATARB_ORDER',
    'event_wait_time': 30,
    'api_attrs': {
        'client_id': 171,
        'order_config': {
            'order_type': 'LMT',
            'lmt_offset': 'MID',
        }
    }
}

OPLACE_CAL_IV_STATARB_MID_PARAMS_2 = {
    'oplacer_name': 'CAL_IV_STATARB_ORDER',
    'event_wait_time': 30,
    'api_attrs': {
        'client_id': 172,
        'order_config': {
            'order_type': 'LMT',
            'lmt_offset': 'MID',
        }
    }
}

OPLACE_FUTURES_SPD_BIDASK_PARAMS = {
    'oplacer_name': 'FUTURES_HEDGE_BIDASK_DYNAMIC_ORDER',
    'event_wait_time': 5,
    'api_attrs': {
        'client_id': 173,
        'order_config': {
            'order_type_hedge': 'MTL',
            'ba_max_limit': 0.4
        }
    }
}

OPLACE_FUTURES_SPD_BIDASK_PARAMS2 = {
    'oplacer_name': 'FUTURES_HEDGE_BIDASK_DYNAMIC_ORDER',
    'event_wait_time': 5,
    'api_attrs': {
        'client_id': 176,
        'order_config': {
            'order_type_hedge': 'MTL',
            'ba_max_limit': 0.4
        }
    }
}

OPLACE_OPT_BSK_BIDASK_DYN_PARAMS = {
    'oplacer_name': 'OPTIONS_BSK_BIDASK_DYNAMIC',
    'event_wait_time': 5,
    'api_attrs': {
        'client_id': 174,
        'order_config': {
            'lmt_offset': 0.05,
            'static_reset': False,
            'ba_max_limit': 0.4
        }
    }
}

OPLACE_OPT_BSK_BIDASK_DYN_FX_PARAMS = {
    'oplacer_name': 'OPTIONS_BSK_BIDASK_DYNAMIC',
    'event_wait_time': 5,
    'api_attrs': {
        'client_id': 178,
        'order_config': {
            'lmt_offset': 0.0025,
            'static_reset': False,
            'ba_max_limit': 0.4
        }
    }
}

OPLACE_FUT_BSK_BIDASK_DYN_PARAMS = {
    'oplacer_name': 'FUTURES_BSK_BIDASK_DYNAMIC_ORDER',
    'event_wait_time': 5,
    'api_attrs': {
        'client_id': 175,
        'order_config': {
            'lmt_offset': 0.05,
            'static_reset': True,
            'ba_max_limit': 0.4
        }
    }
}

OPLACE_OPTIONS_HDG_BIDASK_PARAMS = {
    'oplacer_name': 'OPTIONS_HEDGE_BIDASK_DYNAMIC_ORDER',
    'event_wait_time': 5,
    'api_attrs': {
        'client_id': 177,
        'order_config': {
            'order_type_hedge': 'MTL',
            'ba_max_limit': 0.4
        }
    }
}

OPLACER_IB_CONFIG_MAP = {
    'futures-spread-rel': OPLACE_FUTURES_SPD_REL_PARAMS,
    'futures-spread-adapt': OPLACE_FUTURES_SPD_ADAPT_PARAMS,
    'futures-spread-adaptlmt': OPLACE_FUTURES_SPD_ADAPT_LMT_PARAMS,
    'futures-spread-adaptmid': OPLACE_FUTURES_SPD_ADAPT_MID_PARAMS,
    'futures-spread-monitor-adapt': OPLACE_FUTURES_SPD_MONITOR_ADAPT_PARAMS,
    'futures-spread-bidask': OPLACE_FUTURES_SPD_BIDASK_PARAMS,
    'futures-spread-bidask2': OPLACE_FUTURES_SPD_BIDASK_PARAMS2,
    'fut-bsk-bidask-dyn': OPLACE_FUT_BSK_BIDASK_DYN_PARAMS,
    'opt-bsk-mid-1': OPLACE_OPT_BSK_MID_PARAMS_1,
    'opt-bsk-mid-2': OPLACE_OPT_BSK_MID_PARAMS_2,
    'opt-bsk-mid-3': OPLACE_OPT_BSK_MID_PARAMS_3,
    'opt-bsk-depth-1': OPLACE_OPT_BSK_DEPTH_PARAMS_TEST_1,
    'opt-bsk-depth-2': OPLACE_OPT_BSK_DEPTH_PARAMS_TEST_2,
    'opt-bsk-depth-3': OPLACE_OPT_BSK_DEPTH_PARAMS_TEST_3,
    'opt-bsk-bidask-dyn': OPLACE_OPT_BSK_BIDASK_DYN_PARAMS,
    'opt-bsk-bidask-dyn-fx': OPLACE_OPT_BSK_BIDASK_DYN_FX_PARAMS,
    'opt-hdg-bidask-dyn': OPLACE_OPTIONS_HDG_BIDASK_PARAMS,
    'callput-iv-arb-midadapt': OPLACE_CALLPUT_IV_ARB_MIDADAPT_PARAMS,
    'callput-iv-arb-midadapt2': OPLACE_CALLPUT_IV_ARB_MIDADAPT_PARAMS_2,
    'cal-iv-statarb-mid': OPLACE_CAL_IV_STATARB_MID_PARAMS,
    'cal-iv-statarb-mid2': OPLACE_CAL_IV_STATARB_MID_PARAMS_2,
}