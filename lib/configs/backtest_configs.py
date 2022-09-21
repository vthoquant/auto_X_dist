# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 14:35:59 2020

@author: vivin
"""
import copy

MOMENTUM_REBAL_BT_PARAMS = {
    'strategy_name': 'MOMENTUM_REBAL_STRATEGY',
    'params': {
        'rebal_freq_days': 7,
        'ma_window': 10,
        'M_c': 0.0
    }
}

MULTICLASS_DECTREE_REBAL_BT_PARAMS = {
    'strategy_name': 'MULTICLASS_CLASSIFIER_REBAL',
    'params':{
        'rebal_freq_days': 7,
        'do_pca': False,
        'predict_probab_thresh': 0.5,
        'use_sample_weights': False,
        'model_params': {
            'name': 'DecisionTreeClassifier', 
            'params': {'max_depth': 10, 'random_state': 40}
        }
    }
}

MULTICLASS_SVC_REBAL_BT_PARAMS = {
    'strategy_name': 'MULTICLASS_CLASSIFIER_REBAL',
    'params':{
        'rebal_freq_days': 7,
        'do_pca': True,
        'use_sample_weights': True,
        'model_params': {
            'name': 'SVC', 
            'params': {"C": 2, "kernel": 'poly'}
        }
    }
}

MULTICLASS_KNN_REBAL_BT_PARAMS_D = {
    'strategy_name': 'MULTICLASS_CLASSIFIER_REBAL',
    'params':{
        'rebal_freq_days': 7,
        'do_pca': True,
        'predict_probab_thresh': 0.5,
        'model_params': {
            'name': 'KNN', 
            'params': {"n_neighbors": 10, "weights": 'distance', "p": 2}
        }
    }
}

MULTICLASS_KNN_REBAL_BT_PARAMS_U = {
    'strategy_name': 'MULTICLASS_CLASSIFIER_REBAL',
    'params':{
        'rebal_freq_days': 7, 
        'do_pca': True,
        'predict_probab_thresh': 0.5,
        'model_params': {
            'name': 'KNN', 
            'params': {"n_neighbors": 10, "weights": 'uniform', "p": 2}
        }
    }
}

MULTICLASS_GNB_REBAL_BT_PARAMS = {
    'strategy_name': 'MULTICLASS_CLASSIFIER_REBAL',
    'params':{
        'rebal_freq_days': 7, 
        'model_params': {}
    }
}

MULTICLASS_KNN_REBAL_BT_PARAMS_U_BAGGED = {
    'strategy_name': 'MULTICLASS_CLASSIFIER_REBAL',
    'params':{
        'rebal_freq_days': 7, 
        'model_params': {
            'name': 'BaggedKNN', 
            'base_model_params': {"n_neighbors": 10, "weights": 'uniform', "p": 1},
            'params': {'max_samples': 0.5, 'max_features': 0.5, 'random_state': 40}
        }
    }
}

MULTICLASS_KNN_REBAL_BT_PARAMS_D_BAGGED = {
    'strategy_name': 'MULTICLASS_CLASSIFIER_REBAL',
    'params':{
        'rebal_freq_days': 7, 
        'model_params': {
            'name': 'BaggedKNN', 
            'base_model_params': {"n_neighbors": 10, "weights": 'distance', "p": 1},
            'params': {'max_samples': 0.5, 'max_features': 0.5, 'random_state': 40}
        }
    }
}

MULTICLASS_GBOOSTING_REBAL_BT_PARAMS = {
    'strategy_name': 'MULTICLASS_CLASSIFIER_REBAL',
    'params':{
        'rebal_freq_days': 7, 
        'model_params': {
            'name': 'GradientBoostingClassifier', 
            'params': {"n_estimators": 30, "loss": 'deviance', "learning_rate": 0.5, "subsample": 0.5, "max_depth": 2, 'random_state': 40},
        }
    }
}

MULTICLASS_RFOREST_REBAL_BT_PARAMS = {
    'strategy_name': 'MULTICLASS_CLASSIFIER_REBAL',
    'params':{
        'rebal_freq_days': 7, 
        'model_params': {
            'name': 'RandomForestClassifier', 
            'params': {"n_estimators": 300, "criterion": 'entropy', "max_depth": 5, 'random_state': 40},
        }
    }
}

MULTICLASS_XGBOOST_REBAL_BT_PARAMS = {
    'strategy_name': 'MULTICLASS_CLASSIFIER_REBAL',
    'params':{
        'rebal_freq_days': 7,
        'do_pca': False,
        'predict_probab_thresh': 0.5,
        'use_sample_weights': False,
        'model_params': {
            'name': 'XGBoostClassifier',
            'params': {"n_estimators": 100, 'objective': "multi:softprob", "learning_rate": 0.1, "subsample": 0.2, "max_depth": 3, 'random_state': 40},
        }
    }
}

MULTICLASS_ADABOOST_REBAL_BT_PARAMS = {
    'strategy_name': 'MULTICLASS_CLASSIFIER_REBAL',
    'params':{
        'rebal_freq_days': 7, 
        'model_params': {
            'name': 'AdaBoostedTree',
            'params': {"n_estimators": 30, "learning_rate": 0.5, 'random_state': 40},
        }
    }
}

MULTICLASS_MLP_REBAL_BT_PARAMS = {
    'strategy_name': 'MULTICLASS_CLASSIFIER_REBAL',
    'params':{
        'rebal_freq_days': 7, 
        'model_params': {
            'name': 'MLP',
            'params': {"hidden_layer_sizes": 10, "activation": 'relu', 'solver': 'adam', 'random_state': 401},
        }
    }
}

PORTFOLIO_MOM_REBAL_BT_PARAMS = {
    'strategy_name': 'PORTFOLIO_MOM_REBAL',
    'params': {
        'rebal_freq_days': 2,
        'ma_window': 10,
        'M_c': -0.01,
        'static_tickers': [
            "CARBORUNIV.NS", "KSCL.NS", "MAANALU.NS", "REMSONSIND.NS", "BAJAJ-AUTO.NS", "HEROMOTOCO.NS", "ASALCBR.NS",
            "POLYCAB.NS", "GTPL.NS", "HEIDELBERG.NS", "SHREDIGCEM.NS", "OAL.NS", "COMPINFO.NS", "PNCINFRA.NS",
            "RVNL.NS", "THANGAMAYL.NS", "GSPL.NS", "AIAENG.NS", "BEL.NS", "MAITHANALL.NS", "CHAMBLFERT.NS",
            "TATACHEM.NS", "MGL.NS", "INDRAMEDCO.NS", "HGINFRA.NS", "DPWIRES.NS", "KSL.NS", "JSLHISAR.NS",
            "MPHASIS.NS", "GREENLAM.NS", "GEEKAYWIRE.NS", "COSMOFILMS.NS", "JINDALPOLY.NS", "JKPAPER.NS", "NAHARPOLY.NS",
            "BHARATRAS.NS", "IOLCP.NS", "GRANULES.NS", "AUROPHARMA.NS", "DRREDDY.NS", "FINPIPE.NS", "GPPL.NS",
            "POWERGRID.NS", "NUCLEUS.NS", "ANDHRSUGAR.NS", "TRIVENI.NS", "CCL.NS", "RITES.NS", "WELSPUNIND.NS", "TVTODAY.NS", "^NSEI", "^NSEMDCP50", "^CRSLDX"
        ],
        'default_weight_alloc': [
            0.03, 0.02, 0.01, 0.01, 0.03, 0.03, 0.02,
            0.03, 0.02, 0.02, 0.02, 0.02, 0.01, 0.02,
            0.01, 0.02, 0.03, 0.03, 0.03, 0.01, 0.03,
            0.03, 0.03, 0.02, 0.01, 0.01, 0.02, 0.02,
            0.02, 0.02, 0.01, 0.02, 0.01, 0.01, 0.01,
            0.02, 0.02, 0.02, 0.03, 0.03, 0.01, 0.02,
            0.03, 0.02, 0.02, 0.02, 0.01, 0.02, 0.02, 0.02, 0.0, 0.0, 0.0
        ],
        'reweight': True,
        'reweight_max_wt': 0.1
    }
}
'''
PORTOFLIO_MOM_REBAL_TALIB_BT_PARAMS = copy.deepcopy(PORTFOLIO_MOM_REBAL_BT_PARAMS)
PORTOFLIO_MOM_REBAL_TALIB_BT_PARAMS['strategy_name'] = 'PORTFOLIO_TALIB_REBAL'
PORTOFLIO_MOM_REBAL_TALIB_BT_PARAMS['params']['ma_window'] = 10
PORTOFLIO_MOM_REBAL_TALIB_BT_PARAMS['params']['ind_thresh'] = 15
PORTOFLIO_MOM_REBAL_TALIB_BT_PARAMS['params']['rebal_freq_days'] = 2
PORTOFLIO_MOM_REBAL_TALIB_BT_PARAMS['params']['ind_type'] = 'supershort'
'''
PORTOFLIO_MOM_REBAL_TALIB_BT_PARAMS = copy.deepcopy(PORTFOLIO_MOM_REBAL_BT_PARAMS)
PORTOFLIO_MOM_REBAL_TALIB_BT_PARAMS['strategy_name'] = 'PORTFOLIO_TALIB_REBAL'
PORTOFLIO_MOM_REBAL_TALIB_BT_PARAMS['params']['ma_window'] = 1
PORTOFLIO_MOM_REBAL_TALIB_BT_PARAMS['params']['ind_thresh'] = -16
PORTOFLIO_MOM_REBAL_TALIB_BT_PARAMS['params']['rebal_freq_days'] = 1
PORTOFLIO_MOM_REBAL_TALIB_BT_PARAMS['params']['ind_type'] = 'def'

PORTFOLIO_STATIC_REBAL_BT_PARAMS = copy.deepcopy(PORTFOLIO_MOM_REBAL_BT_PARAMS)
PORTFOLIO_STATIC_REBAL_BT_PARAMS['strategy_name'] = 'PORTFOLIO_STATIC_REBAL'
PORTFOLIO_STATIC_REBAL_BT_PARAMS['params']['rebal_freq_days'] = 10
del PORTFOLIO_STATIC_REBAL_BT_PARAMS['params']['ma_window']
del PORTFOLIO_STATIC_REBAL_BT_PARAMS['params']['M_c']

PORTFOLIO_STATIC_BT_PARAMS = copy.deepcopy(PORTFOLIO_STATIC_REBAL_BT_PARAMS)
PORTFOLIO_STATIC_BT_PARAMS['strategy_name'] = 'PORTFOLIO_STATIC'
PORTFOLIO_STATIC_BT_PARAMS['params']['rebal_on_new'] = True
del PORTFOLIO_STATIC_BT_PARAMS['params']['rebal_freq_days']

INTDY_TREND_CAPTURE_BT_PARAMS = {
    'strategy_name': 'INTRADAY_TREND_CAPTURE',
    'params':{
        'trade_agr_score': 0,
        'sqoff_agr_score': 3,
        'ema_kwargs': {'timeperiod': 20},
        'rescale_shorts': False
    }
}

INTDY_TREND_HEIKIN_BT_PARAMS = {
    'strategy_name': 'INTRADAY_TREND_HEIKIN',
    'params':{
        'rescale_shorts': False,
        'barsize_thresh_trade': 3,
        'stop_loss': 1,
        'ema_baseline': 50,
        'add_transaction_costs': False
    }
}

INTDY_TREND_HEIKIN2_BT_PARAMS = {
    'strategy_name': 'INTRADAY_TREND_HEIKIN_2',
    'params':{
        'rescale_shorts': False,
        'ema_baseline': 50,
        'ignore_indecisive': False,
        'add_transaction_costs': True,
        'inst_delta': 1.0
    }
}

INTDY_TREND_HEIKIN3_BT_PARAMS = {
    'strategy_name': 'INTRADAY_TREND_HEIKIN_3',
    'params':{
        'rescale_shorts': False,
        'ema_baseline': 50,
        'sl_on_ha': True,
        'add_transaction_costs': True,
        'inst_delta': 1.0
    }
}

INTDY_MA_BT_PARAMS = {
    'strategy_name': 'INTRADAY_MA',
    'params': {
        'rescale_shorts': False,
        'ema_window': 100,
        'on_heikin_ashi': True,
        'eod_sqoff': False,
        'add_transaction_costs': True,
        'inst_delta': 1.0
    }
}

INTDY_MAC_BT_PARAMS = {
    'strategy_name': 'INTRADAY_MAC',
    'params': {
        'rescale_shorts': False,
        'ema_window_short': 60,
        'ema_long_window_mult': 2,
        'add_transaction_costs': True,
        'wait_for_crossover': False,
        'restrict_trade_time': False,
        'inst_delta': 1.0
    }
}

INTDY_MACD_BT_PARAMS = {
    'strategy_name': 'INTRADAY_MACD',
    'params': {
        'rescale_shorts': False,
        'window_short': 5,
        'long_window_mult': 1.2,
        'signal_window_mult': 1,
        'add_transaction_costs': True,
        'restrict_trade_time': True,
        'inst_delta': 0.5
    }
}

INTDY_MACD_TPSL_BT_PARAMS = {
    'strategy_name': 'INTRADAY_MACD_TP_SL',
    'params': {
        'rescale_shorts': False,
        'window_short': 10,
        'long_window_mult': 1.5,
        'signal_window_mult': 0.5,
        'tp_atr': 10,
        'sl_atr': 2,
        'is_trailing_sl': False,
        'watch_reversal': False,
        'add_transaction_costs': True,
        'restrict_trade_time': True,
        'inst_delta': 1.0
    }
}

INTDY_MAC_SL_BT_PARAMS = {
    'strategy_name': 'INTRADAY_MAC_SL',
    'params': {
        'rescale_shorts': False,
        'ema_window_short': 60,
        'ema_long_window_mult': 2,
        'add_transaction_costs': True,
        'stop_loss': 3,
        'inst_delta': 1.0
    }
}

INTDY_MAC_MA_BT_PARAMS = {
    'strategy_name': 'INTRADAY_MAC_MA',
    'params': {
        'rescale_shorts': False,
        'ema_window_short': 50,
        'ema_long_window_mult': 3,
        'ema_window_cutoff': 10,
        'add_transaction_costs': True,
        'inst_delta': 1.0
    }
}

INTDY_PULLBACK_BT_PARAMS = {
    'strategy_name': 'INTRADAY_PULLBACK',
    'params': {
        'rescale_shorts': False,
        'rsi_period': 2, 
        'rsi_entry': (10, 90),
        'rsi_exit': (40, 60),
        'max_holding': 5,
        'trend_baseline': 100,
        'side_restriction': 1,
        'add_transaction_costs': True,
        'restrict_trade_time': False,
        'inst_delta': 0.5
    }
}

INTDY_PULLBACK_CRSI_BT_PARAMS = {
    'strategy_name': 'INTRADAY_PULLBACK_CUMUL_RSI',
    'params': {
        'rescale_shorts': False,
        'rsi_period': 2,
        'cumul_rsi_period': 2,
        'rsi_entry': (10, 90),
        'rsi_exit': (40, 60),
        'max_holding': 5,
        'trend_baseline': 100,
        'side_restriction': 1,
        'add_transaction_costs': True,
        'restrict_trade_time': False,
        'inst_delta': 0.5
    }
}

INTDY_PULLBACK_LB_BT_PARAMS = {
    'strategy_name': 'INTRADAY_PULLBACK_PRICE_LB',
    'params': {
        'rescale_shorts': False,
        'rsi_period': 2, 
        'lb_period': 10,
        'rsi_exit': (55, 45),
        'max_holding': 5,
        'trend_baseline': 100,
        'add_transaction_costs': True,
        'restrict_trade_time': False,
        'inst_delta': 1.0
    }
}

INTDY_PULLBACK_BB_BT_PARAMS = {
    'strategy_name': 'INTRADAY_PULLBACK_BB',
    'params': {
        'rescale_shorts': False,
        'bb_period': 20, 
        'bb_stdev': 2.0,
        'trend_baseline': 100,
        'add_transaction_costs': True,
        'inst_delta': 1.0
    }
}

INTDY_PULLBACK_CSTICK_REV_BT_PARAMS = {
    'strategy_name': 'INTRADAY_PULLBACK_CSTICK_REV',
    'params': {
        'rescale_shorts': False,
        'rsi_period': 5, 
        'rsi_entry': (20, 80),
        'rsi_exit': (55, 45),
        'max_holding': 5,
        'cstick_modes': '1,2,3,4,5',
        'trend_baseline': 100,
        'side_restriction': None,
        'add_transaction_costs': True,
        'restrict_trade_time': False,
        'inst_delta': 0.5
    }
}

INTDY_OT_RSI_BT_PARAMS = {
    'strategy_name': 'INTRADAY_OVERTRADE_RSI',
    'params': {
        'rescale_shorts': False,
        'rsi_period': 3, 
        'rsi_entry': (10, 90),
        'rsi_exit': (55, 45),
        'max_holding': 3,
        'trend_baseline_long': 100,
        'trend_baseline_short': 20,
        'side_restriction': -1,
        'add_transaction_costs': True,
        'restrict_trade_time': True,
        'inst_delta': 0.5
    }
}

INTDY_OT_CUMUL_RSI_BT_PARAMS = {
    'strategy_name': 'INTRADAY_OVERTRADE_CUMUL_RSI',
    'params': {
        'rescale_shorts': False,
        'rsi_period': 2,
        'cumul_rsi_period': 2,
        'rsi_entry': (10, 90),
        'rsi_exit': (40, 60),
        'side_restriction': 1,
        'max_holding': 5,
        'trend_baseline_long': 100,
        'trend_baseline_short': 20,
        'add_transaction_costs': True,
        'restrict_trade_time': True,
        'inst_delta': 0.5
    }
}

INTDY_OT_LB_BT_PARAMS = {
    'strategy_name': 'INTRADAY_OVERTRADE_PRICE_LB',
    'params': {
        'rescale_shorts': False,
        'rsi_period': 2, 
        'lb_period': 10,
        'rsi_exit': (55, 45),
        'max_holding': 5,
        'trend_baseline_short': 10,
        'trend_baseline_long': 100,
        'add_transaction_costs': True,
        'restrict_trade_time': False,
        'inst_delta': 1.0
    }
}

INTDY_OT_BB_BT_PARAMS = {
    'strategy_name': 'INTRADAY_OVERTRADE_BB',
    'params': {
        'rescale_shorts': False,
        'bb_period': 20, 
        'bb_stdev': 2.0,
        'trend_baseline': 100,
        'max_holding': 5,
        'add_transaction_costs': True,
        'inst_delta': 1.0
    }
}

INTDY_OTRADE_RSI_CSTICK_REV_BT_PARAMS = {
    'strategy_name': 'INTRADAY_OVERTRADE_RSI_CSTICK_REV',
    'params': {
        'rescale_shorts': False,
        'rsi_period': 5, 
        'rsi_entry': (20, 80),
        'rsi_exit': (55, 45),
        'max_holding': 5,
        'cstick_modes': '1,2,3,4,5',
        'trend_baseline_long': 100,
        'trend_baseline_short': 20,
        'side_restriction': None,
        'add_transaction_costs': True,
        'restrict_trade_time': False,
        'inst_delta': 0.5
    }
}

INTDY_CONT_HLDG_BT_PARAMS = {
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
}

INTDY_CONT_ATRTP_BT_PARAMS = {
    'strategy_name': 'INTRADAY_CONTINUATION_ATRTP',
    'params': {
        'rescale_shorts': False,
        'rsi_period': 5, 
        'rsi_entry': (75, 25),
        'atr_tp': 2,
        'cstick_modes': '3,4,6',
        'trend_baseline': 50,
        'side_restriction': None,
        'add_transaction_costs': True,
        'restrict_trade_time': False,
        'inst_delta': 0.5
    }
}

INTDY_CONT_ATRSLSHIFT_BT_PARAMS = {
    'strategy_name': 'INTRADAY_CONTINUATION_ATRSLSHIFT',
    'params': {
        'rescale_shorts': False,
        'rsi_period': 5, 
        'rsi_entry': (75, 25),
        'atr_tp': 2,
        'cstick_modes': '3,4,6',
        'trend_baseline': 50,
        'side_restriction': None,
        'add_transaction_costs': True,
        'restrict_trade_time': False,
        'inst_delta': 0.5
    }
}

INTDY_BB_BT_PARAMS = {
    'strategy_name': 'INTRADAY_BB',
    'params': {
        'rescale_shorts': False,
        'bb_period': 20, 
        'bb_stdev': 2.0,
        'max_holding': 5,
        'add_transaction_costs': True,
        'inst_delta': 1.0
    }
}

INTDY_BKOUT_HILO_BT_PARAMS = {
    'strategy_name': 'INTRADAY_BREAKOUT_HILO',
    'params': {
        'rescale_shorts': False,
        'sl_atr': 5,
        'tp_atr': 5,
        'is_trailing_sl': False,
        'false_breakout': True,
        'add_transaction_costs': True,
        'inst_delta': 1.0
    }
}

INTDY_HA_CCI_BT_PARAMS = {
    'strategy_name': 'INTRADAY_HA_CCI',
    'params': {
        'rescale_shorts': False,
        'cci_period': 40,
        'cci_entry': (-100, 100),
        'cci_exit': (75, -75),
        'sl_atr': 5,
        'tp_atr': 10,
        'side_restriction': 1,
        'is_trailing_sl': True,
        'add_transaction_costs': False,
        'inst_delta': 1.0
    }
}

INTDY_BKOUT_CSTICK_BT_PARAMS = {
    'strategy_name': 'INTRADAY_BREAKOUT_CSTICK',
    'params': {
        'rescale_shorts': False,
        'sl_atr': 1,
        'tp_atr': 1,
        'is_trailing_sl': False,
        'lookback_period': 1,
        'add_transaction_costs': False,
        'inst_delta': 1.0
    }
}

INTDY_DBLBKOUT_CSTICK_BT_PARAMS = {
    'strategy_name': 'INTRADAY_DBLBREAKOUT_CSTICK',
    'params': {
        'rescale_shorts': False,
        'sl_atr': 0.1,
        'tp_atr': 2,
        'is_trailing_sl': False,
        'lookback_period': 10,
        'eod_lookback_period': 3,
        'add_transaction_costs': False,
        'inst_delta': 1.0
    }
}

FUTURES_SPREAD_STATARB_PARAMS = {
    'strategy_name': 'FUTURES_SPREAD_STATARB',
    'params': {
        'add_transaction_costs': True
    }
}

STRATEGY_BT_CONFIG_MAP = {
    'mom-rebal': MOMENTUM_REBAL_BT_PARAMS,
    'multiclass-dectree': MULTICLASS_DECTREE_REBAL_BT_PARAMS,
    'multiclass-svc': MULTICLASS_SVC_REBAL_BT_PARAMS,
    'multiclass-knn-d': MULTICLASS_KNN_REBAL_BT_PARAMS_D,
    'multiclass-knn-u': MULTICLASS_KNN_REBAL_BT_PARAMS_U,
    'multiclass-gnb': MULTICLASS_GNB_REBAL_BT_PARAMS,
    'multiclass-knn-u-bagged': MULTICLASS_KNN_REBAL_BT_PARAMS_U_BAGGED,
    'multiclass-knn-d-bagged': MULTICLASS_KNN_REBAL_BT_PARAMS_D_BAGGED,
    'multiclass-gboosting': MULTICLASS_GBOOSTING_REBAL_BT_PARAMS,
    'multiclass-rforest': MULTICLASS_RFOREST_REBAL_BT_PARAMS,
    'multiclass-xgb': MULTICLASS_XGBOOST_REBAL_BT_PARAMS,
    'multiclass-adaboost': MULTICLASS_ADABOOST_REBAL_BT_PARAMS,
    'multiclass-mlp': MULTICLASS_MLP_REBAL_BT_PARAMS,
    'portfolio-mom-rebal': PORTFOLIO_MOM_REBAL_BT_PARAMS,
    'portfolio-rebal-talib': PORTOFLIO_MOM_REBAL_TALIB_BT_PARAMS,
    'portfolio-static-rebal': PORTFOLIO_STATIC_REBAL_BT_PARAMS,
    'portfolio-static': PORTFOLIO_STATIC_BT_PARAMS,
    'intraday-trend': INTDY_TREND_CAPTURE_BT_PARAMS,
    'intraday-trend-heikin': INTDY_TREND_HEIKIN_BT_PARAMS,
    'intraday-trend-heikin2': INTDY_TREND_HEIKIN2_BT_PARAMS,
    'intraday-trend-heikin3': INTDY_TREND_HEIKIN3_BT_PARAMS,
    'intraday-ma': INTDY_MA_BT_PARAMS,
    'intraday-mac': INTDY_MAC_BT_PARAMS,
    'intraday-mac-sl': INTDY_MAC_SL_BT_PARAMS,
    'intraday-mac-ma': INTDY_MAC_MA_BT_PARAMS,
    'intraday-macd': INTDY_MACD_BT_PARAMS,
    'intraday-macd-tpsl': INTDY_MACD_TPSL_BT_PARAMS,
    'intraday-pullback': INTDY_PULLBACK_BT_PARAMS,
    'intraday-pullback-crsi': INTDY_PULLBACK_CRSI_BT_PARAMS,
    'intraday-pullback-lb': INTDY_PULLBACK_LB_BT_PARAMS,
    'intraday-pullback-bb': INTDY_PULLBACK_BB_BT_PARAMS,
    'intraday-pullback-cstick-rev': INTDY_PULLBACK_CSTICK_REV_BT_PARAMS,
    'intraday-otrade-rsi': INTDY_OT_RSI_BT_PARAMS,
    'intraday-otrade-crsi': INTDY_OT_CUMUL_RSI_BT_PARAMS,
    'intraday-otrade-lb': INTDY_OT_LB_BT_PARAMS,
    'intraday-otrade-bb': INTDY_OT_BB_BT_PARAMS,
    'intraday-otrade-rsi-cstick-rev': INTDY_OTRADE_RSI_CSTICK_REV_BT_PARAMS,
    'intraday-cont-hldg': INTDY_CONT_HLDG_BT_PARAMS,
    'intraday-cont-atrtp': INTDY_CONT_ATRTP_BT_PARAMS,
    'intraday-cont-atrslshift': INTDY_CONT_ATRSLSHIFT_BT_PARAMS,
    'intraday-bb': INTDY_BB_BT_PARAMS,
    'intraday-bkout-hilo': INTDY_BKOUT_HILO_BT_PARAMS,
    'intraday-bkout-cstick': INTDY_BKOUT_CSTICK_BT_PARAMS,
    'intraday-dblbkout-cstick': INTDY_DBLBKOUT_CSTICK_BT_PARAMS,
    'intraday-ha-cci': INTDY_HA_CCI_BT_PARAMS,
    'futures-spread-nifty': FUTURES_SPREAD_STATARB_PARAMS,
    'test': PORTFOLIO_MOM_REBAL_BT_PARAMS,
}