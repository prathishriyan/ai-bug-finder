import re
import requests
import json
from llm.llm_explainer import parse_llm_sections

# ======================================================
# DEFINITE ERRORS
# ======================================================

def static_c_errors(code: str):
    errors = []
    lines = code.splitlines()

    if "main(" not in code:
        errors.append("Error: C program must contain main() function")

    if "printf(" in code and "#include <stdio.h>" not in code:
        errors.append("Error: Missing #include <stdio.h>")

    for i, line in enumerate(lines):
        stripped = line.strip()

        # print instead of printf
        if stripped.startswith("print("):
            errors.append(
                f"Line {i+1}: {line}\n"
                f"       ^^^ Error: 'print' is not valid in C (use printf)"
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

def possible_c_issues(code: str):
    issues = []
    lines = code.splitlines()

    for i, line in enumerate(lines):
        # Unsafe functions
        if re.search(r"\bgets\(", line):
            issues.append(
                f"Line {i+1}: 'gets()' is unsafe; use fgets() instead"
            )

        # Uninitialized variables
        if re.search(r"\bint\s+\w+;\b", line):
            issues.append(
                f"Line {i+1}: Variable declared but not initialized"
            )

    return issues


# ======================================================
# LLM EXPLANATION
# ======================================================

def review_with_llm(code: str):
    definite = static_c_errors(code)
    possible = possible_c_issues(code)

    if not definite:
        return {
            "error": "No definite errors found.",
            "hint": "Your C code is structurally correct.",
            "solution": code,
            "additional_tips": "- Follow C best practices.",
            "possible_issues": "\n".join(possible) if possible else ""
        }

    error_block = "\n".join(definite)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi",
            "prompt": f"""
You are a senior C programming instructor.

Errors:
{error_block}

TASK:
Explain fixes and provide corrected C code.
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
