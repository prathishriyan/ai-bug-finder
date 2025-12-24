import re
import requests
import json
from llm.llm_explainer import parse_llm_sections

# ======================================================
# DEFINITE ERRORS
# ======================================================

def static_java_errors(code: str):
    errors = []
    lines = code.splitlines()

    if "class" not in code:
        errors.append("Error: Java program must be inside a class")

    if "main(" not in code:
        errors.append("Error: Java program must contain a main() method")

    for i, line in enumerate(lines):
        stripped = line.strip()

        # print instead of System.out.println
        if "print(" in line:
            errors.append(
                f"Line {i+1}: {line}\n"
                f"       ^^^ Error: Use System.out.println() in Java"
            )

        # Missing semicolon
        if (
            stripped.endswith(")")
            and not stripped.endswith(");")
            and not stripped.startswith(("if", "for", "while"))
        ):
            errors.append(
                f"Line {i+1}: {line}\n"
                f"       ^^^ Error: Missing semicolon"
            )

    return errors


# ======================================================
# POSSIBLE ISSUES
# ======================================================

def possible_java_issues(code: str):
    issues = []
    lines = code.splitlines()

    for i, line in enumerate(lines):
        # Magic numbers
        if re.search(r"\b\d+\b", line) and "for" not in line:
            issues.append(
                f"Line {i+1}: Consider replacing magic numbers with constants"
            )

        # Empty catch block
        if "catch" in line and "{}" in line:
            issues.append(
                f"Line {i+1}: Empty catch block may hide exceptions"
            )

    return issues


# ======================================================
# LLM EXPLANATION
# ======================================================

def review_with_llm(code: str):
    definite = static_java_errors(code)
    possible = possible_java_issues(code)

    if not definite:
        return {
            "error": "No definite errors found.",
            "hint": "Your Java code is structurally correct.",
            "solution": code,
            "additional_tips": "- Follow Java coding standards.",
            "possible_issues": "\n".join(possible) if possible else ""
        }

    error_block = "\n".join(definite)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi",
            "prompt": f"""
You are a senior Java instructor.

Errors:
{error_block}

TASK:
Explain fixes and provide corrected Java code.
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
