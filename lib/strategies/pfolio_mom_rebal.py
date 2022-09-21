# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 12:49:24 2021

@author: vivin
"""

from lib.strategies.momentum_rebal import MOMENTUM_REBAL_STRATEGY
from lib.configs.talib_feature_configs import TALIB_FEATURES_CONFIG_MAP 
import numpy as np
import importlib
from talib.abstract import ROCP

class PORTFOLIO_MOM_REBAL(MOMENTUM_REBAL_STRATEGY):
    def __init__(self, identifier, initial_capital=1000000, run_days=0, tickers=None, ma_window=None, M_c=None, static_tickers=None, default_weight_alloc=None, rebal_freq_days=1, reweight=None, reweight_max_wt=None):
        tickers = static_tickers if static_tickers is not None else tickers
        super(PORTFOLIO_MOM_REBAL, self).__init__(identifier, initial_capital, run_days, tickers, ma_window, M_c, rebal_freq_days)
        self.default_weight_alloc = dict(zip(self.tickers, default_weight_alloc))
        self.reweight = reweight
        self.reweight_max_wt = reweight_max_wt        

    def _rebalance(self, mom_dict):
        for ticker, momentum in mom_dict.items():
            self.weights[ticker] = self.default_weight_alloc[ticker] if momentum > self.M_c and self.live_prices[ticker] > 0 else 0.0
            
        if self.reweight:
            self.weights['Cash'] = 0
            prev_assigned_wts = np.array(list(self.weights.values())).sum()
            for ticker in self.tickers:
                self.weights[ticker] = min(self.weights[ticker]/prev_assigned_wts, self.reweight_max_wt)
            
        self._allocate_capital_by_weights()
        
    def skip_event(self, events_df):
        skip = False
        skip = skip or (len(np.unique(events_df['TimeStamp'].values)) != 1)
        return skip
    
class PORTFOLIO_TALIB_REBAL(PORTFOLIO_MOM_REBAL):
    def __init__(self, identifier, initial_capital=1000000, run_days=0, tickers=None, ma_window=None, M_c=None, ind_thresh=None, ind_type=None, static_tickers=None, default_weight_alloc=None, rebal_freq_days=1, reweight=None, reweight_max_wt=None):
        super(PORTFOLIO_TALIB_REBAL, self).__init__(identifier, initial_capital, run_days, tickers, ma_window, M_c, static_tickers, default_weight_alloc, rebal_freq_days, reweight, reweight_max_wt)
        
        self.ind_thresh = ind_thresh
        self.ind_type = ind_type
        self.talib_feature_data = TALIB_FEATURES_CONFIG_MAP['PORTFOLIO_TALIB_REBAL']
    
    def update_indicators(self, dt=None):
        self.run_days = self.run_days + 1
        self.units_whole_prev = self.units_whole.copy()
        is_trade_day = False
        if self.run_days > self.ma_window:
            self.days_since_start = self.days_since_start + 1
            data = self.extended_mkt.loc[dt]
            for ticker in self.tickers:
                price = data['{} Close'.format(ticker)]
                returns = data['{} returns'.format(ticker)]
                self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
                if self.run_days > self.ma_window + 1:
                    #update per asset capital based on c-c returns
                    self.per_asset_capital[ticker] = self.per_asset_capital[ticker] * (1+returns) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            if self.days_since_start > 1:
                self.current_capital = np.array(list(self.per_asset_capital.values())).sum()
            if ((self.days_since_start-1) % self.rebal_freq_days) == 0:
                #rebalance
                is_trade_day = True
                self._rebalance(data)
        else:
            data = self.extended_mkt.loc[dt]
            for ticker in self.tickers:
                price = data['{} Close'.format(ticker)]
                self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
                
        self._update_quick_bt_attrs(dt, is_trade=is_trade_day)
    
    def prepare_strategy_attributes(self, dt_till=None):
        self.extended_mkt = self.db_cache_mkt.copy()
        #special handling incase particular tickers dont have data as of a given day
        self.extended_mkt.fillna(method='ffill', inplace=True)
        self._add_talib_features(self.extended_mkt)        
        for ticker in self.tickers:
            self.extended_mkt['{} returns'.format(ticker)] = ROCP(self.extended_mkt['{} Close'.format(ticker)], timeperiod=1)

    def _rebalance(self, data):
        for ticker in self.tickers:
            ind_val = data['{} ADX_{}'.format(ticker, self.ind_type)]
            ind_val = ind_val or 0.0
            self.weights[ticker] = self.default_weight_alloc[ticker] if ind_val > self.ind_thresh else 0.0
           
        if self.reweight:
            self.weights['Cash'] = 0
            prev_assigned_wts = np.array(list(self.weights.values())).sum()
            for ticker in self.tickers:
                self.weights[ticker] = min(self.weights[ticker]/prev_assigned_wts, self.reweight_max_wt) if prev_assigned_wts != 0.0 else 0.0
            
        self._allocate_capital_by_weights()
        
    def _add_talib_features(self, df):
        for ticker in self.tickers:
            for col_name, data in self.talib_feature_data.items():
                data_cols = data['data_cols']
                data_args = [df['{} {}'.format(ticker, col_name)] for col_name in data_cols]
                return_results = getattr(importlib.import_module('talib.abstract'), data['name'])(*data_args, **data['kwargs'])
                if isinstance(return_results, list):
                    #multiple return values
                    for idx, return_name in enumerate(data['return']):
                        if data['filter'][idx]:
                            df.loc[:, '{} {}'.format(ticker, return_name)] = return_results[idx]
                else:
                    df.loc[:, '{} {}'.format(ticker, data['return'][0])] = return_results