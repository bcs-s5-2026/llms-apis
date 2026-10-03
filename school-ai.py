import os
import sys
import dotenv

# This program demonstrates how to use the OpenAI Python client to interact with the school's hosted AI models.
# It loads the API key from an environment variable, sends a prompt to a specified model,
# and prints the response in a streaming manner (or as a single reply when SCHOOL_STREAM is set to false).
# Run it with the --list-models flag to only print the models the server offers.
# For this to work, you need to set the SCHOOL_HOSTED_MODEL_API_KEY environment variable 
# with your API key from your school's hosted AI model server.
# The server URL and your personal access authorisation key are sent to you
# by email by the course team. Each student gets one personal key: keep it to
# yourself, never share it, and never commit it.
# You must copy the template from .env.example to .env and fill in your actual API key and server URL.
# MAKE SURE TO NEVER COMMIT YOUR .env FILE WITH REAL API KEYS.
# IF YOU EVER DO, LET ME KNOW IMMEDIATELY: WE WILL REVOKE THE KEY AND GIVE YOU A NEW ONE. DO NOT TRY TO UNDO THIS VIA GIT HISTORY.

from openai import OpenAI


def list_available_models(client):
  # Prints the models the server says are available, using the SDK's built-in
  # method for the standard OpenAI-compatible /models endpoint.
  print("Models available on the server:", flush=True)
  try:
    models_page = client.models.list()
  except Exception as e:
    print(f"Failed to fetch the model list: {e}", flush=True)
    print("Some OpenAI-compatible servers do not implement the /models endpoint.", flush=True)
    return

  for model_info in getattr(models_page, "data", models_page) or []:
    # .id is the only field guaranteed by the OpenAI spec - some compatible
    # servers return very minimal objects, so fall back to str() for them.
    print(f"- {getattr(model_info, 'id', str(model_info))}", flush=True)

  # Tip: you can use one of the names printed above to replace the value of
  # "model_name" in this Python script, or the value of the
  # SCHOOL_MODEL_NAME env variable in your .env file.


def main():
  # Load SCHOOL hosted models env vairables (server URL, API key, model name) from environment variable
  # For example, in bash:
  #   export SCHOOL_HOSTED_MODEL_API_KEY='your_api_key_here'
  # Or, if you have a .env file, you may source it before running this script
  # by doing so at the bash:
  #   source .env
  # Or, you can use the python-dotenv package to load it from a .env file automatically, which is what this script does if the variable is not already set.
  # as it is done in the code below.
  api_key = os.getenv("SCHOOL_HOSTED_MODEL_API_KEY")

  if not api_key:
    # Try loading api_key from .env file if not set in environment variables
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("SCHOOL_HOSTED_MODEL_API_KEY")
    if not api_key:
      print("Error: SCHOOL_HOSTED_MODEL_API_KEY is not set.")
      print("Set it before running, for example:")
      print("  export SCHOOL_HOSTED_MODEL_API_KEY='your_api_key_here'")
      sys.exit(1)

  model_name = os.getenv("SCHOOL_MODEL_NAME", "gemma-4-31b-it")

  prompt = os.getenv("PROMPT", "Imagine a dialog between a human and an AI - 5 interactions. Make the AI snarky. Interactions are 3 sentences maximum.")
  stream_mode = os.getenv("SCHOOL_STREAM", "true").lower() in {"1", "true", "yes", "y"}

  client = OpenAI(
    base_url = os.getenv("SCHOOL_HOSTED_MODEL_SERVER_URL"),
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

  completion = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": prompt}],
    temperature=1.5,
    top_p=0.95,
    max_tokens=256,
    # max_completion_tokens=4096,
    stream=stream_mode,
    timeout=60, # Set a longer timeout for the request to allow for slower responses
  )

  if stream_mode:
    # The reply arrives as a stream of small updates (tokens): print each
    # piece of text as it comes in. Only report "no tokens" after the
    # whole stream has been read, not on every empty chunk.
    got_any_token = False
    for chunk in completion:
      if not getattr(chunk, "choices", None):
        continue
      if chunk.choices and chunk.choices[0].delta.content is not None:
        got_any_token = True
        print(chunk.choices[0].delta.content, end="", flush=True)

    if not got_any_token:
      print("No tokens received.", flush=True)
  else:
    # With SCHOOL_STREAM=false the whole reply arrives in a single response,
    # and it must be read from a different place than in the streaming case.
    if completion.choices and completion.choices[0].message.content:
      print(completion.choices[0].message.content, flush=True)
    else:
      print("No content received.", flush=True)

  print("\nDone.", flush=True)

if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
