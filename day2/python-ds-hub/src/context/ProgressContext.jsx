import React, { createContext, useContext, useState, useEffect } from 'react';

const ProgressContext = createContext();

export const useProgress = () => useContext(ProgressContext);

export const ProgressProvider = ({ children }) => {
    // Load initial state from local storage
    const [completedModules, setCompletedModules] = useState(() => {
        const saved = localStorage.getItem('completedModules');
        return saved ? JSON.parse(saved) : [];
    });

    const [points, setPoints] = useState(() => {
        return parseInt(localStorage.getItem('userPoints') || '0');
    });

    useEffect(() => {
        localStorage.setItem('completedModules', JSON.stringify(completedModules));
    }, [completedModules]);

    useEffect(() => {
        localStorage.setItem('userPoints', points.toString());
    }, [points]);

    const markComplete = (moduleId) => {
        if (!completedModules.includes(moduleId)) {
            setCompletedModules([...completedModules, moduleId]);
            setPoints(prev => prev + 50); // Award points
        }
    };

    const isComplete = (moduleId) => completedModules.includes(moduleId);

    return (
        <ProgressContext.Provider value={{ completedModules, points, markComplete, isComplete }}>
            {children}
        </ProgressContext.Provider>
    );
};
