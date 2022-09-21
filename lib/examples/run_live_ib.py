# -*- coding: utf-8 -*-
"""
Created on Mon May 17 17:50:27 2021

@author: vivin
"""
import argparse
from lib.engines.runner_utils import IB_LIVE_RUNNER

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parse optimizer arguments')
    parser.add_argument('--run_name', default='intraday-mac-usdinr')
    parser.add_argument('--tickers', default='USDINR')
    parser.add_argument('--initial_capital', default=10000000, type=float)
    parser.add_argument('--db_loc', default=None)
    args = parser.parse_args()
    tickers = args.tickers.split(',') if args.tickers is not None else None
    IB_LIVE_RUNNER.main(
        run_name=args.run_name,
        tickers=tickers,
        initial_capital=args.initial_capital,
        db_loc=args.db_loc
    )