from pycoingecko import CoinGeckoAPI
import time
import pandas as pd
import plotly.graph_objects as go

# Initialize the CoinGeckoAPI
cg = CoinGeckoAPI()

# Convert the dates to Unix timestamps
from_timestamp = int(time.mktime(time.strptime('2024-04-17', '%Y-%m-%d')))
to_timestamp = int(time.mktime(time.strptime('2024-05-16', '%Y-%m-%d')))

# Fetch the Bitcoin market chart range data
bitcoin_data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='usd', from_timestamp=from_timestamp, to_timestamp=to_timestamp)

# Extract the data
timestamps = [item[0] // 1000 for item in bitcoin_data['prices']]
prices = [item[1] for item in bitcoin_data['prices']]
market_caps = [item[1] for item in bitcoin_data['market_caps']]
total_volumes = [item[1] for item in bitcoin_data['total_volumes']]

# Create a DataFrame
df = pd.DataFrame({
    'timestamp': timestamps,
    'price': prices,
    'market_cap': market_caps,
    'total_volume': total_volumes
})

# Convert timestamps to datetime
df['date'] = pd.to_datetime(df['timestamp'], unit='s')

# Resample the data to get OHLC (Open, High, Low, Close)
df.set_index('date', inplace=True)
df_ohlc = df['price'].resample('D').ohlc()

# Create the candlestick chart
fig = go.Figure(data=[go.Candlestick(x=df_ohlc.index,
                                     open=df_ohlc['open'],
                                     high=df_ohlc['high'],
                                     low=df_ohlc['low'],
                                     close=df_ohlc['close'])])

# Update layout
fig.update_layout(title='Bitcoin Candlestick Chart (USD)',
                  xaxis_title='Date',
                  yaxis_title='Price (USD)')

# Show the plot
fig.show()
