# sentiment_analysis.py
import io
import os
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
load_dotenv()  # This will load variables from a .env file in your project directory
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY environment variable!")

genai.configure(api_key=GOOGLE_API_KEY)  # Configure the Google Generative AI client with the API key

MODEL_NAME = 'gemini-2.0-flash'  # Specify the model name for AI analysis
client = genai.GenerativeModel(MODEL_NAME)  # Instantiate the generative model for later use

# ------------------------------------------------------------------------------
# Sentiment Analysis
# ------------------------------------------------------------------------------
def analyze_sentiment_for_news(df, ticker, model="gemini-2.0-flash"):
    """Performs sentiment analysis on each news article using Google GenAI."""
    # # Initialize the GenAI client with your API key (set it in your environment or configure here)
    # client = genai.Client(api_key="Google AI Studio API Key Goes Here")
    
    # Add empty columns for sentiment results
    df["Score"] = None
    df["Confidence Level"] = None

    for index, row in df.iterrows():
        # Adjust column index if needed; here we assume the article text is in column index 2
        article_text = row.iloc[2]
        prompt = (
            f"Analyze the sentiment of these news article headlines about {ticker}:\n{article_text}\n"
            "Provide a single sentiment score (1 [most negative] to 5 [most positive]) and a single confidence percentage based on all relevant headlines.\n"
            "Only consider headlines that could directly or indirectly impact {ticker}'s stock price.\n"
            "The single sentiment score can be a float.\n"
            "Respond exactly in CSV format as: Score, Confidence Level\n"
            "Example: value, value\n"
            "Do not produce any other characters, text, etc."
        )
        
        response_text = client.generate_content(contents=[{"role": "user", "parts": [prompt]}]).text.strip()
        try:
            score_str, conf_str = response_text.split(",")
            score = float(score_str.strip())
            confidence = float(conf_str.strip())
        except Exception:
            print(f"Error parsing response for row {index}: {response_text}")
            score, confidence = None, None

        df.at[index, "Score"] = score
        df.at[index, "Confidence Level"] = confidence
    return df

# ------------------------------------------------------------------------------
# Plot the Results
# ------------------------------------------------------------------------------
def plot_sentiment(df):
    """Plots the sentiment scores over time if a 'Timestamp' column exists and returns the figure."""
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df = df.sort_values("Timestamp")
        conf = df["Confidence Level"].astype(float)
        min_size, max_size = 20, 200
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
    return None

