import React from 'react';
import { useParams, Navigate, Link } from 'react-router-dom';
import { courseContent } from '../data/courseContent';
import { libraries } from '../data/courseData';
import CodeBlock from '../components/ui/CodeBlock';
import InteractiveCodeBlock from '../components/interactive/InteractiveCodeBlock';
import QuizSection from '../components/interactive/QuizSection';
import { useProgress } from '../context/ProgressContext';
import { ChevronRight, ChevronLeft, AlertCircle, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import './ChapterPage.css';

const ChapterPage = () => {
    const { libraryId, moduleId } = useParams();
    const contentKey = `${libraryId}/${moduleId}`;
    const data = courseContent[contentKey];
    const { markComplete, isComplete } = useProgress();
    const completed = isComplete(contentKey);

    if (!data) {
        return (
            <div className="not-found">
                <h2>Content Under Construction</h2>
                <p>This module is currently being authored. Check back soon!</p>
                <Link to="/" className="btn btn-primary">Go Home</Link>
            </div>
        );
    }

    // Find prev/next navigation
    const currentLib = libraries.find(l => l.id === libraryId);
    const moduleIndex = currentLib.modules.findIndex(m => m.id === moduleId);
    const prevModule = moduleIndex > 0 ? currentLib.modules[moduleIndex - 1] : null;
    const nextModule = moduleIndex < currentLib.modules.length - 1 ? currentLib.modules[moduleIndex + 1] : null;

    return (
        <motion.div
            className="chapter-page"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
            key={contentKey}
        >
            <header className="chapter-header">
                <div className="breadcrumbs">
                    <span style={{ color: currentLib.color }}>{currentLib.name}</span>
                    <ChevronRight size={14} />
                    <span>{data.title}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h1>{data.title}</h1>
                    {completed && (
                        <div className="badge" style={{ borderColor: '#4ade80', color: '#4ade80' }}>
                            <CheckCircle size={14} /> Only Completed
                        </div>
                    )}
                </div>
            </header>

            <div className="chapter-content">
                {data.sections.map((section, idx) => {
                    if (section.type === 'text') {
                        const htmlContent = section.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                        return <p key={idx} dangerouslySetInnerHTML={{ __html: htmlContent }} />;
                    }
                    if (section.type === 'code') {
                        return <CodeBlock key={idx} code={section.code} title={section.title} />;
                    }
                    if (section.type === 'interactive-code') {
                        return <InteractiveCodeBlock key={idx} initialCode={section.code} setupCode={section.setup || ''} />;
                    }
                    if (section.type === 'callout') {
                        return (
                            <div key={idx} className={`callout callout-${section.variant}`}>
                                <div className="callout-icon">
                                    <AlertCircle size={20} />
                                </div>
                                <div>
                                    <h4>{section.title}</h4>
                                    <p>{section.content}</p>
                                </div>
                            </div>
                        );
                    }
                    return null;
                })}

                {data.quiz && (
                    <QuizSection
                        quizzes={data.quiz}
                        onComplete={() => markComplete(contentKey)}
                    />
                )}
            </div>

            <div style={{ marginTop: '3rem', display: 'flex', justifyContent: 'center' }}>
                <button
                    onClick={() => markComplete(contentKey)}
                    className={`btn ${completed ? 'btn-outline' : 'btn-primary'}`}
                    disabled={completed}
                    style={completed ? { borderColor: '#4ade80', color: '#4ade80' } : {}}
                >
                    {completed ? (
                        <>
                            <CheckCircle size={18} /> Completed
                        </>
                    ) : (
                        'Mark as Complete'
                    )}
                </button>
            </div>

            <nav className="chapter-nav">
                {prevModule ? (
                    <Link to={`/course/${libraryId}/${prevModule.id}`} className="nav-btn prev">
                        <ChevronLeft size={16} />
                        <div>
                            <span className="label">Previous</span>
                            <span className="title">{prevModule.title}</span>
                        </div>
                    </Link>
                ) : <div />}

                {nextModule ? (
                    <Link to={`/course/${libraryId}/${nextModule.id}`} className="nav-btn next">
                        <div>
                            <span className="label">Next</span>
                            <span className="title">{nextModule.title}</span>
                        </div>
                        <ChevronRight size={16} />
                    </Link>
                ) : <div />}
            </nav>
        </motion.div>
    );
};

export default ChapterPage;
