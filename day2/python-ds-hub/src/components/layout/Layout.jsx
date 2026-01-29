import React, { useState } from 'react';
import { NavLink, Outlet, useLocation } from 'react-router-dom';
import { libraries } from '../../data/courseData';
import { useProgress } from '../../context/ProgressContext';
import { ChevronRight, Menu, X, Home, CheckCircle } from 'lucide-react';
import './Layout.css';

const Layout = () => {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const location = useLocation();
    const { isComplete } = useProgress();

    const toggleMenu = () => setIsMobileMenuOpen(!isMobileMenuOpen);

    return (
        <div className="layout">
            {/* Mobile Header */}
            <div className="mobile-header">
                <button onClick={toggleMenu} className="menu-btn">
                    {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                </button>
                <span className="logo-text">PyDS Hub</span>
            </div>

            {/* Sidebar */}
            <aside className={`sidebar ${isMobileMenuOpen ? 'open' : ''}`}>
                <div className="sidebar-header">
                    <div className="logo d-flex align-items-center gap-2">
                        <span style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>PyDS Hub</span>
                    </div>
                </div>

                <nav className="sidebar-nav">
                    <NavLink to="/" className="nav-item home-link" onClick={() => setIsMobileMenuOpen(false)}>
                        <Home size={20} />
                        <span>Home</span>
                    </NavLink>

                    <div className="library-list">
                        {libraries.map((lib) => (
                            <div key={lib.id} className="library-group">
                                <div className="library-header" style={{ color: lib.color }}>
                                    <lib.icon size={18} />
                                    <span>{lib.name}</span>
                                </div>
                                <div className="module-links">
                                    {lib.modules.map((mod) => {
                                        const completed = isComplete(`${lib.id}/${mod.id}`);
                                        return (
                                            <NavLink
                                                key={mod.id}
                                                to={`/course/${lib.id}/${mod.id}`}
                                                className={({ isActive }) => `module-link ${isActive ? 'active' : ''}`}
                                                onClick={() => setIsMobileMenuOpen(false)}
                                                style={({ isActive }) => isActive ? { borderLeftColor: lib.color, color: 'white' } : {}}
                                            >
                                                <div className="module-link-inner">
                                                    <span className="module-title-text">{mod.title}</span>
                                                    {completed && <CheckCircle size={14} className="completion-icon" />}
                                                </div>
                                            </NavLink>
                                        );
                                    })}
                                </div>
                            </div>
                        ))}
                    </div>
                </nav>
            </aside>

            {/* Main Content */}
            <main className="main-content">
                <Outlet />
            </main>

            {/* Overlay for mobile */}
            {isMobileMenuOpen && <div className="overlay" onClick={() => setIsMobileMenuOpen(false)} />}
        </div>
    );
};

export default Layout;
