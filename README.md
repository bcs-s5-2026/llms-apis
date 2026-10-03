# LLMs APIs Python Apps

This repository contains standalone Python applications:

1. REST API client example (`country-webapi.py`)
2. Direct Google Gemini examples
3. Direct NVIDIA examples

All scripts share one Python environment and one `requirements.txt` file.

## Project Layout

- `country-webapi.py` - Country information lookup using https://restcountries.com
- `google-genai.py` - Simple Gemini generation demo
- `google-genai-websearch.py` - Gemini generation with Google Search grounding and source links
- `nvidia-ai.py` - Simple NVIDIA Integrate API generation demo (OpenAI-compatible client)
- `docs/` - Source texts for reference
- `requirements.txt` - Shared dependencies
- `.env.example` - Environment variable template

## Prerequisites

- Python 3.10+
- `pip`
- Internet access (API calls and initial model downloads)
- API keys for GenAI scripts:
   - `GOOGLE_API_KEY` from Google AI Studio
   - `NVIDIA_API_KEY` from NVIDIA Build

## Setup

### 1. Create and activate a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Then set your real keys in `.env`.

## Run Each Application

### REST Countries API

```bash
python country-webapi.py
```

### Simple Google Gemini

```bash
python google-genai.py
```

### Google Gemini with Web Search Grounding

```bash
python google-genai-websearch.py
```

This script demonstrates grounded generation with Gemini by enabling the built-in Google Search tool. It can print source links used by the model when grounding metadata is available.

### Simple NVIDIA Integrate API

```bash
python nvidia-ai.py
```

## Troubleshooting

### Missing imports or package errors

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Missing API key errors

- Verify `.env` exists in project root.
- Ensure variable names are exactly:
   - `GOOGLE_API_KEY`
   - `NVIDIA_API_KEY`

### API/network errors

- Verify network connectivity.
- Retry after a short delay if rate-limited.
- Confirm your API keys are valid and model access is enabled.

## Security Notes

- Keep `.env` private and never commit real API keys.
- Commit only `.env.example` as a template.
