
"""
Created on Fri Apr 15 16:00:55 2022

@author: silvi
"""

import streamlit as st
import pandas as pd
import requests
import altair as alt

st.title("Bitcoin Prices")
page_names = ('cad', 'usd', 'inr')
vs_currency = st.radio('Currency', page_names)
days = st.slider('No. of days', 1, 90, 365)

r = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency={}&days={}&interval=daily'.format(
    vs_currency, days))
if r.status_code == 200:
  data = r.json() 
raw_data = data
df = pd.DataFrame(data=raw_data, columns=['prices'])

df2 = pd.DataFrame(df['prices'].values.tolist())
price = df2.iloc[:, 1]
dates = df2.iloc[:, 0]
     
print(dates)
dateDf = pd.DataFrame({'Old Date':dates})
dates = pd.to_datetime(dates, unit='ms')
   
print(dates)

newDf = pd.DataFrame({'Date':dates, 'Price':price})
newDf.set_index('Date')
print(newDf)

chart = alt.Chart(newDf).mark_line().encode(
  x=alt.X('Date'),
  y=alt.Y('Price')
)
st.altair_chart(chart, use_container_width=True)

st.write("Average price during this time was {}{}".format
         (sum(price)/len(price), vs_currency))   

