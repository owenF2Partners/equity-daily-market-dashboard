import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ------------------------------
# Title & Config
# ------------------------------
st.title("Equity Market Dashboard - Sector Correlation")

st.write("Select number of years of data:")

years = st.selectbox(
    "Years of historical data:",
    options=[1, 5, 10],
    index=0
)

# ------------------------------
# Define tickers
# ------------------------------
tickers = {
    "communication_services": "XLC",
    "consumer_discretionary": "XLY",
    "consumer_staples": "XLP",
    "energy": "XLE",
    "financials": "XLF",
    "health_care": "XLV",
    "industrials": "XLI",
    "information_technology": "XLK",
    "materials": "XLB",
    "real_estate": "XLRE",
    "utilities": "XLU",
    "spx": "^GSPC"
}

start = pd.Timestamp.today() - pd.DateOffset(years=years)
end = pd.Timestamp.today()

# ------------------------------
# Download Data
# ------------------------------
st.write(f"Fetching data for the last {years} years...")
data = yf.download(list(tickers.values()), start=start, end=end, group_by='ticker', auto_adjust=False)

# Build adjusted close dataframe
adj_close = pd.DataFrame()
for ticker in tickers.values():
    try:
        adj_close[ticker] = data[ticker]['Adj Close']
    except Exception as e:
        st.warning(f"No data for ticker: {ticker}")

# Drop rows with any missing values
adj_close = adj_close.dropna()

if adj_close.empty:
    st.error("No data available for the selected period.")
    st.stop()

# ------------------------------
# Compute returns
# ------------------------------
returns = adj_close.pct_change().dropna()

# Rename columns to sector names
col_map = {v: k for k, v in tickers.items() if v in returns.columns}
returns.rename(columns=col_map, inplace=True)

# ------------------------------
# Compute Correlation
# ------------------------------
corr = returns.corr()

# ------------------------------
# Plot Correlation Heatmap
# ------------------------------
st.subheader("Correlation matrix of S&P sectors")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
plt.title("Correlation matrix of S&P sectors")
st.pyplot(fig)
