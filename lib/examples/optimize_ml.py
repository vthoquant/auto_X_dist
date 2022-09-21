# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 10:41:21 2020

@author: vivin
"""

from lib.utils import utils
from lib.engines.runner_utils import RUNNER_UTILS
import numpy as np
import argparse
from sklearnex import patch_sklearn
patch_sklearn()   

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parse optimizer arguments')
    parser.add_argument('--run_name', default='test')
    parser.add_argument('--strategy_name', default='MULTICLASS_CLASSIFIER_REBAL')
    parser.add_argument('--tickers')
    parser.add_argument('--start')
    parser.add_argument('--end')
    parser.add_argument('--initial_capital', default=1000000, type=float)
    parser.add_argument('--tvt_ratio', default='0.6,0.2,0.2', type=str)
    parser.add_argument('--generator_name', default='none')
    parser.add_argument('--generator_kwargs', default=None)
    parser.add_argument('--db_loc', default=None)
    args = parser.parse_args()
    generator_kwargs = utils.str2dict(args.generator_kwargs)
    tickers = args.tickers.split(',') if args.tickers is not None else None
    tvt_ratio = [float(x) for x in args.tvt_ratio.split(',')]
    if len(tvt_ratio) != 3:
        raise Exception("tvt_ratio should be an array of size 2 for regular optimize")
    if np.sum(np.array(tvt_ratio)) != 1.0:
        raise Exception("tvt_ratio specified should sum up to 1")
    RUNNER_UTILS.optimize_ml(
        run_name=args.run_name,
        strategy_name=args.strategy_name,
        tickers=tickers,
        start=args.start,
        end=args.end,
        initial_capital=args.initial_capital,
        tvt_ratio=tvt_ratio,
        generator_name=args.generator_name,
        generator_kwargs=generator_kwargs,
        db_loc=args.db_loc
    )