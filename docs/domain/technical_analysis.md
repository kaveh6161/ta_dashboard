# Technical Analysis Concepts

This document explains the technical analysis concepts and indicators used in the TA Dashboard.

## Fundamental Concepts

### Price Action

Price action refers to the movement of a security's price plotted over time. In technical analysis, this movement is considered to contain all known information about the security, including fundamental factors, market psychology, and external events.

### Timeframes

The TA Dashboard supports multiple timeframes for analysis:

| Timeframe | Description | Typical Use |
|-----------|-------------|-------------|
| 1m | 1-minute candles | Very short-term scalping |
| 5m | 5-minute candles | Intraday trading |
| 15m | 15-minute candles | Intraday trading |
| 30m | 30-minute candles | Intraday trading |
| 1h | 1-hour candles | Swing trading |
| 1d | Daily candles | Position trading |
| 1wk | Weekly candles | Long-term trends |

### Chart Types

The dashboard primarily uses candlestick charts, which show:
- Open price
- Close price
- High price
- Low price
- (Volume is displayed in a separate panel)

## Indicator Categories

### Trend Indicators

Trend indicators help identify the direction of market momentum.

#### Simple Moving Average (SMA)

A simple average of prices over a specified period.

**Formula:**
```
SMA = (P₁ + P₂ + ... + Pₙ) / n
```

**Interpretation:**
- Price above SMA: Bullish
- Price below SMA: Bearish
- SMA crossovers: Potential trend changes

#### Exponential Moving Average (EMA)

A weighted average that gives more importance to recent prices.

**Formula:**
```
Multiplier = 2 / (n + 1)
EMA = (Close - Previous EMA) × Multiplier + Previous EMA
```

**Interpretation:**
- Similar to SMA but reacts faster to price changes
- Often used in conjunction with slower SMAs

#### Bollinger Bands

Three lines: a middle SMA with upper and lower bands set at standard deviation levels.

**Formula:**
```
Middle Band = 20-day SMA
Upper Band = Middle Band + (20-day standard deviation × 2)
Lower Band = Middle Band - (20-day standard deviation × 2)
```

**Interpretation:**
- Price near upper band: Potentially overbought
- Price near lower band: Potentially oversold
- Band expansion: Increased volatility
- Band contraction: Decreased volatility

### Oscillators

Oscillators are technical indicators that fluctuate between defined values, helping identify overbought or oversold conditions.

#### Relative Strength Index (RSI)

Measures the speed and change of price movements on a scale from 0 to 100.

**Formula:**
```
RS = Average Gain / Average Loss
RSI = 100 - (100 / (1 + RS))
```

**Interpretation:**
- RSI > 70: Potentially overbought
- RSI < 30: Potentially oversold
- Divergence between RSI and price: Potential reversal

#### Moving Average Convergence Divergence (MACD)

Shows the relationship between two moving averages.

**Formula:**
```
MACD Line = 12-day EMA - 26-day EMA
Signal Line = 9-day EMA of MACD Line
Histogram = MACD Line - Signal Line
```

**Interpretation:**
- MACD Line crosses above Signal Line: Bullish
- MACD Line crosses below Signal Line: Bearish
- Histogram increasing: Bullish momentum increasing
- Histogram decreasing: Bearish momentum increasing

#### Stochastic Oscillator

Compares a closing price to its price range over a period, displayed as %K and %D lines.

**Formula:**
```
%K = ((Current Close - Lowest Low) / (Highest High - Lowest Low)) × 100
%D = 3-day SMA of %K
```

**Interpretation:**
- Above 80: Potentially overbought
- Below 20: Potentially oversold
- %K crosses above %D: Bullish
- %K crosses below %D: Bearish

### Volume Indicators

Volume indicators analyze the strength of price movements based on trading volume.

#### On-Balance Volume (OBV)

Relates volume to price change to measure buying and selling pressure.

**Formula:**
```
If Close > Previous Close: OBV = Previous OBV + Current Volume
If Close < Previous Close: OBV = Previous OBV - Current Volume
If Close = Previous Close: OBV = Previous OBV
```

**Interpretation:**
- Rising OBV: Positive volume pressure
- Falling OBV: Negative volume pressure
- Divergence between OBV and price: Potential reversal

## Combining Indicators

The TA Dashboard allows users to combine multiple indicators for comprehensive analysis:

### Common Combinations

1. **Trend Confirmation**
   - SMA (longer period) for trend direction
   - RSI for momentum confirmation
   - Volume to confirm strength

2. **Volatility Assessment**
   - Bollinger Bands for volatility range
   - ATR for volatility measurement
   - RSI for overbought/oversold conditions

3. **Reversal Detection**
   - RSI divergence
   - MACD crossovers
   - OBV confirmation

## AI Enhancement

The dashboard enhances traditional technical analysis with AI interpretation by:

1. Identifying chart patterns automatically
2. Detecting confluence between multiple indicators
3. Providing probability-based trend assessments
4. Highlighting divergences that may be difficult to spot manually

The AI analysis complements, rather than replaces, traditional technical indicators, providing users with additional insights that may not be immediately apparent from the indicators alone.