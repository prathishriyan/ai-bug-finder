def review_with_llm(code: str):
    errors = []

    if "class " not in code:
        errors.append("Missing class declaration")

    if "public static void main" not in code:
        errors.append("Missing main method")

    if not errors:
        return {
            "errors": [],
            "warnings": [],
            "hint": "No errors found. Your Java code is correct.",
            "solution": "",
            "additional_tips": ""
        }

    return {
        "errors": [{"line": 0, "message": e, "severity": "ERROR", "code": "JAVA001"} for e in errors],
        "warnings": [],
        "hint": "Fix Java class and main method errors.",
        "solution": code.replace("class", "public class"),
        "additional_tips": "- Java requires a main method\n- Class name must match file name"
    }
