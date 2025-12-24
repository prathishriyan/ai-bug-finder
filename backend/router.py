from analyzers.python_analyzer import review_with_llm as analyze_python
from analyzers.javascript_analyzer import review_with_llm as analyze_javascript
from analyzers.java_analyzer import review_with_llm as analyze_java
from analyzers.c_analyzer import review_with_llm as analyze_c

def analyze_by_language(language: str, code: str):
    language = language.lower()

    if language == "python":
        return analyze_python(code)
    elif language == "javascript":
        return analyze_javascript(code)
    elif language == "java":
        return analyze_java(code)
    elif language == "c":
        return analyze_c(code)
    else:
        return {
            "error": f"Unsupported language: {language}",
            "hint": "",
            "solution": "",
            "additional_tips": ""
        }
