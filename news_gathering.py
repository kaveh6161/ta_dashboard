# news_gathering.py
import datetime
import yfinance as yf
import requests

def get_recent_articles(ticker, days=3):
    """Fetches news articles for the ticker from the past 'days' (UTC)."""
    news = yf.Search(ticker).news
    now = datetime.datetime.now(datetime.timezone.utc)
    threshold = now - datetime.timedelta(days=days)
    articles = [
        art for art in news
        if art.get("providerPublishTime") and
           datetime.datetime.fromtimestamp(art["providerPublishTime"], datetime.timezone.utc) > threshold
    ]
    return articles

def build_headline_data(ticker, articles):
    """Builds a long string containing news headlines and details."""
    data = f"News headlines for {ticker}:\n\n"
    for art in articles:
        title = art.get("title", "No title available")
        link = art.get("link", "No link available")
        pub_time = datetime.datetime.fromtimestamp(
            art["providerPublishTime"], datetime.timezone.utc
        ).strftime("%Y-%m-%d %H:%M:%S")
        data += f"Title: {title}\nLink: {link}\nPublished At (UTC): {pub_time}\n\n"
    return data

def submit_to_google_form(ticker, headline_data, forms_url):
    """Submits the headline data to the Google Forms using Python requests."""
    payload = {
        "entry.110810626": ticker,
        "entry.1981258790": headline_data    
    }
    r = requests.post(forms_url, data=payload)
    return r.status_code

def main_news(ticker, forms_url):
    """Orchestrates the news fetching and submission process."""
    articles = get_recent_articles(ticker)
    if not articles:
        print("No articles found in the past 3 days (UTC).")
        return None
    headline_data = build_headline_data(ticker, articles)
    print("=== HEADLINE DATA ===")
    print(headline_data)
    print("=====================")
    status = submit_to_google_form(ticker, headline_data, forms_url)
    print("Data submitted. Status code:", status)
    return headline_data
