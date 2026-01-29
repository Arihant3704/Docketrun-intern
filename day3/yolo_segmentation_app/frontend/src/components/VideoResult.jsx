import React from 'react';
import { MonitorPlay, CheckCircle } from 'lucide-react';

const VideoResult = () => {
    const videoUrl = "http://localhost:8000/results/output_web.mp4";

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', alignItems: 'center' }}>
            <div style={{ textAlign: 'center', maxWidth: '800px' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
                    <CheckCircle color="#10b981" size={24} />
                    <h2 style={{ margin: 0 }}>Safety Analysis Report</h2>
                </div>
                <p style={{ color: '#94a3b8', fontSize: '1.1rem' }}>
                    Automated object detection and segmentation analysis for safety compliance.
                </p>
            </div>

            <div className="glass" style={{ padding: '1.5rem', width: '100%', maxWidth: '900px', background: 'rgba(15, 23, 42, 0.6)' }}>
                <div style={{ position: 'relative', borderRadius: '0.75rem', overflow: 'hidden', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5)' }}>
                    <video
                        controls
                        autoPlay
                        loop
                        src={videoUrl}
                        style={{ width: '100%', display: 'block' }}
                    />
                </div>
                <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#6366f1' }}>
                        <MonitorPlay size={20} />
                        <span style={{ fontWeight: 600 }}>Inferred Stream</span>
                    </div>
                    <div style={{ background: '#1e293b', padding: '0.4rem 0.8rem', borderRadius: '2rem', fontSize: '0.9rem', color: '#94a3b8' }}>
                        Source: output.mp4
                    </div>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1.5rem', width: '100%', maxWidth: '900px' }}>
                <div className="glass" style={{ padding: '1.25rem', textAlign: 'center' }}>
                    <div style={{ color: '#6366f1', fontWeight: 700, fontSize: '1.5rem', marginBottom: '0.25rem' }}>100%</div>
                    <div style={{ color: '#94a3b8', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Coverage</div>
                </div>
                <div className="glass" style={{ padding: '1.25rem', textAlign: 'center' }}>
                    <div style={{ color: '#10b981', fontWeight: 700, fontSize: '1.5rem', marginBottom: '0.25rem' }}>Active</div>
                    <div style={{ color: '#94a3b8', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Real-time Monitoring</div>
                </div>
                <div className="glass" style={{ padding: '1.25rem', textAlign: 'center' }}>
                    <div style={{ color: '#ec4899', fontWeight: 700, fontSize: '1.5rem', marginBottom: '0.25rem' }}>Verified</div>
                    <div style={{ color: '#94a3b8', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>AI Compliance</div>
                </div>
            </div>
        </div>
    );
};

export default VideoResult;
