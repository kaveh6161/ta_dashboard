# CLAUDE.md - Coding Guide for TA Dashboard

## Project Overview
A technical analysis dashboard for stocks with AI-powered insights. Combines traditional technical indicators with AI interpretation of charts and sentiment analysis of news.

## Environment Setup
- Python 3.12 required
- Uses UV for dependency management
- Requires Google AI Studio API key in .env file

## Build/Run Commands
```bash
# Setup environment
uv add -r requirements.txt
uv sync

# Run the application
uv run --active streamlit run main.py

# Troubleshooting
streamlit cache clear  # Clear cache after data-related changes
```

## Project Structure
- `main.py`: Main Streamlit application
- `sentiment_analysis.py`: News sentiment analysis with Google Gemini
- `news_gathering.py`: News data collection from Yahoo Finance
- No testing framework found

## Code Style
- Follows PEP 8 conventions
- Functions have descriptive names and docstrings
- Heavy use of comments for code organization
- Sections clearly marked with decorative comment blocks
- Exception handling with descriptive error messages

## Key Dependencies
- streamlit: Web UI framework
- google-generativeai: Gemini AI integration
- yfinance: Stock data provider
- pandas: Data manipulation
- plotly: Interactive charting
- ta: Technical analysis indicators

## Workflow
1. User configures ticker symbols and indicators
2. Application fetches stock data
3. Technical indicators are calculated and displayed
4. Google Gemini analyzes charts and provides recommendations
5. News sentiment analysis available as supplementary information