import re
import requests
import json
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

def static_js_errors(code: str):
    errors = []
    lines = code.splitlines()

    for i, line in enumerate(lines):
        stripped = line.strip()

        # ignore comments
        if stripped.startswith("//") or stripped.startswith("/*"):
            continue

        # missing semicolon check
        if (
            stripped not in ["", "{", "}"]
            and not stripped.endswith(";")
            and not stripped.endswith("{")
            and not stripped.endswith("}")
        ):
            errors.append(f"Line {i+1}: Missing semicolon")

    return errors


def review_with_llm(code: str):
    errors = static_js_errors(code)

    if not errors:
        return {
            "errors": [],
            "warnings": [],
            "hint": "No errors found. Your JavaScript code looks correct.",
            "solution": "",
            "additional_tips": "",
        }
    error_block = "\n".join(errors)
    prompt = f"""
Act as a senior JavaScript engine (V8) expert.

Fix ONLY syntax errors.

STRICT RULES:
- Do NOT modify logic
- Do NOT add comments
- Do NOT create new variables
- Only fix syntax mistakes like semicolons or braces

Errors:
{error_block}

Code:
{code}

Return ONLY corrected JavaScript code.
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": "phi3:latest", "prompt": prompt},
        stream=True
    )

    fixed_code = ""

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode())
            if "response" in data:
                fixed_code += data["response"]

    return {
        "errors": [{"line": 0, "message": e, "severity": "ERROR", "code": "JS001"} for e in errors],
        "warnings": [],
        "hint": "Fix the JavaScript syntax errors shown above.",
        "solution": fixed_code,
        "additional_tips": "- Use semicolons\n- Declare variables before use",
    }
