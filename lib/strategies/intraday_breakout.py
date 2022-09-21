# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 13:51:08 2021

@author: vivin
"""
from lib.strategies.intraday_ma import INTRADAY_MA
from lib.strategies.base_classes import INTRADAY_BASE
from lib.configs.directory_names import STRATEGY_RUN_BASE_PATHS
from talib.abstract import ROCP, ATR
import datetime
import pandas as pd
import numpy as np

class INTRADAY_BREAKOUT_HILO(INTRADAY_MA):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_BREAKOUT_HILO']
        
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, sl_atr=None, tp_atr=None, is_trailing_sl=None, false_breakout=None, rescale_shorts=False, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, None, tickers, rescale_shorts, None, add_transaction_costs, inst_delta, app)
        self.trade_state = self.TRADE_STATES.Start
        self.sl_atr = sl_atr or 1.0
        self.tp_atr = tp_atr
        self.is_trailing_sl = is_trailing_sl or False
        self.false_breakout = false_breakout or False
        self.range_fin_time = (9, 30) # in (hour, min) format
        self.run_bars_since_sod = run_bars_since_sod
        self._state_vars = {'prev_state': None, 'day_hi': None, 'day_lo': None, 'entry_price': None, 'trailing_price': None}
        self.trade_contracts = {self.tickers[0]: {'long': None, 'short': None}}
        self.ticker_to_conid = {}
        
    def update_indicators(self, dt=None):
        #assume capital requirement for short position is the same as going long
        self.run_bars_since_sod = self.run_bars_since_sod + 1
        self.units_whole_prev = self.units_whole.copy()
        is_trade_bar = False
        py_dt = pd.Timestamp(dt).to_pydatetime()
        ticker = self.tickers[0] #only 1 ticker in this strategy
        data = self.extended_mkt_dict[pd.Timestamp(dt)]
        price = data['{} Close'.format(ticker)]
        returns = data['{} returns'.format(ticker)]
        self.live_prices[ticker] = price if ~np.isnan(price) else -1.0
        self._state_vars['prev_state'] = self.trade_state
        self.indicators_to_publish['entry_price'] = None
        self.indicators_to_publish['trailing_price'] = None
        if 'day_hi' not in self.indicators_to_publish:
            self.indicators_to_publish['day_hi'] = data['{} High'.format(ticker)]
            self.indicators_to_publish['day_lo'] = data['{} Low'.format(ticker)]
        #else:
        #    self.indicators_to_publish['day_hi'] = max(self.indicators_to_publish['day_hi'], data['{} High'.format(ticker)])
        #    self.indicators_to_publish['day_lo'] = min(self.indicators_to_publish['day_lo'], data['{} Low'.format(ticker)])
        if (py_dt.hour == self.range_fin_time[0] and py_dt.minute > self.range_fin_time[1]) or (py_dt.hour > self.range_fin_time[0]):            
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
            self.indicators_to_publish['day_hi'] = max(self.indicators_to_publish['day_hi'], data['{} High'.format(ticker)])
            self.indicators_to_publish['day_lo'] = min(self.indicators_to_publish['day_lo'], data['{} Low'.format(ticker)])
            
        self._update_quick_bt_attrs(dt, is_trade=is_trade_bar)
        
    def _generate_trades_on_indicators(self, data, dt, isEOD=False):
        self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_MA.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        signal = None
        atr = data['ATR']
        price_trailing = self._state_vars['trailing_price']
        price_entry = self._state_vars['entry_price']
        price_close = data['{} Close'.format(ticker)]
        buy_signal = price_close > self.indicators_to_publish['day_hi'] if not self.false_breakout else price_close < self.indicators_to_publish['day_lo']
        sell_signal = price_close < self.indicators_to_publish['day_lo'] if not self.false_breakout else price_close > self.indicators_to_publish['day_hi']
        sl_hit_price = price_entry if not self.is_trailing_sl else price_trailing
        buy_squareoff = price_entry is not None and ((price_close - price_entry > atr * self.tp_atr) or (price_close - sl_hit_price < -atr * self.sl_atr))
        sell_squareoff = price_entry is not None and ((price_close - price_entry < -atr * self.tp_atr) or (price_close - sl_hit_price > atr * self.sl_atr))
        
        if not isEOD:
            if self.trade_state == self.TRADE_STATES.Intraday_squareoff:
                if buy_signal:
                    signal = 1
                    self.trade_state = self.TRADE_STATES.Regular_buy
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
                    self._state_vars['trailing_price'] = price_close
                elif sell_signal:
                    signal = -1
                    self.trade_state = self.TRADE_STATES.Regular_sell
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
                    self._state_vars['trailing_price'] = price_close
            elif self.trade_state == self.TRADE_STATES.Regular_buy:
                if buy_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self.bars_since_trade = None
                    self.indicators_to_publish['entry_price'] = self._state_vars['entry_price']
                    self.indicators_to_publish['trailing_price'] = self._state_vars['trailing_price']
                else:
                    self.bars_since_trade = self.bars_since_trade + 1
                    self._state_vars['trailing_price'] = max(self._state_vars['trailing_price'], price_close)
            elif self.trade_state == self.TRADE_STATES.Regular_sell:
                if sell_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self.bars_since_trade = None
                    self.indicators_to_publish['entry_price'] = self._state_vars['entry_price']
                    self.indicators_to_publish['trailing_price'] = self._state_vars['trailing_price']
                else:
                    self.bars_since_trade = self.bars_since_trade + 1
                    self._state_vars['trailing_price'] = min(self._state_vars['trailing_price'], price_close)
            else:
                signal = None
                print("unknown condition at state:{} at {}".format(self.trade_state, dt))
        else:
            signal = 0
            self.run_bars_since_sod = 0 #reset this attribute for next days run
            self.trade_state = self.TRADE_STATES.Start #reset this attribute for next days run
            
        self.indicators_to_publish['Signal'] = signal
        self.indicators_to_publish['trade_state'] = self.trade_state
        self.indicators_to_publish['day_hi'] = max(self.indicators_to_publish['day_hi'], data['{} High'.format(ticker)])
        self.indicators_to_publish['day_lo'] = min(self.indicators_to_publish['day_lo'], data['{} Low'.format(ticker)])
        
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
        self.extended_mkt['ATR'] = ATR(self.extended_mkt['{} High'.format(ticker)], self.extended_mkt['{} Low'.format(ticker)], self.extended_mkt['{} Close'.format(ticker)])
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
class INTRADAY_BREAKOUT_CSTICK(INTRADAY_MA):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_BREAKOUT_CSTICK']
        
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, lookback_period=None, sl_atr=None, tp_atr=None, is_trailing_sl=None, rescale_shorts=False, add_transaction_costs=False, inst_delta=1.0, app=None):
        INTRADAY_BASE.__init__(self, identifier, initial_capital, run_bars_since_sod, tickers, rescale_shorts, None, add_transaction_costs, inst_delta, app)
        self.trade_state = self.TRADE_STATES.Start
        self.lookback_period = lookback_period or 1
        self.sl_atr = sl_atr or 1.0
        self.tp_atr = tp_atr or 1.0
        self.is_trailing_sl = is_trailing_sl or False
        self.min_bars_to_trade = 2   #hardcoded for now
        self._state_vars = {'prev_state': None, 'entry_price': None, 'trailing_price': None}
        self.trade_contracts = {self.tickers[0]: {'long': None, 'short': None}}
        self.ticker_to_conid = {}
        
    def update_indicators(self, dt=None):
        #assume capital requirement for short position is the same as going long
        self.run_bars_since_sod = self.run_bars_since_sod + 1
        self.units_whole_prev = self.units_whole.copy()
        is_trade_bar = False
        ticker = self.tickers[0] #only 1 ticker in this strategy
        #data = self.extended_mkt.loc[dt]
        data = self.extended_mkt_dict[pd.Timestamp(dt)]
        price = data['{} Close'.format(ticker)]
        returns = data['{} returns'.format(ticker)]
        self._update_indicators_to_publish(data)
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
        
    def _update_indicators_to_publish(self, data):
        self.indicators_to_publish['lookback_min'] = data['lookback_min']
        self.indicators_to_publish['lookback_max'] = data['lookback_max']
        self.indicators_to_publish['entry_price'] = None
        self.indicators_to_publish['trailing_price'] = None
        
    def _generate_trades_on_indicators(self, data, dt, isEOD=False):
        signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff = self._generate_trade_conditions(data, dt)
        is_trade_bar = self._process_conditions(data, dt, signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff, isEOD)
        return is_trade_bar
    
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_MA.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        signal = None
        atr = data['ATR']
        price_trailing = self._state_vars['trailing_price']
        price_entry = self._state_vars['entry_price']
        price_close = data['{} Close'.format(ticker)]
        lookback_max = data['lookback_max']
        lookback_min = data['lookback_min']
        buy_signal = price_close > lookback_max
        sell_signal = price_close < lookback_min
        sl_hit_price = price_entry if not self.is_trailing_sl else price_trailing
        buy_squareoff = price_entry is not None and ((price_close - price_entry > atr * self.tp_atr) or (price_close - sl_hit_price < -atr * self.sl_atr))
        sell_squareoff = price_entry is not None and ((price_close - price_entry < -atr * self.tp_atr) or (price_close - sl_hit_price > atr * self.sl_atr))
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
        
    def _process_conditions(self, data, dt, signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff, isEOD=False):
        if hasattr(self, 'side_restriction'):
            if self.side_restriction == 1:
                #only long trades allowed
                sell_signal, sell_squareoff = False, False
            elif self.side_restriction == -1:
                #only short trades allowed
                buy_signal, buy_squareoff = False, False
        
        price_close = data['{} Close'.format(self.tickers[0])]
        if not isEOD:
            if self.trade_state == self.TRADE_STATES.Intraday_squareoff:
                if buy_signal:
                    signal = 1
                    self.trade_state = self.TRADE_STATES.Regular_buy
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
                    self._state_vars['trailing_price'] = price_close
                elif sell_signal:
                    signal = -1
                    self.trade_state = self.TRADE_STATES.Regular_sell
                    self.bars_since_trade = 1
                    self._state_vars['entry_price'] = price_close
                    self._state_vars['trailing_price'] = price_close
            elif self.trade_state == self.TRADE_STATES.Regular_buy:
                if buy_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self.bars_since_trade = None
                    self.indicators_to_publish['entry_price'] = self._state_vars['entry_price']
                    self.indicators_to_publish['trailing_price'] = self._state_vars['trailing_price']
                else:
                    self.bars_since_trade = self.bars_since_trade + 1
                    self._state_vars['trailing_price'] = max(self._state_vars['trailing_price'], price_close)
            elif self.trade_state == self.TRADE_STATES.Regular_sell:
                if sell_squareoff:
                    signal = 0
                    self.trade_state = self.TRADE_STATES.Intraday_squareoff
                    self.bars_since_trade = None
                    self.indicators_to_publish['entry_price'] = self._state_vars['entry_price']
                    self.indicators_to_publish['trailing_price'] = self._state_vars['trailing_price']
                else:
                    self.bars_since_trade = self.bars_since_trade + 1
                    self._state_vars['trailing_price'] = min(self._state_vars['trailing_price'], price_close)
            else:
                signal = None
                print("unknown condition at state:{} at {}".format(self.trade_state, dt))
        else:
            signal = 0
            self.run_bars_since_sod = 0 #reset this attribute for next days run
            self.trade_state = self.TRADE_STATES.Start #reset this attribute for next days run
            
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
        self.extended_mkt['ATR'] = ATR(self.extended_mkt['{} High'.format(ticker)], self.extended_mkt['{} Low'.format(ticker)], self.extended_mkt['{} Close'.format(ticker)])
        self.extended_mkt['lookback_max'] = self.extended_mkt['{} High'.format(ticker)].shift(1).rolling(window=self.lookback_period).max()
        self.extended_mkt['lookback_min'] = self.extended_mkt['{} Low'.format(ticker)].shift(1).rolling(window=self.lookback_period).min()
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
class INTRADAY_DBLBREAKOUT_CSTICK(INTRADAY_BREAKOUT_CSTICK):
    db_loc = STRATEGY_RUN_BASE_PATHS['INTRADAY_DBLBREAKOUT_CSTICK']
    
    def __init__(self, identifier, initial_capital=1000000, run_bars_since_sod=0, tickers=None, lookback_period=None, eod_lookback_period=None, sl_atr=None, tp_atr=None, is_trailing_sl=None, rescale_shorts=False, add_transaction_costs=False, inst_delta=1.0, app=None):
        super(INTRADAY_DBLBREAKOUT_CSTICK, self).__init__(identifier, initial_capital, run_bars_since_sod, tickers, lookback_period, sl_atr, tp_atr, is_trailing_sl, rescale_shorts, add_transaction_costs, inst_delta, app)
        self.eod_lookback_period = eod_lookback_period or 1
        
    def prepare_strategy_attributes(self, dt=None):
        super(INTRADAY_DBLBREAKOUT_CSTICK, self).prepare_strategy_attributes(dt)
        ticker = self.tickers[0]
        ohlcv_agg = {'{} Open'.format(ticker): 'first', '{} High'.format(ticker): 'max', '{} Low'.format(ticker): 'min', '{} Close'.format(ticker): 'last'}
        df_resampled = self.extended_mkt.resample('1D', origin='9:15:00').agg(ohlcv_agg)
        df_resampled = df_resampled.shift(1)
        df_resampled.rename(columns={'{} Open'.format(ticker): 'prev_open', '{} High'.format(ticker): 'prev_high', '{} Low'.format(ticker): 'prev_low', '{} Close'.format(ticker): 'prev_close'}, inplace=True)
        df_resampled['eod_lookback_max'] = df_resampled['prev_high'].rolling(window=self.eod_lookback_period).max()
        df_resampled['eod_lookback_min'] = df_resampled['prev_low'].rolling(window=self.eod_lookback_period).min()
        #upsample
        df_resampled = df_resampled.reindex(self.extended_mkt.index)
        df_resampled.fillna(method='ffill', inplace=True)
        self.extended_mkt['eod_lookback_max'] = df_resampled.loc[:, 'eod_lookback_max']
        self.extended_mkt['eod_lookback_min'] = df_resampled.loc[:, 'eod_lookback_min']
        self.extended_mkt_dict = self.extended_mkt.to_dict(orient='index')
        
    def _update_indicators_to_publish(self, data):
        super(INTRADAY_DBLBREAKOUT_CSTICK, self)._update_indicators_to_publish(data)
        self.indicators_to_publish['eod_lookback_min'] = data['eod_lookback_min']
        self.indicators_to_publish['eod_lookback_max'] = data['eod_lookback_max']
        
    def _generate_trade_conditions(self, data, dt):
        self.trade_state = INTRADAY_MA.TRADE_STATES.Intraday_squareoff if self.trade_state == INTRADAY_MA.TRADE_STATES.Start else self.trade_state
        ticker = self.tickers[0]
        signal = None
        atr = data['ATR']
        price_trailing = self._state_vars['trailing_price']
        price_entry = self._state_vars['entry_price']
        price_close = data['{} Close'.format(ticker)]
        lookback_max = data['lookback_max']
        lookback_min = data['lookback_min']
        eod_lookback_max = data['eod_lookback_max']
        eod_lookback_min = data['eod_lookback_min']
        buy_signal = price_close > lookback_max and price_close > eod_lookback_max
        sell_signal = price_close < lookback_min and price_close < eod_lookback_min
        sl_hit_price = price_entry if not self.is_trailing_sl else price_trailing
        buy_squareoff = price_entry is not None and ((price_close - price_entry > atr * self.tp_atr) or (price_close - sl_hit_price < -atr * self.sl_atr))
        sell_squareoff = price_entry is not None and ((price_close - price_entry < -atr * self.tp_atr) or (price_close - sl_hit_price > atr * self.sl_atr))
        return signal, buy_signal, buy_squareoff, sell_signal, sell_squareoff
