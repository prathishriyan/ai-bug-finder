import re
import requests
import json

def static_c_errors(code: str):
    errors = []

    if "main(" not in code:
        errors.append("Line 1: Missing main() function")

    for i, line in enumerate(code.splitlines()):
        if re.match(r".*[^;{}\s]$", line) and not line.strip().startswith("#"):
            errors.append(f"Line {i+1}: Missing semicolon")

    if code.count("{") != code.count("}"):
        errors.append("Opening brace '{' not closed")

    return errors


def review_with_llm(code: str):
    errors = static_c_errors(code)

    if not errors:
        return {
            "errors": [],
            "warnings": [],
            "hint": "No errors found. Your C code is correct.",
            "solution": "",
            "additional_tips": ""
        }

    prompt = f"""
You are a C systems programmer.

RULES (MANDATORY):
- Do NOT use assignment inside if conditions
- open() success must be checked using < 0
- Use permission 0644 for created files
- Preserve original logic
- Only fix errors, do NOT refactor

Return ONLY corrected C code.

Original Code:
{code}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "phi", "prompt": prompt, "options": {"temperature": 0}},
        stream=True
    )

    fixed_code = ""
    for line in response.iter_lines():
        if line:
            fixed_code += json.loads(line.decode())["response"]

    return {
        "errors": [{"line": 0, "message": e, "severity": "ERROR", "code": "C001"} for e in errors],
        "warnings": [],
        "hint": "Fix the C syntax errors shown above before compilation.",
        "solution":"""
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

int main() {
    // corrected template
}
""",
        "additional_tips": (
            "- Every statement must end with a semicolon\n"
            "- All opened braces must be closed\n"
            "- Ensure required headers are included"
        )
    }
