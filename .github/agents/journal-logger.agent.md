---
description: 'Updates the JOURNAL.md file after each prompt.'

tools: [vscode, execute, read, agent, browser, edit, search, web, ms-python.python/getPythonEnvironmentInfo, ms-python.python/getPythonExecutableCommand, ms-python.python/installPythonPackage, ms-python.python/configurePythonEnvironment, todo]
---
## Journal Logger Agent Version
- Agent Version: 2.3

## Purpose
After each prompt, update the JOURNAL.md file in the repository root with a new entry according to the following template. If JOURNAL.md does not exist, create it at the root of the repository before logging the entry.

## Silent Operation
- Operate silently by default.
- Do not generate user-facing narration that announces you are about to write a journal entry or that you have written one.
- Only surface logging details if the user explicitly asks about the journal, or if logging fails and the failure needs to be reported.

## User Field Normalization

Use:
`User: default_user`

One-time normalization rule:
- Replace `default_user` with git identity from `git config user.email` (preferred) or `git config user.name`.
- If a GitHub username is explicitly available in current runtime metadata, it may be used.
- Otherwise use `$USER` as the final fallback.
- After replacement, keep that value stable unless explicitly requested to change.


Example format:

```md
### **New Interaction**
- **Agent Version**: [Agent Version]
- **Date**: [DD-MM-YYYY HH:MM]
- **User**: [User as defined in normalization rules]
- **Prompt**: [strictly verbatim raw user prompt. Do not truncate or summarize.]
- **CoPilot Mode**: [Ask|Plan|Edit|Agent]
- **CoPilot Model**: [actual runtime model name]
- **Socratic Mode**: [ON|OFF]
- **Changes Made**: [concise summary]
- **Context and Reasons for Changes**: [concise context/reasoning]

```

Ensure that the JOURNAL.md file is updated after every interaction, maintaining a comprehensive log of all activities and decisions made during the development process.

New entries are **appended at the end** of the file. The journal is in chronological order, oldest first. Do not read the existing file content or rewrite it — use the `execute` tool to append the new entry with a shell redirect (`>>`) for maximum efficiency.

## Safeguards Against Corruption

**UTF-8 Encoding**
- Always open JOURNAL.md with explicit UTF-8 encoding: use `open(path, 'a', encoding='utf-8')` in Python or specify encoding in shell tools
- Never rely on system default encoding — explicit UTF-8 is mandatory
- If handling bytes, use `.encode('utf-8')` and `.decode('utf-8')` explicitly

**Pre-flight Validation**
Before appending, validate that the new entry content:
- Does NOT contain single characters separated by spaces (pattern `X X X` is a corruption signal)
- Does NOT have unusual spacing patterns like `* * ` or ` - ` at unusual positions
- If detected, reject the write, report the corruption to the user, and do not append

**Safe String Operations**
- Use string concatenation (e.g., `string_a + string_b`), NEVER use `' '.join(chars)` on character lists
- For multi-line content, use `'\n'.join(lines)` not character-by-character iteration
- Never iterate through strings character-by-character for output generation

**Append-Only Pattern**
- Read the file once at the start (ONLY if validation logic requires it)
- Build the new entry in memory as a complete string
- Append once to disk using shell redirect (`>>`) or file mode `'a'` with a single `.write()` call
- Do NOT read back and rewrite — this prevents cascading corruption from multiple passes

**Post-Write Integrity Check**
- After appending, read the last 5 lines of JOURNAL.md
- Verify newlines are literal `\n` (not escaped or corrupted)
- Verify markdown formatting (`###`, `**`, `-`) is intact and not space-separated
- If corruption detected, alert the user immediately and provide the corrupted content for manual repair

**Error Handling**
- If any validation step fails, do not proceed with the append
- Report exact error to the user with the offending content
- Suggest manual fix or rollback steps if available
