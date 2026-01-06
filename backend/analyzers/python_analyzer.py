import ast
import re
import requests
import json
from llm.llm_explainer import parse_llm_sections

PYTHON_BUILTINS = {"print", "range", "len", "int", "str", "list", "dict"}

def static_python_errors(code: str):
    errors = []
    lines = code.splitlines()
    defined_vars = set()

    try:
        ast.parse(code)
    except SyntaxError as e:
        errors.append(
            f"Line {e.lineno}: {e.text.rstrip()}\n"
            f"       ^^^ Error: {e.msg}"
        )

    for line in lines:
        m = re.match(r"\s*(\w+)\s*=", line)
        if m:
            defined_vars.add(m.group(1))

    for i, line in enumerate(lines):
        if re.search(r"\bfor\s*\(\s*int\b", line):
            errors.append(f"Line {i+1}: C-style for loop not allowed")

        if re.search(r"print\((\w+)\)", line):
            var = re.search(r"print\((\w+)\)", line).group(1)
            if var not in defined_vars and var not in PYTHON_BUILTINS:
                errors.append(f"Line {i+1}: name '{var}' is not defined")

    return list(dict.fromkeys(errors))


def review_with_llm(code: str):
    errors = static_python_errors(code)

    if not errors:
        return {
            "errors": [],
            "warnings": [],
            "hint": "No errors found. Your code is correct.",
            "solution": "",
            "additional_tips": ""
        }

    error_block = "\n".join(errors)

    prompt = f"""
Fix the Python code below.
Return ONLY corrected Python code.

Errors:
{error_block}

Code:
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
        "errors": [{"line": 0, "message": e, "severity": "ERROR", "code": "PY001"} for e in errors],
        "warnings": [],
        "hint": "Fix the Python syntax errors shown above.",
        "solution": fixed_code,
        "additional_tips": "- Use proper indentation\n- Define variables before use"
    }
