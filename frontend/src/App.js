import React, { useRef, useState } from "react";
import Editor from "@monaco-editor/react";
import "./App.css";

const LANGUAGES = [
  { key: "python", label: "Python" },
  { key: "javascript", label: "JavaScript" },
  { key: "java", label: "Java" },
  { key: "c", label: "C" },
  { key: "cpp", label: "C++" },
];

const DEFAULT_CODE = {
  python: "# Start typing your Python code here\n",
  javascript: "// Start typing your JavaScript code here\n",
  java: "// Start typing your Java code here\n",
  c: "// Start typing your C code here\n",
  cpp: "// Start typing your C++ code here\n",
};

function App() {
  const editorRef = useRef(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState("python");

  const [fileName, setFileName] = useState("");
  const [codeByLanguage, setCodeByLanguage] = useState({
    python: "",
    javascript: "",
    java: "",
    c: "",
    cpp: "",
  });

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;
  
    const reader = new FileReader();
  
    reader.onload = (e) => {
      const content = e.target.result;
  
      // Save code for current language
      setCodeByLanguage((prev) => ({
        ...prev,
        [language]: content,
      }));
  
      // Update editor
      if (editorRef.current) {
        editorRef.current.setValue(content);
      }
  
      // Update filename
      setFileName(file.name);
    };
  
    reader.readAsText(file);
  
    // IMPORTANT: allow selecting same file again
    event.target.value = "";
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


            onClick={() => {
              // Save current editor code
              if (editorRef.current) {
                const currentCode = editorRef.current.getValue();
                setCodeByLanguage((prev) => ({
                  ...prev,
                  [language]: currentCode,
                }));
              }
            
              // Switch language
              setLanguage(lang.key);
            
              // Restore code for selected language
              setTimeout(() => {
                if (editorRef.current) {
                  editorRef.current.setValue(codeByLanguage[lang.key] || "");
                }
              }, 0);
            }}
            
          >
            {lang.label}
          </div>
        ))}
      </div>

      <div className="file-upload-wrapper">
        <label className="file-label">
          Choose File
        <input type="file" accept=".py,.js,.java,.c,.cpp,.txt" onChange={handleFileUpload} hidden />
      </label>

      {fileName && <span className="file-name">{fileName}</span>}
    </div>

    <Editor
      height="50vh"
      language={language}
      theme="vs-dark"
      onMount={handleEditorDidMount}
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
