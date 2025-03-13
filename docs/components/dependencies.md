# TA Dashboard Dependencies

This document outlines the key dependencies of the TA Dashboard application, their purposes, and their relationships.

## Library Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.42.0+ | Web UI framework and application rendering |
| google-generativeai | 0.8.4+ | Integration with Google Gemini AI models |
| yfinance | 0.2.40+ | Fetching stock data and financial news |
| pandas | 2.2.3+ | Data manipulation and analysis |
| plotly | 6.0.0+ | Interactive chart generation |
| ta | 0.11.0+ | Technical analysis indicators calculation |
| kaleido | 0.2.1+ | Static image rendering for AI analysis |

## External Service Dependencies

| Service | Purpose | Authentication |
|---------|---------|---------------|
| Google Gemini AI | AI-powered chart analysis and sentiment scoring | API Key required in `.env` file |
| Yahoo Finance | Stock price data and financial news | No authentication required |
| Google Forms/Sheets | Storage and retrieval of news data | Preconfigured form/sheet URLs |

## Component Dependencies

### Main Application (main.py)

Internal dependencies:
- `news_gathering.py`: For retrieving financial news
- `sentiment_analysis.py`: For analyzing news sentiment

External dependencies:
- streamlit: UI framework
- yfinance: Stock data provider
- pandas: Data manipulation
- plotly: Chart generation
- ta: Technical analysis calculations
- google-generativeai: AI chart analysis

### News Gathering (news_gathering.py)

External dependencies:
- yfinance: News data source
- pandas: Data manipulation
- requests: HTTP requests for form submission

### Sentiment Analysis (sentiment_analysis.py)

External dependencies:
- google-generativeai: AI sentiment analysis
- pandas: Data manipulation

## Environment Setup

The application requires Python 3.12 and can be set up using UV package manager:

```bash
uv add -r requirements.txt
uv sync
```

Required environment variables:
- `GOOGLE_API_KEY`: API key for Google Gemini AI integration

## Versioning and Compatibility

The application has been tested with the library versions specified above. Major version changes, particularly in the following libraries, may require code adaptations:

- streamlit: UI component rendering and layout
- google-generativeai: API changes and model capabilities
- yfinance: Data retrieval methods and response formats