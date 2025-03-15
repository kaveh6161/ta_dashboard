# sentiment_analysis.py
import io
import os
import re
import requests
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai  # Google Generative AI client library
from dotenv import load_dotenv

def fetch_news_data(csv_url):
    """Downloads the CSV data from the published Google Sheet."""
    csv_text = requests.get(csv_url).text
    df = pd.read_csv(io.StringIO(csv_text))
    return df

# ------------------------------------------------------------------------------
# API & Model Configuration
# ------------------------------------------------------------------------------
load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY environment variable!")

genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = 'gemini-2.0-flash'
client = genai.GenerativeModel(MODEL_NAME)

# ------------------------------------------------------------------------------
# Sentiment Analysis
# ------------------------------------------------------------------------------
def analyze_sentiment_for_news(df, ticker=None, model="gemini-2.0-flash"):
    """
    Performs sentiment analysis on each news article using Google GenAI.
    Expects a column with headlines in df.iloc[2] (or adapt as needed).
    
    Parameters:
    - df: DataFrame containing news data
    - ticker: Optional ticker symbol to filter by. If None, analyzes all news.
    - model: GenAI model to use
    """
    # Filter by ticker if specified
    if ticker is not None:
        df = df[df['Ticker'] == ticker].copy()
        
    # If no data after filtering, return empty dataframe
    if df.empty:
        return df
    # Ensure columns exist
    if "Score" not in df.columns:
        df["Score"] = None
    if "Confidence Level" not in df.columns:
        df["Confidence Level"] = None

    for index, row in df.iterrows():
        # If there's no actual headlines, skip or default
        article_text = str(row.iloc[2])  # Adjust column index if your sheet differs
        if not article_text.strip() or article_text.strip().lower() == "nan":
            # Default to neutral if no headlines
            df.at[index, "Score"] = 3.0
            df.at[index, "Confidence Level"] = 50
            continue

        # Get the ticker for this specific news item
        news_ticker = row.get('Ticker', 'Unknown')
        
        # [CHANGED] We can't use "system" role. Merge it into the user role message:
        system_plus_prompt = (
            "You are a specialized financial news sentiment analysis tool. "
            "Output exactly one line in the format 'X, Y' where X is a float in [1..5] "
            "and Y is a float in [0..100], with no additional text.\n\n"
            f"Analyze the sentiment of these news article headlines about {news_ticker}:\n\n"
            f"{article_text}\n\n"
            "Provide a single sentiment score (1 to 5) and a single confidence percentage (0-100). "
            "Output exactly 'X, Y' with no extra text."
        )

        contents = [
            {"role": "user", "parts": [system_plus_prompt]}
        ]
        response_text = client.generate_content(contents=contents).text.strip()

        # Use regex to find the first "number, number" pattern
        match = re.search(r"(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)(?!.*\d)", response_text)
        if match:
            try:
                score = float(match.group(1))
                confidence = float(match.group(2))
            except ValueError:
                score, confidence = 3.0, 25.0  # fallback
        else:
            # fallback if we cannot parse
            score, confidence = 3.0, 25.0

        df.at[index, "Score"] = score
        df.at[index, "Confidence Level"] = confidence

    return df

# ------------------------------------------------------------------------------
# Plot the Results
# ------------------------------------------------------------------------------
def plot_sentiment(df, ticker=None):
    """
    Plots the sentiment scores over time if a 'Timestamp' column exists.
    
    Parameters:
    - df: DataFrame containing sentiment data
    - ticker: Optional ticker symbol to include in chart title
    
    Returns a matplotlib Figure or None.
    """
    if "Timestamp" not in df.columns:
        return None

    # Convert to datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df.dropna(subset=["Timestamp"])  # drop rows where timestamp is invalid
    df = df.sort_values("Timestamp")

    # Drop rows that have no valid numeric Score
    df = df.dropna(subset=["Score", "Confidence Level"])
    if df.empty:
        return None

    # Convert columns to float
    df["Score"] = df["Score"].astype(float)
    df["Confidence Level"] = df["Confidence Level"].astype(float)

    # If the entire column is the same or only one row, handle gracefully
    if df["Confidence Level"].min() == df["Confidence Level"].max():
        marker_sizes = [50]*len(df)
    else:
        min_size, max_size = 20, 200
        conf = df["Confidence Level"]
        marker_sizes = ((conf - conf.min()) / (conf.max() - conf.min())) * (max_size - min_size) + min_size

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df["Timestamp"], df["Score"], s=marker_sizes, color="orange", alpha=0.7)
    ax.plot(df["Timestamp"], df["Score"], color="blue", marker="o")
    ax.set_ylim(1, 5)
    
    # Set title based on whether a ticker is provided
    title = f"Sentiment Score Over Time - {ticker}" if ticker else "Sentiment Score Over Time"
    ax.set_title(title)
    
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Score")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def analyze_and_plot_by_ticker(df):
    """
    Analyzes sentiment and generates separate charts for each ticker in the dataset.
    
    Parameters:
    - df: DataFrame containing news data with a 'Ticker' column
    
    Returns:
    - Dictionary mapping each ticker to its matplotlib Figure
    """
    if "Ticker" not in df.columns:
        # If no Ticker column, return empty dictionary
        return {}
    
    # Get unique tickers
    tickers = df["Ticker"].unique()
    
    # Create a dictionary to store the figures for each ticker
    ticker_figures = {}
    
    # Analyze and plot each ticker separately
    for ticker in tickers:
        # Skip empty tickers
        if not ticker or str(ticker).lower() == "nan":
            continue
            
        # Filter and analyze data for this ticker
        ticker_analyzed = analyze_sentiment_for_news(df, ticker=ticker)
        
        # Generate plot for this ticker
        fig = plot_sentiment(ticker_analyzed, ticker)
        
        # Store the figure if it was created successfully
        if fig is not None:
            ticker_figures[ticker] = fig
    
    return ticker_figures

def save_ticker_charts(ticker_figures, output_dir="charts"):
    """
    Saves the ticker-specific charts to image files.
    
    Parameters:
    - ticker_figures: Dictionary mapping tickers to matplotlib Figures
    - output_dir: Directory to save the charts to (will be created if it doesn't exist)
    
    Returns:
    - List of saved file paths
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    saved_files = []
    
    # Save each figure to a file
    for ticker, fig in ticker_figures.items():
        if fig is None:
            continue
            
        # Create a safe filename
        safe_ticker = re.sub(r'[^\w\-\.]', '_', str(ticker))
        filename = os.path.join(output_dir, f"sentiment_{safe_ticker}.png")
        
        # Save the figure
        fig.savefig(filename, dpi=100, bbox_inches='tight')
        plt.close(fig)  # Close the figure to free memory
        
        saved_files.append(filename)
    
    return saved_files
