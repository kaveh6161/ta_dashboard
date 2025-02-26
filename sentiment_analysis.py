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
def analyze_sentiment_for_news(df, ticker, model="gemini-2.0-flash"):
    """
    Performs sentiment analysis on each news article using Google GenAI.
    Expects a column with headlines in df.iloc[2] (or adapt as needed).
    """
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

        # [CHANGED] We can't use "system" role. Merge it into the user role message:
        system_plus_prompt = (
            "You are a specialized financial news sentiment analysis tool. "
            "Output exactly one line in the format 'X, Y' where X is a float in [1..5] "
            "and Y is a float in [0..100], with no additional text.\n\n"
            f"Analyze the sentiment of these news article headlines about {ticker}:\n\n"
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
def plot_sentiment(df):
    """
    Plots the sentiment scores over time if a 'Timestamp' column exists.
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
    ax.set_title("Sentiment Score Over Time")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Score")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
