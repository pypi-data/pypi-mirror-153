import re
import datetime
import threading
import numpy as np
import pandas as pd
from typing import Union
from pandas.tseries.offsets import DateOffset

import finlab
from finlab import data, market_info, report
from finlab import mae_mfe as maemfe
from finlab.utils import check_version, requests, set_global
from finlab.backtest_core import backtest_, get_trade_stocks
from finlab.dataframe import FinlabDataFrame


def download_backtest_encryption_function_factory():

    encryption_time = datetime.datetime.now()
    encryption = ''

    def ret():

        nonlocal encryption_time
        nonlocal encryption

        if datetime.datetime.now() < encryption_time + datetime.timedelta(days=1) and encryption:
            return encryption

        res = requests.get('https://asia-east2-fdata-299302.cloudfunctions.net/auth_backtest',
                {'api_token': finlab.get_token(), 'time': str(datetime.datetime.now())})

        if not res.ok:
            try:
                result = res.json()
            except:
                result = None

            print(result)
            return ''

        d = res.json()

        if 'v' in d and 'v_msg' in d and finlab.__version__ < d['v']:
            print(d['v_msg'])

        if 'msg' in d:
            print(d['msg'])

        encryption_time = datetime.datetime.now()
        encryption = d['encryption']

        return encryption
    return ret

download_backtest_encryption = download_backtest_encryption_function_factory()

def arguments(price, position, resample_dates=None):
    resample_dates = price.index if resample_dates is None else resample_dates
    resample_dates = pd.Series(resample_dates).view(np.int64).values

    position = position.astype(float).fillna(0)
    price = price.astype(float)

    return [price.values,
            price.index.view(np.int64),
            price.columns.astype(str).values,
            position.values,
            position.index.view(np.int64),
            position.columns.astype(str).values,
            resample_dates
            ]

def sim(position: Union[pd.DataFrame, pd.Series], resample=None, trade_at_price='close',
        position_limit=1, fee_ratio=1.425/1000,
        tax_ratio=3/1000, name=None, stop_loss=None,
        take_profit=None, touched_exit=False,
        mae_mfe_window=0, mae_mfe_window_step=1, market='AUTO', trade_info=None, upload=True):

    # check version
    check_version()

    # auto detect market type
    if market == 'AUTO':
        market = 'TWSTOCK'

        if isinstance(position, pd.DataFrame) and (position.columns.str.find('USDT') != -1).any():
            market = 'CRYPTO'
        if isinstance(position, pd.Series) and 'USDT' in position.name:
            market = 'CRYPTO'

    # get market position according to market type
    if isinstance(market, str):
        assert market in ['TWSTOCK', 'CRYPTO']
        market = {
            'TWSTOCK': market_info.TWMarketInfo,
            'CRYPTO': market_info.CryptoMarketInfo,
        }[market]

    # determine trading price
    price = market.get_price(trade_at_price, adj=True)

    # check position types
    if isinstance(position, pd.Series):
        if position.name in price.columns:
            position = position.to_frame()
        else:
            raise Exception('Asset name not found. Please asign asset name by "position.name = \'2330\'".')

    # check name is valid
    if name:
        head_is_eng = len(re.findall(
            r'[\u0041-\u005a|\u0061-\u007a]', name[0])) > 0
        has_cn = len(re.findall('[\u4e00-\u9fa5]', name[1:])) > 0
        if head_is_eng and has_cn:
            raise Exception('Strategy Name Error: 名稱如包含中文，需以中文當開頭。')

    # check position is valid
    if position.sum().sum() == 0 or len(position.index) == 0:
        raise Exception('Position is empty and zero stock is selected.')

    # format position index
    if isinstance(position.index[0], str):
        position = FinlabDataFrame(position).index_str_to_date()

    # if position date is very close to price end date, run all backtesting dates
    assert len(position.shape) >= 2
    delta_time_rebalance = position.index[-1] - position.index[-3]
    backtest_to_end = position.index[-1] + \
        delta_time_rebalance > price.index[-1]

    position = position[position.index <= price.index[-1]]
    backtest_end_date = price.index[-1] if backtest_to_end else position.index[-1]

    # resample dates
    dates = None
    next_trading_date = position.index[-1].tz_localize(None)
    if isinstance(resample, str):

        offset_days = 0
        if '+' in resample:
            offset_days = int(resample.split('+')[-1])
            resample = resample.split('+')[0]
        if '-' in resample and resample.split('-')[-1].isdigit():
            offset_days = -int(resample.split('-')[-1])
            resample = resample.split('-')[0]

        dates = pd.date_range(
            position.index[0], position.index[-1]+ datetime.timedelta(days=720), freq=resample, tz=position.index.tzinfo)
        dates += DateOffset(days=offset_days)
        dates = [d for d in dates if position.index[0]
                 <= d and d <= position.index[-1]]

        next_trading_date = min(
                set(pd.date_range(position.index[0],
                    datetime.datetime.now(position.index.tzinfo)
                    + datetime.timedelta(days=720),
                    freq=resample)) - set(dates))

        if dates[-1] != position.index[-1]:
            dates += [next_trading_date]

    if stop_loss is None or stop_loss == 0:
        stop_loss = -np.inf

    if take_profit is None or take_profit == 0:
        take_profit = np.inf

    if dates is not None:
        position = position.reindex(dates, method='ffill')

    encryption = download_backtest_encryption()

    if encryption == '':
      return

    creturn_value = backtest_(*arguments(price, position, dates),
                              encryption=encryption,
                              fee_ratio=fee_ratio, tax_ratio=tax_ratio,
                              stop_loss=stop_loss, take_profit=take_profit,
                              touched_exit=touched_exit, position_limit=position_limit,
                              mae_mfe_window=mae_mfe_window, mae_mfe_window_step=mae_mfe_window_step)

    total_weight = position.sum(axis=1)

    position = position.div(total_weight.where(total_weight!=0, np.nan), axis=0).fillna(0)
    position = position.clip(-abs(position_limit), abs(position_limit))

    creturn = pd.Series(creturn_value, price.index)
    creturn = creturn[(creturn != 1).cumsum().shift(-1, fill_value=1) != 0]
    creturn = creturn.loc[:backtest_end_date]
    if len(creturn) == 0:
        creturn = pd.Series(1, position.index)

    trades, operation_and_weight = get_trade_stocks(position.columns.astype(str).values, price.index.view(np.int64))
    trades = pd.DataFrame(trades)

    if len(trades) != 0:

        trades.columns = ['stock_id', 'entry_date', 'exit_date',
                     'entry_sig_date', 'exit_sig_date',
                     'position', 'period', 'entry_index', 'exit_index']

        trades.index.name = 'trade_index'

        for col in ['entry_date', 'exit_date', 'entry_sig_date', 'exit_sig_date']:
            trades[col] = pd.to_datetime(trades[col])
            trades[col] = trades[col].dt.tz_localize(None)

        trades.loc[trades.exit_index == -1, ['exit_date', 'exit_sig_date']] = pd.NaT

        m = pd.DataFrame(maemfe.mae_mfe)
        nsets = int((m.shape[1]-1) / 6)

        metrics = ['mae', 'gmfe', 'bmfe', 'mdd', 'pdays', 'return']

        tuples = sum([[(n, metric) if n == 'exit' else (n * mae_mfe_window_step, metric)
                       for metric in metrics] for n in list(range(nsets)) + ['exit']], [])

        m.columns = pd.MultiIndex.from_tuples(
            tuples, names=["window", "metric"])
        m.index.name = 'trade_index'
        m[m == -1] = np.nan

        trades['return'] = m.iloc[:, -1]

    r = report.Report(
        creturn=creturn,
        position=position,
        fee_ratio=fee_ratio,
        tax_ratio=tax_ratio,
        trade_at=trade_at_price,
        next_trading_date=next_trading_date,
        market_info=market)

    r.resample = resample

    if len(trades) != 0:
        r.trades = trades

    if len(m) != 0:
        r.mae_mfe = m

    r.add_trade_info('entry_price', market.get_price(trade_at_price, adj=False), 'entry_date')
    r.add_trade_info('exit_price', market.get_price(trade_at_price, adj=False), 'exit_date')

    if trade_info is not None:
        for t in trade_info:
            r.add_trade_info(*t)

    if len(operation_and_weight['actions']) != 0:

        # find selling and buying stocks
        actions = pd.Series(operation_and_weight['actions'])
        actions.index = r.position.columns[actions.index]
        r.actions = actions

        sell_sids = actions[actions == 'exit'].index
        buy_sids = actions[actions == 'enter'].index
        r_position = set(trades.stock_id[trades.exit_sig_date.isnull()])

        # check if the sell stocks are in the current position
        assert len(set(sell_sids) - r_position) == 0

        # fill exit_sig_date and exit_date
        trades.loc[trades.stock_id.isin(sell_sids), 'exit_sig_date'] = \
            trades.loc[trades.stock_id.isin(sell_sids), 'exit_sig_date'].fillna(r.position.index[-1].tz_localize(None))
        trades.loc[trades.stock_id.isin(sell_sids), 'exit_date'] = \
            trades.loc[trades.stock_id.isin(sell_sids), 'exit_date']

        final_trades = pd.concat([trades, pd.DataFrame({
          'stock_id': buy_sids,
          'entry_date': pd.NaT,
          'entry_sig_date': r.position.index[-1].tz_localize(None),
          'exit_date': pd.NaT,
          'exit_sig_date': pd.NaT,
        })], ignore_index=True)

        r.trades = final_trades
    else:
        r.actions = pd.Series(dtype=object)

    # add mae mfe to report
    if hasattr(r, 'trades') and hasattr(r, 'mae_mfe'):
        trades = r.trades
        mae_mfe = r.mae_mfe
        exit_mae_mfe = mae_mfe['exit'].copy()
        exit_mae_mfe = exit_mae_mfe.drop(columns=['return'])
        r.trades = pd.concat([trades, exit_mae_mfe], axis=1)
        r.trades.index.name = 'trade_index'

    # calculate r.current_trades
    # find trade without end or end today
    maxday = r.trades.entry_sig_date.max()
    r.current_trades = r.trades[(r.trades.entry_sig_date == maxday ) | (r.trades.exit_sig_date == maxday) | (r.trades.exit_sig_date.isnull())].set_index('stock_id')

    if len(operation_and_weight['weights']) != 0:
        r.weights = pd.Series(operation_and_weight['weights'])
        r.weights.index = r.position.columns[r.weights.index]
        r.current_trades['weight'] = (r.weights / r.weights.sum()).reindex(r.current_trades.index).fillna(0).clip(-position_limit, position_limit)
    else:
        r.current_trades['weight'] = 0

    if len(operation_and_weight['next_weights']) != 0:
        r.next_weights = pd.Series(operation_and_weight['next_weights'])
        r.next_weights.index = r.position.columns[r.next_weights.index]
        r.current_trades['next_weights'] = (r.next_weights / r.next_weights.sum()).reindex(r.current_trades.index).fillna(0).clip(-position_limit, position_limit)
    else:
        r.current_trades['next_weights'] = 0

    # fill stock id to trade history
    if len(trades) != 0:
        snames = market.get_asset_id_to_name()
        r.trades['stock_id'] = r.trades.stock_id.map(lambda sid: f"{sid + ' ' + snames[sid] if sid in snames else sid}")
        r.current_trades.index = r.current_trades.index.map(lambda sid: f"{sid + ' ' + snames[sid] if sid in snames else sid}")

    if hasattr(r, 'actions') and len(r.actions) != 0:
        snames = market.get_asset_id_to_name()
        r.actions.index = r.actions.index.map(lambda sid: f"{sid + ' ' + snames[sid] if sid in snames else sid}")

    if hasattr(r, 'weights') and len(r.weights) != 0:
        snames = market.get_asset_id_to_name()
        r.weights.index = r.weights.index.map(lambda sid: f"{sid + ' ' + snames[sid] if sid in snames else sid}")

    set_global('backtest_report', r)

    if not upload:
        return r

    r.upload(name)
    return r
