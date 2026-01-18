import requests
import json
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")


def static_cpp_errors(code: str):
    errors = []

    # Require main()
    if "main(" not in code:
        errors.append("Missing main() function")

    # Require iostream if using namespace std
    if "using namespace std" in code and "#include<iostream>" not in code:
        errors.append("Missing #include <iostream>")

    # Basic missing semicolon check
    for i, line in enumerate(code.splitlines()):
        stripped = line.strip()
        if stripped and not stripped.endswith(";") and not stripped.endswith("{") and not stripped.endswith("}") and not stripped.startswith("#"):
            errors.append(f"Line {i+1}: Missing semicolon")

    # Check braces balance
    if code.count("{") != code.count("}"):
        errors.append("Mismatched braces")

    return errors


def review_with_llm(code: str):
    errors = static_cpp_errors(code)

    if not errors:
        return {
            "errors": [],
            "warnings": [],
            "hint": "No errors found. Your C++ code is correct.",
            "solution": "",
            "additional_tips": ""
        }
    error_block = "\n".join(errors)
    prompt = f"""
Act as a senior C++ compiler expert.

Your job is to fix ONLY syntax errors.

STRICT RULES:
- Do NOT modify logic
- Do NOT add comments
- Do NOT create new code
- Do NOT optimize
- Only correct syntax mistakes
- Return ONLY valid C++ code

Errors:
{error_block}

Code:
{code}

Return ONLY corrected C++ code.
"""

    # Call Ollama safely
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": "phi3:latest", "prompt": prompt, "options": {"temperature": 0}},
        stream=True
    )

    fixed_code = ""

    # SAFE STREAM PROCESSING
    for line in response.iter_lines():
        if not line:
            continue

        data = json.loads(line.decode())

        # Normal model output
        if "response" in data:
            fixed_code += data["response"]

        # Handle Ollama error
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

    # Final response structure
    return {
        "errors": [{"line": 0, "message": e, "severity": "ERROR", "code": "CPP001"} for e in errors],
        "warnings": [],
        "hint": "Fix the C++ syntax issues shown above.",
        "solution": fixed_code.strip(),
        "additional_tips": "- Include correct headers\n- Ensure proper semicolons and braces"
    }
