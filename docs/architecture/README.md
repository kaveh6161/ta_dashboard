# TA Dashboard Architecture

## Overview

The TA Dashboard is a Streamlit-based web application that combines traditional technical analysis with AI-powered insights for stock market analysis. It integrates multiple components to fetch data, perform calculations, generate visualizations, and leverage AI for interpretations.

## System Architecture

```
┌─────────────────────────────────────┐
│              User Interface         │
│           (Streamlit Frontend)      │
└───────────────────┬─────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│          Main Application           │
│              (main.py)              │
└───┬───────────────┬─────────────┬───┘
    │               │             │
    ▼               ▼             ▼
┌────────┐    ┌──────────┐   ┌──────────┐
│ Yahoo  │    │  News    │   │Sentiment │
│ Finance│    │Gathering │   │Analysis  │
│  API   │    │  Module  │   │  Module  │
└────┬───┘    └────┬─────┘   └────┬─────┘
     │             │              │
     ▼             ▼              ▼
┌────────┐    ┌──────────┐   ┌──────────┐
│Technical│    │ Google   │   │  Google  │
│Analysis │    │  Forms/  │   │  Gemini  │
│ Engine  │    │  Sheets  │   │    API   │
└────────┘    └──────────┘   └──────────┘
```

## Key Components

1. **Main Application (main.py)**:
   - Core orchestration module
   - Handles UI rendering, configuration, and state management
   - Coordinates data flow between components

2. **News Gathering Module (news_gathering.py)**:
   - Retrieves news articles related to stock tickers
   - Stores data in Google Forms/Sheets for persistence

3. **Sentiment Analysis Module (sentiment_analysis.py)**:
   - Analyzes news sentiment using Google Gemini AI
   - Provides scoring and interpretation of news impact

## Data Flow

1. User selects ticker symbols, timeframes, and indicators in the UI
2. Main application fetches stock data from Yahoo Finance
3. Technical indicators are calculated and displayed in interactive charts
4. News articles are fetched and stored via Google Forms/Sheets
5. Sentiment analysis is performed on news articles
6. Google Gemini analyzes charts and provides recommendations
7. All insights are displayed in the UI for user interpretation

## Integration Points

1. **External APIs**:
   - Yahoo Finance: Stock data and news
   - Google Gemini: AI analysis engine

2. **Data Storage**:
   - Streamlit session state: In-memory storage during session
   - Google Forms/Sheets: External persistence for news data

## Design Principles

1. **Modularity**: Clear separation of concerns between components
2. **Caching**: Optimization of performance-heavy operations
3. **Graceful Degradation**: Fallback mechanisms when services are unavailable
4. **Configurability**: User-defined settings for analysis parameters

## Dependencies

See [Component Dependencies](../components/dependencies.md) for a detailed breakdown of library dependencies and their purposes.