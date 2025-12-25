import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=60_000, key="silver_refresh")
# -----------------------------
# Last 5 Years Historical Data
# -----------------------------
# -----------------------------
# REAL-TIME SILVER DATA
# -----------------------------
silver = yf.download(
    "SI=F",
    period="1d",
    interval="1m"
)

silver.dropna(inplace=True)

# Fix MultiIndex columns
if isinstance(silver.columns, pd.MultiIndex):
    silver.columns = silver.columns.get_level_values(0)



# Get last two close prices SAFELY
current_price = silver["Close"].iloc[-1].item()
previous_price = silver["Close"].iloc[-2].item()

price_change = current_price - previous_price

st.metric(
    label="🔴 Live Silver Price (USD/oz)",
    value=round(current_price, 2),
    delta=round(price_change, 2)
)

usd_inr = yf.download("USDINR=X", period="1d", interval="1m")
usd_inr.dropna(inplace=True)

silver_inr = current_price * usd_inr["Close"].iloc[-1] * (10 / 31.103)

st.metric(
    label="🇮🇳 Silver Price (₹ per 10g)",
    value=round(silver_inr, 2)
)
st.subheader("📈 Intraday Silver Price Movement")
st.line_chart(silver["Close"])
silver["MA20"] = silver["Close"].rolling(20).mean()
silver["MA50"] = silver["Close"].rolling(50).mean()

st.subheader("📊 Moving Average Analysis")
st.line_chart(silver[["Close", "MA20", "MA50"]])
silver["Returns"] = silver["Close"].pct_change()
volatility = silver["Returns"].std() * 100

st.metric(
    label="⚠️ Intraday Volatility (%)",
    value=round(volatility, 3)
)
if silver["MA20"].iloc[-1] > silver["MA50"].iloc[-1]:
    st.success("📢 Signal: BUY (Uptrend detected)")
else:
    st.error("📢 Signal: SELL (Downtrend detected)")

