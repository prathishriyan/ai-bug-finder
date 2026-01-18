import re
import requests
import json
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

def static_java_errors(code: str):
    errors = []
    lines = code.splitlines()

    class_found = any("class " in line for line in lines)
    main_found = any("public static void main" in line for line in lines)

    if not class_found:
        errors.append("Missing class declaration")

    if not main_found:
        errors.append("Missing main method")

    return errors


def review_with_llm(code: str):
    errors = static_java_errors(code)

    if not errors:
        return {
            "errors": [],
            "warnings": [],
            "hint": "No errors found. Your Java code is correct.",
            "solution": "",
            "additional_tips": "",
        }
    error_block = "\n".join(errors)
    prompt = f"""
Act as a senior Java compiler (javac) expert.

Your task is to fix ONLY Java syntax errors.

STRICT RULES:
- Do NOT modify logic
- Do NOT add comments
- Do NOT create new methods
- Do NOT rewrite structure
- Only fix missing semicolons, braces, parentheses

Errors:
{error_block}

Code:
{code}

Return ONLY corrected Java code.

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
        "errors": [{"line": 0, "message": e, "severity": "ERROR", "code": "JAVA001"} for e in errors],
        "warnings": [],
        "hint": "Fix the Java syntax issues shown above.",
        "solution": fixed_code,
        "additional_tips": "- Java class name should match file name\n- main() must be inside a public class",
    }
