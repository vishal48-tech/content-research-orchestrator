# 🔍 Content Research Agent

Multi-agent content research system using LangGraph, Groq API, and Streamlit.

## Features

- **AI-powered research planning** — Automatically plans search angles based on topic
- **Web search** — DuckDuckGo search with real URL extraction
- **Content extraction** — Jina AI Reader for full article text
- **Credibility scoring** — Heuristic scoring based on domain + content length
- **Streaming outline generation** — Real-time outline creation with LLM streaming
- **Content evaluation** — Multi-dimensional scoring (Intent, Engagement, Accuracy, etc.)
- **LangSmith observability** — Full tracing of research pipeline

## Architecture
```mermaid
flowchart TD
    A [User Query] --> B [Coordinator]
    B --> C [Plan angles]
    C --> D [Search]
    D --> E [Find sources]
    E --> F [Synthesis]
    F --> G [Outline]
    G --> H [Evaluation]
    H --> I [Score & recommend]
    I --> J [Output]
```


## Setup

```bash
# Clone repo
git clone https://github.com/vishal48-tech/content-research-orchestrator.git
cd content-research-orchestrator

# Create virtual environment
uv venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Set environment variables

# Run Streamlit app
streamlit run app.py
```

## Environment Variables
| Variable            | Description                     | Required |
| ------------------- | ------------------------------- | -------- |
| `GROQ_API_KEY`      | Groq API key                    | Yes      |
| `LANGSMITH_API_KEY` | LangSmith API key               | Optional |
| `LANGSMITH_PROJECT` | LangSmith project name          | Optional |
| `LANGSMITH_TRACING` | Enable tracing (`true`/`false`) | Optional |

## Usage

1. Enter a research topic (e.g., "AI agent frameworks 2026")
2. Click "Start Research"
3. Watch the pipeline: planning → searching → synthesizing → evaluating
4. Download the markdown output

## Tech Stack

- **LangGraph** — Multi-agent orchestration
- **Groq/Openrouter API** — LLM inference (Nex-N2-Pro, Llama, etc.)
- **DuckDuckGo** — Web search
- **Jina AI** — Content extraction
- **Streamlit** — UI
- **LangSmith** — Observability