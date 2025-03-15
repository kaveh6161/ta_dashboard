# Main Application File for the AI-Powered Technical Stock Analysis Dashboard

# News Sentiment Analysis Modules
from news_gathering import main_news
from sentiment_analysis import fetch_news_data, analyze_sentiment_for_news, plot_sentiment

import streamlit as st  # Web app framework for interactive dashboards
import yfinance as yf  # Library for fetching stock data from Yahoo Finance
import pandas as pd  # Data manipulation and analysis library
import plotly.graph_objects as go  # Plotly module for creating interactive plots
from plotly.subplots import make_subplots  # Helper for creating subplot layouts in Plotly
import tempfile  # Module for creating temporary files
import os  # OS module for interacting with the operating system
import json  # Library for handling JSON data
from datetime import datetime, timedelta  # For working with dates and time intervals
import io
from io import BytesIO  # In-memory binary streams for image handling
import re  # Regular expressions for text processing
import base64  # For encoding binary data into a base64 string for downloads
import requests

import google.generativeai as genai  # Google Generative AI client library
from google.generativeai import types  # Importing specific types from the generative AI library

# ta library imports for technical analysis indicators
import ta
from ta.trend import SMAIndicator, EMAIndicator, MACD, ADXIndicator, CCIIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.momentum import RSIIndicator, StochasticOscillator, ROCIndicator, WilliamsRIndicator
from ta.volume import OnBalanceVolumeIndicator, VolumeWeightedAveragePrice, MFIIndicator
from dotenv import load_dotenv

# ------------------------------------------------------------------------------
# 2. API & Model Configuration
# ------------------------------------------------------------------------------
load_dotenv()  # This will load variables from a .env file in your project directory
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY environment variable!")

genai.configure(api_key=GOOGLE_API_KEY)  # Configure the Google Generative AI client with the API key

MODEL_NAME = 'gemini-2.0-flash'  # Specify the model name for AI analysis
gen_model = genai.GenerativeModel(MODEL_NAME)  # Instantiate the generative model for later use

# ------------------------------------------------------------------------------
# Streamlit Setup
# ------------------------------------------------------------------------------
st.set_page_config(layout="wide")  # Configure the Streamlit app layout to use the full width of the page
st.title("AI-Powered Technical Stock Analysis Dashboard")  # Set the main title of the dashboard
st.sidebar.header("Configuration")  # Add a header in the sidebar for configuration options

# Reset Button to clear session state if needed
if st.sidebar.button("Reset App"):
    st.session_state.clear()

# ------------------------------------------------------------------------------
# Clear Cached Data
# ------------------------------------------------------------------------------
if st.sidebar.button("Clear Cache"):
    st.cache_data.clear()
    st.success("Cache has been cleared!")

# ------------------------------------------------------------------------------
# Timeframe & Date Range
# ------------------------------------------------------------------------------
timeframe = st.sidebar.selectbox(
    "Timeframe:",
    ["Daily", "Weekly", "1 Hour", "30 Minutes", "15 Minutes", "5 Minutes", "1 Minute"],
    index=0
)
interval_map = {
    "Daily": "1d",
    "Weekly": "1wk",
    "1 Hour": "1h",
    "30 Minutes": "30m",
    "15 Minutes": "15m",
    "5 Minutes": "5m",
    "1 Minute": "1m"
}
yf_interval = interval_map[timeframe]

end_date_default = datetime.today()
if timeframe in ["1 Hour", "30 Minutes", "15 Minutes", "5 Minutes", "1 Minute"]:
    start_date_default = end_date_default - timedelta(days=7)
else:
    start_date_default = end_date_default - timedelta(days=365)

start_date = st.sidebar.date_input("Start Date", value=start_date_default)
end_date = st.sidebar.date_input("End Date", value=end_date_default)

# ------------------------------------------------------------------------------
# Ticker & Indicator Selection
# ------------------------------------------------------------------------------
tickers_input = st.sidebar.text_input("Enter Stock Tickers (comma-separated):", "AAPL,MSFT,GOOG")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

st.sidebar.subheader("Technical Indicators")
indicators = st.sidebar.multiselect(
    "Select Indicators:",
    [
        "SMA", "EMA", "Bollinger Bands", "VWAP", "Fibonacci Retracements",
        "RSI", "MACD", "OBV", "Stochastic Oscillator", "ATR", "ADX",
        "CCI", "Williams %R", "ROC", "MFI"
    ],
    default=["SMA"]
)

selected_indicators_code = indicators
overlay_indicators_set = {"SMA", "EMA", "Bollinger Bands", "VWAP", "Fibonacci Retracements"}

# ------------------------------------------------------------------------------
# Indicator Parameters
# ------------------------------------------------------------------------------
indicator_params = {}
if any(i in indicators for i in ["SMA", "EMA", "Bollinger Bands"]):
    indicator_params["length_20"] = st.sidebar.slider("Length (SMA/EMA/Bollinger)", 5, 100, 20)
if "RSI" in indicators:
    indicator_params["rsi_length"] = st.sidebar.slider("RSI Length", 5, 30, 14)
if "MACD" in indicators:
    indicator_params["macd_fast"] = st.sidebar.slider("MACD Fast Length", 5, 30, 12)
    indicator_params["macd_slow"] = st.sidebar.slider("MACD Slow Length", 10, 50, 26)
    indicator_params["macd_signal"] = st.sidebar.slider("MACD Signal Length", 3, 20, 9)
if "Stochastic Oscillator" in indicators:
    indicator_params["stoch_k"] = st.sidebar.slider("Stoch %K Length", 5, 30, 14)
    indicator_params["stoch_d"] = st.sidebar.slider("Stoch %D Smoothing", 2, 10, 3)
    indicator_params["stoch_smooth_k"] = st.sidebar.slider("Stoch %K Smoothing", 2, 10, 3)
if "ATR" in indicators:
    indicator_params["atr_length"] = st.sidebar.slider("ATR Length", 5, 30, 14)
if "ADX" in indicators:
    indicator_params["adx_length"] = st.sidebar.slider("ADX Length", 5, 30, 14)
if "CCI" in indicators:
    indicator_params["cci_length"] = st.sidebar.slider("CCI Length", 5, 30, 20)
if "Williams %R" in indicators:
    indicator_params["wr_length"] = st.sidebar.slider("Williams %R Length", 5, 30, 14)
if "ROC" in indicators:
    indicator_params["roc_length"] = st.sidebar.slider("ROC Length", 5, 30, 12)
if "MFI" in indicators:
    indicator_params["mfi_length"] = st.sidebar.slider("MFI Length", 5, 14, 14)

# ------------------------------------------------------------------------------
# The Analyze Function
# ------------------------------------------------------------------------------
def analyze_ticker(ticker, data, indicator_params, start_date, end_date):
    try:
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            if col in data.columns:
                data[col] = data[col].squeeze()
        
        oscillator_list = [ind for ind in indicators if ind not in overlay_indicators_set]
        total_rows = 2 + len(oscillator_list)

        row_specs = []
        row_heights = []

        row_specs.append([{"secondary_y": False}])
        row_heights.append(0.4)
        row_specs.append([{"secondary_y": False}])
        row_heights.append(0.2)

        if oscillator_list:
            each_height = 0.4 / len(oscillator_list)
            for _ in oscillator_list:
                row_specs.append([{"secondary_y": False}])
                row_heights.append(each_height)

        fig = make_subplots(
            rows=total_rows, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.04,
            row_heights=row_heights,
            specs=row_specs
        )

        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name="Candlestick"
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name="Volume",
                marker_color='rgba(166, 166, 166, 0.5)'
            ),
            row=2, col=1
        )

        for r in range(1, total_rows):
            if r != total_rows:
                fig.update_xaxes(showticklabels=False, row=r, col=1)

        fig.update_layout(xaxis_rangeslider_visible=False)

        def add_overlay(ind_name):
            length_20  = indicator_params.get("length_20", 20)
            if ind_name == "SMA":
                sma_val = ta.trend.SMAIndicator(close=data['Close'], window=length_20).sma_indicator()
                fig.add_trace(
                    go.Scatter(x=data.index, y=sma_val, mode='lines', name=f"SMA({length_20})"),
                    row=1, col=1
                )
            elif ind_name == "EMA":
                ema_val = ta.trend.EMAIndicator(close=data['Close'], window=length_20).ema_indicator()
                fig.add_trace(
                    go.Scatter(x=data.index, y=ema_val, mode='lines', name=f"EMA({length_20})"),
                    row=1, col=1
                )
            elif ind_name == "Bollinger Bands":
                bb = BollingerBands(close=data['Close'], window=length_20, window_dev=2)
                upper = bb.bollinger_hband()
                lower = bb.bollinger_lband()
                fig.add_trace(
                    go.Scatter(x=data.index, y=upper, mode='lines', name=f"BB Upper({length_20})", line=dict(dash='dash')),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(x=data.index, y=lower, mode='lines', name=f"BB Lower({length_20})", line=dict(dash='dash')),
                    row=1, col=1
                )
            elif ind_name == "VWAP":
                vwap_data = ta.volume.VolumeWeightedAveragePrice(
                    high=data['High'], low=data['Low'], close=data['Close'], volume=data['Volume']
                ).volume_weighted_average_price()
                fig.add_trace(
                    go.Scatter(x=data.index, y=vwap_data, mode='lines', name="VWAP"),
                    row=1, col=1
                )
            elif ind_name == "Fibonacci Retracements":
                high_pt = data['High'].max()
                low_pt  = data['Low'].min()
                diff = high_pt - low_pt
                fibs = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
                for f in fibs:
                    lvl_price = high_pt - diff*f
                    fig.add_trace(
                        go.Scatter(
                            x=[data.index[0], data.index[-1]],
                            y=[lvl_price, lvl_price],
                            mode='lines',
                            line=dict(dash='dot'),
                            name=f"Fib {f*100:.1f}%"
                        ),
                        row=1, col=1
                    )

        def add_oscillator(ind_name, row_idx):
            length_20  = indicator_params.get("length_20", 20)
            rsi_length = indicator_params.get("rsi_length", 14)
            macd_fast  = indicator_params.get("macd_fast", 12)
            macd_slow  = indicator_params.get("macd_slow", 26)
            macd_signal= indicator_params.get("macd_signal", 9)
            stoch_k    = indicator_params.get("stoch_k", 14)
            stoch_d    = indicator_params.get("stoch_d", 3)
            atr_length = indicator_params.get("atr_length", 14)
            adx_length = indicator_params.get("adx_length", 14)
            cci_length = indicator_params.get("cci_length", 20)
            wr_length  = indicator_params.get("wr_length", 14)
            roc_length = indicator_params.get("roc_length", 12)
            mfi_length = indicator_params.get("mfi_length", 14)

            if ind_name == "RSI":
                rsi_val = ta.momentum.RSIIndicator(close=data['Close'], window=rsi_length).rsi()
                fig.add_trace(
                    go.Scatter(x=data.index, y=rsi_val, mode='lines', name=f"RSI({rsi_length})"),
                    row=row_idx, col=1
                )
            elif ind_name == "MACD":
                macd_obj = ta.trend.MACD(
                    close=data['Close'],
                    window_slow=macd_slow,
                    window_fast=macd_fast,
                    window_sign=macd_signal
                )
                macd_line = macd_obj.macd()
                macd_sig  = macd_obj.macd_signal()
                macd_hist = macd_obj.macd_diff()
                fig.add_trace(
                    go.Scatter(x=data.index, y=macd_line, mode='lines', name="MACD Line"),
                    row=row_idx, col=1
                )
                fig.add_trace(
                    go.Scatter(x=data.index, y=macd_sig, mode='lines', line=dict(dash='dash'), name="MACD Signal"),
                    row=row_idx, col=1
                )
                fig.add_trace(
                    go.Scatter(x=data.index, y=macd_hist, mode='lines', line=dict(dash='dot'), name="MACD Hist"),
                    row=row_idx, col=1
                )
            elif ind_name == "OBV":
                obv_val = ta.volume.OnBalanceVolumeIndicator(close=data['Close'], volume=data['Volume']).on_balance_volume()
                fig.add_trace(
                    go.Scatter(x=data.index, y=obv_val, mode='lines', name="OBV"),
                    row=row_idx, col=1
                )
            elif ind_name == "Stochastic Oscillator":
                stoch = ta.momentum.StochasticOscillator(
                    high=data['High'], low=data['Low'], close=data['Close'],
                    window=stoch_k, smooth_window=stoch_d
                )
                k_val = stoch.stoch()
                d_val = stoch.stoch_signal()
                fig.add_trace(
                    go.Scatter(x=data.index, y=k_val, mode='lines', name=f"Stoch %K({stoch_k})"),
                    row=row_idx, col=1
                )
                fig.add_trace(
                    go.Scatter(x=data.index, y=d_val, mode='lines', line=dict(dash='dash'), name=f"Stoch %D({stoch_d})"),
                    row=row_idx, col=1
                )
            elif ind_name == "ATR":
                atr_val = ta.volatility.AverageTrueRange(
                    high=data['High'], low=data['Low'], close=data['Close'], window=atr_length
                ).average_true_range()
                fig.add_trace(
                    go.Scatter(x=data.index, y=atr_val, mode='lines', name=f"ATR({atr_length})"),
                    row=row_idx, col=1
                )
            elif ind_name == "ADX":
                adx_obj = ta.trend.ADXIndicator(
                    high=data['High'], low=data['Low'], close=data['Close'], window=adx_length
                )
                adx_val = adx_obj.adx()
                plus_di = adx_obj.adx_pos()
                minus_di= adx_obj.adx_neg()
                fig.add_trace(
                    go.Scatter(x=data.index, y=adx_val, mode='lines', name=f"ADX({adx_length})"),
                    row=row_idx, col=1
                )
                fig.add_trace(
                    go.Scatter(x=data.index, y=plus_di, mode='lines', line=dict(dash='dash'), name="+DI"),
                    row=row_idx, col=1
                )
                fig.add_trace(
                    go.Scatter(x=data.index, y=minus_di, mode='lines', line=dict(dash='dash'), name="-DI"),
                    row=row_idx, col=1
                )
            elif ind_name == "CCI":
                cci_val = ta.trend.CCIIndicator(
                    high=data['High'], low=data['Low'], close=data['Close'], window=cci_length
                ).cci()
                fig.add_trace(
                    go.Scatter(x=data.index, y=cci_val, mode='lines', name=f"CCI({cci_length})"),
                    row=row_idx, col=1
                )
            elif ind_name == "Williams %R":
                wr_val = ta.momentum.WilliamsRIndicator(
                    high=data['High'], low=data['Low'], close=data['Close'], lbp=wr_length
                ).williams_r()
                fig.add_trace(
                    go.Scatter(x=data.index, y=wr_val, mode='lines', name=f"Williams %R({wr_length})"),
                    row=row_idx, col=1
                )
            elif ind_name == "ROC":
                roc_val = ta.momentum.ROCIndicator(close=data['Close'], window=roc_length).roc()
                fig.add_trace(
                    go.Scatter(x=data.index, y=roc_val, mode='lines', name=f"ROC({roc_length})"),
                    row=row_idx, col=1
                )
            elif ind_name == "MFI":
                mfi_val = ta.volume.MFIIndicator(
                    high=data['High'], low=data['Low'], close=data['Close'],
                    volume=data['Volume'], window=mfi_length
                ).money_flow_index()
                fig.add_trace(
                    go.Scatter(x=data.index, y=mfi_val, mode='lines', name=f"MFI({mfi_length})"),
                    row=row_idx, col=1
                )

        for ov in [i for i in indicators if i in overlay_indicators_set]:
            add_overlay(ov)

        osc_row_start = 3
        for i, osc_ind in enumerate(oscillator_list):
            row_idx = osc_row_start + i
            add_oscillator(osc_ind, row_idx)
            fig.update_yaxes(title_text=osc_ind, row=row_idx, col=1)

        fig.update_layout(
            template="plotly",
            height=1600,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=80)
        )
        fig.update_yaxes(title_text="Price + Overlays", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)

        st.session_state[f"plotly_fig_{ticker}"] = fig
        return fig, None

    except Exception as e:
        st.error(f"General error in analyze_ticker: {e}")
        return (None, {
            "action": "Error",
            "confidence_score": 0,
            "price_target": "N/A",
            "justification": f"General Analysis Error: {e}"
        })

# ------------------------------------------------------------------------------
@st.cache_data(ttl=timedelta(minutes=30))
def fetch_stock_data(tickers, start_date, end_date, yf_interval):
    adjusted_end = end_date
    if start_date == end_date:
        adjusted_end = start_date + timedelta(days=1)
    stock_data = {}
    with st.spinner("Fetching Stock Data..."):
        for t in tickers:
            data = yf.download(t, start=start_date, end=adjusted_end, interval=yf_interval, multi_level_index=False)
            if not data.empty:
                for col in data.columns:
                    data[col] = data[col].squeeze()
                stock_data[t] = data
            else:
                st.warning(f"No data found for {t}.")
    return stock_data

# ------------------------------------------------------------------------------
# Technical Analysis
# ------------------------------------------------------------------------------
st.sidebar.header("Technical Analysis")

# ------------------------------------------------------------------------------
# Fetch Data
# ------------------------------------------------------------------------------
if st.sidebar.button("Fetch Data"):
    st.session_state["stock_data"] = fetch_stock_data(tickers, start_date, end_date, yf_interval)
    st.session_state.pop("analysis_results", None)

# ------------------------------------------------------------------------------
# Generate & Display Charts
# ------------------------------------------------------------------------------
if "stock_data" in st.session_state and st.session_state["stock_data"]:
    for tkr in st.session_state["stock_data"]:
        if f"plotly_fig_{tkr}" not in st.session_state:
            data_df = st.session_state["stock_data"][tkr]
            fig, _ = analyze_ticker(tkr, data_df, indicator_params, start_date, end_date)
            if fig:
                st.session_state[f"plotly_fig_{tkr}"] = fig

# ------------------------------------------------------------------------------
# Run AI Analysis
# ------------------------------------------------------------------------------
if st.sidebar.button("Run AI Technical Analysis"):
    if "stock_data" not in st.session_state or not st.session_state["stock_data"]:
        st.warning("Please fetch stock data first.")
    else:
        analysis_results = {}
        with st.spinner("Running AI Technical Analysis..."):
            for tkr in st.session_state["stock_data"]:
                data_df = st.session_state["stock_data"][tkr]
                fig_result = analyze_ticker(tkr, data_df, indicator_params, start_date, end_date)
                if fig_result:
                    fig, _ = fig_result

                    # Write the Plotly figure as a PNG image to a temporary file using kaleido
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                        fig.write_image(tmpfile.name, format="png", engine="kaleido")
                        tmp_path = tmpfile.name
                    with open(tmp_path, "rb") as f:
                        img_bytes = f.read()
                    os.remove(tmp_path)

                    # [CHANGED] Remove "system" role. Merge it into user role text.
                    analysis_prompt = (
                        "You are an 10x expert Financial Analyst who focuses on Technical Analysis at a top financial institution. "
                        "Return your result as valid JSON only. "
                        f"Analyze the stock chart for {tkr} ({timeframe} timeframe) based on its candlestick chart, volume, and "
                        f"the displayed technical indicators: {', '.join(selected_indicators_code)}. "
                        f"Taking into account the parameters chosen for each indicator, "
                        "Provide a detailed justification of your analysis, explaining patterns, signals, and trends, "
                        "explicitly mentioning the indicators and their parameter settings that lead to your conclusions. "
                        "Your interpretation should take into account the time frame examined, whether it's day trading, "
                        "longer-term investing, or anything in-between. "
                        "Based *only* on the chart, recommend an action ('Strong Buy', 'Buy', 'Weak Buy', 'Hold', 'Weak Sell', "
                        "'Sell', or 'Strong Sell') and provide a confidence score (1-10, 10 highest confidence). "
                        "Return a JSON object with 'action', 'confidence_score', 'price_target', and 'justification'."
                    )

                    image_part = {"data": img_bytes, "mime_type": "image/png"}

                    with st.spinner("AI Analyzing Chart..."):
                        contents = [
                            # Single user role with instructions
                            {"role": "user", "parts": [analysis_prompt]},
                            # The second user part with the image
                            {"role": "user", "parts": [image_part]}
                        ]
                        response = gen_model.generate_content(contents=contents)

                    try:
                        text = response.text
                        start_marker = "```json"
                        end_marker   = "```"
                        start_idx = text.find(start_marker)
                        end_idx   = text.find(end_marker, start_idx + len(end_marker))
                        if start_idx != -1 and end_idx != -1:
                            json_str = text[start_idx + len(start_marker):end_idx].strip()
                        else:
                            json_str = text.strip()

                        def clean_js(js_str):
                            return re.sub(r'[\x00-\x1F\x7F-\x9F]', '', js_str)

                        cleaned_js = clean_js(json_str)
                        parsed = json.loads(cleaned_js)
                        analysis_results[tkr] = parsed

                    except json.JSONDecodeError as e:
                        st.error(f"JSON Parsing Error: {e}")
                        analysis_results[tkr] = {
                            "action": "Error",
                            "confidence_score": 0,
                            "price_target": "N/A",
                            "justification": f"AI Analysis Error: JSON Parsing Error - {e}"
                        }
                else:
                    analysis_results[tkr] = {
                        "action":"Error","confidence_score":0,"price_target":"N/A",
                        "justification":"AI Analysis Failed. See error above."
                    }
        st.session_state["analysis_results"] = analysis_results
        st.success("AI Technical Analysis Completed!")

# ------------------------------------------------------------------------------
# News & Sentiment Analysis
# ------------------------------------------------------------------------------
st.sidebar.header("News & Sentiment Analysis")

# Add a dropdown to select which ticker to analyze for news
selected_news_ticker = st.sidebar.selectbox(
    "Select Ticker for News Analysis:",
    tickers if tickers else ["AAPL"],
    index=0
)

if st.sidebar.button("Fetch and Submit News"):
    forms_url = "https://docs.google.com/forms/d/e/1FAIpQLSd4thJmOPdR04W998INg6CeVDViR6HZu0KDveQQoL_aL5H3NQ/formResponse"
    news_data = main_news(selected_news_ticker, forms_url)
    if news_data:
        st.success(f"News data fetched and submitted for {selected_news_ticker}!")

if st.sidebar.button("Run AI Sentiment Analysis"):
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQrwIWMC_TxpeQENtV6SdHjBrQNXGkwO8ASDPJW-Lv-Vf__EilcN74_XzRe_lRX5OWR85pd8skiOkQA/pub?output=csv"
    csv_text = requests.get(csv_url).text
    print(csv_text)  # Make sure you see comma-separated text with a Timestamp column
    
    # df_news = fetch_news_data(csv_url)
    df_news = pd.read_csv(io.StringIO(csv_text))
    print(df_news.columns)  # Should see ["Timestamp", "Ticker", "News", ...]

    df_sentiment = analyze_sentiment_for_news(df_news, ticker=selected_news_ticker)
    st.write("Sentiment Analysis Results:")
    st.dataframe(df_sentiment)

    fig = plot_sentiment(df_sentiment)
    if fig:
        st.pyplot(fig)
    else:
        st.info("No valid sentiment data to plot, or 'Timestamp' column is missing/invalid.")

# ------------------------------------------------------------------------------
# Final Tabs
# ------------------------------------------------------------------------------
if "stock_data" in st.session_state and st.session_state["stock_data"]:
    tickers_list = list(st.session_state["stock_data"].keys())
    tab_names = ["Overall Summary"] + tickers_list
    tabs = st.tabs(tab_names)
    overall_results = []
    analysis_results = st.session_state.get("analysis_results", {})

    for i, tkr in enumerate(tickers_list):
        result = analysis_results.get(tkr, {})
        fig = st.session_state.get(f"plotly_fig_{tkr}")
        if fig is not None:
            overall_results.append({
                "Stock": tkr,
                "Recommendation": result.get("action", "N/A"),
                "Confidence": result.get("confidence_score", "N/A")
            })
            with tabs[i + 1]:
                st.subheader(f"Analysis for {tkr} ({timeframe})")
                st.plotly_chart(fig)

                if tkr in analysis_results:
                    st.write("**AI Recommendation:**", result.get("action", "N/A"))
                    st.write("**Confidence Score (1-10):**", result.get("confidence_score", "N/A"))
                    st.write("**Detailed Justification:**")
                    st.write(result.get("justification", "No justification provided."))
                else:
                    st.info("AI analysis not yet run.")

                buf = BytesIO()
                fig.write_image(buf, format="png", engine="kaleido")
                buf.seek(0)
                b64_data = base64.b64encode(buf.read()).decode("utf-8")
                download_filename = f"{tkr}_chart.png"
                download_link = f'<a href="data:image/png;base64,{b64_data}" download="{download_filename}">**Download Chart as PNG**</a>'
                st.markdown(download_link, unsafe_allow_html=True)

    with tabs[0]:
        st.subheader("Overall Structured Recommendations")
        if "analysis_results" not in st.session_state:
            st.info("Click 'Run AI Analysis' to see results")
        elif overall_results:
            df_summary = pd.DataFrame(overall_results)
            st.table(df_summary[['Stock', 'Recommendation', 'Confidence']])
        else:
            st.info("No stocks selected or analyzed yet.")
else:
    st.info("Please fetch stock data and then run AI Analysis to see results.")
