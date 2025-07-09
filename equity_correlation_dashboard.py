import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# App title
st.title("Equity Market Dashboard - Sector Correlation")

# Tickers and labels
tickers = {
    'communication_services': 'XLC',
    'consumer_discretionary': 'XLY',
    'consumer_staples': 'XLP',
    'energy': 'XLE',
    'financials': 'XLF',
    'health_care': 'XLV',
    'industrials': 'XLI',
    'information_technology': 'XLK',
    'materials': 'XLB',
    'real_estate': 'XLRE',
    'utilities': 'XLU',
    'spx': '^GSPC'
}

years = st.selectbox("Select number of years of data:", [1, 3, 5], index=1)

# Download data
end = pd.Timestamp.today()
start = end - pd.DateOffset(years=years)

data = yf.download(list(tickers.values()), start=start, end=end, group_by='ticker')

adj_close = pd.DataFrame()
for ticker in tickers.values():
    if ('Adj Close' in data[ticker].columns):
        adj_close[ticker] = data[ticker]['Adj Close']
        
returns = data.pct_change().dropna()
returns.columns = list(tickers.keys())

# Correlation matrix
corr = returns.corr()

# Plot
fig, ax = plt.subplots(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, ax=ax)
plt.title("Correlation Matrix of S&P Sectors", fontsize=14)
plt.tight_layout()

st.pyplot(fig)
