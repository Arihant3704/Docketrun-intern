import React, { useState, useEffect, useRef } from 'react';
import { Play, RotateCcw, Loader, Terminal } from 'lucide-react';
import { PrismLight as SyntaxHighlighter } from 'react-syntax-highlighter';
import python from 'react-syntax-highlighter/dist/esm/languages/prism/python';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import './InteractiveCodeBlock.css';

SyntaxHighlighter.registerLanguage('python', python);

const InteractiveCodeBlock = ({ initialCode, setupCode = '' }) => {
    const [code, setCode] = useState(initialCode.trim());
    const [output, setOutput] = useState([]);
    const [isRunning, setIsRunning] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [pyodide, setPyodide] = useState(null);
    const [isReady, setIsReady] = useState(false);

    useEffect(() => {
        const loadPyodide = async () => {
            if (window.pyodide) {
                setPyodide(window.pyodide);
                setIsReady(true);
                return;
            }

            setIsLoading(true);
            try {
                // Dynamically load Pyodide script
                if (!document.querySelector('script[src*="pyodide.js"]')) {
                    const script = document.createElement('script');
                    script.src = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js";
                    script.async = true;
                    document.body.appendChild(script);

                    await new Promise((resolve, reject) => {
                        script.onload = resolve;
                        script.onerror = reject;
                    });
                }

                const pyodideInstance = await window.loadPyodide();
                // Load common packages
                await pyodideInstance.loadPackage(['numpy', 'pandas']);

                window.pyodide = pyodideInstance; // Cache it
                setPyodide(pyodideInstance);
                setIsReady(true);
            } catch (err) {
                console.error("Failed to load Pyodide", err);
                setOutput(["Error: Failed to load Python environment."]);
            } finally {
                setIsLoading(false);
            }
        };

        // Only load when user interacts or visible? 
        // For now, load on mount effectively, but we could make it wait for a "Start Python" button.
    }, []);

    const runCode = async () => {
        if (!pyodide || !isReady) {
            // Trigger load if not loaded?
            return;
        }

        setIsRunning(true);
        setOutput([]); // Clear previous output

        try {
            // Capture stdout
            pyodide.setStdout({
                batched: (msg) => {
                    setOutput(prev => [...prev, msg]);
                }
            });

            await pyodide.runPythonAsync(setupCode + '\n' + code);

        } catch (err) {
            setOutput(prev => [...prev, `Error: ${err.message}`]);
        } finally {
            setIsRunning(false);
        }
    };

    const resetCode = () => {
        setCode(initialCode.trim());
        setOutput([]);
    };

    if (!isReady && !isLoading) {
        return (
            <div className="interactive-placeholder">
                <button onClick={() => window.location.reload()} className="btn btn-primary">
                    Initialize Python Environment (Requires Refresh if failed)
                </button>
            </div>
        );
    }

    return (
        <div className="interactive-block">
            <div className="interactive-header">
                <div className="header-title">
                    <Terminal size={16} className="text-accent" />
                    <span>Interactive Python</span>
                </div>
                <div className="header-actions">
                    <button className="icon-btn" onClick={resetCode} title="Reset Code">
                        <RotateCcw size={16} />
                    </button>
                    <button
                        className="btn btn-sm btn-run"
                        onClick={runCode}
                        disabled={isRunning || isLoading}
                    >
                        {isRunning || isLoading ? <Loader size={16} className="spin" /> : <Play size={16} fill="currentColor" />}
                        {isRunning ? 'Running...' : 'Run'}
                    </button>
                </div>
            </div>

            {isLoading && (
                <div className="loading-overlay">
                    <Loader size={24} className="spin text-accent" />
                    <span>Loading Python Environment... (This happens once)</span>
                </div>
            )}

            <div className="editor-area">
                <textarea
                    className="code-editor"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    spellCheck="false"
                />
                {/* We use SyntaxHighlighter just for display? No, using textarea for simplicity now. 
            A real editor would layer them. For MVP, simple textarea with monospace font. */}
            </div>

            <div className="output-console">
                <div className="console-label">Output:</div>
                {output.length === 0 ? (
                    <div className="output-empty">Run the code to see output</div>
                ) : (
                    output.map((line, i) => (
                        <div key={i} className="output-line">{line}</div>
                    ))
                )}
            </div>
        </div>
    );
};

export default InteractiveCodeBlock;
