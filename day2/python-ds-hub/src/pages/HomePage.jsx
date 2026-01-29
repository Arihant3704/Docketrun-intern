import React from 'react';
import { libraries } from '../data/courseData';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Terminal } from 'lucide-react';
import './HomePage.css';

const HomePage = () => {
    return (
        <div className="home-page">
            <header className="hero">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="hero-content"
                >
                    <div className="badge">
                        <Terminal size={14} />
                        <span>Interactive Documentation</span>
                    </div>
                    <h1>
                        Master the <span className="gradient-text">Python Data Stack</span>
                    </h1>
                    <p>
                        An interactive, deep-dive guide to NumPy, Pandas, Matplotlib, OpenCV, and Scikit-Learn.
                        From zero to ML Hero.
                    </p>
                    <div className="hero-actions">
                        <Link to="/course/numpy/intro" className="btn btn-primary btn-lg">
                            Start Learning <ArrowRight size={18} />
                        </Link>
                        <a href="https://github.com/topics/data-science" target="_blank" rel="noreferrer" className="btn btn-outline">
                            View Resources
                        </a>
                    </div>
                </motion.div>
            </header>

            <section className="library-grid-section">
                <h2>Choose a Module</h2>
                <div className="library-grid">
                    {libraries.map((lib, index) => (
                        <motion.div
                            key={lib.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                        >
                            <Link
                                to={`/course/${lib.id}/${lib.modules[0].id}`}
                                className="library-card"
                                style={{ '--hover-color': lib.color }}
                            >
                                <div className="card-icon" style={{ color: lib.color, background: `${lib.color}20` }}>
                                    <lib.icon size={32} />
                                </div>
                                <h3>{lib.name}</h3>
                                <p>{lib.description}</p>
                                <div className="card-footer">
                                    <span>{lib.modules.length} Modules</span>
                                    <ArrowRight size={16} className="arrow" />
                                </div>
                            </Link>
                        </motion.div>
                    ))}
                </div>
            </section>
        </div>
    );
};

export default HomePage;
