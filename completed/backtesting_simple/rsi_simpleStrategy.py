from backtesting import Backtest, Strategy
import pandas as pd

from indicators import RSI


class RSISimpleStrategy(Strategy):
    rsi_period = 14
    oversold = 30
    overbought = 70
    stop_loss = 10
    take_profit = 20

    def init(self):
        prices = self.data.Close
        rsi_values = RSI(prices, self.rsi_period)
        self.rsi = self.I(lambda x: rsi_values, self.data.Close)

    def next(self):
        if not self.position:
            # Buy signal: RSI crosses below oversold
            if self.rsi[-1] < self.oversold:
                self.entry_price = self.data.Close[-1]
                self.stop_loss_price = self.entry_price - self.stop_loss
                self.target_price = self.entry_price + self.take_profit
                self.buy(
                    limit=self.entry_price,
                    sl=self.stop_loss_price,
                    tp=self.target_price,
                    size=50,
                )

            # Sell signal: RSI crosses above overbought
            elif self.rsi[-1] > self.overbought:
                self.entry_price = self.data.Close[-1]
                self.stop_loss_price = self.entry_price + self.stop_loss
                self.target_price = self.entry_price - self.take_profit
                self.sell(
                    limit=self.entry_price,
                    sl=self.stop_loss_price,
                    tp=self.target_price,
                    size=50,
                )

        current_time = self.data.index[-1].time()
        if current_time > pd.to_datetime("14:50").time() and self.position:
            self.position.close()
