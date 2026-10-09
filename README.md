# LLMs APIs Python Apps

This repository contains standalone Python applications:

1. Direct Google Gemini examples
2. Direct NVIDIA examples
3. School-hosted models example (`school-ai.py`)

All scripts share one Python environment and one `requirements.txt` file.

## SDK Notes

- The Google Gemini examples use Google's own SDK (`google-genai` package).
- The school and NVIDIA examples are based on the widely used OpenAI-compatible Python SDK (`openai` package) - the same client library, pointed at a different `base_url` for each provider.

## Project Layout

- `google-genai.py` - Simple Gemini generation demo
- `google-genai-websearch.py` - Gemini generation with Google Search grounding and source links
- `nvidia-ai.py` - Simple NVIDIA Integrate API generation demo (OpenAI-compatible client)
- `school-ai.py` - School-hosted model generation demo (OpenAI-compatible client), with notes on how to list the available models
- `school-ai-response-api.py` - School-hosted Responses API demo (requires server support for `/v1/responses`)
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
   - `SCHOOL_HOSTED_MODEL_API_KEY` and `SCHOOL_HOSTED_MODEL_SERVER_URL` for the school example - both are sent to you by email by the course team. Each student gets one personal access authorisation key: keep it to yourself and never share it.

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

### School Hosted Models

```bash
python school-ai.py
```

This script sends a prompt to the school's hosted model server. The model is selected with `SCHOOL_MODEL_NAME` in `.env` (default: `gemma-4-31b-it`). By default the reply is streamed token by token; set `SCHOOL_STREAM` to `false` in `.env` to receive the full completion in a single response. Run `python school-ai.py --list-models` to print the model names offered by the server (from the OpenAI-compatible `/v1/models` endpoint) and stop, without sending the prompt - use one of the printed names as `SCHOOL_MODEL_NAME`.

Your personal access authorisation key (`SCHOOL_HOSTED_MODEL_API_KEY`) and the server URL (`SCHOOL_HOSTED_MODEL_SERVER_URL`) are sent to you by email - copy them into your local `.env` before running.

### School Hosted Models with the Responses API

```bash
python school-ai-response-api.py
python school-ai-response-api.py --list-models
```

This example uses `client.responses.create()` from `openai>=1.66.0` with the same school configuration. It sends `input` instead of Chat Completions `messages`, uses `max_output_tokens`, prints streamed `response.output_text.delta` events, and reads `response.output_text` in non-streaming mode (`SCHOOL_STREAM=false`). Requests use `store=False` to avoid requesting server-side response storage.

The request settings are collected in a typed `response_parameters` dictionary and passed to one `create(**response_parameters)` call. The script then branches on the returned type to consume a stream or a complete response.

**School endpoint support was reported working in a manual test on 9 October 2026.** This does not establish support for every model or parameter combination. Supporting `/v1/chat/completions` alone does not imply support for `/v1/responses`. Model listing still uses `/v1/models` and does not verify Responses support. Run a generation request to check support for the selected model and parameters. HTTP 404, 405, or 501 triggers a compatibility hint and a nonzero exit; authentication, validation, and other API errors remain errors. Failed/incomplete responses and interrupted streams also exit with an error rather than reporting success. There is no automatic fallback: use `school-ai.py` if the school server only supports Chat Completions.

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
   - `SCHOOL_HOSTED_MODEL_API_KEY`
   - `SCHOOL_HOSTED_MODEL_SERVER_URL`
   - `SCHOOL_MODEL_NAME`

### API/network errors

- Verify network connectivity.
- Retry after a short delay if rate-limited.
- Confirm your API keys are valid and model access is enabled.

## Security Notes

- Keep `.env` private and never commit real API keys.
- Commit only `.env.example` as a template.
