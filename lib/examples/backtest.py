# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 18:04:34 2020

@author: vivin
"""

from lib.utils import utils
from lib.engines.runner_utils import RUNNER_UTILS
import numpy as np
import argparse        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parse optimizer arguments')
    parser.add_argument('--run_name', default='intraday-bkout-cstick')
    parser.add_argument('--tickers')
    parser.add_argument('--start', default='2021-05-25')
    parser.add_argument('--end', default='2022-08-21')
    parser.add_argument('--interval', default='15min', type=str)
    parser.add_argument('--initial_capital', default=3000000, type=float)
    parser.add_argument('--tvt_ratio', default='0.0,1.0', type=str)
    parser.add_argument('--generator_name', default='none')
    parser.add_argument('--generator_kwargs', default=None)
    parser.add_argument('--db_loc', default=None)
    args = parser.parse_args()
    generator_kwargs = utils.str2dict(args.generator_kwargs)
    tickers = args.tickers.split(',') if args.tickers is not None else ['NIFTY50.NS']
    tvt_ratio = [float(x) for x in args.tvt_ratio.split(',')]
    if len(tvt_ratio) != 2:
        raise Exception("tvt_ratio should be an array of size 2 for regular optimize")
    if np.sum(np.array(tvt_ratio)) != 1.0:
        raise Exception("tvt_ratio specified should sum up to 1")
    RUNNER_UTILS.backtest(
        run_name=args.run_name,
        tickers=tickers,
        start=args.start,
        end=args.end,
        interval=args.interval,
        initial_capital=args.initial_capital,
        tvt_ratio=tvt_ratio,
        generator_name=args.generator_name,
        generator_kwargs=generator_kwargs,
        db_loc=args.db_loc
    )