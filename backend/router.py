from analyzers.python_analyzer import review_with_llm as analyze_python
from analyzers.javascript_analyzer import review_with_llm as analyze_javascript
from analyzers.java_analyzer import review_with_llm as analyze_java
from analyzers.c_analyzer import review_with_llm as analyze_c
from analyzers.cpp_analyzer import review_with_llm as analyze_cpp
from language_detector import detect_language


def analyze_by_language(language: str, code: str):
    selected = language.lower()
    detected = detect_language(code)

    # 🔴 HARD STOP: language mismatch
    if detected != "unknown" and detected != selected:
        return {
            "errors": [
                {
                    "line": 1,
                    "message": f"This code appears to be {detected.upper()} code, not {selected.upper()}",
                    "severity": "ERROR",
                    "code": "LANG001"
                }
            ],
            "warnings": [],
            "hint": f"Please select the correct language ({detected.upper()}) before analysis.",
            "solution": "",
            "additional_tips": ""
        }

    # ✅ Correct routing
    if selected == "python":
        return analyze_python(code)
    elif selected == "javascript":
        return analyze_javascript(code)
    elif selected == "java":
        return analyze_java(code)
    elif selected == "c":
        return analyze_c(code)
    elif selected == "cpp":
        return analyze_cpp(code)
    else:
        return {
            "errors": [
                {
                    "line": 1,
                    "message": f"Unsupported language selected: {selected}",
                    "severity": "ERROR",
                    "code": "LANG002"
                }
            ],
            "warnings": [],
            "hint": "",
            "solution": "",
            "additional_tips": ""
        }
