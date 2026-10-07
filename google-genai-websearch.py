import os
from wsgiref import types

# This program demonstrates the use of Google's GenAI API to generate content using the Gemini model.
# It loads the API key from an environment variable, sends a prompt to the model, and prints the generated response. 
# It also supports streaming responses, which allows it to print the output as it
# is generated, rather than waiting for the entire response to be ready.

# We are importing Google's GenAI module, which is a locally installed python library.
# That library is what will connect your application to their genai web api on their servers. 
# It provides higher level function and utilities.
# Documentation:
# https://googleapis.github.io/python-genai/
from google import genai

# Helper library to load environment variables from a .env file into the process's environment.
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# The client gets the API key from the environment variable `GOOGLE_API_KEY`.
api_key = os.getenv("GOOGLE_API_KEY")

# We create a client object that will be used to interact with the GenAI API.
client = genai.Client(api_key=api_key)

# Stream vs non-streaming response:
STREAM_ON = False

# Gemini Model
#MODEL = "gemini-3-flash-preview"
#MODEL = "gemini-3.1-flash-lite-preview"
MODEL = "gemini-2.5-flash" # This one supports web search grounding

# Prompt
PROMPT = "What is the weather in Paris right now?" # Testing grounding with web search

# Configure the grounding tool
# Using the 'google_search' tool type
config = genai.types.GenerateContentConfig(
    system_instruction="You are a overzealous character with a penchant for dramatics, who speaks in Old fashion and quaint English.",
    tools=[genai.types.Tool(google_search=genai.types.GoogleSearch())],
    automatic_function_calling=genai.types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

def main():
  # Generate content with the Gemini 3 Flash Preview model.
  if STREAM_ON:
    # If streaming is on, we will receive an iterator that yields parts of the response as they are generated.
    for chunk in client.models.generate_content_stream(
        model=MODEL,
        contents=PROMPT,
        config=config

    ):
      print(chunk.text, end='', flush=True)  # flush=True makes it print immediately
  else:
    response = client.models.generate_content(
        model=MODEL,
        contents=PROMPT,
        config=config
    ) 
    # The response is a Python object that contains the generated content and metadata.
    print(response.text)
    # 5. Optional: Inspect the grounding metadata (sources/links)
    if response and response.candidates and response.candidates[0].grounding_metadata:
        print("\nSources used:")
        if response.candidates[0].grounding_metadata.grounding_chunks:
          for chunk in response.candidates[0].grounding_metadata.grounding_chunks:
            if chunk.web:
              print(f"- {chunk.web.title}: {chunk.web.uri}")


if __name__ == "__main__":
  main()