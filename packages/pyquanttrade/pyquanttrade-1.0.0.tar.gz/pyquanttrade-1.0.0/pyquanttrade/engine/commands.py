# -*- coding: utf-8 -*-
"""Functions from market data"""

# -*- coding: utf-8 -*-
"""Functions from market data"""

__author__ = "Miguel Martin"
__version__ = "1"

import logging
from datetime import datetime, timedelta
from pyquanttrade import market
from pyquanttrade.features.functions import third_order_exponential_smoothing
from pyquanttrade.market import marketData
from pyquanttrade.engine.trade import TradeList
from pyquanttrade.engine.test_result import TestResult
from pyquanttrade.engine.utils import default_comission_cost, default_slippage_cost
import pandas as pd
import numpy as np
from tqdm.auto import tqdm
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# TODO: end positions closes to compute final return
def backtest(
    policy,
    tickers,
    start_at,
    stop_at,
    capital=10000,
    commission=default_comission_cost,
    slippage_perc=default_slippage_cost,
    level=logging.WARNING,
    time_buffer=250,
    progress_bar = False
):
    logging.basicConfig(level=level)
    if not isinstance(tickers, list):
        tickers = [tickers]

    trade_list = TradeList(level=level)
    first_day = (
        datetime.strptime(start_at, "%Y-%m-%d").date() - timedelta(days=time_buffer)
    ).isoformat()

    policies = {}
    data_sims = {}
    data_dict = {}
    policy_class = policy
    logging.info(policy_class)
    remaining_capital = {tick: capital for tick in tickers}
    for ticker in tickers:
        policies[ticker] = policy_class
        logging.info(policy_class.name)
        data = marketData.get_data(ticker, first_day, stop_at)
        data_sim = data.loc[data.index >= start_at]

        if not data_sims:
            result = TestResult(data_sim, ticker, capital)
        else:
            result.add_ticker(data_sim, ticker, capital)

        data_sims[ticker] = data_sim
        data_dict[ticker] = data

    def calculate_num_shares(capital, share_price):
        num_shares = int(capital / share_price)
        remaining = capital - num_shares * share_price
        return (num_shares, remaining)

    def execute_policy(policy, i, row, data, capital, ticker):
        last_day = data.iloc[data.index.get_loc(i) - 1]
        signals = policy.execute(
            str(last_day.name).split(" ")[0], data, trades=trade_list
        )
        remaining = capital
        for signal in signals:
            if signal == "Buy_long":

                logging.info(str(ticker) + " : " + str(i) + " -- " + signal)
                loss = policy_class.long_stop_loss
                trailling = policy_class.long_stop_loss_trailling
                shares, remaining = calculate_num_shares(remaining, row["open"])
                trade_list.open_trade(
                    ticker,
                    "long",
                    str(i),
                    row["open"],
                    shares,
                    loss,
                    trailling,
                    commission,
                    slippage_perc,
                )
                logging.info("num of shares buyed: " + str(shares))
                logging.info("cost of shares buyed: " + str(shares * row["open"]))

            if signal == "Close_long":

                logging.info(str(ticker) + " : " + str(i) + " -- " + signal)
                money = trade_list.close_open_trades(
                    ticker, "long", str(i), row["open"]
                )
                remaining += money

            if signal == "Sell_short":

                logging.info(str(ticker) + " : " + str(i) + " -- " + signal)
                loss = policy_class.short_stop_loss
                trailling = policy_class.short_stop_loss_trailling
                shares, remaining = calculate_num_shares(remaining, row["open"])
                trade_list.open_trade(
                    ticker,
                    "short",
                    str(i),
                    row["open"],
                    shares,
                    loss,
                    trailling,
                    commission,
                    slippage_perc,
                )

            if signal == "Close_short":

                logging.info(str(ticker) + " : " + str(i) + " -- " + signal)
                money = trade_list.close_open_trades(
                    ticker, "short", str(i), row["open"]
                )
                remaining += money
        return remaining

    if progress_bar == True:
        iterable = tqdm(data_sims[tickers[0]].iterrows(), total = data_sims[tickers[0]].shape[0], smoothing=0)
    else:
        iterable = data_sims[tickers[0]].iterrows()

    for i, row in iterable:
        for ticker in policies.keys():
            if i in data_sims[ticker].index:
                ticker_row = data_sims[ticker].loc[i]
                remaining_capital[ticker] = execute_policy(
                    policies[ticker],
                    i,
                    ticker_row,
                    data_dict[ticker],
                    remaining_capital[ticker], 
                    ticker
                )
                money = trade_list.verify_stop_loss(
                    str(i), ticker, ticker_row["low"], ticker_row["high"]
                )
                remaining_capital[ticker] += money

                result.update(i, trade_list, ticker)

    #Data returns only works with one ticker, for visualization purposes
    return result, data

def plot_activity_list(activity_list, fig):
    
    #Decoding signal list as separate lists
    activity_list['buy_long'] = None
    activity_list.loc[activity_list['signals']=='Buy_long','buy_long'] = activity_list.loc[activity_list['signals']=='Buy_long','close']
    activity_list['rebuy_long'] = None
    activity_list.loc[activity_list['signals']=='Rebuy_long','rebuy_long'] = activity_list.loc[activity_list['signals']=='Rebuy_long','close']
    activity_list['close_long'] = None
    activity_list.loc[activity_list['signals']=='Close_long','close_long'] = activity_list.loc[activity_list['signals']=='Close_long','close']
    activity_list['sell_short'] = None
    activity_list.loc[activity_list['signals']=='Sell_short','sell_short'] = activity_list.loc[activity_list['signals']=='Sell_short','close']
    activity_list['resell_short'] = None
    activity_list.loc[activity_list['signals']=='Resell_short','resell_short'] = activity_list.loc[activity_list['signals']=='Resell_short','close']
    activity_list['close_short'] = None
    activity_list.loc[activity_list['signals']=='Close_short','close_short'] = activity_list.loc[activity_list['signals']=='Close_short','close']

    fig.add_trace(go.Scatter(x=activity_list['close'].index, y=activity_list['close'], mode='lines', name='Price', line={'width':1,'color':'black'}))
    if not activity_list['buy_long'].isnull().all(): 
        fig.add_trace(go.Scatter(x=activity_list['buy_long'].index, y=activity_list['buy_long'], mode='markers', name='Buy Long', marker ={'symbol':'arrow-up', 'size':9, 'color':'green'}))
    if not activity_list['rebuy_long'].isnull().all(): 
        fig.add_trace(go.Scatter(x=activity_list['rebuy_long'].index, y=activity_list['rebuy_long'], mode='markers', name='ReBuy Long', marker ={'symbol':'triangle-ne', 'size':9, 'color':'green'}))
    if not activity_list['close_long'].isnull().all(): 
        fig.add_trace(go.Scatter(x=activity_list['close_long'].index, y=activity_list['close_long'], mode='markers', name='Close Long', marker ={'symbol':'x', 'size':9, 'color':'green'}))
    if not activity_list['sell_short'].isnull().all(): 
        fig.add_trace(go.Scatter(x=activity_list['sell_short'].index, y=activity_list['sell_short'], mode='markers', name='Sell Short', marker ={'symbol':'arrow-down', 'size':9, 'color':'red'}))
    if not activity_list['resell_short'].isnull().all(): 
        fig.add_trace(go.Scatter(x=activity_list['resell_short'].index, y=activity_list['resell_short'], mode='markers', name='ReSell Short', marker ={'symbol':'triangle-se', 'size':9, 'color':'red'}))
    if not activity_list['close_short'].isnull().all(): 
        fig.add_trace(go.Scatter(x=activity_list['close_short'].index, y=activity_list['close_short'], mode='markers', name='Close Short', marker ={'symbol':'x', 'size':9, 'color':'red'}))
    
    return fig


def backtest_and_visualise(
    policy,
    ticker,
    start_at,
    stop_at,
    capital=10000,
    commission=default_comission_cost,
    slippage_perc=default_slippage_cost,
    level=logging.WARNING,
    time_buffer=250,
    progress_bar = False
):
    assert ticker is not list

    result, data = backtest(
        policy,
        ticker,
        start_at,
        stop_at,
        capital=capital,
        commission=commission,
        slippage_perc=slippage_perc,
        level=level,
        time_buffer=time_buffer,
        progress_bar = progress_bar)

    for _, trade in result.data.trade_list.trades_closed.items():
        if trade.type == 'long':
            data.loc[trade.open_day,'signals'] = 'Buy_long'
            data.loc[trade.close_day,'signals'] = 'Close_long'
        elif trade.type == 'short':
            data.loc[trade.open_day,'signals'] = 'Sell_short'
            data.loc[trade.close_day,'signals'] = 'Close_short'

    if len(policy.fourth_plot_functions)>0 : rows = 4
    elif len(policy.third_plot_functions)>0 : rows = 3
    elif len(policy.second_plot_functions)>0 : rows = 2
    else: rows = 1
    plot_dict = {2: policy.second_plot_functions, 3: policy.third_plot_functions, 4: policy.fourth_plot_functions}


    row, col = None, None
    if rows > 0 :
        row, col = 1, 1
        fig = make_subplots(rows = rows, cols = 1, shared_xaxes=True)
        if rows > 2: fig.update_layout(autosize=True, height=600)
        for i in range(2,rows+1):
            for elem in plot_dict[i]:
                if elem in data.columns:
                    fig.add_trace(go.Scatter(x = data.index, y = data[elem], mode='lines', name=elem, line={'width':1}), row = i, col = 1)
        

    else: 
        fig = go.Figure()

    plot_activity_list(data, fig)
    for elem in policy.plot_functions:
        if elem in data.columns:
            fig.add_trace(go.Scatter(x = data.index, y = data[elem], mode='lines', name=elem, line={'width':1}), row = row, col = col)

    return result, fig