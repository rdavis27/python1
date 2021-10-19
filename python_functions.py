import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def stockdata(symbol, start, end, graphtype, pricetype):
  dd = yf.download(symbol, start=start, end=end)
  #if isinstance(dd, pd.core.frame.DataFrame):
  if ',' in symbol:
    dd = dd[pricetype]
  if (graphtype == 'cumulative % change'):
    for i in range(0,len(dd.columns)):
      dd.iloc[:,i] = 100 * (dd.iloc[:,i] - dd.iloc[0,i]) / dd.iloc[0,i]
  return(dd)
  
def stockchart(dd, symbol, graphtype, pricetype):
  plt.style.use('ggplot')
  # if isinstance(dd, np.ndarray):
  #   dd = pd.Series(dd)
  if ',' not in symbol:
    dd = dd[pricetype]
  dd.plot(figsize=(15,7))
  if (graphtype == 'cumulative % change'):
    plt.ylabel('Cumulative % Change')
    plt.title(symbol+' '+pricetype+' (cumulative % change)')
  else:
    plt.ylabel(pricetype)
    plt.title(symbol+' '+pricetype)
  #plt.show()
  plt.savefig('myplot.png', bbox_inches='tight')
  plt.close()
