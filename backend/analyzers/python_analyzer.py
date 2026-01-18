import ast
import re
import requests
import json
import os

from llm.llm_explainer import parse_llm_sections

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

PYTHON_BUILTINS = {"print", "range", "len", "int", "str", "list", "dict"}


def static_python_errors(code: str):
    errors = []
    lines = code.splitlines()
    defined_vars = set()

    # Syntax errors via AST
    try:
        ast.parse(code)
    except SyntaxError as e:
        errors.append(
            f"Line {e.lineno}: {e.text.rstrip()}\n       ^^^ Error: {e.msg}"
        )

    # Track defined variables
    for line in lines:
        m = re.match(r"\s*(\w+)\s*=", line)
        if m:
            defined_vars.add(m.group(1))

    # Undefined variable check
    for i, line in enumerate(lines):
        m = re.search(r"print\((\w+)\)", line)
        if m:
            var = m.group(1)
            if var not in defined_vars and var not in PYTHON_BUILTINS:
                errors.append(f"Line {i+1}: name '{var}' is not defined")

    return list(dict.fromkeys(errors))


def review_with_llm(code: str):
    errors = static_python_errors(code)

    # No issues → return clean
    if not errors:
        return {
            "errors": [],
            "warnings": [],
            "hint": "No errors found. Your code is correct.",
            "solution": "",
            "additional_tips": ""
        }

    # Build error prompt for LLM
    error_block = "\n".join(errors)

    prompt = f"""
Act as a senior Python compiler and interpreter expert.

Your only job is to fix syntax errors in the following Python code.

STRICT RULES:
- Fix ONLY syntax errors
- Do NOT add comments
- Do NOT explain anything
- Do NOT change variable names
- Do NOT change logic
- Do NOT add missing functions
- Do NOT add imports
- Do NOT optimize or refactor
- Do NOT rewrite the code differently
- Do NOT add print statements
- Do NOT add new lines unless required for syntax
- Return ONLY valid corrected Python code with no explanations

Here are the detected errors:
{error_block}

Correct this code:
{code}

Return ONLY the corrected Python code, with no other text.
"""

    # Send to Ollama
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": "phi3:latest", "prompt": prompt, "options": {"temperature": 0}},
        stream=True
    )

    fixed_code = ""

    # SAFE STREAMING
    for line in response.iter_lines():
        if not line:
            continue

        data = json.loads(line.decode())

        # Normal response
        if "response" in data:
            fixed_code += data["response"]

        # Error from Ollama
        if "error" in data:
            return {
                "errors": [
                    {
                        "line": 0,
                        "message": data["error"],
                        "severity": "ERROR",
                        "code": "LLM001"
                    }
                ],
                "warnings": [],
                "hint": "Ollama returned an error.",
                "solution": "",
                "additional_tips": "Run: docker exec -it ollama ollama pull phi3"
            }

    return {
        "errors": [{"line": 0, "message": e, "severity": "ERROR", "code": "PY001"} for e in errors],
        "warnings": [],
        "hint": "Fix the Python syntax errors shown above.",
        "solution": fixed_code,
        "additional_tips": "- Use proper indentation\n- Define variables before use"
    }
