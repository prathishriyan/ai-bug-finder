import React, { useRef, useState } from "react";
import Editor from "@monaco-editor/react";
import "./App.css";

const LANGUAGES = [
  { key: "python", label: "Python" },
  { key: "javascript", label: "JavaScript" },
  { key: "java", label: "Java" },
  { key: "c", label: "C" },
];

function App() {
  const editorRef = useRef(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState("python");

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      if (editorRef.current) {
        editorRef.current.setValue(e.target.result);
      }
    };
    reader.readAsText(file);
  };

  function handleEditorDidMount(editor) {
    editorRef.current = editor;
  }

  const handleAnalyze = async () => {
    setLoading(true);
    const code = editorRef.current ? editorRef.current.getValue() : "";

    try {
      const response = await fetch("http://localhost:9000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          language: language,
          code: code,
        }),
      });

      const data = await response.json();
      setAnalysisResult(data);
    } catch (error) {
      setAnalysisResult({
        error: "Failed to analyze code: " + error.message,
      });
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1 className="title">🪲 AI Bug Finder</h1>

      {/* Language Tabs */}
      <div className="language-tabs">
        {LANGUAGES.map((lang) => (
          <div
            key={lang.key}
            className={`language-tab ${language === lang.key ? "active" : ""}`}


            onClick={() => setLanguage(lang.key)}
          >
            {lang.label}
          </div>
        ))}
      </div>

      <input
        className="file-upload"
        type="file"
        accept=".py,.js,.java,.c,.cpp,.txt"
        onChange={handleFileUpload}
      />

      <Editor
        height="50vh"
        language={language}
        defaultValue="# Type your code here"
        onMount={handleEditorDidMount}
        theme="vs-dark"
      />

      <button
        className="analyze-btn"
        onClick={handleAnalyze}
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {analysisResult && (
        <div className="results">
          {analysisResult.error && (
            <div className="result-block error">
              <h3>❌ Error</h3>
              <pre>{analysisResult.error}</pre>
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
              <pre>{analysisResult.solution}</pre>
            </div>
          )}

          {analysisResult.additional_tips && (
            <div className="result-block tips">
              <h3>📌 Additional Tips</h3>
              <ul>
                {analysisResult.additional_tips
                  .split("\n")
                  .map((tip, i) => (
                    <li key={i}>{tip.replace(/^-\s*/, "")}</li>
                  ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
