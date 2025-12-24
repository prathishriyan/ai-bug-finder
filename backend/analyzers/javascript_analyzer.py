import re
import requests
import json
from llm.llm_explainer import parse_llm_sections

# ======================================================
# DEFINITE ERRORS
# ======================================================

def static_javascript_errors(code: str):
    errors = []
    lines = code.splitlines()

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Typed variables (C/Java style)
        if re.search(r"\b(int|float|double)\b", line):
            errors.append(
                f"Line {i+1}: {line}\n"
                f"       ^^^ Error: JavaScript does not support typed variable declarations"
            )

        # print() instead of console.log()
        if stripped.startswith("print("):
            errors.append(
                f"Line {i+1}: {line}\n"
                f"       ^^^ Error: Use console.log() instead of print()"
            )

        # Missing ); in console.log
        if "console.log(" in line and not stripped.endswith(");"):
            errors.append(
                f"Line {i+1}: {line}\n"
                f"       ^^^ Error: Missing closing parenthesis or semicolon"
            )

    return errors


# ======================================================
# POSSIBLE ISSUES
# ======================================================

def possible_javascript_issues(code: str):
    issues = []
    lines = code.splitlines()

    for i, line in enumerate(lines):
        # Using var
        if re.search(r"\bvar\b", line):
            issues.append(
                f"Line {i+1}: Prefer 'let' or 'const' instead of 'var'"
            )

        # == instead of ===
        if "==" in line and "===" not in line:
            issues.append(
                f"Line {i+1}: Use '===' instead of '==' for comparison"
            )

    return issues


# ======================================================
# LLM EXPLANATION
# ======================================================

def review_with_llm(code: str):
    definite = static_javascript_errors(code)
    possible = possible_javascript_issues(code)

    if not definite:
        return {
            "error": "No definite errors found.",
            "hint": "Your JavaScript code is syntactically correct.",
            "solution": code,
            "additional_tips": "- Follow JavaScript best practices.",
            "possible_issues": "\n".join(possible) if possible else ""
        }

    error_block = "\n".join(definite)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi",
            "prompt": f"""
You are a senior JavaScript instructor.

Errors:
{error_block}

TASK:
Explain fixes and provide corrected JavaScript code.

FORMAT:
Hint
Solution
Additional tips
""",
            "options": {"temperature": 0}
        },
        stream=True
    )

    llm_text = ""
    for line in response.iter_lines():
        if line:
            llm_text += json.loads(line.decode()).get("response", "")

    result = parse_llm_sections(error_block, llm_text)
    result["possible_issues"] = "\n".join(possible)

    return result
