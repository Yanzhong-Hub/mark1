import pandas as pd
import matplotlib.pyplot as plt
from sys import exit


class YZBackTest:

    def __init__(self, start_date, end_date):
        # set backtest starting date and end date
        self.start_date = pd.to_datetime(start_date).date()
        self.end_date = pd.to_datetime(end_date).date()
        # data, indicators, signal attribute
        self.all_data = pd.DataFrame()
        self.all_indicators = pd.DataFrame()
        self.signal = None
        # returns tables
        self.returns = None
        self.accumulate_returns = None
        # strategy returns tables
        self.strategy_returns = None
        self.accumulate_strategy_returns = None
        # portfolio result
        self.portfolio = pd.DataFrame()

    def add_data(self, ticker, data):
        if 'close' in data.columns:
            # washing data to concat
            # data.set_index('trade_date', inplace=True)
            data = data['close']
            data.index = pd.to_datetime(data.index).date
            data = data[self.start_date:self.end_date]
            data.name = ticker

            # concat to all_data
            self.all_data = pd.concat([self.all_data, data], axis=1, join='outer')
        else:
            print('close price not found')
            exit()

    def add_indicator(self, indicator):  # suppose to add multiple indicators

        # indicator should be processed data, such as SMA
        self.all_indicators = pd.concat([self.all_indicators, indicator], axis=1, join='outer')

    def add_signal(self, signal):  # suppose to generate multiple signal

        # the logic of long & short signal
        self.signal = signal

    def run(self):

        # data process
        def cal_return_table(data):
            return data / data.shift(1) - 1

        def cal_accumulate_return(data):
            returns_table = cal_return_table(data)
            output = (returns_table + 1).cumprod()
            output.iloc[0, :] = 1
            return output

        # referee
        self.returns = cal_return_table(self.all_data)
        self.accumulate_returns = cal_accumulate_return(self.all_data)

        # strategy
        self.strategy_returns = self.returns * self.signal
        self.accumulate_strategy_returns = cal_accumulate_return(self.strategy_returns)

        # Portfolio
        # average weighted portfolio
        self.portfolio['strategy'] = cal_accumulate_return(self.strategy_returns.mean(axis=1))
        self.portfolio['referee'] = cal_accumulate_return(self.returns.mead(axis=1))

    def plot(self):
        plt.figure(figsize=(15, 7))
        plt.plot(self.portfolio)
        plt.legend(self.portfolio.columns)
        plt.grid('both')

    def optimize(self):
        pass


if __name__ == '__main__':
    back_test = YZBackTest(start_date='20201231', end_date='20220311')
    # get data
    from Tushare.TusharePro import TushareData
    ts = TushareData()
    hs_300 = ts.daily_index(ts_code='000300.SH')
    zz_500 = ts.daily_index(ts_code='000905.SH')

    # add data
    back_test.add_data(ticker='000300.SH', data=hs_300)
    back_test.add_data(ticker='000905.SH', data=zz_500)

    # add indicator
    def indicators_sma_20(data):
        sma_20 = data.rolling(20).mean()
        sma_20.columns = [f'{_} sma_20' for _ in sma_20.columns]
        return sma_20

    def indicators_sma_50(data):
        sma_50 = data.rolling(50).mean()
        sma_50.columns = [f'{_} sma_50' for _ in sma_50.columns]
        return sma_50

    back_test.add_indicator(indicators_sma_20(back_test.all_data))
    back_test.add_indicator(indicators_sma_50(back_test.all_data))

    # output
    print(back_test.all_indicators.head())

