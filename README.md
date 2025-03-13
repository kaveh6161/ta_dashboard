# Technical Analysis Dashboard with AI Insights

A technical analysis dashboard for stocks with AI-powered insights. Combines traditional technical indicators with AI interpretation of charts and sentiment analysis of news.

## Documentation

Comprehensive documentation is available in the [docs](./docs) directory:

- [Architecture Overview](./docs/architecture/README.md)
- [Component Documentation](./docs/components/README.md)
- [Domain Knowledge](./docs/domain/README.md)
- [Usage Examples](./docs/examples/README.md)
- [System Diagrams](./docs/diagrams/README.md)

## Features

- Interactive technical analysis charts with customizable indicators
- AI-powered chart interpretation and trading recommendations
- News sentiment analysis for stocks
- Multiple timeframes and historical periods
- Customizable technical indicators

## Getting Started

### Prerequisites

- Python 3.12
- Google AI Studio API key

### Installation

#### With UV (Recommended)

```bash
# Check which venv is active now
echo $VIRTUAL_ENV
# Deactivate if it's not your desired project
deactivate
# Create a virtual environment if needed
python3 -m venv .venv
source .venv/bin/activate

# Prepare the environment
uv python install 3.12
uv init --python 3.12
# Add project dependencies
uv add -r requirements.txt
uv sync
```

#### With Conda

```bash
conda create -n ta_dashboard_env python=3.9
conda activate ta_dashboard_env
pip install streamlit==1.42.0 google-generativeai==0.8.4 yfinance==0.2.40 pandas==2.2.3 plotly==6.0.0 ta==0.11.0 kaleido==0.2.1
```

### API Key Setup

1. Obtain a Google AI Studio API key from [Google AI Studio](https://ai.google.dev/)
2. Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

### Running the Application

```bash
uv run --active streamlit run main.py
```

Or if using conda:

```bash
streamlit run main.py
```

## Troubleshooting

- If you encounter data-related issues, clear the Streamlit cache:
  ```bash
  streamlit cache clear
  ```

- If you need to update a specific library:
  ```bash
  uv pip install --upgrade yfinance
  ```

## Full Disclaimer

This software is provided as-is, without any warranties, express or implied. 
The author(s) and distributor(s) disclaim all liability for any loss, damage, 
or financial decision made based on this application.

### No Financial or Investment Advice

This application is intended solely for educational and research purposes. 
It does not provide financial, investment, or trading advice. Users are responsible 
for conducting their own independent research before making any financial decisions. 
The authors and distributors are not licensed financial professionals, and this software 
should not be used as a substitute for professional financial advice.

### Use at Your Own Risk

Trading and investing involve substantial risk of loss. Past performance is not 
indicative of future results.
The authors, sellers, and distributors assume no responsibility for any financial 
losses, misinterpretations, or incorrect decisions made based on this software.
This tool is provided without any express or implied warranties, including but not limited 
to fitness for a particular purpose, accuracy, reliability, or availability.

### Experimental AI Output

This software integrates Generative AI models, which can sometimes produce inaccurate, 
misleading, or hallucinated results. AI-generated insights should never be used as the sole 
basis for investment decisions—always verify results independently.
The AI models are constantly evolving, and output quality may vary based on the dataset, 
timeframe, or market conditions.