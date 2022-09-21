# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 09:44:23 2021

@author: vivin
"""
from lib.strategies.pfolio_mom_rebal import PORTFOLIO_MOM_REBAL
from talib.abstract import ROCP
import numpy as np

class PORTFOLIO_STATIC_REBAL(PORTFOLIO_MOM_REBAL):
    def __init__(self, identifier, initial_capital=1000000, run_days=0, tickers=None, static_tickers=None, default_weight_alloc=None, rebal_freq_days=1, reweight=None, reweight_max_wt=None):
        super(PORTFOLIO_STATIC_REBAL, self).__init__(identifier, initial_capital, run_days, tickers, None, None, static_tickers, default_weight_alloc, rebal_freq_days, reweight, reweight_max_wt)
        
    def update_indicators(self, dt=None):
        self.run_days = self.run_days + 1
        self.units_whole_prev = self.units_whole.copy()
        is_trade_day = False
        self.days_since_start = self.days_since_start + 1
        data = self.extended_mkt.loc[dt]
        for ticker in self.tickers:
            returns = data['{} returns'.format(ticker)]
            price = data['{} Close'.format(ticker)]
            self.live_prices[ticker] = price
            if self.days_since_start > 1:
                #update per asset capital based on c-c returns
                self.per_asset_capital[ticker] = self.per_asset_capital[ticker] * (1+returns)
        if self.days_since_start > 1:
            self.current_capital = np.array(list(self.per_asset_capital.values())).sum()
        if ((self.days_since_start-1) % self.rebal_freq_days) == 0:
            #rebalance
            is_trade_day = True
            self._rebalance()
                
        self._update_quick_bt_attrs(dt, is_trade=is_trade_day)
        
    def prepare_strategy_attributes(self, dt_till=None):
        self.extended_mkt = self.db_cache_mkt.copy()
        for ticker in self.tickers:
            self.extended_mkt['{} returns'.format(ticker)] = np.nan_to_num(ROCP(self.extended_mkt['{} Close'.format(ticker)], timeperiod=1))
        #special handling incase particular tickers dont have data as of a given day
        self.extended_mkt.fillna(method='ffill', inplace=True)
        self.extended_mkt.fillna(-1.0, inplace=True)
    
    def _rebalance(self):
       for ticker in self.tickers:
           self.weights[ticker] = self.default_weight_alloc[ticker] if self.live_prices[ticker] > 0 else 0.0
           
       if self.reweight:
           self.weights['Cash'] = 0
           prev_assigned_wts = np.array(list(self.weights.values())).sum()
           for ticker in self.tickers:
               self.weights[ticker] = min(self.weights[ticker]/prev_assigned_wts, self.reweight_max_wt)

       self._allocate_capital_by_weights()
        
class PORTFOLIO_STATIC(PORTFOLIO_STATIC_REBAL):
    def __init__(self, identifier, initial_capital=1000000, run_days=0, tickers=None, static_tickers=None, default_weight_alloc=None, rebal_on_new=False, reweight=None, reweight_max_wt=None):
        super(PORTFOLIO_STATIC, self).__init__(identifier, initial_capital, run_days, tickers, static_tickers, default_weight_alloc, 1e12, reweight, reweight_max_wt)
        self.rebal_on_new = rebal_on_new
        self.asset_tradable_now = dict(zip(self.tickers, [False] * len(tickers)))
        self.asset_tradable_prev = dict(zip(self.tickers, [False] * len(tickers)))
        
    def update_indicators(self, dt=None):
        self.run_days = self.run_days + 1
        self.units_whole_prev = self.units_whole.copy()

        self.days_since_start = self.days_since_start + 1
        data = self.extended_mkt.loc[dt]
        make_rebal_on_new_trade = False
        is_trade_day = False
        for ticker in self.tickers:
            returns = data['{} returns'.format(ticker)]
            price = data['{} Close'.format(ticker)]
            self.live_prices[ticker] = price
            if price > 0:
                #this switches the first time a ticker becomes available. This is to eventually trigger a rebalancing
                #...when a new asset comes into play
                self.asset_tradable_now[ticker] = True
                if not self.asset_tradable_prev[ticker]:
                    make_rebal_on_new_trade = True
            if self.days_since_start > 1:
                #update per asset capital based on c-c returns
                self.per_asset_capital[ticker] = self.per_asset_capital[ticker] * (1+returns)
        if self.days_since_start > 1:
            self.current_capital = np.array(list(self.per_asset_capital.values())).sum()
        if (self.days_since_start == 1 and not self.rebal_on_new) or (make_rebal_on_new_trade and self.rebal_on_new): #balancing only on first day
            is_trade_day = True    
            self._rebalance()
                
        self._update_quick_bt_attrs(dt, is_trade=is_trade_day)
        self.asset_tradable_prev = self.asset_tradable_now.copy()