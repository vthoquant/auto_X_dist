# -*- coding: utf-8 -*-
"""
Created on Fri May 21 11:16:11 2021

@author: vivin
"""

from lib.strategies.base_classes import INTRADAY_BASE
from lib.configs.directory_names import STRATEGY_RUN_BASE_PATHS
import pandas as pd
import numpy as np
import datetime
from talib.abstract import ROCP, EMA, RSI, MACD, ATR
from enum import Enum

class INTRADAY_TREND_CAPTURE(INTRADAY_BASE):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_TREND_CAPTURE']
    excl_attr_store = ['db_cache_mkt', 'last_processed_time', 'db_cache_algo']
    
    class TRADE_STATES(Enum):
        Start = 1
        Regular_buy = 2
        Overbought_takeprofit = 3
        Regular_sell = 4
        Oversold_takeprofit = 5
        Overbought_notrade = 6
        Oversold_notrade = 7
        Intraday_squareoff = 8
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, ema_kwargs=None, trade_agr_score=None, sqoff_agr_score=None, rescale_shorts=False, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, run_bars_since_sod, tickers, rescale_shorts, add_transaction_costs, inst_delta, app)
        self.ema_kwargs = ema_kwargs
        self.trade_agr_score = trade_agr_score
        self.sqoff_agr_score = sqoff_agr_score
        self.min_bars_to_trade = ema_kwargs.get('timeperiod', 9)
        self.trade_state = INTRADAY_TREND_CAPTURE.TRADE_STATES.Start
        self._state_vars = {}


    def update_indicators(self, dt=None):
        #assume capital requirement for short position is the same as going long
        self.run_bars_since_sod = self.run_bars_since_sod + 1
        self.units_whole_prev = self.units_whole.copy()
        is_trade_bar = False
        ticker = self.tickers[0] #only 1 ticker in this strategy
        if self.run_bars_since_sod >= self.min_bars_to_trade:
            data = self.extended_mkt.loc[dt]
            price = data['{} Close'.format(ticker)]
            returns = data['{} returns'.format(ticker)]
            ema = data['{} EMA'.format(ticker)]
            ohlc_cols = ['{} {}'.format(ticker, x) for x in ['Open', 'High', 'Low', 'Close'] ]
            ohlc = data[ohlc_cols]
            self.indicators_to_publish['EMA'] = ema
            self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
            #update per asset capital based on c-c returns
            if self.units_whole[ticker] >= 0:
                #if long then per_asset_capital increase is directly proportional to returns
                self.per_asset_capital[ticker] = self.per_asset_capital[ticker] * (1+self.inst_delta*returns) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            else:
                #if short then per asset capital increase is inversely proportional to returns
                self.per_asset_capital[ticker] = max(self.per_asset_capital[ticker] * (1-self.inst_delta*returns), 0.0) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            
            self.current_capital = np.array(list(self.per_asset_capital.values())).sum()
            is_trade_bar = self._generate_trades_on_indicators(ohlc, ema, dt, data['isEOD'])
        else:
            data = self.extended_mkt.loc[dt]
            price = data['{} Close'.format(ticker)]
            self.indicators_to_publish['EMA'] = None
            self.indicators_to_publish['Signal'] = None
            self.indicators_to_publish['trade_state'] = self.trade_state
            self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
                
        self._update_quick_bt_attrs(dt, is_trade=is_trade_bar)

    def _generate_trades_on_indicators(self, ohlc, ema, dt, isEOD=False):
        self.trade_state = INTRADAY_TREND_CAPTURE.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_TREND_CAPTURE.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        o, h, l, c = ['{} {}'.format(ticker, x) for x in ['Open', 'High', 'Low', 'Close']]
        signal = None
        
        is_up_bar = ohlc[c] > ohlc[o]
        is_dn_bar = ohlc[c] < ohlc[o]
        h_up_ema = ohlc[h] >= ema
        h_dn_ema = ohlc[h] <= ema
        c_up_ema = ohlc[c] >= ema
        c_dn_ema = ohlc[c] <= ema
        o_up_ema = ohlc[o] >= ema
        o_dn_ema = ohlc[o] <= ema
        l_up_ema = ohlc[l] >= ema
        l_dn_ema = ohlc[l] <= ema
        
        buy_signal_conditions = [
            l_up_ema and is_up_bar,
            o_up_ema and is_up_bar,
            c_up_ema and is_up_bar,
            h_up_ema and is_up_bar
        ]
        
        sell_signal_conditions = [
            h_dn_ema and is_dn_bar,
            o_dn_ema and is_dn_bar,
            c_dn_ema and is_dn_bar,
            l_dn_ema and is_dn_bar
        ]
        
        buy_sqoff_conditions = sell_signal_conditions.copy()
        buy_sqoff_conditions.reverse()
        sell_sqoff_conditions = buy_signal_conditions.copy()
        sell_sqoff_conditions.reverse()
        
        buy_signal = buy_signal_conditions[self.trade_agr_score]
        sell_signal = sell_signal_conditions[self.trade_agr_score]
        buy_sqoff_signal = buy_sqoff_conditions[self.sqoff_agr_score]
        sell_sqoff_signal = sell_sqoff_conditions[self.sqoff_agr_score]
        
        if not isEOD:
            if self.trade_state == INTRADAY_TREND_CAPTURE.TRADE_STATES.Intraday_squareoff:
                if buy_signal:
                    signal = 1
                    self.trade_state = INTRADAY_TREND_CAPTURE.TRADE_STATES.Regular_buy
                elif sell_signal:
                    signal = -1
                    self.trade_state = INTRADAY_TREND_CAPTURE.TRADE_STATES.Regular_sell
            elif self.trade_state == INTRADAY_TREND_CAPTURE.TRADE_STATES.Regular_buy:
                if sell_signal:
                    signal = -1
                    self.trade_state = INTRADAY_TREND_CAPTURE.TRADE_STATES.Regular_sell
                elif buy_sqoff_signal:
                    signal = 0
                    self.trade_state = INTRADAY_TREND_CAPTURE.TRADE_STATES.Intraday_squareoff
            elif self.trade_state == INTRADAY_TREND_CAPTURE.TRADE_STATES.Regular_sell:
                if buy_signal:
                    signal = 1
                    self.trade_state = INTRADAY_TREND_CAPTURE.TRADE_STATES.Regular_buy
                elif sell_sqoff_signal:
                    signal = 0
                    self.trade_state = INTRADAY_TREND_CAPTURE.TRADE_STATES.Intraday_squareoff
            else:
                signal = None
                print("unknown condition at state:{} at {}".format(self.trade_state, dt))
        else:
            signal = 0
            self.run_bars_since_sod = 0 #reset this attribute for next days run
            self.trade_state = INTRADAY_TREND_CAPTURE.TRADE_STATES.Start #reset this attribute for next days run
            
        self.indicators_to_publish['Signal'] = signal
        self.indicators_to_publish['trade_state'] = self.trade_state
        
        is_trade_bar = False
        for ticker in self.tickers:
            prev_wts = self.weights[ticker]
            self.weights[ticker] = signal if signal is not None else self.weights[ticker]
            #assuming only 1 ticker here
            is_trade_bar = False if prev_wts == self.weights[ticker] else True
    
        self._allocate_capital_by_weights()
        return is_trade_bar
    
    def prepare_strategy_attributes(self, dt_till=None):
        self.extended_mkt = self.db_cache_mkt.copy()
        #special handling incase particular tickers dont have data as of a given day
        self.extended_mkt.fillna(method='ffill', inplace=True)
        day_in_pydt = pd.Series(np.vectorize(lambda x: x.day)(pd.Series(self.extended_mkt.index.values).map(datetime.datetime.date)))
        self.extended_mkt['isEOD'] = (day_in_pydt != day_in_pydt.shift(-1)).values
        for ticker in self.tickers:
            self.extended_mkt['{} returns'.format(ticker)] = ROCP(self.extended_mkt['{} Close'.format(ticker)], timeperiod=1)
            self.extended_mkt['{} EMA'.format(ticker)] = EMA(self.extended_mkt['{} Close'.format(ticker)], **self.ema_kwargs)
        
    
class INTRADAY_TREND_HEIKIN(INTRADAY_BASE):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_TREND_HEIKIN']
    excl_attr_store = ['db_cache_mkt', 'last_processed_time', 'db_cache_algo']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, barsize_thresh_trade=None, ema_baseline=None, rescale_shorts=False, stop_loss=None, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, run_bars_since_sod, tickers, rescale_shorts, stop_loss, add_transaction_costs, inst_delta, app)
        self.min_bars_to_trade = 2
        self.barsize_thresh_trade = barsize_thresh_trade
        self.ema_baseline = ema_baseline
        self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Start
        self._state_vars = {'trailing_open': None, 'trailing_close': None, 'entry_barlen': None, 'entry_barlen_ha': None, 'entry_state': None, 'entry_rsi': None, 'entry_signal': None, 'entry_macd': None, 'entry_rocp': None, 'entry_price': None, 'entry_lw': None, 'entry_uw': None, 'prev_state': None}
        self.ha_barlen = None
        self.trade_contracts = {self.tickers[0]: {'long': None, 'short': None}}
        self.trade_direction = {self.tickers[0]: {'long': None, 'short': None}}
        self.ticker_to_conid = {}
        #self.models = {}
        
    def update_indicators(self, dt=None):
        #assume capital requirement for short position is the same as going long
        self.run_bars_since_sod = self.run_bars_since_sod + 1
        self.units_whole_prev = self.units_whole.copy()
        is_trade_bar = False
        ticker = self.tickers[0] #only 1 ticker in this strategy
        data = self.extended_mkt.loc[dt]
        price = data['{} Close'.format(ticker)]
        returns = data['{} returns'.format(ticker)]
        self.indicators_to_publish['{} Open_HA'.format(ticker)] = data['Open_HA']
        self.indicators_to_publish['{} High_HA'.format(ticker)] = data['High_HA']
        self.indicators_to_publish['{} Low_HA'.format(ticker)] = data['Low_HA']
        self.indicators_to_publish['{} Close_HA'.format(ticker)] = data['Close_HA']
        self.indicators_to_publish['RSI'] = data['RSI']
        self.indicators_to_publish['EMA'] = data['EMA']
        self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
        self._state_vars['prev_state'] = self.trade_state
        if self.run_bars_since_sod >= self.min_bars_to_trade:            
            #update per asset capital based on c-c returns
            if self.units_whole[ticker] >= 0:
                #if long then per_asset_capital increase is directly proportional to returns
                self.per_asset_capital[ticker] = self.per_asset_capital[ticker] * (1+self.inst_delta*returns) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            else:
                #if short then per asset capital increase is inversely proportional to returns
                self.per_asset_capital[ticker] = max(self.per_asset_capital[ticker] * (1-self.inst_delta*returns), 0.0) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            
            self.current_capital = np.array(list(self.per_asset_capital.values())).sum()
            is_trade_bar = self._generate_trades_on_indicators(data, dt, data['isEOD'])
        else:
            self.indicators_to_publish['Signal'] = None
            self.indicators_to_publish['trade_state'] = self.trade_state
            self._update_statevar_based_indicators(isnone=True)
                
        self._update_quick_bt_attrs(dt, is_trade=is_trade_bar)

    def _get_candle_thresholds(self, dt):
        avail_ha_barlen = self.ha_barlen[:dt].values
        nbr_candles = min(len(avail_ha_barlen), 5000)
        bar_lengths = np.abs(avail_ha_barlen[-1*nbr_candles:])
        bar_length_thresh = np.percentile(bar_lengths, self.barsize_thresh_trade)
        return bar_length_thresh
        
    def _generate_trades_on_indicators(self, data, dt, isEOD=False):
        self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_TREND_HEIKIN.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        signal = None
        ema = data['EMA']
        trending_up = data['{} Close'.format(ticker)] > ema if self.ema_baseline >= 1 else True
        trending_down = data['{} Close'.format(ticker)] < ema if self.ema_baseline >= 1 else True
        buy_signal = data['Close_HA'] > data['Open_HA']
        sell_signal = data['Close_HA'] < data['Open_HA']
        is_ignorable_buy_signal, is_ignorable_sell_signal = self._process_ignorable_signals(data, dt, buy_signal, sell_signal)
        is_sell_sl_triggered = self.trade_state == INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_sell and data['{} High'.format(ticker)] > self._state_vars['entry_price'] + (self.stop_loss * data['ATR'])
        is_buy_sl_triggered = self.trade_state == INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_buy and data['{} Low'.format(ticker)] < self._state_vars['entry_price'] - (self.stop_loss * data['ATR'])
        '''
        sample_barlen = (data['{} Close'.format(ticker)] - data['{} Open'.format(ticker)])*1e4/data['{} Close'.format(ticker)]
        sample_rsi = data['RSI']
        sample_macd = data['MACD']
        if self.models.get('buy', None) is not None:
            try:
                is_good_buy_signal = self.models['buy'].predict(np.array([sample_barlen, sample_rsi, sample_macd]).reshape(1,-1))[0]
                is_good_sell_signal = self.models['sell'].predict(np.array([sample_barlen, sample_rsi, sample_macd]).reshape(1,-1))[0]
            except:
                is_good_buy_signal, is_good_sell_signal = True, True
        else:
            is_good_buy_signal, is_good_sell_signal = True, True
        #print("signals are ({},{})".format(is_good_buy_signal, is_good_sell_signal))
        '''
        '''
        sample_barlen = (data['{} Close'.format(ticker)] - data['{} Open'.format(ticker)])*1e4/data['{} Close'.format(ticker)]
        sample_lw = (min(data['{} Close'.format(ticker)], data['{} Open'.format(ticker)]) - data['{} Low'.format(ticker)])*1e4/data['{} Close'.format(ticker)]
        sample_uw = (data['{} High'.format(ticker)] - max(data['{} Close'.format(ticker)], data['{} Open'.format(ticker)]))*1e4/data['{} Close'.format(ticker)]
        if self.models.get('buy', None) is not None:
            try:
                is_good_buy_signal = self.models['buy'].predict(np.array([sample_barlen, sample_lw, sample_uw]).reshape(1,-1))[0]
                is_good_sell_signal = self.models['sell'].predict(np.array([sample_barlen, sample_lw, sample_uw]).reshape(1,-1))[0]
            except:
                is_good_buy_signal, is_good_sell_signal = True, True
        else:
            is_good_buy_signal, is_good_sell_signal = True, True
        
        is_good_buy_signal, is_good_sell_signal = True, True
        '''
        if not isEOD:
            if self.trade_state == INTRADAY_TREND_HEIKIN.TRADE_STATES.Intraday_squareoff:
                if buy_signal and not is_ignorable_buy_signal and trending_up:
                    self._update_statevar_based_indicators()
                    signal = 1
                    self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_buy
                    self._update_statevars(data, signal)
                elif sell_signal and not is_ignorable_sell_signal and trending_down:
                    self._update_statevar_based_indicators()
                    signal = -1
                    self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_sell
                    self._update_statevars(data, signal)
                else:
                    self._update_statevar_based_indicators(isnone=True)
            elif self.trade_state == INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_buy:
                if sell_signal and not is_ignorable_sell_signal and trending_down:
                    self._update_statevar_based_indicators()
                    signal = -1
                    self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_sell
                    self._update_statevars(data, signal)
                elif is_buy_sl_triggered or (sell_signal and not is_ignorable_sell_signal and not trending_down):
                    self._update_statevar_based_indicators()
                    signal = 0
                    self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Intraday_squareoff
                    self._update_statevars(data, signal)
                else:
                    self._update_statevar_based_indicators(isnone=True)
            elif self.trade_state == INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_sell:
                if buy_signal and not is_ignorable_buy_signal and trending_up:
                    self._update_statevar_based_indicators()
                    signal = 1
                    self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_buy
                    self._update_statevars(data, signal)
                elif is_sell_sl_triggered or (buy_signal and not is_ignorable_buy_signal and not trending_up):
                    self._update_statevar_based_indicators()
                    signal = 0
                    self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Intraday_squareoff
                    self._update_statevars(data, signal)
                else:
                    self._update_statevar_based_indicators(isnone=True)
            else:
                self._update_statevar_based_indicators(isnone=True)
                signal = None
                print("unknown condition at state:{} at {}".format(self.trade_state, dt))
        else:
            self._update_statevar_based_indicators()
            signal = 0
            self.run_bars_since_sod = 0 #reset this attribute for next days run
            self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Start #reset this attribute for next days run
            self._update_statevars(data, signal)
            
        self.indicators_to_publish['Signal'] = signal
        self.indicators_to_publish['trade_state'] = self.trade_state
        
        is_trade_bar = False
        for ticker in self.tickers:
            prev_wts = self.weights[ticker]
            self.weights[ticker] = signal if signal is not None else self.weights[ticker]
            #assuming only 1 ticker here
            is_trade_bar = False if prev_wts == self.weights[ticker] else True
    
        self._allocate_capital_by_weights()
        return is_trade_bar
    
    def _update_statevars(self, data, signal):
        ticker = self.tickers[0]
        self._state_vars['entry_barlen'] = (data['{} Close'.format(ticker)] - data['{} Open'.format(ticker)])*1e4/data['{} Close'.format(ticker)]
        self._state_vars['entry_barlen_ha'] = (data['Close_HA'] - data['Open_HA'])*1e4/data['Close_HA']
        self._state_vars['entry_lw'] = (min(data['{} Close'.format(ticker)], data['{} Open'.format(ticker)]) - data['{} Low'.format(ticker)])*1e4/data['{} Close'.format(ticker)]
        self._state_vars['entry_uw'] = (data['{} High'.format(ticker)] - max(data['{} Close'.format(ticker)], data['{} Open'.format(ticker)]))*1e4/data['{} Close'.format(ticker)]
        self._state_vars['entry_state'] = self.trade_state
        self._state_vars['entry_rsi'] = data['RSI']
        self._state_vars['entry_rocp'] = data['ROCP-5']
        self._state_vars['entry_macd'] = data['MACD']
        self._state_vars['entry_price'] = data['{} Close'.format(ticker)] #this is a pure sv not to be published
        self._state_vars['entry_signal'] = signal
        
    def _update_statevar_based_indicators(self, isnone=False):
        self.indicators_to_publish['entry_barlen'] = self._state_vars['entry_barlen'] if not isnone else None
        self.indicators_to_publish['entry_barlen_ha'] = self._state_vars['entry_barlen_ha'] if not isnone else None
        self.indicators_to_publish['entry_lw'] = self._state_vars['entry_lw'] if not isnone else None
        self.indicators_to_publish['entry_uw'] = self._state_vars['entry_uw'] if not isnone else None
        self.indicators_to_publish['entry_state'] = self._state_vars['entry_state'] if not isnone else None
        self.indicators_to_publish['entry_rsi'] = self._state_vars['entry_rsi'] if not isnone else None
        self.indicators_to_publish['entry_rocp'] = self._state_vars['entry_rocp'] if not isnone else None
        self.indicators_to_publish['entry_macd'] = self._state_vars['entry_macd'] if not isnone else None
        self.indicators_to_publish['entry_signal'] = self._state_vars['entry_signal'] if not isnone else None
    
    def _process_ignorable_signals(self, data, dt, buy_signal, sell_signal):
        bar_length_thresh = self._get_candle_thresholds(dt)
        curr_bar_length = data['Close_HA'] - data['Open_HA']
        if abs(curr_bar_length) < bar_length_thresh:
            if self._state_vars['trailing_open'] is None:
                self._state_vars['trailing_open'] = data['Open_HA']
                self._state_vars['trailing_close'] = data['Close_HA']
            elif np.sign(curr_bar_length) != np.sign(self._state_vars['trailing_close'] - self._state_vars['trailing_open']):
                self._state_vars['trailing_open'] = data['Open_HA']
                self._state_vars['trailing_close'] = data['Close_HA']
            elif np.sign(curr_bar_length) == -1:
                self._state_vars['trailing_open'] = max(self._state_vars['trailing_open'], data['Open_HA'])
                self._state_vars['trailing_close'] = min(self._state_vars['trailing_close'], data['Close_HA'])
            elif np.sign(curr_bar_length) == 1:
                self._state_vars['trailing_open'] = min(self._state_vars['trailing_open'], data['Open_HA'])
                self._state_vars['trailing_close'] = max(self._state_vars['trailing_close'], data['Close_HA'])
            else:
                print('unknown condition encountered at {} for processing prevailing levels'.format(dt))
        else:
            self._state_vars['trailing_open'] = None
            self._state_vars['trailing_close'] = None
            
        is_ignorable_buy_signal = buy_signal and self._state_vars['trailing_open'] is not None and abs(self._state_vars['trailing_close'] - self._state_vars['trailing_open']) < bar_length_thresh
        is_ignorable_sell_signal = sell_signal and self._state_vars['trailing_open'] is not None and abs(self._state_vars['trailing_close'] - self._state_vars['trailing_open']) < bar_length_thresh
        
        return is_ignorable_buy_signal, is_ignorable_sell_signal

    def prepare_strategy_attributes(self, dt=None):
        self.extended_mkt = self.db_cache_mkt.copy()
        #special handling incase particular tickers dont have data as of a given day
        self.extended_mkt.fillna(method='ffill', inplace=True)
        day_in_pydt = pd.Series(np.vectorize(lambda x: x.day)(pd.Series(self.extended_mkt.index.values).map(datetime.datetime.date)))
        self.extended_mkt['isEOD'] = (day_in_pydt != day_in_pydt.shift(-1)).values
        if dt is not None:
            #hack for live run
            self.extended_mkt.loc[dt, 'isEOD'] = False
        ticker = self.tickers[0]
        
        self.extended_mkt['{} returns'.format(ticker)] = ROCP(self.extended_mkt['{} Close'.format(ticker)], timeperiod=1)
        self.extended_mkt['RSI'] = RSI(self.extended_mkt['{} Close'.format(ticker)], timeperiod=14)
        self.extended_mkt['ROCP-5'] = ROCP(self.extended_mkt['{} Close'.format(ticker)], timeperiod=5)
        self.extended_mkt['MACD'] = MACD(self.extended_mkt['{} Close'.format(ticker)])[2]
        self.extended_mkt['ATR'] = ATR(self.extended_mkt['{} High'.format(ticker)], self.extended_mkt['{} Low'.format(ticker)], self.extended_mkt['{} Close'.format(ticker)])
        self.extended_mkt['EMA'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.ema_baseline) if self.ema_baseline >= 1 else [np.nan] * len(self.extended_mkt) 
        self.extended_mkt = self.extended_mkt.loc[:dt].iloc[-5:] if dt is not None else self.extended_mkt
        o, h, l, c = ['{} {}'.format(ticker, x) for x in ['Open', 'High', 'Low', 'Close']]
        ha_open_l, ha_high_l, ha_low_l, ha_close_l, ha_barlen_l = [self.extended_mkt.iloc[0][o]], [self.extended_mkt.iloc[0][h]], [self.extended_mkt.iloc[0][l]], [self.extended_mkt.iloc[0][c]], [self.extended_mkt.iloc[0][c] - self.extended_mkt.iloc[0][o]]
        
        prices_open = self.extended_mkt[o].values
        prices_high = self.extended_mkt[h].values
        prices_low = self.extended_mkt[l].values
        prices_close = self.extended_mkt[c].values
        for index in range(0, len(self.extended_mkt)):
            if index == 0:
                continue
            prev_ha_open = ha_open_l[index-1]
            prev_ha_close = ha_close_l[index-1]
            curr_ha_close = (prices_open[index] + prices_high[index] + prices_low[index] + prices_close[index]) * 0.25
            curr_ha_open = (prev_ha_open + prev_ha_close) * 0.5
            ha_barlen_l.append(curr_ha_close - curr_ha_open)
            ha_close_l.append(curr_ha_close)
            ha_open_l.append(curr_ha_open)
            ha_high_l.append(max(prices_high[index], curr_ha_close, curr_ha_open))
            ha_low_l.append(min(prices_low[index], curr_ha_close, curr_ha_open))
        
        ha_dict = dict(zip(['Open_HA', 'High_HA', 'Low_HA', 'Close_HA', 'HA_barlen'], [ha_open_l, ha_high_l, ha_low_l, ha_close_l, ha_barlen_l])) 
        ha_ext = pd.DataFrame(data=ha_dict, index=self.extended_mkt.index.values)
        self.extended_mkt = pd.concat([self.extended_mkt, ha_ext], axis=1)
        if dt is None:
            self.ha_barlen = self.extended_mkt['HA_barlen']
        else:
            #assume that ha_barlen is of type pd.series which has already been populated  prior to running this
            self.ha_barlen[dt] = self.extended_mkt.loc[dt]['HA_barlen']
        #self._train_classifier()

    '''
    def _train_classifier(self):
        if not isfile(self.db_loc + 'train_data.csv'):
            return
        df_train = pd.read_csv(self.db_loc + 'train_data.csv')
        df_train.set_index('TimeStamp', inplace=True)
        df_train.loc[:, 'Eq Curve Realized'] = df_train['Eq Curve Realized'].fillna(method='ffill')
        df_train['returns'] = df_train['Eq Curve Realized'].pct_change()
        df_train['returns_bps'] = np.round(df_train['returns'] * 1e4, 1)
        #df_train_buy = df_train[df_train['entry_signal'] == 1][['entry_barlen', 'entry_rsi', 'entry_macd', 'entry_signal', 'returns_bps']].dropna(how='any')
        #df_train_sell = df_train[df_train['entry_signal'] == -1][['entry_barlen', 'entry_rsi', 'entry_macd', 'entry_signal', 'returns_bps']].dropna(how='any')
        df_train_buy = df_train[df_train['entry_signal'] == 1][['entry_barlen', 'entry_lw', 'entry_uw', 'entry_signal', 'returns_bps']].dropna(how='any')
        df_train_sell = df_train[df_train['entry_signal'] == -1][['entry_barlen', 'entry_lw', 'entry_uw', 'entry_signal', 'returns_bps']].dropna(how='any')
        df_train_buy['outcome'] = np.where(df_train_buy['returns_bps'] > 0, 1, 0)
        df_train_sell['outcome'] = np.where(df_train_sell['returns_bps'] > 0, 1, 0)
        
        params = {'name': 'KNN', 'params': {"n_neighbors": 10, "weights": 'distance', "p": 2}}
        #params = {'name': 'DecisionTreeClassifier', 'params': {'max_depth': 5, 'random_state': 40}}
        #params = {'name': 'SVC', 'params': {"C": 2, "kernel": 'poly'}}
        
        #self.models['buy'] = utils.construct_model(df_train_buy[['entry_barlen', 'entry_rsi', 'entry_macd']], df_train_buy['outcome'], params)
        #self.models['sell'] = utils.construct_model(df_train_sell[['entry_barlen', 'entry_rsi', 'entry_macd']], df_train_sell['outcome'], params)
        self.models['buy'] = utils.construct_model(df_train_buy[['entry_barlen', 'entry_lw', 'entry_uw']], df_train_buy['outcome'], params)
        self.models['sell'] = utils.construct_model(df_train_sell[['entry_barlen', 'entry_lw', 'entry_uw']], df_train_sell['outcome'], params)
    '''
    
class INTRADAY_TREND_HEIKIN_2(INTRADAY_BASE):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_TREND_HEIKIN_2']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, ema_baseline=None, ignore_indecisive=None, rescale_shorts=False, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, run_bars_since_sod, tickers, rescale_shorts, None, add_transaction_costs, inst_delta, app)
        self.min_bars_to_trade = 2
        self.ema_baseline = ema_baseline
        self.ignore_indecisive = ignore_indecisive or False
        self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Start
        self._state_vars = {'entry_state': None, 'entry_signal': None, 'entry_price': None, 'prev_state': None}
        self.trade_contracts = {self.tickers[0]: {'long': None, 'short': None}}
        self.trade_direction = {self.tickers[0]: {'long': None, 'short': None}}
        self.ticker_to_conid = {}
        
    def update_indicators(self, dt=None):
        #assume capital requirement for short position is the same as going long
        self.run_bars_since_sod = self.run_bars_since_sod + 1
        self.units_whole_prev = self.units_whole.copy()
        is_trade_bar = False
        ticker = self.tickers[0] #only 1 ticker in this strategy
        data = self.extended_mkt_dict[pd.Timestamp(dt)]
        price = data['{} Close'.format(ticker)]
        returns = data['{} returns'.format(ticker)]
        self.indicators_to_publish['EMA'] = data['EMA']
        self.indicators_to_publish['{} Open_HA'.format(ticker)] = data['Open_HA']
        self.indicators_to_publish['{} High_HA'.format(ticker)] = data['High_HA']
        self.indicators_to_publish['{} Low_HA'.format(ticker)] = data['Low_HA']
        self.indicators_to_publish['{} Close_HA'.format(ticker)] = data['Close_HA']
        self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
        self._state_vars['prev_state'] = self.trade_state
        if self.run_bars_since_sod >= self.min_bars_to_trade:            
            #update per asset capital based on c-c returns
            if self.units_whole[ticker] >= 0:
                #if long then per_asset_capital increase is directly proportional to returns
                self.per_asset_capital[ticker] = self.per_asset_capital[ticker] * (1+self.inst_delta*returns) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            else:
                #if short then per asset capital increase is inversely proportional to returns
                self.per_asset_capital[ticker] = max(self.per_asset_capital[ticker] * (1-self.inst_delta*returns), 0.0) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            
            self.current_capital = np.array(list(self.per_asset_capital.values())).sum()
            is_trade_bar = self._generate_trades_on_indicators(data, dt, data['isEOD'])
        else:
            self.indicators_to_publish['Signal'] = None
            self.indicators_to_publish['trade_state'] = self.trade_state
                
        self._update_quick_bt_attrs(dt, is_trade=is_trade_bar)
        
    def _generate_trades_on_indicators(self, data, dt, isEOD=False):
        self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_TREND_HEIKIN.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        signal = None
        ema = data['EMA']
        trending_up = data['{} Close'.format(ticker)] > ema if self.ema_baseline is not None else True
        trending_down = data['{} Close'.format(ticker)] < ema if self.ema_baseline is not None else True
        is_strong_bullish = data['Close_HA'] > data['Open_HA'] and data['Open_HA'] == data['Low_HA']
        is_strong_bearish = data['Close_HA'] < data['Open_HA'] and data['Open_HA'] == data['High_HA']
        is_indecisive_bullish = data['Close_HA'] > data['Open_HA'] and data['Open_HA'] != data['Low_HA']
        is_indecisive_bearish = data['Close_HA'] < data['Open_HA'] and data['Open_HA'] != data['High_HA']
        buy_signal = is_strong_bullish and trending_up
        buy_squareoff = is_indecisive_bearish or (is_strong_bearish and trending_up) if not self.ignore_indecisive else is_strong_bearish and trending_up
        sell_signal = is_strong_bearish and trending_down
        sell_squareoff = is_indecisive_bullish or (is_strong_bullish and trending_down) if not self.ignore_indecisive else is_strong_bullish and trending_down
        
        if not isEOD:
            if self.trade_state == INTRADAY_TREND_HEIKIN.TRADE_STATES.Intraday_squareoff:
                if buy_signal:
                    signal = 1
                    self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_buy
                elif sell_signal:
                    signal = -1
                    self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_sell
            elif self.trade_state == INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_buy:
                if buy_squareoff:
                    signal = 0
                    self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Intraday_squareoff
                elif sell_signal:
                    signal = -1
                    self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_sell
            elif self.trade_state == INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_sell:
                if sell_squareoff:
                    signal = 0
                    self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Intraday_squareoff
                elif buy_signal:
                    signal = 1
                    self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Regular_buy
            else:
                signal = None
                print("unknown condition at state:{} at {}".format(self.trade_state, dt))
        else:
            signal = 0
            self.run_bars_since_sod = 0 #reset this attribute for next days run
            self.trade_state = INTRADAY_TREND_HEIKIN.TRADE_STATES.Start #reset this attribute for next days run
            
        self.indicators_to_publish['Signal'] = signal
        self.indicators_to_publish['trade_state'] = self.trade_state
        
        is_trade_bar = False
        for ticker in self.tickers:
            prev_wts = self.weights[ticker]
            self.weights[ticker] = signal if signal is not None else self.weights[ticker]
            #assuming only 1 ticker here
            is_trade_bar = False if prev_wts == self.weights[ticker] else True
    
        self._allocate_capital_by_weights()
        return is_trade_bar

    def prepare_strategy_attributes(self, dt=None):
        self.extended_mkt = self.db_cache_mkt.copy()
        #special handling incase particular tickers dont have data as of a given day
        self.extended_mkt.fillna(method='ffill', inplace=True)
        day_in_pydt = pd.Series(np.vectorize(lambda x: x.day)(pd.Series(self.extended_mkt.index.values).map(datetime.datetime.date)))
        self.extended_mkt['isEOD'] = (day_in_pydt != day_in_pydt.shift(-1)).values
        if dt is not None:
            #hack for live run
            self.extended_mkt.loc[dt, 'isEOD'] = False
        ticker = self.tickers[0]
        
        self.extended_mkt['{} returns'.format(ticker)] = ROCP(self.extended_mkt['{} Close'.format(ticker)], timeperiod=1)
        self.extended_mkt['EMA'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.ema_baseline) if self.ema_baseline is not None else [np.nan] * len(self.extended_mkt) 
        self.extended_mkt = self.extended_mkt.loc[:dt].iloc[-5:] if dt is not None else self.extended_mkt
        o, h, l, c = ['{} {}'.format(ticker, x) for x in ['Open', 'High', 'Low', 'Close']]
        ha_open_l, ha_high_l, ha_low_l, ha_close_l, ha_barlen_l = [self.extended_mkt.iloc[0][o]], [self.extended_mkt.iloc[0][h]], [self.extended_mkt.iloc[0][l]], [self.extended_mkt.iloc[0][c]], [self.extended_mkt.iloc[0][c] - self.extended_mkt.iloc[0][o]]
        
        prices_open = self.extended_mkt[o].values
        prices_high = self.extended_mkt[h].values
        prices_low = self.extended_mkt[l].values
        prices_close = self.extended_mkt[c].values
        for index in range(0, len(self.extended_mkt)):
            if index == 0:
                continue
            prev_ha_open = ha_open_l[index-1]
            prev_ha_close = ha_close_l[index-1]
            curr_ha_close = (prices_open[index] + prices_high[index] + prices_low[index] + prices_close[index]) * 0.25
            curr_ha_open = (prev_ha_open + prev_ha_close) * 0.5
            ha_barlen_l.append(curr_ha_close - curr_ha_open)
            ha_close_l.append(curr_ha_close)
            ha_open_l.append(curr_ha_open)
            ha_high_l.append(max(prices_high[index], curr_ha_close, curr_ha_open))
            ha_low_l.append(min(prices_low[index], curr_ha_close, curr_ha_open))
        
        ha_dict = dict(zip(['Open_HA', 'High_HA', 'Low_HA', 'Close_HA', 'HA_barlen'], [ha_open_l, ha_high_l, ha_low_l, ha_close_l, ha_barlen_l])) 
        ha_ext = pd.DataFrame(data=ha_dict, index=self.extended_mkt.index.values)
        self.extended_mkt = pd.concat([self.extended_mkt, ha_ext], axis=1)
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
class INTRADAY_TREND_HEIKIN_3(INTRADAY_BASE):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_TREND_HEIKIN_3']
    
    class TRADE_STATES(Enum):
        Start = 1
        Regular_buy = 2
        Regular_sell = 3
        Regular_buy_pback = 4
        Regular_sell_pback = 5
        Intraday_squareoff = 6
    
    buy_states = [TRADE_STATES.Regular_buy, TRADE_STATES.Regular_buy_pback]
    sell_states = [TRADE_STATES.Regular_sell, TRADE_STATES.Regular_sell_pback]
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, ema_baseline=None, sl_on_ha=None, rescale_shorts=False, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, run_bars_since_sod, tickers, rescale_shorts, None, add_transaction_costs, inst_delta, app)
        self.min_bars_to_trade = 2
        self.ema_baseline = ema_baseline
        self.sl_on_ha = sl_on_ha or False
        self.trade_state = self.TRADE_STATES.Start
        self._state_vars = {'entry_state': None, 'entry_signal': None, 'entry_price': None, 'prev_state': None, 'swing_low': None, 'swing_high': None, 'swing_low_compute': None, 'swing_high_compute': None}
        self.trade_contracts = {self.tickers[0]: {'long': None, 'short': None}}
        self.trade_direction = {self.tickers[0]: {'long': None, 'short': None}}
        self.ticker_to_conid = {}
        
    def update_indicators(self, dt=None):
        #assume capital requirement for short position is the same as going long
        self.run_bars_since_sod = self.run_bars_since_sod + 1
        self.units_whole_prev = self.units_whole.copy()
        is_trade_bar = False
        ticker = self.tickers[0] #only 1 ticker in this strategy
        data = self.extended_mkt_dict[pd.Timestamp(dt)]
        price = data['{} Close'.format(ticker)]
        returns = data['{} returns'.format(ticker)]
        self.indicators_to_publish['EMA'] = data['EMA']
        self.indicators_to_publish['{} Open_HA'.format(ticker)] = data['Open_HA']
        self.indicators_to_publish['{} High_HA'.format(ticker)] = data['High_HA']
        self.indicators_to_publish['{} Low_HA'.format(ticker)] = data['Low_HA']
        self.indicators_to_publish['{} Close_HA'.format(ticker)] = data['Close_HA']
        self.indicators_to_publish['Price_swing_high'] = None
        self.indicators_to_publish['Price_swing_low'] = None
        self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
        self._state_vars['prev_state'] = self.trade_state
        if self.run_bars_since_sod >= self.min_bars_to_trade:            
            #update per asset capital based on c-c returns
            if self.units_whole[ticker] >= 0:
                #if long then per_asset_capital increase is directly proportional to returns
                self.per_asset_capital[ticker] = self.per_asset_capital[ticker] * (1+self.inst_delta*returns) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            else:
                #if short then per asset capital increase is inversely proportional to returns
                self.per_asset_capital[ticker] = max(self.per_asset_capital[ticker] * (1-self.inst_delta*returns), 0.0) if ~np.isnan(returns) else self.per_asset_capital[ticker]
            
            self.current_capital = np.array(list(self.per_asset_capital.values())).sum()
            is_trade_bar = self._generate_trades_on_indicators(data, dt, data['isEOD'])
        else:
            self.indicators_to_publish['Signal'] = None
            self.indicators_to_publish['trade_state'] = self.trade_state
                
        self._update_quick_bt_attrs(dt, is_trade=is_trade_bar)
        
    def _generate_trades_on_indicators(self, data, dt, isEOD=False):
        self.trade_state = self.TRADE_STATES.Intraday_squareoff if self.trade_state == self.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        signal = None
        ema = data['EMA']
        price_close = data['{} Close'.format(ticker)] if not self.sl_on_ha else data['Close_HA']
        price_high = data['{} High'.format(ticker)] if not self.sl_on_ha else data['High_HA']
        price_low = data['{} Low'.format(ticker)] if not self.sl_on_ha else data['Low_HA']
        trending_up = data['{} Close'.format(ticker)] > ema if self.ema_baseline is not None else True
        trending_down = data['{} Close'.format(ticker)] < ema if self.ema_baseline is not None else True
        is_strong_bullish = data['Close_HA'] > data['Open_HA'] and data['Open_HA'] == data['Low_HA']
        is_strong_bearish = data['Close_HA'] < data['Open_HA'] and data['Open_HA'] == data['High_HA']
        is_indecisive_bullish = data['Close_HA'] > data['Open_HA'] and data['Open_HA'] != data['Low_HA']
        is_indecisive_bearish = data['Close_HA'] < data['Open_HA'] and data['Open_HA'] != data['High_HA']
        buy_signal = is_strong_bullish and trending_up
        buy_compute_swing_low = is_indecisive_bearish or is_indecisive_bullish or is_strong_bearish
        buy_squareoff = price_close <= self._state_vars['swing_low'] if self._state_vars['swing_low'] is not None else False
        sell_signal = is_strong_bearish and trending_down
        sell_compute_swing_high = is_indecisive_bearish or is_indecisive_bullish or is_strong_bullish
        sell_squareoff = price_close >= self._state_vars['swing_high'] if self._state_vars['swing_high'] is not None else False
        
        if not isEOD:
            if self.trade_state == self.TRADE_STATES.Intraday_squareoff:
                if buy_signal:
                    signal = 1
                    self.trade_state = self.TRADE_STATES.Regular_buy
                    self._state_vars['swing_low'] = price_low
                elif sell_signal:
                    signal = -1
                    self.trade_state = self.TRADE_STATES.Regular_sell
                    self._state_vars['swing_high'] = price_high
            elif self.trade_state == self.TRADE_STATES.Regular_buy:
                if sell_signal and buy_squareoff:
                    signal = -1
                    self.trade_state = self.TRADE_STATES.Regular_sell
                    self._state_vars['swing_low'] = None
                    self._state_vars['swing_low_compute'] = None
                    self._state_vars['swing_high'] = price_high
                elif buy_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self._state_vars['swing_low'] = None
                    self._state_vars['swing_low_compute'] = None
                elif buy_compute_swing_low:
                    signal = None
                    self.trade_state = self.TRADE_STATES.Regular_buy_pback
                    self._state_vars['swing_low_compute'] = price_low
            elif  self.trade_state == self.TRADE_STATES.Regular_buy_pback:
                if sell_signal and buy_squareoff:
                    signal = -1
                    self.trade_state = self.TRADE_STATES.Regular_sell
                    self._state_vars['swing_low'] = None
                    self._state_vars['swing_low_compute'] = None
                    self._state_vars['swing_high'] = price_high
                elif buy_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self._state_vars['swing_low'] = None
                    self._state_vars['swing_low_compute'] = None
                elif is_strong_bullish: #not necessarily conventional buy_signal
                    signal = None
                    self.trade_state = self.TRADE_STATES.Regular_buy
                    self._state_vars['swing_low'] = max(self._state_vars['swing_low'], self._state_vars['swing_low_compute'])
                    self._state_vars['swing_low_compute'] = None
                elif buy_compute_swing_low:
                    signal = None
                    self.trade_state = self.TRADE_STATES.Regular_buy_pback
                    self._state_vars['swing_low_compute'] = min(price_low, self._state_vars['swing_low_compute'])
            elif self.trade_state == self.TRADE_STATES.Regular_sell:
                if buy_signal and sell_squareoff:
                    signal = 1
                    self.trade_state = self.TRADE_STATES.Regular_buy
                    self._state_vars['swing_high'] = None
                    self._state_vars['swing_high_compute'] = None
                    self._state_vars['swing_low'] = price_low
                elif sell_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self._state_vars['swing_high'] = None
                    self._state_vars['swing_high_compute'] = None
                elif sell_compute_swing_high:
                    signal = None
                    self.trade_state = self.TRADE_STATES.Regular_sell_pback
                    self._state_vars['swing_high_compute'] = price_high
            elif  self.trade_state == self.TRADE_STATES.Regular_sell_pback:
                if buy_signal and sell_squareoff:
                    signal = 1
                    self.trade_state = self.TRADE_STATES.Regular_buy
                    self._state_vars['swing_high'] = None
                    self._state_vars['swing_high_compute'] = None
                    self._state_vars['swing_low'] = price_low
                elif sell_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self._state_vars['swing_high'] = None
                    self._state_vars['swing_high_compute'] = None
                elif is_strong_bearish: #not necessarily conventional sell_signal
                    signal = None
                    self.trade_state = self.TRADE_STATES.Regular_sell
                    self._state_vars['swing_high'] = min(self._state_vars['swing_high'], self._state_vars['swing_high_compute'])
                    self._state_vars['swing_high_compute'] = None
                elif sell_compute_swing_high:
                    signal = None
                    self.trade_state = self.TRADE_STATES.Regular_sell_pback
                    self._state_vars['swing_high_compute'] = max(price_high, self._state_vars['swing_high_compute'])
            else:
                signal = None
                print("unknown condition at state:{} at {}".format(self.trade_state, dt))
        else:
            signal = 0
            self.run_bars_since_sod = 0 #reset this attribute for next days run
            self.trade_state = self.TRADE_STATES.Start #reset this attribute for next days run
            
        self.indicators_to_publish['Signal'] = signal
        self.indicators_to_publish['trade_state'] = self.trade_state
        self.indicators_to_publish['Price_swing_high'] = self._state_vars['swing_high']
        self.indicators_to_publish['Price_swing_low'] = self._state_vars['swing_low']
        
        is_trade_bar = False
        for ticker in self.tickers:
            prev_wts = self.weights[ticker]
            self.weights[ticker] = signal if signal is not None else self.weights[ticker]
            #assuming only 1 ticker here
            is_trade_bar = False if prev_wts == self.weights[ticker] else True
    
        self._allocate_capital_by_weights()
        return is_trade_bar

    def prepare_strategy_attributes(self, dt=None):
        self.extended_mkt = self.db_cache_mkt.copy()
        #special handling incase particular tickers dont have data as of a given day
        self.extended_mkt.fillna(method='ffill', inplace=True)
        day_in_pydt = pd.Series(np.vectorize(lambda x: x.day)(pd.Series(self.extended_mkt.index.values).map(datetime.datetime.date)))
        self.extended_mkt['isEOD'] = (day_in_pydt != day_in_pydt.shift(-1)).values
        if dt is not None:
            #hack for live run
            self.extended_mkt.loc[dt, 'isEOD'] = False
        ticker = self.tickers[0]
        
        self.extended_mkt['{} returns'.format(ticker)] = ROCP(self.extended_mkt['{} Close'.format(ticker)], timeperiod=1)
        self.extended_mkt['EMA'] = EMA(self.extended_mkt['{} Close'.format(ticker)], timeperiod=self.ema_baseline) if self.ema_baseline is not None else [np.nan] * len(self.extended_mkt) 
        self.extended_mkt = self.extended_mkt.loc[:dt].iloc[-5:] if dt is not None else self.extended_mkt
        o, h, l, c = ['{} {}'.format(ticker, x) for x in ['Open', 'High', 'Low', 'Close']]
        ha_open_l, ha_high_l, ha_low_l, ha_close_l, ha_barlen_l = [self.extended_mkt.iloc[0][o]], [self.extended_mkt.iloc[0][h]], [self.extended_mkt.iloc[0][l]], [self.extended_mkt.iloc[0][c]], [self.extended_mkt.iloc[0][c] - self.extended_mkt.iloc[0][o]]
        
        prices_open = self.extended_mkt[o].values
        prices_high = self.extended_mkt[h].values
        prices_low = self.extended_mkt[l].values
        prices_close = self.extended_mkt[c].values
        for index in range(0, len(self.extended_mkt)):
            if index == 0:
                continue
            prev_ha_open = ha_open_l[index-1]
            prev_ha_close = ha_close_l[index-1]
            curr_ha_close = (prices_open[index] + prices_high[index] + prices_low[index] + prices_close[index]) * 0.25
            curr_ha_open = (prev_ha_open + prev_ha_close) * 0.5
            ha_barlen_l.append(curr_ha_close - curr_ha_open)
            ha_close_l.append(curr_ha_close)
            ha_open_l.append(curr_ha_open)
            ha_high_l.append(max(prices_high[index], curr_ha_close, curr_ha_open))
            ha_low_l.append(min(prices_low[index], curr_ha_close, curr_ha_open))
        
        ha_dict = dict(zip(['Open_HA', 'High_HA', 'Low_HA', 'Close_HA', 'HA_barlen'], [ha_open_l, ha_high_l, ha_low_l, ha_close_l, ha_barlen_l])) 
        ha_ext = pd.DataFrame(data=ha_dict, index=self.extended_mkt.index.values)
        self.extended_mkt = pd.concat([self.extended_mkt, ha_ext], axis=1)
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')