import ast
import re
import requests
import json
from llm.llm_explainer import parse_llm_sections

PYTHON_BUILTINS = {"print", "range", "len", "int", "str", "list", "dict"}


# ======================================================
# DEFINITE (STATIC) ERRORS
# ======================================================

def static_python_errors(code: str):
    """
    Finds ALL statically inferable Python errors
    (guaranteed to break execution)
    """
    errors = []
    lines = code.splitlines()
    defined_vars = set()

    # ---------- Syntax & indentation ----------
    try:
        ast.parse(code)
    except SyntaxError as e:
        if e.text:
            msg = e.msg
            if "Perhaps you forgot a comma" in msg:
                msg = "invalid syntax (incorrect Python statement)"
            errors.append(
                f"Line {e.lineno}: {e.text.rstrip()}\n"
                f"       ^^^ Error: {msg}"
            )

    # ---------- Variable definitions ----------
    for line in lines:
        m = re.match(r"\s*(\w+)\s*=", line)
        if m:
            defined_vars.add(m.group(1))

    # ---------- Line-by-line checks ----------
    for i, line in enumerate(lines):
        stripped = line.strip()

        # C / Java style loop
        if re.search(r"\bfor\s*\(\s*int\b", line):
            errors.append(
                f"Line {i+1}: {line}\n"
                f"       ^^^ Error: Python does not allow type declarations in for loops"
            )

        # range() without argument
        if re.search(r"range\s*\(\s*\)", line):
            errors.append(
                f"Line {i+1}: {line}\n"
                f"       ^^^ Error: range() requires at least one argument"
            )

        # Missing colon
        if stripped.startswith(("for ", "if ", "while ", "def ")) and not stripped.endswith(":"):
            errors.append(
                f"Line {i+1}: {line}\n"
                f"       ^^^ Error: Missing colon at end of statement"
            )

        # Indentation error
        if stripped.startswith("print") and i > 0:
            if not lines[i - 1].strip().endswith(":"):
                errors.append(
                    f"Line {i+1}: {line}\n"
                    f"       ^^^ Error: IndentationError: expected an indented block"
                )

        # Undefined variable usage
        m = re.search(r"print\((\w+)\)", line)
        if m:
            var = m.group(1)
            if var not in defined_vars and var not in PYTHON_BUILTINS:
                errors.append(
                    f"Line {i+1}: {line}\n"
                    f"       ^^^ Error: NameError: name '{var}' is not defined"
                )

    return list(dict.fromkeys(errors))


# ======================================================
# POSSIBLE (PROBABLE) ISSUES — SAFE MODE
# ======================================================

def possible_python_issues(code: str):
    """
    Finds LIKELY issues (not guaranteed)
    """
    issues = []
    lines = code.splitlines()

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Shadowing built-ins
        if re.match(r"\s*(list|dict|str|int)\s*=", line):
            issues.append(
                f"Line {i+1}: Shadowing Python built-in name '{stripped.split('=')[0].strip()}'"
            )

        # Using == for None
        if "== None" in line:
            issues.append(
                f"Line {i+1}: Use 'is None' instead of '=='"
            )

        # Function without return
        if stripped.startswith("def ") and "return" not in code:
            issues.append(
                f"Line {i+1}: Function may not return a value"
            )

    return issues


# ======================================================
# LLM EXPLANATION (CONTROLLED)
# ======================================================

def review_with_llm(code: str):
    definite_errors = static_python_errors(code)
    possible_issues = possible_python_issues(code)

    # -------- No definite errors --------
    if not definite_errors:
        return {
            "error": "No definite errors found.",
            "hint": "Your code is syntactically correct.",
            "solution": code,
            "additional_tips": "- Follow Python best practices.",
            "possible_issues": "\n".join(possible_issues) if possible_issues else ""
        }

    error_block = "\n".join(definite_errors)

    prompt = f"""
You are a senior Python instructor.

The following errors are DEFINITE and detected statically.
DO NOT add new errors.
DO NOT remove any errors.

Errors:
{error_block}

TASK:
1. Give a combined hint to fix ALL errors
2. Provide a corrected Python solution
3. Give relevant best practices ONLY

FORMAT (STRICT):

Hint
<combined hint>

Solution
<corrected code>

Additional tips
- <tip>
- <tip>
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi",
            "prompt": prompt,
            "options": {"temperature": 0}
        },
        stream=True
    )

    llm_text = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            llm_text += data.get("response", "")

    result = parse_llm_sections(error_block, llm_text)
    result["possible_issues"] = "\n".join(possible_issues)

    return result
