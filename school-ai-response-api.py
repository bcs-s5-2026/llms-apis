import os
import sys
from typing import TypedDict
from dotenv import load_dotenv

# This program demonstrates how to use the OpenAI Python client to interact with the school's hosted AI models.
# It loads the API key from an environment variable, sends a prompt to a specified model,
# and prints the response in a streaming manner (or as a single reply when SCHOOL_STREAM is set to false).
# Run it with the --list-models flag to only print the models the server offers.
# This example requires /v1/responses support, which is not guaranteed by
# OpenAI-compatible Chat Completions support. Use school-ai.py if unavailable.
# For this to work, you need to set the SCHOOL_HOSTED_MODEL_API_KEY environment variable 
# with your API key from your school's hosted AI model server.
# The server URL and your personal access authorisation key are sent to you
# by email by the course team. Each student gets one personal key: keep it to
# yourself, never share it, and never commit it.
# You must copy the template from .env.example to .env and fill in your actual API key and server URL.
# MAKE SURE TO NEVER COMMIT YOUR .env FILE WITH REAL API KEYS.
# IF YOU EVER DO, LET ME KNOW IMMEDIATELY: WE WILL REVOKE THE KEY AND GIVE YOU A NEW ONE. DO NOT TRY TO UNDO THIS VIA GIT HISTORY.

from openai import APIStatusError, OpenAI, Stream
from openai.types.responses import Response


class ResponseRequestParameters(TypedDict):
  model: str
  input: str
  temperature: float
  top_p: float
  max_output_tokens: int
  store: bool
  stream: bool
  timeout: int


def list_available_models(client: OpenAI) -> None:
  # Prints the models the server says are available, using the SDK's built-in
  # method for the standard OpenAI-compatible /models endpoint.
  print("Models available on the server:", flush=True)
  models_page = client.models.list()
  for model_info in models_page.data:
    print(f"- {model_info.id}", flush=True)

  # Tip: you can use one of the names printed above to replace the value of
  # "model_name" in this Python script, or the value of the
  # SCHOOL_MODEL_NAME env variable in your .env file.


def check_response(response: Response) -> None:
  if response.status == "failed":
    detail = response.error.message if response.error else "No error details supplied."
    raise RuntimeError(f"Response failed: {detail}")
  if response.status == "incomplete":
    reason = response.incomplete_details.reason if response.incomplete_details else "unknown"
    raise RuntimeError(f"Response incomplete: {reason}")
  if response.status != "completed":
    raise RuntimeError(f"Unexpected response status: {response.status}")


def main() -> None:
  # Load SCHOOL hosted models env vairables (server URL, API key, model name) from environment variable
  # For example, in bash:
  #   export SCHOOL_HOSTED_MODEL_API_KEY='your_api_key_here'
  # Or, if you have a .env file, you may source it before running this script
  # by doing so at the bash:
  #   source .env
  # Or, use python-dotenv to load it from a .env file without overriding existing environment variables.
  # as it is done in the code below.
  load_dotenv()
  api_key = os.getenv("SCHOOL_HOSTED_MODEL_API_KEY")

  if not api_key:
    print("Error: SCHOOL_HOSTED_MODEL_API_KEY is not set.")
    print("Set it before running, for example:")
    print("  export SCHOOL_HOSTED_MODEL_API_KEY='your_api_key_here'")
    sys.exit(1)

  server_url = os.getenv("SCHOOL_HOSTED_MODEL_SERVER_URL")
  if not server_url:
    raise RuntimeError("SCHOOL_HOSTED_MODEL_SERVER_URL is not set. Use the school URL from your email.")

  model_name = os.getenv("SCHOOL_MODEL_NAME", "gemma-4-31b-it")

  prompt = os.getenv("PROMPT", "Imagine a dialog between a human and an AI - 5 interactions. Make the AI snarky. Interactions are 3 sentences maximum.")
  stream_mode = os.getenv("SCHOOL_STREAM", "true").lower() in {"1", "true", "yes", "y"}

  client = OpenAI(
    base_url = server_url,
    api_key = api_key,
    timeout=25, # Set a reasonable timeout for the request
    max_retries=0
  )

  # ------------------------------------------------------------------
  # Listing the models available on the school server (/v1/models)
  # ------------------------------------------------------------------
  # Run this script with the --list-models command-line flag and it will
  # print the model names offered by the server (see
  # list_available_models() above) and stop, without sending the prompt.
  #
  # The same endpoint also works straight from your terminal, without
  # Python. If SCHOOL_HOSTED_MODEL_SERVER_URL already ends with /v1, just
  # append /models to it:
  #
  #   curl -s -H "Authorization: Bearer $SCHOOL_HOSTED_MODEL_API_KEY" \
  #        "$SCHOOL_HOSTED_MODEL_SERVER_URL/models"
  #
  # (If the URL does not end with /v1, request the "/v1/models" path instead.)

  if "--list-models" in sys.argv[1:]:
    list_available_models(client)
    return

  print("Sending request...", flush=True)
  print(f"Primary model: {model_name} | stream={stream_mode}", flush=True)

  response_parameters: ResponseRequestParameters = {
    "model": model_name,
    "input": prompt,
    "temperature": 1.5,
    "top_p": 0.95,
    "max_output_tokens": 256,
    "store": False,
    "stream": stream_mode,
    "timeout": 60,
  }
  response = client.responses.create(**response_parameters)

  # Narrow the actual return type: a bool stream setting gives a union type.
  if isinstance(response, Stream):
    got_text = False
    got_completed = False
    with response:
      for event in response:
        # Responses streams contain typed events, not Chat Completion choices.
        if event.type == "response.output_text.delta":
          if event.delta:
            got_text = True
            print(event.delta, end="", flush=True)
        elif event.type == "response.refusal.delta":
          if event.delta:
            got_text = True
            print(event.delta, end="", flush=True)
        elif event.type == "error":
          raise RuntimeError(f"Response stream error: {event.message}")
        elif (
          event.type == "response.completed"
          or event.type == "response.failed"
          or event.type == "response.incomplete"
        ):
          check_response(event.response)
          got_completed = True
    if not got_completed:
      raise RuntimeError("Response stream ended without a completed event.")
    if not got_text:
      raise RuntimeError("Response completed without text or a refusal.")
  else:
    check_response(response)
    if response.output_text:
      print(response.output_text, flush=True)
    else:
      got_refusal = False
      for item in response.output:
        if item.type == "message":
          for content in item.content:
            if content.type == "refusal" and content.refusal:
              got_refusal = True
              print(content.refusal, flush=True)
      if not got_refusal:
        raise RuntimeError("Response completed without text or a refusal.")

  print("\nDone.", flush=True)

if __name__ == "__main__":
  try:
    main()
  except APIStatusError as e:
    print(f"API request failed (HTTP {e.status_code}): {e}", file=sys.stderr)
    if "--list-models" not in sys.argv[1:] and e.status_code in {404, 405, 501}:
      print(
        "The configured route or model may not support the Responses API. "
        "Check the school base URL and model; use school-ai.py for Chat Completions. "
        "No automatic fallback was attempted.",
        file=sys.stderr,
      )
    sys.exit(1)
  except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
