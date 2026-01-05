# 🪲 AI Bug Finder

AI Bug Finder is a **multi-language static code analysis tool** with an IDE-like interface that helps identify syntax errors, logical issues, and **language mismatches** in source code.

---

## ✨ Key Features

- Supports **Python, JavaScript, Java, C, and C++**
- **Language mismatch detection** (prevents incorrect analysis)
- **Each language remembers its own content**
- File upload support (`.py`, `.js`, `.java`, `.c`, `.cpp`, `.txt`)
- AI-powered error explanations, hints, and solutions
- IDE-like experience using Monaco Editor (VS Code engine)

---

## 🏗️ Tech Stack

### Frontend
- React
- Monaco Editor
- CSS (custom UI)

### Backend
- FastAPI (Python)
- Language-specific analyzers
- Signature-based language detection
- Ollama (LLM for explanations)

---

## 📂 Project Structure

```text
ai-bug-finder/
│
├── backend/
│   ├── main.py
│   ├── router.py
│   ├── language_detector.py
│   ├── models.py
│   └── analyzers/
│       ├── python_analyzer.py
│       ├── javascript_analyzer.py
│       ├── java_analyzer.py
│       └── c_analyzer.py
│
├── frontend/
│   └── src/
│       ├── App.js
│       ├── App.css
│       └── index.js
│
└── README.md

## 🔍 How It Works

1. User selects a programming language
2. User types or uploads source code
3. System detects the **actual language** using signature-based rules
4. If the language does not match:
   - Analysis stops
   - User is prompted to select the correct language
5. If the language matches:
   - Static analyzer runs
   - AI generates errors, hints, and suggested fixes

---

## ⚠️ Example: Language Mismatch Detection

**Input Code (C++):**
```cpp
#include<iostream>
using namespace std;
cout << "Hello";

Selected Language: Python

output:
❌ Error (LANG001)
This code appears to be CPP code, not PYTHON.

💡 Hint
Please select the correct language (CPP) before analysis.

## 🎯 Design Decisions

1.Monaco Editor is used in uncontrolled mode to prevent editor resets
2.Language validation is enforced before analysis
3.Each language has its own dedicated analyzer
4.Generic or misleading fixes are avoided
5.UX inspired by real IDEs such as VS Code

## 🚀 Future Enhancements

