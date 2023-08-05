import pandas as pd
from finlab import data
from abc import ABC, abstractmethod

class MarketInfo():

    @staticmethod
    def get_benchmark():
        return pd.Series([])

    @staticmethod
    def get_asset_id_to_name():
        return {}

    @staticmethod
    def get_price(trade_at_price, adj=True):
        """"adj price"""
        return trade_at_price

    def calc_atr(self, atr_freq=10):
        adj_close = self.get_price('close', adj=True)
        adj_high = self.get_price('high', adj=True)
        adj_low = self.get_price('low', adj=True)
        tr_cond1 = (adj_high - adj_low).unstack()
        tr_cond2 = abs(adj_close.shift() - adj_high).unstack()
        tr_cond3 = abs(adj_close.shift() - adj_low).unstack()
        tr_df = pd.concat([tr_cond1, tr_cond2, tr_cond3],
                          axis=1).max(axis=1).unstack(level=0)
        atr_df = tr_df.rolling(atr_freq, min_periods=int(atr_freq / 2)).mean()
        volatility = atr_df / adj_close
        return volatility

class TWMarketInfo(MarketInfo):

    @staticmethod
    def get_benchmark():
        return data.get('benchmark_return:發行量加權股價報酬指數').squeeze()

    @staticmethod
    def get_asset_id_to_name():
        stock_names = data.cs.get_stock_names()

        if stock_names == {}:
            categories = data.get('security_categories')
            new_stock_names = dict(
                zip(categories['stock_id'], categories['name']))
            data.cs.cache_stock_names(new_stock_names)
            stock_names = data.cs.get_stock_names()

        return stock_names

    @staticmethod
    def get_price(trade_at_price, adj=True):
        if isinstance(trade_at_price, pd.Series):
            trade_at_price.name = position.name
            return trade_at_price.to_frame()

        if isinstance(trade_at_price, pd.DataFrame):
            return trade_at_price

        if isinstance(trade_at_price, str):
            if adj:
                table_name = 'etl:adj_'
                price_name = trade_at_price
            else:
                table_name = 'price:'
                price_name = {'open':'開盤價', 'close': '收盤價'}[trade_at_price]

            price = data.get(f'{table_name}{price_name}')
            return price

        raise Exception(f'**ERROR: trade_at_price is not allowed (accepted types: pd.DataFrame, pd.Series, str).')

class CryptoMarketInfo(MarketInfo):

    @staticmethod
    def get_benchmark():
        return data.get('crypto:close').pct_change().mean(axis=1).add(1).cumprod().resample('1d').last()

    @staticmethod
    def get_asset_id_to_name():
        return {}

    @staticmethod
    def get_price(trade_at_price, adj=True):
        table_name = 'crypto:'
        if isinstance(trade_at_price, str):
            price = data.get(f'{table_name}{trade_at_price}')
        elif isinstance(trade_at_price, pd.Series):
            trade_at_price.name = position.name
            price = trade_at_price.to_frame()
        elif isinstance(trade_at_price, pd.DataFrame):
            price = trade_at_price
        else:
            raise Exception(f'**ERROR: trade_at_price is not allowed (accepted types: pd.DataFrame, pd.Series, str).')
        return price

