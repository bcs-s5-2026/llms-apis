# This Journal gets updated automatically by the Journal Logger Agent



### **New Interaction**
- **Hook Version**: 1.02
- **Date**: 03-10-2026 18:18
- **Prompt**: can you update the README file to include the latest changes, in particular the new school related stuff. Add an explanation about the school hosted models access authorisation key which will be sent to them by email in the README, the .env.example file and in the school-ai.py files if it isn't in there already. Add aslo something about the fact that the Gemini example is using their own sdk, while the school (and nvidia) examples are based on the widely used openai compatible sdk. Add a section in the school-ai.py that explains how to list the models that are available (I think the end point is /v1/models).
- **CoPilot Mode**: Agent
- **CoPilot Model**: not reported by runtime
- **Socratic Mode**: ON
- **Changes Made**: README.md: added school-ai.py to the intro list and project layout, new "SDK Notes" section (Gemini examples use the google-genai SDK; school and NVIDIA examples use the widely used OpenAI-compatible openai SDK with different base_url), school key/URL bullet in Prerequisites with the by-email explanation, new "School Hosted Models" run section (SCHOOL_MODEL_NAME default gemma-4-31b-it, pointer to /v1/models listing notes), SCHOOL_* variables added to Troubleshooting. .env.example: added explanation that the server URL and personal access authorisation key are sent by email, one personal key per student. school-ai.py: header now states key/URL are sent by email; new comment section in main() documenting how to list available models via /v1/models using client.models.list() and a curl example. Verified school-ai.py with py_compile. No commit made (user only asked to update files).
- **Context and Reasons for Changes**: Course-owner request to bring documentation in line with the new school-hosted-models example (school-ai.py is not yet tracked in git). Executed directly since this is a documentation/course-material maintenance task, not a student learning exercise. Deliberately did not document SCHOOL_STREAM as toggling streaming: the script computes stream_mode but the create() call hardcodes stream=True, so the docs stay accurate.

### **New Interaction**
- **Hook Version**: 1.02
- **Date**: 03-10-2026 18:25
- **Prompt**: yes, fix those
