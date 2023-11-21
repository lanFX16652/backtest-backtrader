import backtrader as bt  # thư viện các indicator
import yfinance as yf
import numpy as np

# Chiến lược giao dịch
# ĐIỀU KIỆN VÀO LỆNH: MA10 cắt lên MA50 --> vào lệnh mua
# STOPLOSS: không có
# TAKEPROFIT: MA10 cắt dưới MA50


class MovingAverageStrategy(bt.Strategy):
    def __init__(self):
        self.ma10 = bt.indicators.SimpleMovingAverage(self.data, period=10)  # MA10
        self.ma50 = bt.indicators.SimpleMovingAverage(self.data, period=50)  # MA50

    def next(self):
        if self.ma10[0] > self.ma50[0] and self.ma10[-1] < self.ma50[-1]:
            # MA10 just crossed above MA50
            self.buy()

        elif self.ma10[0] < self.ma50[0] and self.ma10[-1] > self.ma50[-1]:
            # MA10 just crossed below MA50
            self.sell()


# Select symbol and time range for backtesting
symbol = "BTC-USD"
start_date = "2016-01-01"
end_date = "2023-01-01"

# Download historical price data from Yahoo Finance
data = yf.download(symbol, start=start_date, end=end_date)

# Convert the DataFrame to a CSV file
data.to_csv("data.csv")

# Create a `backtrader` data feed
data_feed = bt.feeds.YahooFinanceData(dataname="data.csv")

# Initialize `backtrader` cerebro
cerebro = bt.Cerebro()

# Add the data feed to cerebro
cerebro.adddata(data_feed)

# Add the strategy to cerebro
cerebro.addstrategy(MovingAverageStrategy)

# Set the initial capital
cerebro.broker.setcash(10000.0)

# Set the commission
cerebro.broker.setcommission(commission=0.001)

# Run the backtest
cerebro.run()

# Get the final portfolio value
port_value = cerebro.broker.getvalue()

print(f"Final portfolio value: ${port_value:.2f}")

# Vẽ biểu đồ
cerebro.plot()
