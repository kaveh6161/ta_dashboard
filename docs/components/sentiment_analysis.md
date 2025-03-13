# Sentiment Analysis Component

The Sentiment Analysis component (`sentiment_analysis.py`) leverages Google's Gemini AI to analyze the sentiment of financial news articles and provide actionable insights.

## Responsibilities

- Processing news article content for analysis
- Analyzing sentiment using Google Gemini AI
- Scoring sentiment on a scale (positive, neutral, negative)
- Providing justification for sentiment assessment
- Generating time-series visualization of sentiment trends

## Key Functions

- `analyze_sentiment(news_data)`: Processes news articles and analyzes sentiment
- `format_prompt(article)`: Prepares news content for AI analysis
- `parse_sentiment_response(response)`: Extracts structured data from AI responses
- `visualize_sentiment_trends(sentiment_data)`: Generates time-series visualizations

## AI Integration

The component uses Google Gemini to perform sophisticated sentiment analysis:

1. **Prompt Construction**: News articles are formatted into prompts that instruct the AI to analyze sentiment
2. **Response Structure**: AI responses are structured to include:
   - Sentiment score (1-10, with 1 being very negative and 10 being very positive)
   - Confidence level (1-10)
   - Key factors influencing the sentiment assessment
   - Summary of potential market impact

3. **Error Recovery**: Implements robust error handling for AI response parsing with fallback mechanisms

## Data Flow

1. **Input**: Receives structured news data from the News Gathering component
2. **Processing**: Formats news for AI analysis
3. **Analysis**: Submits to Google Gemini for sentiment assessment
4. **Response Parsing**: Extracts structured data from AI responses
5. **Visualization**: Generates visualizations of sentiment trends
6. **Output**: Returns sentiment data to the main application

## Integration Points

- **Google Gemini API**: AI engine for sentiment analysis
- **News Gathering Component**: Source of news data
- **Main Application**: Returns sentiment analysis results for display

## Error Handling

The component implements comprehensive error handling for:
- API connectivity issues
- Malformed AI responses
- Rate limiting and quota management
- Timeout handling

## Configuration

The sentiment analysis component requires:
- Google Gemini API key (loaded from environment variables)
- Model configuration parameters (temperature, max tokens, etc.)

## Example Usage

```python
# Fetch news data
news_data = fetch_published_news()

# Analyze sentiment
sentiment_results = analyze_sentiment(news_data)

# Visualize sentiment trends
sentiment_chart = visualize_sentiment_trends(sentiment_results)
```

## Performance Considerations

- **Batching**: Processes news in batches to optimize API usage
- **Caching**: Implements caching to reduce redundant API calls
- **Asynchronous Processing**: Uses asynchronous processing for improved performance

## Privacy and Ethical Considerations

- No personal user data is sent to the AI model
- Only publicly available news content is analyzed
- AI analysis is clearly labeled as machine-generated
- Confidence levels are provided to indicate AI uncertainty