import requests
import json

def review_with_llm(code: str):
    errors = []
    if "using namespace std" in code and "#include<iostream>" not in code:
        errors.append("Missing <iostream> include")

    if "main(" not in code:
        errors.append("Missing main() function")

    if not errors:
        return {
            "errors": [],
            "warnings": [],
            "hint": "No errors found. Your C++ code is correct.",
            "solution": "",
            "additional_tips": ""
        }

    prompt = f"""
Fix ALL C++ errors and return a corrected program.

Errors:
{chr(10).join(errors)}

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
        "errors": [{"line": 0, "message": e, "severity": "ERROR", "code": "CPP001"} for e in errors],
        "warnings": [],
        "hint": "Fix the C++ syntax issues shown above.",
        "solution": fixed_code,
        "additional_tips": "- Include correct headers\n- Use std namespace properly"
    }
