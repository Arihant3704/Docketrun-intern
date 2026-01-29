import React from 'react';
import { ArrowRight, Activity, ShieldCheck, Maximize } from 'lucide-react';

const Home = ({ onStart }) => {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
            {/* Hero Section */}
            <div className="glass" style={{ padding: '2rem', textAlign: 'center', position: 'relative', overflow: 'hidden' }}>
                <img
                    src="/banner.png"
                    alt="YOLO26 Demo"
                    style={{ width: '100%', borderRadius: '1rem', marginBottom: '2rem', border: '1px solid #6366f1' }}
                />
                <h2 style={{ fontSize: '2.5rem', fontWeight: '800', margin: '0 0 1rem 0' }}>
                    Next-Gen <span style={{ color: '#6366f1' }}>Real-time</span> Vision
                </h2>
                <p style={{ fontSize: '1.2rem', color: '#cbd5e1', maxWidth: '800px', margin: '0 auto 2rem auto' }}>
                    Experience the power of YOLO26. Advanced segmentation, object detection, and color classification
                    running directly in your browser powered by a robust Python backend.
                </p>
                <button className="btn" style={{ fontSize: '1.2rem', padding: '1rem 2rem' }} onClick={onStart}>
                    Getting Started <ArrowRight size={20} />
                </button>
            </div>

            {/* Features Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
                <div className="glass" style={{ padding: '2rem' }}>
                    <Activity size={32} color="#ec4899" style={{ marginBottom: '1rem' }} />
                    <h3 style={{ margin: '0 0 0.5rem 0' }}>High Performance</h3>
                    <p style={{ color: '#94a3b8' }}>Optimized inference for real-time video and high-resolution imagery.</p>
                </div>
                <div className="glass" style={{ padding: '2rem' }}>
                    <ShieldCheck size={32} color="#a855f7" style={{ marginBottom: '1rem' }} />
                    <h3 style={{ margin: '0 0 0.5rem 0' }}>Multiple Models</h3>
                    <p style={{ color: '#94a3b8' }}>Switch seamlessly between Segmentation, Object Detection, and Color Analysis models.</p>
                </div>
                <div className="glass" style={{ padding: '2rem' }}>
                    <Maximize size={32} color="#6366f1" style={{ marginBottom: '1rem' }} />
                    <h3 style={{ margin: '0 0 0.5rem 0' }}>Versatile Inputs</h3>
                    <p style={{ color: '#94a3b8' }}>Analyze files from your device or fetch directly from URLs.</p>
                </div>
            </div>
        </div>
    );
};

export default Home;
