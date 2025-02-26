import yfinance as yf
import requests

# Create a custom session with a common browser User-Agent
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
})
# Set this session as the default for yfinance
yf.utils._DEFAULT_SESSION = session

data = yf.download("AAPL", period="1d")
print(data)
