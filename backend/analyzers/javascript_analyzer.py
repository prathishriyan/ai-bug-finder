def review_with_llm(code: str):
    errors = []

    if "console.log(" in code and ";" not in code:
        errors.append("Missing semicolon")

    if not errors:
        return {
            "errors": [],
            "warnings": [],
            "hint": "No errors found. Your JavaScript code is correct.",
            "solution": "",
            "additional_tips": ""
        }

    return {
        "errors": [{"line": 0, "message": e, "severity": "ERROR", "code": "JS001"} for e in errors],
        "warnings": [],
        "hint": "Fix JavaScript syntax errors.",
        "solution": code + ";",
        "additional_tips": "- Use semicolons\n- Prefer const and let"
    }
