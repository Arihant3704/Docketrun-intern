import React, { useState } from 'react';
import { CheckCircle, XCircle, Award } from 'lucide-react';
import './QuizSection.css';

const QuizSection = ({ quizzes, onComplete }) => {
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [selectedOption, setSelectedOption] = useState(null);
    const [isCorrect, setIsCorrect] = useState(null);
    const [score, setScore] = useState(0);
    const [showResults, setShowResults] = useState(false);

    const handleOptionSelect = (index) => {
        setSelectedOption(index);
        const correct = index === quizzes[currentQuestion].answer;
        setIsCorrect(correct);
    };

    const handleNext = () => {
        if (isCorrect) {
            setScore(score + 1);
        }

        if (currentQuestion < quizzes.length - 1) {
            setCurrentQuestion(currentQuestion + 1);
            setSelectedOption(null);
            setIsCorrect(null);
        } else {
            setShowResults(true);
            if (onComplete) onComplete();
        }
    };

    const resetQuiz = () => {
        setCurrentQuestion(0);
        setSelectedOption(null);
        setIsCorrect(null);
        setScore(0);
        setShowResults(false);
    };

    if (showResults) {
        const percentage = (score / quizzes.length) * 100;
        return (
            <div className="quiz-container results-view">
                <Award size={48} className="text-accent mb-4" />
                <h3>Quiz Completed!</h3>
                <div className="score-display">
                    You scored <span className="text-accent">{score}</span> out of {quizzes.length}
                </div>
                <div className="progress-bar-bg">
                    <div className="progress-bar-fill" style={{ width: `${percentage}%` }}></div>
                </div>
                <p className="mt-4 text-secondary">
                    {percentage === 100 ? 'Perfect Score! You are a master.' : 'Good job! Keep practicing.'}
                </p>
                <button className="btn btn-outline mt-4" onClick={resetQuiz}>
                    Retake Quiz
                </button>
            </div>
        );
    }

    const question = quizzes[currentQuestion];

    return (
        <div className="quiz-container">
            <div className="quiz-header">
                <h4>Knowledge Check</h4>
                <span className="quiz-counter">Question {currentQuestion + 1} / {quizzes.length}</span>
            </div>

            <div className="question-text">
                {question.question}
            </div>

            <div className="options-list">
                {question.options.map((option, idx) => {
                    let className = "quiz-option";
                    if (selectedOption !== null) {
                        if (idx === question.answer) className += " correct";
                        if (idx === selectedOption && idx !== question.answer) className += " wrong";
                    }

                    return (
                        <div
                            key={idx}
                            className={className}
                            onClick={() => selectedOption === null && handleOptionSelect(idx)}
                        >
                            <div className="option-marker">
                                {String.fromCharCode(65 + idx)}
                            </div>
                            <span>{option}</span>
                            {selectedOption !== null && idx === question.answer && <CheckCircle size={16} />}
                            {selectedOption !== null && idx === selectedOption && idx !== question.answer && <XCircle size={16} />}
                        </div>
                    );
                })}
            </div>

            {selectedOption !== null && (
                <div className="quiz-footer">
                    <div className={`feedback ${isCorrect ? 'text-success' : 'text-error'}`}>
                        {isCorrect ? 'Correct! Well done.' : 'Incorrect. Try again next time.'}
                    </div>
                    <button className="btn btn-primary" onClick={handleNext}>
                        {currentQuestion < quizzes.length - 1 ? 'Next Question' : 'Finish Quiz'}
                    </button>
                </div>
            )}
        </div>
    );
};

export default QuizSection;
