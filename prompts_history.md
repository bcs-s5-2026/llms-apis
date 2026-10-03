# Prompts History

Automatically captured prompt log. Entries are appended in chronological order (oldest first).

s### 03-10-2026 17:22
- **Prompt**: /explain No overloads for "create" match the provided arguments, Argument of type "str | None" cannot be assigned to parameter "model" of type "ChatModel | str" in function "create"   Type "str | None" is not assignable to type "ChatModel | str"     Type "None" is not assignable to type "ChatModel | str"       "None" is not assignable to "str"       "None" is not assignable to "Literal['gpt-6-astra']"       "None" is not assignable to "Literal['gpt-6.1-sol']"       "None" is not assignable to "Literal['gpt-6-sol']"       "None" is not assignable to "Literal['gpt-6-luna']"       "None" is not assignable to "Literal['gpt-5.6-sol']"   ...

### 03-10-2026 18:18
- **Prompt**: can you update the README file to include the latest changes, in particular the new school related stuff. Add an explanation about the school hosted models access authorisation key which will be sent to them by email in the README, the .env.example file and in the school-ai.py files if it isn't in there already. Add aslo something about the fact that the Gemini example is using their own sdk, while the school (and nvidia) examples are based on the widely used openai compatible sdk. Add a section in the school-ai.py that explains how to list the models that are available (I think the end point is /v1/models).

### 03-10-2026 18:25
- **Prompt**: yes, fix those

### 03-10-2026 18:35
- **Prompt**: what would it take to add to school-ai.py a function that could be called to query the list of models provided by the server? do not change the code yet, just tell me

### 03-10-2026 18:39
- **Prompt**: implement the command-line argument option - and yes, when invoked, it should not continue with the prompt. Add a comment at the end of listing the models that the model name can be used to replace the value of either "model_name" in the python script, or in the SCHOOL_MODEL_NAME env variable in the .env file

