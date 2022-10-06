# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 08:34:19 2020

@author: vivin
"""
from lib.utils import utils
import numpy as np
import copy
import itertools

MOMENTUM_REBAL_M_c = [0.0]
MOMENTUM_REBAL_WINDOW = [1, 2, 5, 7, 10, 20, 50, 100]
MOMENTUM_REBAL_PARAMS = {
    'rebal_freq_days': MOMENTUM_REBAL_WINDOW,
    'ma_window': MOMENTUM_REBAL_WINDOW,
    'M_c': MOMENTUM_REBAL_M_c
}
MOMENTUM_REBAL_OPT_CONFIGS = utils.params_iterator(MOMENTUM_REBAL_PARAMS)

MULTICLASS_REBAL_GLOBAL_CONFIGS_1 = {
    'do_pca': [True, False],
    'predict_probab_thresh': [-1, 0.5, 0.7]
}

MULTICLASS_REBAL_GLOBAL_CONFIGS_2 = {
    'do_pca': [True, False],
    'use_sample_weights': [True, False],
    'predict_probab_thresh': [-1, 0.5, 0.7]
}

MULTICLASS_REBAL_GLOBAL_CONFIGS_3 = {
    'do_pca': [True, False],
    'predict_probab_thresh': [-1, 0.5, 0.7]
}

MULTICLASS_REBAL_PARAMS_DT = {"max_depth": [1, 2, 3, 5, 10], 'random_state': [40]}
MULTICLASS_REBAL_OPT_CONFIGS_DT = utils.params_iterator(MULTICLASS_REBAL_PARAMS_DT)
#MULTICLASS_REBAL_OPT_CONFIGS_DT = [{'use_sample_weights': False, 'model_params':{'name': 'DecisionTreeClassifier', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_DT] + [{'use_sample_weights': True, 'model_params':{'name': 'DecisionTreeClassifier', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_DT]
MULTICLASS_REBAL_OPT_CONFIGS_DT_MP = {'model_params':[{'name': 'DecisionTreeClassifier', 'params': x} for x in MULTICLASS_REBAL_OPT_CONFIGS_DT]}
MULTICLASS_REBAL_OPT_CONFIGS_DT = utils.params_iterator({**MULTICLASS_REBAL_GLOBAL_CONFIGS_2, **MULTICLASS_REBAL_OPT_CONFIGS_DT_MP})

MULTICLASS_REBAL_PARAMS_SVC = {
    "C": [1, 2, 4], 
    "kernel": ['linear', 'poly', 'rbf'],
    "probability": [True]
}
MULTICLASS_REBAL_OPT_CONFIGS_SVC = utils.params_iterator(MULTICLASS_REBAL_PARAMS_SVC)
#MULTICLASS_REBAL_OPT_CONFIGS_SVC = [{'use_sample_weights': True, 'model_params':{'name': 'SVC', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_SVC] + [{'use_sample_weights': False, 'model_params':{'name': 'SVC', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_SVC]
MULTICLASS_REBAL_OPT_CONFIGS_SVC_MP = {'model_params':[{'name': 'SVC', 'params': x} for x in MULTICLASS_REBAL_OPT_CONFIGS_SVC]}
MULTICLASS_REBAL_OPT_CONFIGS_SVC = utils.params_iterator({**MULTICLASS_REBAL_GLOBAL_CONFIGS_2, **MULTICLASS_REBAL_OPT_CONFIGS_SVC_MP})

MULTICLASS_REBAL_PARAMS_KNN = {
    'n_neighbors': [5, 10, 20, 50, 100],
    'weights': ['uniform', 'distance'],
    'algorithm': ['auto'],
    'p': [1, 2]
}
MULTICLASS_REBAL_OPT_CONFIGS_KNN = utils.params_iterator(MULTICLASS_REBAL_PARAMS_KNN)
#MULTICLASS_REBAL_OPT_CONFIGS_KNN = [{'model_params':{'name': 'KNN', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_KNN]
MULTICLASS_REBAL_OPT_CONFIGS_KNN_MP = {'model_params':[{'name': 'KNN', 'params': x} for x in MULTICLASS_REBAL_OPT_CONFIGS_KNN]}
MULTICLASS_REBAL_OPT_CONFIGS_KNN = utils.params_iterator({**MULTICLASS_REBAL_GLOBAL_CONFIGS_1, **MULTICLASS_REBAL_OPT_CONFIGS_KNN_MP})

MULTICLASS_REBAL_PARAMS_RFC = {
    'n_estimators': [10, 30, 100, 300],
    'criterion': ['gini', 'entropy'],
    'max_depth': [1, 2, 3],
    'random_state': [40]
}
MULTICLASS_REBAL_OPT_CONFIGS_RFC = utils.params_iterator(MULTICLASS_REBAL_PARAMS_RFC)
#MULTICLASS_REBAL_OPT_CONFIGS_RFC = [{'use_sample_weights': True, 'model_params':{'name': 'RandomForestClassifier', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_RFC] + [{'use_sample_weights': False, 'model_params':{'name': 'RandomForestClassifier', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_RFC]
MULTICLASS_REBAL_OPT_CONFIGS_RFC_MP = {'model_params':[{'name': 'RandomForestClassifier', 'params': x} for x in MULTICLASS_REBAL_OPT_CONFIGS_RFC]}
MULTICLASS_REBAL_OPT_CONFIGS_RFC = utils.params_iterator({**MULTICLASS_REBAL_GLOBAL_CONFIGS_2, **MULTICLASS_REBAL_OPT_CONFIGS_RFC_MP})

MULTICLASS_REBAL_PARAMS_TREE_BOOSTED_BASE = {
    "max_depth": [1, 2, 5]
}
MULTICLASS_REBAL_OPT_CONFIGS_TREE_BOOSTED_BASE = utils.params_iterator(MULTICLASS_REBAL_PARAMS_TREE_BOOSTED_BASE)
MULTICLASS_REBAL_PARAMS_TREE_BOOSTED_PARENT = {
    'n_estimators': [10, 30, 100, 300],
    'learning_rate': [0.01, 0.1, 0.5],
    'random_state': [40]
}
MULTICLASS_REBAL_OPT_CONFIGS_TREE_BOOSTED_PARENT = utils.params_iterator(MULTICLASS_REBAL_PARAMS_TREE_BOOSTED_PARENT)
MULTICLASS_REBAL_PARAMS_TREE_BOOSTED = {
    'params': MULTICLASS_REBAL_OPT_CONFIGS_TREE_BOOSTED_PARENT,
    'base_model_params': MULTICLASS_REBAL_OPT_CONFIGS_TREE_BOOSTED_BASE
}
MULTICLASS_REBAL_OPT_CONFIGS_TREE_BOOSTED = utils.params_iterator(MULTICLASS_REBAL_PARAMS_TREE_BOOSTED)
MULTICLASS_REBAL_OPT_CONFIGS_TREE_BOOSTED = [{'use_sample_weights': True, 'model_params':{**x, **{'name': 'AdaBoostedTree'}}} for x in MULTICLASS_REBAL_OPT_CONFIGS_TREE_BOOSTED] + [{'use_sample_weights': False, 'model_params':{**x, **{'name': 'AdaBoostedTree'}}} for x in MULTICLASS_REBAL_OPT_CONFIGS_TREE_BOOSTED]

MULTICLASS_REBAL_PARAMS_KNN_BAGGED_BASE = {
    'n_neighbors': [5, 10, 20],
    'weights': ['uniform', 'distance'],
    'algorithm': ['auto'],
    'p': [1, 2]
}
MULTICLASS_REBAL_OPT_CONFIGS_KNN_BAGGED_BASE = utils.params_iterator(MULTICLASS_REBAL_PARAMS_KNN_BAGGED_BASE)
MULTICLASS_REBAL_PARAMS_KNN_BAGGED_PARENT = {
    'max_samples': [0.1, 0.2, 0.5],
    'max_features': [0.1, 0.2, 0.5],
    'random_state': [40]
}
MULTICLASS_REBAL_OPT_CONFIGS_KNN_BAGGED_PARENT = utils.params_iterator(MULTICLASS_REBAL_PARAMS_KNN_BAGGED_PARENT)
MULTICLASS_REBAL_PARAMS_KNN_BAGGED = {
    'params': MULTICLASS_REBAL_OPT_CONFIGS_KNN_BAGGED_PARENT,
    'base_model_params': MULTICLASS_REBAL_OPT_CONFIGS_KNN_BAGGED_BASE
}
MULTICLASS_REBAL_OPT_CONFIGS_KNN_BAGGED = utils.params_iterator(MULTICLASS_REBAL_PARAMS_KNN_BAGGED)
MULTICLASS_REBAL_OPT_CONFIGS_KNN_BAGGED = [{'model_params':{**x, **{'name': 'BaggedKNN'}}} for x in MULTICLASS_REBAL_OPT_CONFIGS_KNN_BAGGED]

MULTICLASS_REBAL_PARAMS_GBC = {
    'n_estimators': [10, 30, 100],
    #'n_estimators': [10, 30, 100, 300],
    'loss': ['deviance'],
    'learning_rate': [0.01, 0.1],
    #'learning_rate': [0.01, 0.1, 0.5],
    'max_depth': [1, 2, 3],
    'subsample': [0.2, 0.5],
    #'subsample': [0.2, 0.5, 1],
    'random_state': [40]
}
MULTICLASS_REBAL_OPT_CONFIGS_GBC = utils.params_iterator(MULTICLASS_REBAL_PARAMS_GBC)
MULTICLASS_REBAL_OPT_CONFIGS_GBC = [{'use_sample_weights': True, 'model_params':{'name': 'GradientBoostingClassifier', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_GBC] + [{'use_sample_weights': False, 'model_params':{'name': 'GradientBoostingClassifier', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_GBC]

MULTICLASS_REBAL_PARAMS_XGB = {
    'n_estimators': [10, 30, 100],
    #'n_estimators': [10, 30, 100, 300],
    'learning_rate': [0.01, 0.1],
    #'learning_rate': [0.01, 0.1, 0.5],
    'max_depth': [1, 2, 3],
    'subsample': [0.2, 0.5],
    #'subsample': [0.2, 0.5, 1],
    'objective': ["multi:softprob"],
    'random_state': [40]
}
MULTICLASS_REBAL_OPT_CONFIGS_XGB = utils.params_iterator(MULTICLASS_REBAL_PARAMS_XGB)
#MULTICLASS_REBAL_OPT_CONFIGS_XGB = [{'use_sample_weights': True, 'model_params':{'name': 'XGBoostClassifier', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_XGB] + [{'use_sample_weights': False, 'model_params':{'name': 'XGBoostClassifier', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_XGB]
MULTICLASS_REBAL_OPT_CONFIGS_XGB_MP = {'model_params':[{'name': 'XGBoostClassifier', 'params': x} for x in MULTICLASS_REBAL_OPT_CONFIGS_XGB]}
MULTICLASS_REBAL_OPT_CONFIGS_XGB = utils.params_iterator({**MULTICLASS_REBAL_GLOBAL_CONFIGS_2, **MULTICLASS_REBAL_OPT_CONFIGS_XGB_MP})

MULTICLASS_REBAL_PARAMS_RIDGE = {
    'alpha': [1, 2, 3],
    'fit_intercept': [True, False],
    'random_state': [40]
}
MULTICLASS_REBAL_OPT_CONFIGS_RIDGE = utils.params_iterator(MULTICLASS_REBAL_PARAMS_RIDGE)
#MULTICLASS_REBAL_OPT_CONFIGS_RIDGE = [{'use_sample_weights': True, 'model_params':{'name': 'RidgeClassifier', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_RIDGE] + [{'use_sample_weights': False, 'model_params':{'name': 'RidgeClassifier', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_RIDGE]
MULTICLASS_REBAL_OPT_CONFIGS_RIDGE_MP = {'model_params': [{'name': 'RidgeClassifier', 'params': x} for x in MULTICLASS_REBAL_OPT_CONFIGS_RIDGE]}
MULTICLASS_REBAL_OPT_CONFIGS_RIDGE = utils.params_iterator({**MULTICLASS_REBAL_GLOBAL_CONFIGS_2, **MULTICLASS_REBAL_OPT_CONFIGS_RIDGE_MP})

MULTICLASS_REBAL_PARAMS_LOGISTICREG = {
    'C': [0.5, 1, 2],
    'multi_class': ['multinomial'],
    'random_state': [40]
}
MULTICLASS_REBAL_OPT_CONFIGS_LOGISTICREG = utils.params_iterator(MULTICLASS_REBAL_PARAMS_LOGISTICREG)
#MULTICLASS_REBAL_OPT_CONFIGS_LOGISTICREG = [{'use_sample_weights': True, 'model_params':{'name': 'LogisticRegression', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_LOGISTICREG] + [{'use_sample_weights': False, 'model_params':{'name': 'LogisticRegression', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_LOGISTICREG]
MULTICLASS_REBAL_OPT_CONFIGS_LOGISTICREG_MP = {'model_params': [{'name': 'LogisticRegression', 'params': x} for x in MULTICLASS_REBAL_OPT_CONFIGS_LOGISTICREG]}
MULTICLASS_REBAL_OPT_CONFIGS_LOGISTICREG = utils.params_iterator({**MULTICLASS_REBAL_GLOBAL_CONFIGS_2, **MULTICLASS_REBAL_OPT_CONFIGS_LOGISTICREG_MP})

MULTICLASS_REBAL_PARAMS_LDA = {
    'solver': ['svd', 'lsqr', 'eigen'],
}
MULTICLASS_REBAL_OPT_CONFIGS_LDA = utils.params_iterator(MULTICLASS_REBAL_PARAMS_LDA)
MULTICLASS_REBAL_OPT_CONFIGS_LDA = [{'model_params':{'name': 'LDA', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_LDA]

MULTICLASS_REBAL_PARAMS_QDA = {
    'reg_param': [0.0, 0.1, 0.2],
}
MULTICLASS_REBAL_OPT_CONFIGS_QDA = utils.params_iterator(MULTICLASS_REBAL_PARAMS_QDA)
MULTICLASS_REBAL_OPT_CONFIGS_QDA = [{'model_params':{'name': 'QDA', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_QDA]
"""
MULTICLASS_REBAL_PARAMS_MLP = {
    'hidden_layer_sizes': [5, 10, 50, 100],
    'activation': ['logistic', 'tanh', 'relu'],
    'solver': ['lbfgs', 'sgd', 'adam'],
    'alpha': [0.0001, 0.001, 0.01],
    #'learning_rate': ['constant', 'invscaling', 'adaptive'],
    'random_state': [40]
}
"""
MULTICLASS_REBAL_PARAMS_MLP = {
    'hidden_layer_sizes': [10],
    'activation': ['relu'],
    'solver': ['adam'],
    'random_state': np.arange(1, 101, 1)
}

MULTICLASS_REBAL_OPT_CONFIGS_MLP = utils.params_iterator(MULTICLASS_REBAL_PARAMS_MLP)
MULTICLASS_REBAL_OPT_CONFIGS_MLP = [{'model_params':{'name': 'MLP', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_MLP]

MULTICLASS_REBAL_PARAMS_NCC = {
    'metric': ['euclidean'],
}
MULTICLASS_REBAL_OPT_CONFIGS_NCC = utils.params_iterator(MULTICLASS_REBAL_PARAMS_NCC)
MULTICLASS_REBAL_OPT_CONFIGS_NCC = [{'model_params':{'name': 'NearestCentroid', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_NCC]

MULTICLASS_REBAL_PARAMS_RNC = {
    'radius': [0.5, 1, 2],
    'weights': ['uniform', 'distance'],
}
MULTICLASS_REBAL_OPT_CONFIGS_RNC = utils.params_iterator(MULTICLASS_REBAL_PARAMS_RNC)
MULTICLASS_REBAL_OPT_CONFIGS_RNC = [{'X_transform': 'QuantileTransformer', 'model_params':{'name': 'RadiusNeighborsClassifier', 'params': x}} for x in MULTICLASS_REBAL_OPT_CONFIGS_RNC]

PFOLIO_MOM_REBAL_M_c = [-0.01, -0.001, 0.0]
PFOLIO_MOM_REBAL_WINDOW = [2, 5, 10, 20, 50]
PFOLIO_MOM_REBAL_STATIC_TICKERS = [[
        "CARBORUNIV.NS", "KSCL.NS", "MAANALU.NS", "REMSONSIND.NS", "BAJAJ-AUTO.NS", "HEROMOTOCO.NS", "ASALCBR.NS",
        "POLYCAB.NS", "GTPL.NS", "HEIDELBERG.NS", "SHREDIGCEM.NS", "OAL.NS", "COMPINFO.NS", "PNCINFRA.NS",
        "RVNL.NS", "THANGAMAYL.NS", "GSPL.NS", "AIAENG.NS", "BEL.NS", "MAITHANALL.NS", "CHAMBLFERT.NS",
        "TATACHEM.NS", "MGL.NS", "INDRAMEDCO.NS", "HGINFRA.NS", "DPWIRES.NS", "KSL.NS", "JSLHISAR.NS",
        "MPHASIS.NS", "GREENLAM.NS", "GEEKAYWIRE.NS", "COSMOFILMS.NS", "JINDALPOLY.NS", "JKPAPER.NS", "NAHARPOLY.NS",
        "BHARATRAS.NS", "IOLCP.NS", "GRANULES.NS", "AUROPHARMA.NS", "DRREDDY.NS", "FINPIPE.NS", "GPPL.NS",
        "POWERGRID.NS", "NUCLEUS.NS", "ANDHRSUGAR.NS", "TRIVENI.NS", "CCL.NS", "RITES.NS", "WELSPUNIND.NS", "TVTODAY.NS"
]]
PFOLIO_MOM_REBAL_DEF_WTS = [[
    0.03, 0.02, 0.01, 0.01, 0.03, 0.03, 0.02,
    0.03, 0.02, 0.02, 0.02, 0.02, 0.01, 0.02,
    0.01, 0.02, 0.03, 0.03, 0.03, 0.01, 0.03,
    0.03, 0.03, 0.02, 0.01, 0.01, 0.02, 0.02,
    0.02, 0.02, 0.01, 0.02, 0.01, 0.01, 0.01,
    0.02, 0.02, 0.02, 0.03, 0.03, 0.01, 0.02,
    0.03, 0.02, 0.02, 0.02, 0.01, 0.02, 0.02, 0.02
]]
PFOLIO_MOM_REBAL_PARAMS = {
    'rebal_freq_days': PFOLIO_MOM_REBAL_WINDOW,
    'ma_window': [7],
    'M_c': PFOLIO_MOM_REBAL_M_c,
    'static_tickers': PFOLIO_MOM_REBAL_STATIC_TICKERS,
    'default_weight_alloc': PFOLIO_MOM_REBAL_DEF_WTS
}
PFOLIO_MOM_REBAL_OPT_CONFIGS = utils.params_iterator(PFOLIO_MOM_REBAL_PARAMS)
'''
PFOLIO_TALIB_REBAL_PARAMS = copy.deepcopy(PFOLIO_MOM_REBAL_PARAMS)
PFOLIO_TALIB_REBAL_PARAMS['ind_thresh'] = np.arange(15, 43, 3)
PFOLIO_TALIB_REBAL_PARAMS['ind_type'] = ['def', 'short', 'long', 'supershort']
PFOLIO_TALIB_REBAL_PARAMS['M_c'] = [0.0]
PFOLIO_TALIB_REBAL_OPT_CONFIGS = utils.params_iterator(PFOLIO_TALIB_REBAL_PARAMS)
'''
PFOLIO_TALIB_REBAL_PARAMS = copy.deepcopy(PFOLIO_MOM_REBAL_PARAMS)
PFOLIO_TALIB_REBAL_PARAMS['ind_thresh'] = np.arange(20, -20, -1)
PFOLIO_TALIB_REBAL_PARAMS['ind_type'] = ['def']
PFOLIO_TALIB_REBAL_PARAMS['M_c'] = [0.0]
PFOLIO_TALIB_REBAL_PARAMS['rebal_freq_days'] = [1]
PFOLIO_TALIB_REBAL_PARAMS['ma_window'] = [1]
PFOLIO_TALIB_REBAL_OPT_CONFIGS = utils.params_iterator(PFOLIO_TALIB_REBAL_PARAMS)

PFOLIO_STATIC_REBAL_PARAMS = {
    'rebal_freq_days': PFOLIO_MOM_REBAL_WINDOW,
    'static_tickers': PFOLIO_MOM_REBAL_STATIC_TICKERS,
    'default_weight_alloc': PFOLIO_MOM_REBAL_DEF_WTS,
    'reweight': [True, False],
    'reweight_max_wt': [0.05, 0.1, 0.2]
}

PFOLIO_STATIC_REBAL_OPT_CONFIGS = utils.params_iterator(PFOLIO_STATIC_REBAL_PARAMS)

PFOLIO_STATIC_PARAMS = {
    'static_tickers': PFOLIO_MOM_REBAL_STATIC_TICKERS,
    'default_weight_alloc': PFOLIO_MOM_REBAL_DEF_WTS,
    'reweight': [True, False],
    'reweight_max_wt': [0.05, 0.1, 0.2],
    'rebal_on_new': [True, False]
}

PFOLIO_STATIC_OPT_CONFIGS = utils.params_iterator(PFOLIO_STATIC_PARAMS)

INTRADAY_TREND_EMA_KWARGS = [{'timeperiod': v} for v in [5, 10, 20, 50]]
INTRADAY_TREND_PARAMS = {
    'trade_agr_score': [0, 1, 2, 3],
    'sqoff_agr_score': [0, 1, 2, 3],
    'ema_kwargs': INTRADAY_TREND_EMA_KWARGS
}
INTRADAY_TREND_OPT_CONFIGS = utils.params_iterator(INTRADAY_TREND_PARAMS)

INTRADAY_TREND_HEIKIN_PARAMS = {
    'barsize_thresh_trade': [1, 2, 3, 5, 10, 15, 20, 30, 50],
    'stop_loss': [1e-2, 1e-1, 0.5, 1, 2],
    'ema_baseline': [0, 5, 10, 15, 20, 30, 50, 100, 150],
    'add_transaction_costs': [False, True]
}

INTRADAY_TREND_HEIKIN_OPT_CONFIGS = utils.params_iterator(INTRADAY_TREND_HEIKIN_PARAMS)

INTRADAY_TREND_HEIKIN2_PARAMS = {
    'ema_baseline': [None, 5, 10, 15, 20, 30, 50, 100, 150],
    'ignore_indecisive': [False, True],
    'add_transaction_costs': [True, False],
    'inst_delta': [0.5, 1]
}

INTRADAY_TREND_HEIKIN2_OPT_CONFIGS = utils.params_iterator(INTRADAY_TREND_HEIKIN2_PARAMS)

INTRADAY_TREND_HEIKIN3_PARAMS = {
    'ema_baseline': [None, 5, 10, 15, 20, 30, 50, 100, 150],
    'sl_on_ha': [True, False],
    'add_transaction_costs': [True],
    'inst_delta': [0.5, 1]
}

INTRADAY_TREND_HEIKIN3_OPT_CONFIGS = utils.params_iterator(INTRADAY_TREND_HEIKIN3_PARAMS)

INTRADAY_MA_PARAMS = {
    'rescale_shorts': [False],
    'ema_window': [5, 10, 20, 50, 100, 150, 200],
    'eod_sqoff': [False, True],
    'on_heikin_ashi': [True, False],
    'add_transaction_costs': [True],
    'inst_delta': [1.0]
}

INTRADAY_MA_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_MA_PARAMS)

INTRADAY_MAC_PARAMS = {
    'rescale_shorts': [False],
    'ema_window_short': [int(x) for x in np.arange(40, 110,5)],
    'ema_long_window_mult': [1.2, 1.5, 2, 3],
    'wait_for_crossover': [False],
    'restrict_trade_time': [False],
    'no_trade_days': [(5,)],
    'mean_rev': [False],
    'add_transaction_costs': [True],
    'inst_delta': [1.0]
}

INTRADAY_MAC_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_MAC_PARAMS)

INTRADAY_MAC_SL_PARAMS = {
    'rescale_shorts': [False],
    'ema_window_short': [int(x) for x in np.arange(50, 110,5)],
    'ema_long_window_mult': [1.2, 1.5, 2],
    'add_transaction_costs': [True],
    'inst_delta': [0.5],
    'stop_loss': [None, 0.1, 0.5, 1, 2, 3, 5, 10]
}

INTRADAY_MAC_SL_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_MAC_SL_PARAMS)

INTRADAY_MAC_MA_PARAMS = {
    'rescale_shorts': [False],
    'ema_window_short': [int(x) for x in np.arange(40, 110,5)],
    'ema_long_window_mult': [1.2, 1.5, 2, 3],
    'add_transaction_costs': [True],
    'inst_delta': [1.0],
    'ema_window_cutoff': [5, 10, 20, 30, 40]
}

INTRADAY_MAC_MA_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_MAC_MA_PARAMS)

INTRADAY_MACD_PARAMS = {
    'rescale_shorts': [False],
    'window_short': [5, 10, 20, 50],
    'long_window_mult': [1.2, 1.5, 2],
    'signal_window_mult': [0.5, 0.8, 1, 1.2, 1.5],
    'add_transaction_costs': [True],
    'restrict_trade_time': [True, False],
    'inst_delta': [1.0]
}

INTRADAY_MACD_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_MACD_PARAMS)

INTRADAY_MACD_TPSL_PARAMS = {
    'rescale_shorts': [False],
    'window_short': [5, 10, 20, 50],
    'long_window_mult': [1.5, 2],
    'signal_window_mult': [0.5, 0.8, 1, 1.5],
    'tp_atr': [2, 5, 10],
    'sl_atr': [1, 2, 5],
    'is_trailing_sl': [False, True],
    'watch_reversal': [False, True],
    'add_transaction_costs': [True],
    'restrict_trade_time': [True, False],
    'inst_delta': [1.0]
}

INTRADAY_MACD_TPSL_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_MACD_TPSL_PARAMS)

INTRADAY_PULLBACK_PARAMS = {
    'rescale_shorts': [False],
    'rsi_period': [2, 3, 5], 
    'rsi_entry': [(5, 95), (2, 98), (10, 90)],
    'rsi_exit': [(55, 45), (75, 25), (40, 60)],
    'max_holding': [1, 3, 5],
    'trend_baseline': [50, 100, None],
    'side_restriction': [-1, 1],
    'restrict_trade_time': [False],
    'add_transaction_costs': [True],
    'inst_delta': [0.5]
}

INTRADAY_PULLBACK_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_PULLBACK_PARAMS)

INTRADAY_PULLBACK_CRSI_PARAMS = {
    'rescale_shorts': [False],
    'rsi_period': [2, 3, 5],
    'cumul_rsi_period': [2, 3],
    'rsi_entry': [(5, 95), (2, 98), (10, 90)],
    'rsi_exit': [(55, 45), (75, 25), (40, 60)],
    'max_holding': [1, 3, 5],
    'trend_baseline': [50, 100],
    'side_restriction': [-1, 1],
    'restrict_trade_time': [False],
    'add_transaction_costs': [True],
    'inst_delta': [0.5]
}

INTRADAY_PULLBACK_CRSI_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_PULLBACK_CRSI_PARAMS)

INTRADAY_PULLBACK_LB_PARAMS = {
    'rescale_shorts': [False],
    'rsi_period': [2, 3, 5], 
    'lb_period': [2, 5, 10, 20, 50],
    'rsi_exit': [(55, 45), (75, 25), (40, 60)],
    'max_holding': [3, 5],
    'trend_baseline': [50, 100],
    'restrict_trade_time': [True, False],
    'add_transaction_costs': [True],
    'inst_delta': [0.5]
}

INTRADAY_PULLBACK_LB_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_PULLBACK_LB_PARAMS)

INTRADAY_PULLBACK_BB_PARAMS = {
    'rescale_shorts': [False],
    'bb_period': [5, 10, 20],
    'bb_stdev': [1.5, 2.0, 3.0],
    'trend_baseline': [10, 20, 50, 100],
    'restrict_trade_time': [True, False],
    'add_transaction_costs': [True],
    'inst_delta': [0.5]
}

INTRADAY_PULLBACK_BB_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_PULLBACK_BB_PARAMS)

INTRADAY_PULLBACK_CSTICK_REV_PARAMS = {
    'rescale_shorts': [False],
    'rsi_period': [2, 3, 5, 10], 
    'rsi_entry': [(5, 95), (10, 90), (25, 75)],
    'rsi_exit': [(55, 45), (40, 60)],
    'max_holding': [3, 5, None],
    'cstick_modes': ['1', '2', '3', '4', '5'],
    'trend_baseline': [20, 50, 100],
    'side_restriction': [-1, 1],
    'restrict_trade_time': [False],
    'add_transaction_costs': [True],
    'inst_delta': [0.5]
}

INTRADAY_PULLBACK_CSTICK_REV_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_PULLBACK_CSTICK_REV_PARAMS)

INTRADAY_CONT_HLDG_PARAMS = {
    'rescale_shorts': [False],
    'rsi_period': [2, 3, 5, 10], 
    'rsi_entry': [(95, 5), (90, 10), (75, 25), (55, 45)], # (0, 100) means that no rsi dependency
    'max_holding': [None, 1, 3, 5],
    'cstick_modes': ['0', '2', '3', '6', '7', '8'],
    'trend_baseline': [10, 20, 50],
    'side_restriction': [-1, 1],
    'restrict_trade_time': [False],
    'add_transaction_costs': [True],
    'inst_delta': [1.0]
}

INTRADAY_CONT_HLDG_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_CONT_HLDG_PARAMS)

INTRADAY_CONT_ATRTP_PARAMS = {
    'rescale_shorts': [False],
    'rsi_period': [2, 3, 5, 10], 
    'rsi_entry': [(95, 5), (90, 10), (75, 25)], # (0, 100) means that no rsi dependency
    'atr_tp': [1, 2, 3, 5, 500],
    'cstick_modes': ['0', '2', '3', '6', '7', '8'],
    'trend_baseline': [10, 20, 50],
    'side_restriction': [-1, 1],
    'restrict_trade_time': [False],
    'add_transaction_costs': [True],
    'inst_delta': [1.0]
}

INTRADAY_CONT_ATRTP_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_CONT_ATRTP_PARAMS)

INTRADAY_CONT_ATRSLSHIFT_PARAMS = {
    'rescale_shorts': [False],
    'rsi_period': [2, 3, 5, 10], 
    'rsi_entry': [(95, 5), (90, 10), (75, 25)], # (0, 100) means that no rsi dependency
    'atr_tp': [1, 2, 3, 5, 500],
    'cstick_modes': ['0', '2', '3', '6', '7', '8'],
    'trend_baseline': [10, 20, 50],
    'side_restriction': [-1, 1],
    'restrict_trade_time': [False],
    'add_transaction_costs': [True],
    'inst_delta': [1.0]
}

INTRADAY_CONT_ATRSLSHIFT_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_CONT_ATRSLSHIFT_PARAMS)

INTRADAY_OVERTRADE_RSI_PARAMS = {
    'rescale_shorts': [False],
    'rsi_period': [2, 3, 5], 
    'rsi_entry': [(5, 95), (2, 98), (10, 90)],
    'rsi_exit': [(55, 45), (75, 25), (40, 60)],
    'max_holding': [1, 3, 5],
    'trend_baseline_short': [10, 20],
    'trend_baseline_long': [50, 100, None],
    'side_restriction': [-1, 1],
    'restrict_trade_time': [False],
    'add_transaction_costs': [True],
    'inst_delta': [0.5]
}

INTRADAY_OVERTRADE_RSI_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_OVERTRADE_RSI_PARAMS)

INTRADAY_OVERTRADE_CRSI_PARAMS = {
    'rescale_shorts': [False],
    'rsi_period': [2, 3, 5],
    'cumul_rsi_period': [2, 3],
    'rsi_entry': [(5, 95), (2, 98), (10, 90)],
    'rsi_exit': [(55, 45), (75, 25), (40, 60)],
    'max_holding': [1, 3, 5],
    'trend_baseline_short': [10, 20],
    'trend_baseline_long': [50, 100, None],
    'side_restriction': [-1, 1],
    'restrict_trade_time': [False],
    'add_transaction_costs': [True],
    'inst_delta': [0.5]
}

INTRADAY_OVERTRADE_CRSI_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_OVERTRADE_CRSI_PARAMS)

INTRADAY_OVERTRADE_LB_PARAMS = {
    'rescale_shorts': [False],
    'rsi_period': [2, 3, 5], 
    'lb_period': [2, 5, 10, 20, 50],
    'rsi_exit': [(55, 45), (75, 25), (40, 60)],
    'max_holding': [3, 5],
    'trend_baseline_short': [5, 10, 20, 50],
    'trend_baseline_long': [50, 100, 200, None],
    'restrict_trade_time': [True, False],
    'add_transaction_costs': [True],
    'inst_delta': [0.5]
}

INTRADAY_OVERTRADE_LB_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_OVERTRADE_LB_PARAMS)

INTRADAY_OVERTRADE_BB_PARAMS = {
    'rescale_shorts': [False],
    'bb_period': [5, 10, 20],
    'bb_stdev': [1.5, 2.0, 3.0],
    'trend_baseline': [10, 20, 50, 100],
    'max_holding': [3, 5, 1000],
    'restrict_trade_time': [True, False],
    'add_transaction_costs': [True],
    'inst_delta': [0.5]
}

INTRADAY_OVERTRADE_BB_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_OVERTRADE_BB_PARAMS)

INTRADAY_OVERTRADE_CSTICK_REV_RSI_PARAMS = {
    'rescale_shorts': [False],
    'rsi_period': [2, 3, 5, 10], 
    'rsi_entry': [(5, 95), (10, 90), (25, 75)],
    'rsi_exit': [(55, 45), (40, 60)],
    'cstick_modes': ['1', '2', '3', '4', '5'],
    'max_holding': [3, 5, None],
    'trend_baseline_short': [10, 20, 50],
    'trend_baseline_long': [50, 100, None],
    'side_restriction': [-1, 1],
    'restrict_trade_time': [False],
    'add_transaction_costs': [True],
    'inst_delta': [0.5]
}

INTRADAY_OVERTRADE_RSI_CSTICK_REV_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_OVERTRADE_CSTICK_REV_RSI_PARAMS)

INTRADAY_BB_PARAMS = {
    'rescale_shorts': [False],
    'bb_period': [5, 10, 20],
    'bb_stdev': [1.5, 2.0, 3.0],
    'max_holding': [3, 5, None],
    'restrict_trade_time': [True, False],
    'add_transaction_costs': [True],
    'inst_delta': [1.0]
}

INTRADAY_BB_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_BB_PARAMS)

INTRADAY_BKOUT_HILO_PARAMS = {
    'rescale_shorts': [False],
    'sl_atr': [0.2, 0.5, 1, 2, 5],
    'tp_atr': [0.2, 0.5, 1, 2, 5, 10],
    'is_trailing_sl': [False, True],
    'false_breakout': [False, True],
    'add_transaction_costs': [True],
    'inst_delta': [1.0]
}

INTRADAY_BKOUT_HILO_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_BKOUT_HILO_PARAMS)

INTRADAY_BKOUT_CSTICK_PARAMS = {
    'rescale_shorts': [False],
    'lookback_period': [1, 2, 3, 5, 10],
    'sl_atr': [0.1, 1, 2, 5],
    'tp_atr': [1, 2, 5, 10],
    'is_trailing_sl': [False],
    'add_transaction_costs': [False],
    'inst_delta': [1.0]
}

INTRADAY_BKOUT_CSTICK_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_BKOUT_CSTICK_PARAMS)

INTRADAY_DBLBKOUT_CSTICK_PARAMS = {
    'rescale_shorts': [False],
    'lookback_period': [1, 2, 3, 5, 10],
    'eod_lookback_period': [1, 2, 3, 5, 10],
    'sl_atr': [0.1, 1, 2, 5],
    'tp_atr': [1, 2, 5, 10],
    'is_trailing_sl': [False],
    'add_transaction_costs': [False],
    'inst_delta': [1.0]
}

INTRADAY_DBLBKOUT_CSTICK_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_DBLBKOUT_CSTICK_PARAMS)

INTRADAY_RANGE_BKOUT_PARAMS = {
    'rescale_shorts': [False],
    'range_bars': [3, 6, 9, 15, 30],
    'sl_atr': [0.1, 1, 2, 5],
    'tp_atr': [1, 2, 5, 10],
    'is_trailing_sl': [True, False],
    'add_transaction_costs': [True],
    'inst_delta': [0.5]
}

INTRADAY_RANGE_BKOUT_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_RANGE_BKOUT_PARAMS)

INTRADAY_HA_CCI_PARAMS = {
    'rescale_shorts': [False],
    'sl_atr': [5, 7, 10, 12],
    'tp_atr': [7, 10, 12, 15],
    'is_trailing_sl': [False, True],
    'cci_period': [20, 30, 40, 50],
    'cci_entry': [(-50, 50), (-75, 75), (-100, 100), (-125, 125), (-150, 150)],
    'cci_exit': [(50, -50), (75, -75), (100, -100), (125, -125), (150, -150)],
    'side_restriction': [-1, 1],
    'add_transaction_costs': [False],
    'inst_delta': [1.0]
}

INTRADAY_HA_CCI_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_HA_CCI_PARAMS)

INTRADAY_WILLR_BKOUT_PARAMS = {
    'rescale_shorts': [False],
    'willr_buy': [-10, -20, -30], 
    'willr_sell': [-70, -80, -90],
    'willr_period': [14, 30, 50, 100, 133, 150], 
    'entry_scale': [0, 0.618, 1], 
    'exit_scale': [0, 0.618, 1], 
    'eod_squareoff': [True, False],
    'add_transaction_costs': [False],
    'inst_delta': [1.0]
}

INTRADAY_WILLR_BKOUT_PARAMS_OPT_CONFIGS = utils.params_iterator(INTRADAY_WILLR_BKOUT_PARAMS)


STRATEGY_OPT_CONFIG_MAP = {
    'MOMENTUM_REBAL_STRATEGY': MOMENTUM_REBAL_OPT_CONFIGS,
    'MULTICLASS_CLASSIFIER_REBAL': MULTICLASS_REBAL_OPT_CONFIGS_KNN,
    'PORTFOLIO_MOM_REBAL': PFOLIO_MOM_REBAL_OPT_CONFIGS,
    'PORTFOLIO_TALIB_REBAL': PFOLIO_TALIB_REBAL_OPT_CONFIGS,
    'PORTFOLIO_STATIC_REBAL': PFOLIO_STATIC_REBAL_OPT_CONFIGS,
    'PORTFOLIO_STATIC': PFOLIO_STATIC_OPT_CONFIGS,
    'INTRADAY_TREND_CAPTURE': INTRADAY_TREND_OPT_CONFIGS,
    'INTRADAY_TREND_HEIKIN': INTRADAY_TREND_HEIKIN_OPT_CONFIGS,
    'INTRADAY_TREND_HEIKIN_2': INTRADAY_TREND_HEIKIN2_OPT_CONFIGS,
    'INTRADAY_TREND_HEIKIN_3': INTRADAY_TREND_HEIKIN3_OPT_CONFIGS,
    'INTRADAY_MA': INTRADAY_MA_PARAMS_OPT_CONFIGS,
    'INTRADAY_MAC': INTRADAY_MAC_PARAMS_OPT_CONFIGS,
    'INTRADAY_MAC_SL': INTRADAY_MAC_SL_PARAMS_OPT_CONFIGS,
    'INTRADAY_MAC_MA': INTRADAY_MAC_MA_PARAMS_OPT_CONFIGS,
    'INTRADAY_MACD': INTRADAY_MACD_PARAMS_OPT_CONFIGS,
    'INTRADAY_MACD_TP_SL': INTRADAY_MACD_TPSL_PARAMS_OPT_CONFIGS,
    'INTRADAY_PULLBACK': INTRADAY_PULLBACK_PARAMS_OPT_CONFIGS,
    'INTRADAY_PULLBACK_BB': INTRADAY_PULLBACK_BB_PARAMS_OPT_CONFIGS,
    'INTRADAY_PULLBACK_CUMUL_RSI': INTRADAY_PULLBACK_CRSI_PARAMS_OPT_CONFIGS,
    'INTRADAY_PULLBACK_PRICE_LB': INTRADAY_PULLBACK_LB_PARAMS_OPT_CONFIGS,
    'INTRADAY_PULLBACK_CSTICK_REV': INTRADAY_PULLBACK_CSTICK_REV_PARAMS_OPT_CONFIGS,
    'INTRADAY_CONTINUATION_HLDG': INTRADAY_CONT_HLDG_PARAMS_OPT_CONFIGS,
    'INTRADAY_CONTINUATION_ATRTP': INTRADAY_CONT_ATRTP_PARAMS_OPT_CONFIGS,
    'INTRADAY_CONTINUATION_ATRSLSHIFT': INTRADAY_CONT_ATRSLSHIFT_PARAMS_OPT_CONFIGS,
    'INTRADAY_OVERTRADE_RSI': INTRADAY_OVERTRADE_RSI_PARAMS_OPT_CONFIGS,
    'INTRADAY_OVERTRADE_CUMUL_RSI': INTRADAY_OVERTRADE_CRSI_PARAMS_OPT_CONFIGS,
    'INTRADAY_OVERTRADE_PRICE_LB': INTRADAY_OVERTRADE_LB_PARAMS_OPT_CONFIGS,
    'INTRADAY_OVERTRADE_BB': INTRADAY_OVERTRADE_BB_PARAMS_OPT_CONFIGS,
    'INTRADAY_OVERTRADE_RSI_CSTICK_REV': INTRADAY_OVERTRADE_RSI_CSTICK_REV_PARAMS_OPT_CONFIGS,
    'INTRADAY_BB': INTRADAY_BB_PARAMS_OPT_CONFIGS,
    'INTRADAY_BREAKOUT_HILO': INTRADAY_BKOUT_HILO_PARAMS_OPT_CONFIGS,
    'INTRADAY_DBLBREAKOUT_CSTICK': INTRADAY_DBLBKOUT_CSTICK_PARAMS_OPT_CONFIGS,
    'INTRADAY_BREAKOUT_CSTICK': INTRADAY_BKOUT_CSTICK_PARAMS_OPT_CONFIGS,
    'INTRADAY_RANGE_BREAKOUT': INTRADAY_RANGE_BKOUT_PARAMS_OPT_CONFIGS,
    'INTRADAY_WILLR_BREAKOUT': INTRADAY_WILLR_BKOUT_PARAMS_OPT_CONFIGS,
    'INTRADAY_HA_CCI': INTRADAY_HA_CCI_PARAMS_OPT_CONFIGS,
}