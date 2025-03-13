# TA Dashboard Components

This section provides detailed documentation for each component of the TA Dashboard system.

## Core Components

1. [Main Application](./main.md)
2. [News Gathering](./news_gathering.md)
3. [Sentiment Analysis](./sentiment_analysis.md)

## Component Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                            main.py                              │
├─────────────────┬─────────────────────────┬─────────────────────┤
│                 │                         │                     │
│  Data Fetching  │    Chart Generation     │   AI Integration    │
│                 │                         │                     │
└────────┬────────┴──────────┬──────────────┴─────────┬───────────┘
         │                   │                        │
         ▼                   ▼                        ▼
┌──────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│ Stock Data   │    │Technical Analysis│    │   Chart Analysis    │
│ (yfinance)   │    │    (ta lib)      │    │   (Google Gemini)   │
└──────────────┘    └──────────────────┘    └─────────────────────┘
         │                                              │
         │                                              │
         ▼                                              ▼
┌──────────────┐                              ┌─────────────────────┐
│news_gathering│───────────────────────────▶ │  sentiment_analysis  │
│    .py       │                            │        .py            │
└──────────────┘                            └─────────────────────────┘
```

## Dependencies

The TA Dashboard relies on several key libraries and external services. See the [dependencies](./dependencies.md) page for details.

## Configuration Options

Each component exposes configuration options that can be set through the Streamlit UI. See the individual component pages for configuration details.

## Extension Points

The modular design allows for easy extension in the following areas:

1. **Additional Technical Indicators**: The system can be extended with new indicators in the main application.
2. **Alternative Data Sources**: The data fetching module can be modified to support different data providers.
3. **Enhanced AI Analysis**: The sentiment analysis module can be expanded to support different AI models or analysis techniques.

For implementation details, see the individual component documentation.