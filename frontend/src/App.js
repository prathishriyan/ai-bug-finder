import React, { useRef, useState } from "react";
import Editor from "@monaco-editor/react";
import "./App.css";

/* ---------------- Language Config ---------------- */

const LANGUAGES = [
  { key: "python", label: "Python" },
  { key: "javascript", label: "JavaScript" },
  { key: "java", label: "Java" },
  { key: "c", label: "C" },
  { key: "cpp", label: "C++" },
];

const DEFAULT_CODE = {
  python: "# Write Python code here\n",
  javascript: "// Write JavaScript code here\n",
  java: "// Write Java code here\n",
  c: "// Write C code here\n",
  cpp: "// Write C++ code here\n",
};

function App() {
  const editorRef = useRef(null);

  const [language, setLanguage] = useState("python");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState("");

  const [codeByLanguage, setCodeByLanguage] = useState({
    python: "",
    javascript: "",
    java: "",
    c: "",
    cpp: "",
  });

  /* ---------------- Editor Mount ---------------- */

  function handleEditorDidMount(editor) {
    editorRef.current = editor;
    editor.setValue(DEFAULT_CODE[language]);
  }

  /* ---------------- File Load ---------------- */

  const loadFileToEditor = (file) => {
    if (!file) return;

    setFileName(file.name);

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target.result;

      setCodeByLanguage((prev) => ({
        ...prev,
        [language]: content,
      }));

      editorRef.current?.setValue(content);
    };

    reader.readAsText(file);
  };

  const handleFileUpload = (e) => {
    loadFileToEditor(e.target.files[0]);
    e.target.value = "";
  };

  /* ---------------- Drag & Drop ---------------- */

  const handleDrop = (e) => {
    e.preventDefault();
    loadFileToEditor(e.dataTransfer.files[0]);
  };

  const handleDragOver = (e) => e.preventDefault();

  /* ---------------- Analyze ---------------- */

  const handleAnalyze = async () => {
    setLoading(true);

    const code = editorRef.current?.getValue() || "";

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language, code }),
      });

      const data = await response.json();
      setAnalysisResult(data);
    } catch (err) {
      setAnalysisResult({
        errors: [
          {
            line: 0,
            message: err.message,
            severity: "ERROR",
            code: "NET001",
          },
        ],
        warnings: [],
      });
    }

    setLoading(false);
  };

  /* ---------------- UI ---------------- */

  return (
    <div className="container">
      <h1 className="title">🪲 AI Bug Finder</h1>

      {/* -------- Language Tabs -------- */}
      <div className="language-tabs">
        {LANGUAGES.map((lang) => (
          <div
            key={lang.key}
            className={`language-tab ${
              language === lang.key ? "active" : ""
            }`}
            onClick={() => {
              if (editorRef.current) {
                setCodeByLanguage((prev) => ({
                  ...prev,
                  [language]: editorRef.current.getValue(),
                }));
              }

              setLanguage(lang.key);

              setTimeout(() => {
                editorRef.current?.setValue(
                  codeByLanguage[lang.key] || DEFAULT_CODE[lang.key]
                );
              }, 0);
            }}
          >
            {lang.label}
          </div>
        ))}
      </div>

      {/* -------- Drop Zone -------- */}
      <div className="drop-zone" onDrop={handleDrop} onDragOver={handleDragOver}>
        <div className="drop-content">
          <span className="drop-icon">📂</span>
          <p className="drop-text">
            Drag & drop a file here <span>or</span>
          </p>

          <label className="file-button">
            Browse files
            <input
              type="file"
              accept=".py,.js,.java,.c,.cpp,.txt"
              hidden
              onChange={handleFileUpload}
            />
          </label>

          {fileName && <div className="file-name">📄 {fileName}</div>}
        </div>
      </div>

      {/* -------- Editor -------- */}
      <Editor
        height="50vh"
        language={language}
        theme="vs-dark"
        onMount={handleEditorDidMount}
      />

      {/* -------- Analyze -------- */}
      <button className="analyze-btn" onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {/* -------- Results -------- */}
      {analysisResult && (
  <div className="results">
    {analysisResult.errors?.length > 0 && (
      <div className="result-block error">
        <h3>❌ Errors</h3>
        <pre>
          {analysisResult.errors
            .map(
              (e) => `Line ${e.line}: ${e.message} (${e.code})`
            )
            .join("\n")}
        </pre>
      </div>
    )}

    {analysisResult.warnings?.length > 0 && (
      <div className="result-block hint">
        <h3>⚠️ Warnings</h3>
        <pre>
          {analysisResult.warnings
            .map(
              (w) => `Line ${w.line}: ${w.message} (${w.code})`
            )
            .join("\n")}
        </pre>
      </div>
    )}

    {analysisResult.hint && (
      <div className="result-block hint">
        <h3>💡 Hint</h3>
        <p>{analysisResult.hint}</p>
      </div>
    )}

    {analysisResult.solution && (
      <div className="result-block solution">
        <h3>✅ Solution</h3>
        <pre>
    {analysisResult.solution
      ? analysisResult.solution
      : "No auto-fix available. Resolve the errors above first."}
  </pre>
      </div>
    )}

    {analysisResult.additional_tips && (
      <div className="result-block tips">
        <h3>📌 Additional Tips</h3>
        <pre>{analysisResult.additional_tips}</pre>
      </div>
    )}
  </div>
)}

    </div>
  );
}

export default App;
