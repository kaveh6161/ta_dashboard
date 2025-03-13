# CLAUDE.md - Coding Guide for TA Dashboard

## Project Overview
A technical analysis dashboard for stocks with AI-powered insights. Combines traditional technical indicators with AI interpretation of charts and sentiment analysis of news. Features customizable indicators, interactive charts, multiple timeframes, and AI-powered trading recommendations.

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
- `docs/`: Extensive documentation on architecture, components, and domain knowledge
- No testing framework found

## Architecture and Components
- **Main Application (main.py)**: Core module for UI, data processing, and visualization
- **News Gathering (news_gathering.py)**: Fetches and stores financial news articles
- **Sentiment Analysis (sentiment_analysis.py)**: Uses Google Gemini AI for news analysis
- **External Integrations**:
  - Yahoo Finance API for stock data and news
  - Google Gemini AI for chart analysis and sentiment analysis
  - Google Forms/Sheets for news data storage

## Technical Analysis Features
- Trend indicators: SMA, EMA, Bollinger Bands
- Oscillators: RSI, MACD, Stochastic
- Volume indicators: OBV
- Multiple timeframes (1-minute to weekly)
- Candlestick pattern recognition

## AI Analysis Capabilities
- **Technical Chart Analysis**:
  - Market trend assessment
  - Technical pattern recognition
  - Trade recommendations with risk assessment
- **News Sentiment Analysis**:
  - Sentiment scoring with justification
  - Key factors identification
  - Market impact assessment
  - Sentiment trend visualization

## Code Style
- Follows PEP 8 conventions
- Functions have descriptive names and docstrings
- Heavy use of comments for code organization
- Sections clearly marked with decorative comment blocks
- Exception handling with descriptive error messages

## Key Dependencies
- streamlit (1.42.0+): Web UI framework
- google-generativeai (0.8.4+): Gemini AI integration
- yfinance (0.2.40+): Stock data provider
- pandas (2.2.3+): Data manipulation
- plotly (6.0.0+): Interactive charting
- ta (0.11.0+): Technical analysis indicators
- kaleido (0.2.1+): Static image rendering for AI analysis

## Application Workflow
1. User configures ticker symbols, timeframes, and indicators
2. Application fetches stock data from Yahoo Finance
3. Technical indicators are calculated and visualized
4. News articles are fetched and stored
5. AI performs sentiment analysis on news
6. AI analyzes charts and provides recommendations
7. Results are presented in the interactive UI

## Performance Considerations
- Caching for expensive operations
- Lazy loading of resources
- Batched processing for API interactions
- Resource management for reliability