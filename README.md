## Full Disclaimer
This software is provided as-is, without any warranties, express or implied. 
The author(s) and distributor(s) disclaim all liability for any loss, damage, 
or financial decision made based on this application.

## No Financial or Investment Advice
This application is intended solely for educational and research purposes. 
It does not provide financial, investment, or trading advice. Users are responsible 
for conducting their own independent research before making any financial decisions. 
The authors and distributors are not licensed financial professionals, and this software 
should not be used as a substitute for professional financial advice.

## Use at Your Own Risk
Trading and investing involve substantial risk of loss. Past performance is not 
indicative of future results.
The authors, sellers, and distributors assume no responsibility for any financial 
losses, misinterpretations, or incorrect decisions made based on this software.
This tool is provided without any express or implied warranties, including but not limited 
to fitness for a particular purpose, accuracy, reliability, or availability.

## Experimental AI Output
This software integrates Generative AI models, which can sometimes produce inaccurate, 
misleading, or hallucinated results. AI-generated insights should never be used as the sole 
basis for investment decisions—always verify results independently.
The AI models are constantly evolving, and output quality may vary based on the dataset, 
timeframe, or market conditions.

## API Key Requirement
This application requires a valid Google AI Studio API key to generate AI-powered insights.
The API key is not included in this product and must be obtained separately from 
Google AI Studio. Users must configure and securely store their own API key following 
the provided setup instructions.

## Python Environment Setup (Conda Setup Example)

Run the following in your terminal:

```
conda create -n ta_gemini_prem_env python=3.9
conda activate ta_gemini_prem_env
pip install streamlit==1.42.0 google-generativeai==0.8.4 yfinance==0.2.40 pandas==2.2.3 plotly==6.0.0 ta==0.11.0 kaleido==0.2.1
```

OR, with `UV`:

```
##
# First steps
##

# check which venv is active now
echo $VIRTUAL_ENV
# deactivate it if it's not your desired project
deactivate
# navigate to the project directory, then:
source .venv/bin/activate

##
# Prepare the environment
##

uv python install 3.12
# run this from teh project directory
uv init --python 3.12
# or the following, if the project is already initiated
uv python pin 3.12
# add project dependencies to pyproject.toml project definition, create a venv and download them
uv add -r requirements.txt
uv sync
# activate your venv and run your app
uv run --active streamlit run main.py

##
# Troubleshooting steps
##

# update a specific library manually
uv pip install --upgrade yfinance
```