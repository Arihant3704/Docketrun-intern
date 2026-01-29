import React, { useState } from 'react';
import { PrismLight as SyntaxHighlighter } from 'react-syntax-highlighter';
import python from 'react-syntax-highlighter/dist/esm/languages/prism/python';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Check, Copy } from 'lucide-react';
import './CodeBlock.css';

SyntaxHighlighter.registerLanguage('python', python);

const CodeBlock = ({ code, language = 'python', title = 'Example' }) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(code);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="code-block-container">
            <div className="code-header">
                <span className="code-title">{title}</span>
                <button className="copy-btn" onClick={handleCopy}>
                    {copied ? <Check size={16} color="#4ade80" /> : <Copy size={16} />}
                    {copied ? 'Copied' : 'Copy'}
                </button>
            </div>
            <div className="code-content">
                <SyntaxHighlighter
                    language={language}
                    style={vscDarkPlus}
                    customStyle={{ margin: 0, padding: '1.5rem', background: 'transparent' }}
                    showLineNumbers={true}
                    wrapLines={true}
                >
                    {code.trim()}
                </SyntaxHighlighter>
            </div>
        </div>
    );
};

export default CodeBlock;
