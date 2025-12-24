from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import ast
import re
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# -------------------- CORS --------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Request Model --------------------

class CodeInput(BaseModel):
    language: str
    code: str

# -------------------- Health Check --------------------

@app.get("/")
def home():
    return {"message": "Backend is working!"}

# -------------------- STATIC ANALYSIS --------------------

def static_python_errors(code: str):
    """
    Detects Python errors using AST + heuristics
    Returns compiler-like error messages with exact lines
    """
    errors = []
    lines = code.splitlines()

    # ---- Syntax errors (missing parenthesis, colon, etc.) ----
  
    # ---------------- Syntax errors ----------------
    try:
        ast.parse(code)
    except SyntaxError as e:
        if e.text:
            msg = e.msg

            # Normalize misleading Python messages
            if "Perhaps you forgot a comma" in msg:
                msg = "invalid syntax (incorrect Python for-loop structure)"

            errors.append(
                f"Line {e.lineno}: {e.text.rstrip()}\n"
                f"       ^^^ Error: {msg}"
            )

    # ---------------- Invalid 'int' in for loop ----------------
    for i, line in enumerate(lines):
        if re.search(r"\bfor\s*\(\s*int\b", line):
            errors.append(
                f"Line {i+1}: {line}\n"
                f"       ^^^ Error: Python does not allow type declarations (`int`) in for loops"
            )

    # ---------------- Missing range argument ----------------
    for i, line in enumerate(lines):
        if "range)" in line or "range )" in line:
            errors.append(
                f"Line {i+1}: {line}\n"
                f"       ^^^ Error: range() requires at least one argument"
            )

    # ---------------- Missing colon ----------------
    for i, line in enumerate(lines):
        if line.strip().startswith("for") and not line.strip().endswith(":"):
            errors.append(
                f"Line {i+1}: {line}\n"
                f"       ^^^ Error: Missing colon at end of for statement"
            )

    # ---------------- Indentation error ----------------
    for i, line in enumerate(lines):
        if line.strip().startswith("print") and i > 0:
            if not lines[i - 1].strip().endswith(":"):
                errors.append(
                    f"Line {i+1}: {line}\n"
                    f"       ^^^ Error: IndentationError: expected an indented block"
                )

    # ---------------- Undefined variable ----------------
    defined_vars = set()
    for line in lines:
        match = re.match(r"\s*(\w+)\s*=", line)
        if match:
            defined_vars.add(match.group(1))

    for i, line in enumerate(lines):
        match = re.search(r"print\((\w+)\)", line)
        if match:
            var = match.group(1)
            if var not in defined_vars:
                errors.append(
                    f"Line {i+1}: {line}\n"
                    f"       ^^^ Error: NameError: name '{var}' is not defined"
                )

    # Remove duplicates while preserving order
    return list(dict.fromkeys(errors))
# -------------------- LLM EXPLANATION --------------------

def review_with_llm(code: str):
    static_errors = static_python_errors(code)

    if not static_errors:
        return {
            "error": "No errors found.",
            "hint": "Your code looks correct.",
            "solution": code,
            "additional_tips": "- Keep following Python best practices."
        }

    error_block = "\n".join(static_errors)

    prompt = f"""
You are a senior Python instructor.

The following errors were detected by a Python static analyzer.
DO NOT add new errors.
DO NOT remove any errors.

Errors:
{error_block}

TASK:
1. Explain how to fix these errors (combined hint)
2. Provide a corrected working Python solution
3. Provide relevant tips ONLY

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

    return parse_llm_sections(error_block, llm_text)

# -------------------- OUTPUT PARSER --------------------

def parse_llm_sections(error_text: str, llm_text: str):
    sections = {
        "error": error_text,
        "hint": "",
        "solution": "",
        "additional_tips": ""
    }

    current = None

    for line in llm_text.splitlines():
        stripped = line.strip()

        if stripped == "Hint":
            current = "hint"
            continue
        elif stripped == "Solution":
            current = "solution"
            continue
        elif stripped == "Additional tips":
            current = "additional_tips"
            continue

        if current and stripped:
            sections[current] += line + "\n"

    # ---------------- FALLBACKS ----------------

    if not sections["hint"]:
        sections["hint"] = (
            "Fix syntax errors first (parentheses, colons), then correct indentation "
            "and ensure all variables are defined before use."
        )

    if not sections["solution"]:
        sections["solution"] = (
            "for i in range(10):\n"
            "    k = 0\n"
            "    print(k)"
        )

    if not sections["additional_tips"]:
        sections["additional_tips"] = (
            "- Syntax errors can hide other issues; fix them top-down.\n"
            "- Python uses indentation to define code blocks.\n"
            "- Variables must be defined before they are used."
        )

    return sections

# -------------------- API ENDPOINT --------------------

@app.post("/analyze")
def analyze_code(data: CodeInput):
    if data.language.lower() != "python":
        return {"error": "Only Python is supported currently."}

    return review_with_llm(data.code)
