# System Diagrams

This section contains visual representations of the TA Dashboard system architecture, data flows, and component relationships.

## Available Diagrams

1. [System Architecture](./system_architecture.md)
2. [Data Flow](./data_flow.md)
3. [Component Interactions](./component_interactions.md)
4. [AI Integration](./ai_integration.md)

## System Architecture

The system architecture diagram provides a high-level overview of the TA Dashboard components and their relationships:

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

## Data Flow

The data flow diagram illustrates how data moves through the system:

```
┌─────────┐     ┌───────────┐     ┌──────────────┐
│  User   │────▶│ UI Config │────▶│ Stock Data   │
│ Input   │     │ Selection │     │  Retrieval   │
└─────────┘     └───────────┘     └──────┬───────┘
                                         │
                                         ▼
┌─────────────┐     ┌───────────┐     ┌──────────────┐
│ Results     │◀────│ Display & │◀────│ Technical    │
│ Presentation│     │ Formatting│     │ Calculations │
└─────────────┘     └───────────┘     └──────┬───────┘
                                             │
                          ┌──────────────────┴───────────────┐
                          │                                  │
                          ▼                                  ▼
                   ┌──────────────┐                  ┌──────────────┐
                   │ Chart        │                  │ News         │
                   │ Generation   │                  │ Retrieval    │
                   └──────┬───────┘                  └──────┬───────┘
                          │                                 │
                          ▼                                 ▼
                   ┌──────────────┐                  ┌──────────────┐
                   │ AI Chart     │                  │ AI Sentiment │
                   │ Analysis     │                  │ Analysis     │
                   └──────────────┘                  └──────────────┘
```

## Component Interactions

This diagram shows how the different components interact with each other:

```
┌───────────────────────────────────────────────────────────┐
│                       main.py                              │
├───────────────────────────────────────────────────────────┤
│ ┌─────────────┐   ┌────────────┐   ┌────────────────────┐ │
│ │ UI Handling │   │ Data Fetch │   │ Technical Analysis │ │
│ └──────┬──────┘   └─────┬──────┘   └──────────┬─────────┘ │
│        │                │                     │           │
│        │                │                     │           │
│        ▼                ▼                     ▼           │
│ ┌─────────────┐   ┌────────────┐   ┌────────────────────┐ │
│ │ Chart       │   │ News       │   │ Indicator          │ │
│ │ Generation  │   │ Integration│   │ Calculation        │ │
│ └──────┬──────┘   └─────┬──────┘   └──────────┬─────────┘ │
└────────┼────────────────┼─────────────────────┼───────────┘
         │                │                     │
         ▼                ▼                     │
┌─────────────────┐ ┌────────────────┐         │
│ news_gathering  │ │ sentiment_     │         │
│     .py         │ │ analysis.py    │◀────────┘
└─────────────────┘ └────────────────┘
```

## AI Integration

This diagram illustrates how AI is integrated into the system:

```
┌─────────────────────────────────────────────────────────┐
│                Google Gemini AI API                      │
└───────┬─────────────────────────────────────────────────┘
        │
        │ JSON Responses
        │
┌───────▼─────────────────────────────────────────────────┐
│                AI Integration Layer                      │
├─────────────────────────┬───────────────────────────────┤
│                         │                               │
│                         │                               │
▼                         ▼                               ▼
┌─────────────────┐ ┌────────────────┐         ┌───────────────┐
│ Chart Analysis  │ │ News Sentiment │         │ Prompt        │
│ Processing      │ │ Processing     │         │ Generation     │
└────────┬────────┘ └────────┬───────┘         └───────┬───────┘
         │                   │                         │
         │                   │                         │
         ▼                   ▼                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Main Application                        │
└─────────────────────────────────────────────────────────┘
```

For detailed diagrams, please refer to the individual diagram pages listed above.