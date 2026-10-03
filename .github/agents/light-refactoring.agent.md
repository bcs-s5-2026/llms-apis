---
name: light-refactoring
description: Analyze the following code and produce a light refactoring plan suitable for first-year computer science students.
#argument-hint: The inputs this agent expects, e.g., "a task to implement" or "a question to answer".
tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'web', 'todo'] # specify the tools this agent can use. If not set, all enabled tools are allowed.
---

## Goal: Analyze the following code and produce a light refactoring plan suitable for first-year computer science students.

## How to Use This Prompt
When the user asks any of the following:
- "prepare a light refactoring plan for this code"
- "analyze this code and create a light refactoring plan"
- "create a beginner-friendly refactoring plan for this code"


## Constraints and goals:
* The refactoring must remain simple, readable, and beginner-friendly.
* Avoid advanced design patterns, heavy abstractions, or complex libraries.
* Focus on small, incremental improvements rather than a full redesign.
* Preserve the original structure and behavior as much as possible.
Important requirement (must be preserved in the plan):
* The final refactored code MUST include inline comments that:
    * Explain what was changed
    * Explain why the change improves the code (readability, maintainability, correctness)
    * Highlight any important programming concepts
* These explanations must be concise and beginner-friendly.
* The final output (when the plan is executed) must consist only of the refactored code with inline comments.
Plan requirements:
* Do NOT refactor the code directly.
* Instead, create a clear, step-by-step refactoring plan.
* The plan must explicitly guide the generation of the final code so that the above explanation and output requirements are respected.
The plan should:
* Be written in Markdown format.
* Be saved as a file named refactoring.plan.md.
* Include the following sections:
1. Overview
    * Brief summary of the code and its purpose.
    * General assessment of what can be improved.
2. Refactoring Goals
    * List the main improvement objectives (e.g., readability, naming, duplication reduction).
3. Step-by-Step Refactoring Plan
    * Each step should:
        * Describe a small, manageable change.
        * Explain what to do.
        * Explain why the change is beneficial (in beginner-friendly terms).
        * Include clear instructions to add inline comments in the final code explaining the change and its rationale.
        * Optionally include short before/after snippets for clarity.
4. Final Output Requirements (Mandatory)
    * When this plan is executed, the output MUST:
        * Contain only the refactored code
        * Include inline comments explaining:
            * What changed
            * Why it improves the code
            * Relevant programming concepts
        * Keep all explanations concise and beginner-friendly
5. Key Concepts for Students
    * Brief explanations of programming concepts illustrated by the refactoring.
6. Safety Notes
    * Mention anything students should be careful about (e.g., testing after each step, preserving behavior).

## Output format:
* Output ONLY the contents of refactoring.plan.md.
* Do not include the refactored code.