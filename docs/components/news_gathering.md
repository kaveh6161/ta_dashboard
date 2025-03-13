# News Gathering Component

The News Gathering component (`news_gathering.py`) is responsible for retrieving financial news articles related to stock tickers and storing them for later analysis.

## Responsibilities

- Fetching recent news articles for specified stock tickers
- Filtering and cleaning news data
- Storing news data in Google Forms/Sheets for persistence
- Providing a structured news dataset for sentiment analysis

## Key Functions

- `get_news(ticker)`: Retrieves news articles for a specific ticker
- `submit_to_form(ticker, article)`: Stores news articles in Google Forms
- `fetch_published_news()`: Retrieves stored news from Google Sheets

## Data Flow

1. **News Retrieval**: The component fetches news from Yahoo Finance using the yfinance API
2. **Data Processing**: News articles are cleaned and normalized
3. **Storage**: Processed news is submitted to a Google Form
4. **Retrieval**: The component can retrieve the stored news data from a published Google Sheet

## Data Structure

Each news article is represented with the following attributes:

- **Ticker**: Stock symbol the news relates to
- **Title**: Headline of the article
- **Publisher**: Source of the article
- **Link**: URL to the full article
- **Published Date**: When the article was published
- **Timestamp**: When the article was retrieved

## Integration Points

- **Yahoo Finance API**: Source of news data
- **Google Forms**: Storage endpoint for news data
- **Google Sheets**: Retrieval source for stored news data
- **Main Application**: Called by the main application to fetch news
- **Sentiment Analysis**: Provides data for the sentiment analysis component

## Error Handling

The component implements robust error handling for:
- API connectivity issues
- Data retrieval failures
- Storage submission errors

## Configuration

The news gathering component requires the following configuration:
- Form URL for news submission
- Published sheet URL for news retrieval

These are typically configured in the main application and passed to the news gathering component.

## Example Usage

```python
# Fetch news for a ticker
news_data = get_news("AAPL")

# Store news in Google Forms
for article in news_data:
    submit_to_form("AAPL", article)

# Retrieve stored news
all_news = fetch_published_news()
```

## Performance Considerations

- **Rate Limiting**: Respects Yahoo Finance API rate limits
- **Caching**: Implements caching to reduce redundant API calls
- **Batch Processing**: Processes news in batches to optimize performance