🪲 AI Bug Finder

AI Bug Finder is a multi-language static code analysis tool with an IDE-like interface that helps users identify syntax errors, logical issues, and language mismatches in source code.
It supports Python, JavaScript, Java, C, and C++, and provides clear errors, hints, and suggested fixes.

🚀 Features

🌐 Multi-language support

Python

JavaScript

Java

C

C++

🧠 Language mismatch detection

Detects when the pasted code does not match the selected language

Prevents misleading error analysis

🧪 Static code analysis

Syntax validation

Common programming mistakes

Language-specific rules

💡 AI-powered explanations

Clear error descriptions

Fix suggestions

Best-practice tips

🖥️ IDE-like experience

Monaco Editor (VS Code editor engine)

Language tabs

Syntax highlighting

📂 File upload support

Upload .py, .js, .java, .c, .cpp, .txt files

File content loads directly into editor

🔁 Per-language code persistence

Switching language tabs does NOT erase code

Each language remembers its own content

🏗️ Tech Stack
Frontend

React

Monaco Editor

CSS (custom UI)

Backend

FastAPI (Python)

Language-specific analyzers

Signature-based language detection

Ollama (LLM for explanations)

📂 Project Structure
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
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│
└── README.md

🔍 How It Works

User selects a programming language

User writes or uploads code

System detects the actual language of the code

If language mismatches → error is shown immediately

If language matches → static analyzer runs

AI generates:

Errors

Hints

Suggested solution

Additional tips

⚠️ Example: Language Mismatch Detection

Input Code (C++):

#include<iostream>
using namespace std;
cout << "Hello";


Selected Language: Python

Output:

❌ Error (LANG001)
This code appears to be CPP code, not PYTHON.

💡 Hint
Please select the correct language (CPP) before analysis.

🧪 Running the Project Locally
Backend (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload


Backend runs at:

http://localhost:9000

Frontend (React)
cd frontend
npm install
npm start


Frontend runs at:

http://localhost:3000

🎯 Key Design Decisions

Monaco Editor is used in uncontrolled mode to avoid state reset issues

Language detection happens before analysis

Each language has a dedicated analyzer

Generic or misleading fixes are avoided

IDE-like UX inspired by VS Code

📌 Future Enhancements

C++ static analyzer

Inline error squiggles in Monaco

Auto language switching based on file extension

LocalStorage support

CI/CD deployment on AWS

User authentication & history
