import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Global Top10 Market Cap Dashboard",
    layout="wide"
)

st.title("📈 Global Top 10 Market Cap Stocks (1Y Performance)")

TICKERS = {
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN",
    "Broadcom": "AVGO",
    "TSMC": "TSM",
    "Saudi Aramco": "2222.SR",
    "Meta": "META",
    "Tesla": "TSLA"
}

# 사이드바
selected = st.sidebar.multiselect(
    "Select companies",
    list(TICKERS.keys()),
    default=list(TICKERS.keys())
)

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

@st.cache_data
def load_data(tickers):
    all_data = pd.DataFrame()

    for name, ticker in tickers.items():
        df = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            auto_adjust=True
        )

        if not df.empty:
            normalized = (df["Close"] / df["Close"].iloc[0]) * 100
            all_data[name] = normalized

    return all_data


filtered_tickers = {k: TICKERS[k] for k in selected}
stock_data = load_data(filtered_tickers)

# Plotly line chart
fig = go.Figure()

for company in stock_data.columns:
    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=stock_data[company],
            mode="lines",
            name=company
        )
    )

fig.update_layout(
    title="Normalized Stock Performance (Base = 100)",
    xaxis_title="Date",
    yaxis_title="Relative Performance",
    hovermode="x unified",
    template="plotly_dark",
    height=700
)

st.plotly_chart(fig, use_container_width=True)

# 수익률 테이블
returns = ((stock_data.iloc[-1] - 100)).sort_values(ascending=False)

st.subheader("📊 1Y Return Ranking")
st.dataframe(
    pd.DataFrame({
        "Company": returns.index,
        "Return (%)": returns.values.round(2)
    }),
    use_container_width=True
)
