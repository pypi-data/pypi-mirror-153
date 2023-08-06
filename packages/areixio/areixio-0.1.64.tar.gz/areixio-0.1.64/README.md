# Areix IO (Alpha Test)

[Documentation](http://alphagen.areix-ai.com/doc)

## Installation
Create a virtual environment 
```
virtualenv venv --python=python3
```
Activate the virtual environment 
```python
# Macbook / Linus
source venv/bin/activate 

# Windows
venv/Scripts/activate
```
Deactivate
```
deactivate
```
Install Areix-IO package
```
pip install areixio
```


## Usage
Define your strategy class:
```python

from areixio import (
    create_report_folder, Side,
    Strategy, BinanceSpotDataFeed, BackTest, 
    BackTestBroker, CommissionScheme
)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd
import numpy as np

PRED_DAYS = 2 
PCT_CHANGE = 0.004
"""
Data pre processing step
"""
def bollinger_band(data, n_lookback, n_std):
    hlc3 = (data['high'] + data['low'] + data['close']) / 3
    mean, std = hlc3.rolling(n_lookback).mean(), hlc3.rolling(n_lookback).std()
    upper = mean + n_std*std
    lower = mean - n_std*std
    return upper, lower

def update_df(df):
    upper, lower = bollinger_band(df, 20, 2)

    df['ma10'] = df.close.rolling(10).mean()
    df['ma20'] = df.close.rolling(20).mean()
    df['ma50'] = df.close.rolling(50).mean()
    df['ma100'] = df.close.rolling(100).mean()

    df['x_ma10'] = (df.close - df.ma10) / df.close
    df['x_ma20'] = (df.close - df.ma20) / df.close
    df['x_ma50'] = (df.close - df.ma50) / df.close
    df['x_ma100'] = (df.close - df.ma100) / df.close

    df['x_delta_10'] = (df.ma10 - df.ma20) / df.close
    df['x_delta_20'] = (df.ma20 - df.ma50) / df.close
    df['x_delta_50'] = (df.ma50 - df.ma100) / df.close

    df['x_mom'] = df.close.pct_change(periods=2)
    df['x_bb_upper'] = (upper - df.close) / df.close
    df['x_bb_lower'] = (lower - df.close) / df.close
    df['x_bb_width'] = (upper - lower) / df.close

    # df = df.dropna().astype(float)
    return df

def get_X(data):
    return data.filter(like='x_').values

def get_y(data):
    y = data.close.pct_change(PRED_DAYS).shift(-PRED_DAYS)  # Returns after roughly two days
    y[y.between(-PCT_CHANGE, PCT_CHANGE)] = 0             # Devalue returns smaller than 0.4%
    y[y > 0] = 1
    y[y < 0] = -1
    return y

def get_clean_Xy(df):
    X = get_X(df)
    y = get_y(df).values
    isnan = np.isnan(y)
    X = X[~isnan]
    y = y[~isnan]
    return X, y

class MLStrategy(Strategy):
    num_pre_train = 300

    def initialize(self):
        """
        Model training step
        """
        self.info('initialize')
        self.code = list(self.ctx.feed.keys())[0]
        df = self.ctx.feed[self.code].data
        self.ctx.feed[self.code].data = update_df(df)

        self.y = get_y(df[self.num_pre_train-1:])
        self.y_true = self.y.values

        self.clf = KNeighborsClassifier(7)
        
        df = df.dropna()
        X, y = get_clean_Xy(df[:self.num_pre_train])
        self.clf.fit(X, y)

        self.y_pred = []
    
    def before_trade(self, order):
        return True

    def on_order_ok(self, order):
        self.my_quantity = self.ctx.get_quantity(order['code'])
        self.info(
            f"{order['side'].name} order [number {order['order_id']}] ({order['order_type'].name}) executed [quantity {order['quantity']}] {order['code']} [price ${order['price']:2f}] [Cost ${order['gross_amount']:2f}] [Commission: ${order['commission']}] [Available Cash: ${self.available_cash}] [Position: #{self.ctx.get_quantity(order['code'])}] [Gross P&L: ${order['pnl']}] [Net P&L: ${order['pnl_net']}]"
        )

        if not order['is_open']:
            self.info(f"Trade closed, pnl: {order['pnl']}========")

    def on_market_start(self):
        # self.info('on_market_start')
        pass

    def on_market_close(self):
        # self.info('on_market_close')
        pass

    def on_order_timeout(self, order):
        self.info(f'on_order_timeout. Order: {order}')
        pass

    def finish(self):
        self.info('finish')

    def on_bar(self, tick):
        """
        Model scoring and decisioning step
        """
        bar_data = self.ctx.bar_data[self.code]
        
        X = get_X(bar_data)
        if bar_data.x_ma100 != bar_data.x_ma100:
            return
        forecast = self.clf.predict([X])[0]
        self.y_pred.append(forecast)

        open, high, low, close = bar_data.open, bar_data.high, bar_data.low, bar_data.close

        upper, lower = close * (1 + np.r_[1, -1]*PCT_CHANGE)

        if forecast == 1 and not self.ctx.get_quantity(self.code):
            o1 = self.order_amount(code=self.code,amount=self.available_cash,side=Side.BUY)
            self.info(f"BUY order [number {o1['order_id']}] created, [quantity {o1['quantity']}] [price {o1['price']}] [balance: {self.available_cash}]")
            
            osl = self.sell(code=self.code,quantity=o1['quantity'], price=lower, stop_price=lower)
            self.info(f"STOPLOSS order [number {osl['order_id']}] created, [quantity {osl['quantity']}] [price {osl['price']}] [balance: {self.available_cash}]")
            
        elif forecast == -1 and self.ctx.get_quantity(self.code):
            o2 = self.close(code=self.code, price=upper)
            self.info(f"SELL order [number {o2['order_id']}] created, [quantity {o2['quantity']}] [price {o2['price']}] [balance: {self.available_cash}]")

```

Run your strategy:
```python

if __name__ == '__main__':

    base = create_report_folder()

    start_date = '2021-01-01'
    end_date = '2021-07-01'
    interval = '4h'

    code = 'XRP/USDT'
    benchmark_code = 'BTC/USDT'

    cs = CommissionScheme(
        commission_rate=0.001, 
        min_commission=None, 
        is_contract = False
    )
    broker = BackTestBroker(
        commission_scheme=cs,
        trade_at='close', 
        # trade_at='open', 
        cash=1000, 
        short_cash=False, 
        slippage=0.0)
    
    btc = BinanceSpotDataFeed(
        symbol=benchmark_code,
        start_date=start_date, 
        end_date=end_date,  
        interval=interval, 
        min_volume = 0.00001,
        order_ascending=True, 
        store_path=base
    )
    datefeed = BinanceSpotDataFeed(
        symbol=code,
        start_date=start_date, 
        end_date=end_date,  
        interval=interval, 
        min_volume = 0.0001,
        order_ascending=True, 
        store_path=base
    )

    mytest = BackTest(
        [ datefeed ], 
        MLStrategy, 
        benchmark=btc, 
        store_path=base,
        broker=broker
    )

    mytest.start()


```

Retrieve statistic results:
```python
    prefix = ''
    stats = mytest.ctx.statistic.stats(pprint=True, annualization=252, risk_free=0.0442)
    stats['model_name'] = 'Simple KNN Signal Generation Strategy'
    stats['algorithm'] = ['KNN', 'Simple Moving Average', 'Bollinger Band']
    print(stats)
    mytest.contest_output(is_plot=True)
```
Result:
```
start                                                2021-01-01 00:00:00+08:00
end                                                  2021-07-01 00:00:00+08:00
duration                                                     181 days 00:00:00
trading_pairs                                                        [XRPUSDT]
benchmark                                                              BTCUSDT
beginning_balance                                                         1000
ending_balance                                                     6374.787763
total_net_profit                                                   5374.787763
gross_profit                                                       9919.319576
gross_loss                                                        -4544.531813
profit_factor                                                         2.182693
return_on_initial_capital                                             5.374788
annualized_return                                                     0.536384
total_return                                                          5.374788
max_return                                                            5.401244
min_return                                                           -0.004806
number_trades                                                              630
number_winning_trades                                                      317
number_losing_trades                                                       220
avg_daily_trades                                                      6.899160
avg_weekly_trades                                                    32.840000
avg_monthly_trades                                                  136.833333
win_ratio                                                             0.503175
loss_ratio                                                            0.349206
win_days                                                                    64
loss_days                                                                   18
max_win_in_day                                                      701.189561
max_loss_in_day                                                     -51.928662
max_consecutive_win_days                                                    22
max_consecutive_loss_days                                                    2
avg_profit_per_trade                                                 13.209755
trading_period                                         0 years 6 months 0 days
avg_daily_pnl($)                                                      4.949160
avg_daily_pnl                                                         0.001784
avg_weekly_pnl($)                                                   206.722606
avg_weekly_pnl                                                        0.080719
avg_monthly_pnl($)                                                  868.835518
avg_monthly_pnl                                                       0.398852
avg_quarterly_pnl($)                                               1532.511026
avg_quarterly_pnl                                                     0.463027
avg_annualy_pnl($)                                                         NaN
avg_annualy_pnl                                                            NaN
sharpe_ratio                                                          2.022460
sortino_ratio                                                         6.971285
annualized_volatility                                                 0.200512
omega_ratio                                                           0.011848
downside_risk                                                         0.064485
information_ratio                                                     0.058498
beta                                                                  0.105311
alpha                                                                -0.999939
calmar_ratio                                                          5.527284
tail_ratio                                                            9.548038
max_drawdown                                                          0.097043
max_drawdown_period          (2021-06-21 04:00:00+08:00, 2021-06-28 08:00:0...
max_drawdown_duration                                          7 days 04:00:00
sqn                                                                   5.283288
model_name                               Simple KNN Signal Generation Strategy
algorithm                         [KNN, Simple Moving Average, Bollinger Band]

```