import re
import requests
import json
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

def static_c_errors(code: str):
    errors = []
    lines = code.splitlines()

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("#") or stripped.startswith("//") or stripped == "":
            continue

        if (
            not stripped.endswith(";")
            and not stripped.endswith("{")
            and not stripped.endswith("}")
        ):
            errors.append(f"Line {i+1}: Missing semicolon")

    if code.count("{") != code.count("}"):
        errors.append("Mismatched braces")

    return errors


def review_with_llm(code: str):
    errors = static_c_errors(code)

    if not errors:
        return {
            "errors": [],
            "warnings": [],
            "hint": "No errors detected.",
            "solution": "",
            "additional_tips": ""
        }
    error_block = "\n".join(errors)

    prompt = f"""
Act as a senior C compiler expert.

Your task is to fix ONLY syntax errors in the C code.

STRICT RULES:
- Do NOT add new logic
- Do NOT change variable names
- Do NOT add comments
- Do NOT rewrite or refactor
- Do NOT remove includes
- Only fix missing semicolons, braces, parentheses
- Return ONLY corrected C code

Errors:
{error_block}

Code:
{code}

Return only corrected C code with NO explanations.
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": "phi3:latest", "prompt": prompt},
        stream=True
    )

    fixed_code = ""

    for line in response.iter_lines():
        if not line:
            continue

        data = json.loads(line.decode())

        # ignore metadata
        if "response" in data:
            fixed_code += data["response"]

    # Strip out hallucinated junk
    fixed_code = fixed_code.replace("end", "0")
    fixed_code = fixed_code.replace("return end", "return 0;")

    return {
        "errors": [{"line": 0, "message": e, "severity": "ERROR", "code": "C001"} for e in errors],
        "warnings": [],
        "hint": "Correct the syntax errors shown above.",
        "solution": fixed_code.strip(),
        "additional_tips": "- End statements with ;\n- Ensure braces match"
    }
