def detect_language(code: str):
    code_lower = code.lower()

    # ---- C++ ----
    if (
        "#include<iostream>" in code_lower
        or "#include <iostream>" in code_lower
        or "using namespace std" in code_lower
        or "cout <<" in code_lower
        or "cin >>" in code_lower
    ):
        return "cpp"

    # ---- Java ----
    if (
        "public class" in code_lower
        or "system.out.println" in code_lower
        or "import java." in code_lower
    ):
        return "java"

    # ---- C ----
    if (
        "#include<stdio.h>" in code_lower
        or "#include <stdio.h>" in code_lower
        or "printf(" in code_lower
        or "scanf(" in code_lower
    ):
        return "c"

    # ---- JavaScript ----
    if (
        "console.log(" in code_lower
        or "function " in code_lower
        or "=>" in code_lower
        or "let " in code_lower
        or "const " in code_lower
        or "var " in code_lower
    ):
        return "javascript"

    # ---- Python (LAST) ----
    if (
        "def " in code_lower
        or "import " in code_lower
        or ("print(" in code_lower and "console.log" not in code_lower)
    ):
        return "python"

    return "unknown"
