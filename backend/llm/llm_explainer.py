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

    # Fallbacks
    if not sections["hint"]:
        sections["hint"] = (
            "Fix syntax errors first, then indentation, and finally variable definitions."
        )

    if not sections["solution"]:
        sections["solution"] = (
            "for i in range(10):\n"
            "    k = 0\n"
            "    print(k)"
        )

    if not sections["additional_tips"]:
        sections["additional_tips"] = (
            "- Syntax errors hide other issues.\n"
            "- Python uses indentation.\n"
            "- Define variables before use."
        )

    return sections
