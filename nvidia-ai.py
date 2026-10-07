import os
import sys
import dotenv

# This program demonstrates how to use the OpenAI Python client to interact with NVIDIA's integrated API for free AI models.
# It loads the API key from an environment variable, sends a prompt to a specified model,
# and prints the response in a streaming manner.
# For this to work, you need to set the NVIDIA_API_KEY environment variable 
# with your API key from https://build.nvidia.com/models

from openai import OpenAI

def main():
  # Load NVIDIA API key from environment variable
  # For example, in bash:
  #   export NVIDIA_API_KEY='your_api_key_here'
  # Or, if you have a .env file, you may source it before running this script
  # by doing so at the bash:
  #   source .env
  # Or, you can use the python-dotenv package to load it from a .env file automatically, which is what this script does if the variable is not already set.
  # as it is done in the code below.
  api_key = os.getenv("NVIDIA_API_KEY")

  if not api_key:
    # Try loading api_key from .env file if not set in environment variables
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
      print("Error: NVIDIA_API_KEY is not set.")
      print("Set it before running, for example:")
      print("  export NVIDIA_API_KEY='your_api_key_here'")
      sys.exit(1)

  # Picking one model among the available NVIDIA models. 
  # Be aware that the service is not guaranteed to be available at all times.
  # There are rate limits and the models get retired or updated periodically.
  model_name = "nvidia/nemotron-3-super-120b-a12b"

  prompt = os.getenv("NVIDIA_PROMPT", "Imagine a dialog between a human and an AI - 5 interactions. Make the AI snarky. Interactions are 3 sentences maximum.")
  stream_mode = os.getenv("NVIDIA_STREAM", "true").lower() in {"1", "true", "yes", "y"}

  client = OpenAI(
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = api_key,
    timeout=25, # Set a reasonable timeout for the request
    max_retries=0
  )

  print("Sending request...", flush=True)
  print(f"Primary model: {model_name} | stream={stream_mode}", flush=True)


  completion = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": prompt}],
    temperature=1,
    top_p=0.95,
    max_tokens=2048, # be aware of the token limit: too short and you may not get anything
    stream=stream_mode,
    timeout=60, # Set a longer timeout for the request to allow for slower responses
  )

  if stream_mode:
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
    print(completion.choices[0].message, flush=True)

  # end of main()
  print("\nDone.", flush=True)

if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(f"An error occurred: {e}")
    
sys.exit(1)
