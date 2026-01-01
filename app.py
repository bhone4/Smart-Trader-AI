import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data_loader import get_market_data
from indicators import add_indicators
import config
import time

# 1. Website ခေါင်းစဉ်နှင့် ဒီဇိုင်း
st.set_page_config(page_title="Smart Trader AI", layout="wide")
st.title(f"🤖 Smart Trader AI - {config.SYMBOL}")
st.write("24/7 Intelligent Crypto Market Monitoring System")

# 2. Sidebar (ဘေးတိုက် Menu)
st.sidebar.header("Control Panel")
if st.sidebar.button("🔄 Refresh Data Now"):
    st.rerun()

# 3. Data ဆွဲယူခြင်း
with st.spinner('Analyzing Market Data...'):
    df = get_market_data()
    if df is not None:
        df = add_indicators(df)
        latest = df.iloc[-1]
        
        # 4. အဓိက အချက်အလက်များကို ပြသခြင်း (Metrics)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Price", f"${latest['close']:,.2f}")
            
        with col2:
            rsi_val = latest['rsi']
            rsi_color = "normal"
            if rsi_val < 30: rsi_color = "inverse" # Green
            elif rsi_val > 70: rsi_color = "off"   # Red
            st.metric("RSI (14)", f"{rsi_val:.2f}", delta=None)
            
        with col3:
            macd_val = latest['macd']
            sig_val = latest['macd_signal']
            trend = "UP 🟢" if macd_val > sig_val else "DOWN 🔴"
            st.metric("Market Trend", trend)

        with col4:
            # Recommendation Logic
            if latest['rsi'] < 35 and macd_val > sig_val:
                st.success("Target: BUY ✅")
            elif latest['rsi'] > 70:
                st.error("Target: SELL ❌")
            else:
                st.info("Target: HOLD ✋")

        # 5. ဈေးကွက် ဂရပ်ဖစ် (Chart) ဆွဲခြင်း
        st.subheader("Live Market Chart")
        
        fig = go.Figure()
        
        # Candlestick Chart
        fig.add_trace(go.Candlestick(x=df['timestamp'],
                        open=df['open'], high=df['high'],
                        low=df['low'], close=df['close'],
                        name='Price'))
        
        fig.update_layout(height=500, xaxis_rangeslider_visible=False, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        # 6. နောက်ဆုံး Data ဇယား
        with st.expander("View Raw Data Log"):
            st.dataframe(df.tail(10).sort_values(by='timestamp', ascending=False))
            
    else:
        st.error("Error fetching data from Binance. Please check connection.")

# Auto-refresh (Optional) - Dashboard ကို ဖွင့်ထားရင် ၁ မိနစ်တစ်ခါ Auto ပြောင်းနေအောင်
time.sleep(60)
st.rerun()
