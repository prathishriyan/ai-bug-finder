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
