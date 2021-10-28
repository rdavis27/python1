# https://towardsdatascience.com/automated-interactive-reports-with-plotly-and-python-88dbe3aae5
import time
import requests
import pandas as pd

def load_data(symbol, API_KEY):
  return pd.read_csv(symbol+".csv",  header=0, index_col=0, parse_dates=True)
  if True:
    print("begin sleep")
    time.sleep(13)
    print("end sleep")
  url = 'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol='+symbol+'&market=USD&interval=1min&outputsize=compact&apikey='+API_KEY
  r = requests.get(url)
  data = r.json()
  df = pd.DataFrame.from_dict(data['Time Series Crypto (1min)']).T
  df = df.rename(columns={'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
  df.index = pd.to_datetime(df.index)
  df =df.astype(float)
  df['date'] = df.index.date.astype(str)
  df.to_csv(symbol+".csv") # WGP
  return df

def calculate_rsi(df, period=13):
  net_change = df['close'].diff()
  increase = net_change.clip(lower=0)
  decrease = -1*net_change.clip(upper=0)
  ema_up = increase.ewm(com=period, adjust=False).mean()
  ema_down = decrease.ewm(com=period, adjust=False).mean()
  RS = ema_up/ema_down
  df['RSI'] = 100 - (100/(1+RS)) 
  return df

def generate_table(df):
  df = calculate_rsi(df)
  df['date'] = df.index.date.astype(str)
  df_group = df.groupby(['date']).agg({
      'close': ['mean', 'std', lambda x: x.iloc[0], lambda x: x.iloc[-1]],
      'RSI': ['mean'],
  }).round(2)
  df_group.columns = [x[1] for x in df_group.columns]
  df_group = df_group.reset_index()
  df_group.columns = ['Date', 'Mean Price', 'STD Price', 'Start', 'End', 'RSI Mean']
  df_group['Net Change'] = (df_group['Start'] - df_group['End']).round(2)
  df_group = df_group[['Date', 'Mean Price', 'STD Price', 'RSI Mean', 'Start', 'End', 'Net Change']] # Re-ordering
  return df_group

import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

API_KEY = ""
COINS = ['BTC', 'ETH', 'MKR', 'BCH', 'DOGE']
rolling_period = 15
date_time = str(datetime.datetime.now())[0:16].replace(':','-').replace(' ','_') # File Explorer Safe Name
#with open('Crypto_Report_'+date_time+'.html', 'a') as f:
with open('Crypto_Report.html', 'a') as f:
  for coin in COINS:
    df = load_data(coin, API_KEY)
    df = calculate_rsi(df, rolling_period)
    df_group = generate_table(df)

    fig = go.Figure(make_subplots(
        rows=4, cols=1, shared_xaxes=True,
        vertical_spacing=0.05,
        specs=[[{}],[{}],[{}],[{"type": "table"}]]
    ))
    fig.add_trace(
        go.Candlestick(
            x=df.index, open=df['open'], high=df['high'],
            low=df['low'], close=df['close'], name= coin + ' Candlestick',
            increasing_line_color= 'rgb(27,158,119)', decreasing_line_color= 'rgb(204,80,62)'
        ), row=1, col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df['close'],
            name= coin+' Price', marker_color='#0099C6'
        ),row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=list(df.index)+list(df.index[::-1]),
            y=list(df['close'].transform(lambda x: x.rolling(rolling_period,1).mean()) + (2*df['close'].transform(lambda x: x.rolling(rolling_period,1).std())))
                +list(df['close'].transform(lambda x: x.rolling(rolling_period,1).mean()) - (2*df['close'].transform(lambda x: x.rolling(rolling_period,1).std()))[::-1]),
            fill='toself',
            fillcolor='rgba(0,176,246,0.2)', line_color='rgba(255,255,255,0)',
            name='Bollinger Bands', showlegend=False,
        ),row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df['close'].transform(lambda x: x.rolling(rolling_period,1).mean()),
            line = dict(dash='dot'), marker_color='rgba(0,176,246,0.2)',
            showlegend=False, name='Moving Average'
        ),row=2, col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df['RSI'],
            name='RSI', marker_color='#109618'
        ), row=3, col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, y=[70] * len(df.index),
            name='Overbought', marker_color='#109618',
            line = dict(dash='dot'), showlegend=False,
        ), row=3, col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, y=[30] * len(df.index),
            name='Oversold', marker_color='#109618',
            line = dict(dash='dot'),showlegend=False,
        ),row=3, col=1,
    )
    fig.add_trace(
        go.Table(
            header=dict(
                values=list(df_group.columns),
                font=dict(size=10), align="left"),
            cells=dict(
                values=[df_group[k].tolist() for k in df_group.columns[0:]],align = "left")
        ),row=4, col=1
    )
    fig.update_layout(
        title= coin + ' Report',
        yaxis_title='Price',
        template='plotly_dark',
        #WGP xaxis1_rangeslider_visible=False,
        height=800
    )
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
