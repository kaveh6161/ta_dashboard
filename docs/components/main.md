# Main Application Component

The main application (`main.py`) is the core component of the TA Dashboard. It orchestrates all other components and handles the user interface, data processing, and visualization.

## Responsibilities

- User interface management via Streamlit
- Stock data retrieval from Yahoo Finance
- Technical indicator calculation
- Chart generation
- AI-powered chart analysis
- Integration with news gathering and sentiment analysis

## Key Functions

### Data Management

- `get_ticker_data(ticker, interval, period)`: Fetches historical stock data
- `calculate_technical_indicators(df, indicators)`: Applies selected technical indicators to the data
- `prepare_data_for_charting(df, ticker)`: Formats data for visualization

### Chart Generation

- `analyze_ticker(ticker, interval, period, indicators)`: Creates multi-panel technical charts
- `generate_chart_image(figure)`: Renders charts to images for AI analysis

### AI Integration

- `analyze_chart_with_gemini(chart_image)`: Sends chart images to Google Gemini for analysis
- `parse_ai_analysis(response)`: Extracts structured information from AI responses

## Configuration Options

The main application supports the following configuration options through the Streamlit UI:

- **Ticker Symbols**: Stock symbols to analyze (e.g., AAPL, MSFT)
- **Timeframes**: Time intervals for analysis (1m, 5m, 15m, 30m, 1h, 1d, 1wk)
- **Period**: Historical data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
- **Technical Indicators**:
  - Overlay Indicators (SMA, EMA, Bollinger Bands, etc.)
  - Oscillator Indicators (RSI, MACD, Stochastic, etc.)

## UI Structure

The main application organizes the UI into the following sections:

1. **Configuration Panel**: Sidebar for setting analysis parameters
2. **Chart View**: Main panel for technical analysis charts
3. **AI Analysis**: Section displaying AI interpretations and recommendations
4. **News Analysis**: Section for news sentiment analysis

## State Management

Streamlit's session state is used to manage application state, including:

- User configuration preferences
- Cached data to improve performance
- Analysis results
- Error states

## Integration Points

- **News Gathering**: Calls the news gathering module to retrieve and store news
- **Sentiment Analysis**: Leverages the sentiment analysis module for news interpretation
- **External APIs**: Interacts with Yahoo Finance and Google Gemini

## Error Handling

The main application implements comprehensive error handling for:

- Data retrieval failures
- Technical indicator calculation errors
- Chart generation issues
- AI analysis failures

When errors occur, graceful fallback mechanisms ensure the application remains functional.

## Performance Considerations

- **Caching**: Uses `@st.cache_data` for expensive operations
- **Lazy Loading**: Defers heavy operations until needed
- **Resource Management**: Proper cleanup of resources to prevent memory leaks

## Example Usage

```python
# Configuration
ticker = "AAPL"
interval = "1d"
period = "1y"
indicators = {
    "overlay": ["sma", "bollinger"],
    "oscillators": ["rsi", "macd"]
}

# Analysis
chart = analyze_ticker(ticker, interval, period, indicators)
chart_image = generate_chart_image(chart)
analysis = analyze_chart_with_gemini(chart_image)

# Display results
st.plotly_chart(chart)
st.write(analysis)
```