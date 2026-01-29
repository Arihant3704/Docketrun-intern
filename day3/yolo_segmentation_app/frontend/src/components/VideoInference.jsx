import React, { useState } from 'react';
import { Upload, Video, Loader, Play } from 'lucide-react';

const VideoInference = ({ modelName, threshold }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [processedUrl, setProcessedUrl] = useState(null);
    const [originalUrl, setOriginalUrl] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedFile(file);
            setPreviewUrl(URL.createObjectURL(file));
            setProcessedUrl(null);
            setOriginalUrl(null);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('model_name', modelName);
        formData.append('threshold', threshold);

        try {
            const response = await fetch('http://localhost:8000/predict/video', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Video inference failed');

            const data = await response.json();
            setProcessedUrl(`http://localhost:8000${data.processed_video_url}`);
            setOriginalUrl(`http://localhost:8000${data.original_video_url}`);
        } catch (error) {
            console.error(error);
            alert('Error processing video. Please ensure the backend is running and supports the video format.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            {!processedUrl && (
                <div
                    className="upload-area"
                    onClick={() => !loading && document.getElementById('video-upload').click()}
                    style={{ cursor: loading ? 'wait' : 'pointer' }}
                >
                    <input
                        type="file"
                        id="video-upload"
                        hidden
                        accept="video/*"
                        onChange={handleFileChange}
                        disabled={loading}
                    />
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
                        <Video size={48} color="#a855f7" />
                        <div>
                            <h3 style={{ margin: 0, marginBottom: '0.5rem' }}>
                                {selectedFile ? selectedFile.name : 'Click or Drag Video Here'}
                            </h3>
                            <p style={{ margin: 0, color: '#94a3b8' }}>Supports MP4, AVI, MOV</p>
                        </div>
                    </div>
                </div>
            )}

            {!processedUrl && (
                <div style={{ textAlign: 'center' }}>
                    <button
                        className="btn"
                        onClick={handleUpload}
                        disabled={!selectedFile || loading}
                        style={{ width: '250px', justifyContent: 'center' }}
                    >
                        {loading ? (
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <Loader className="spin" size={20} /> Processing Video...
                            </div>
                        ) : 'Run Full Video Analysis'}
                    </button>
                    {loading && <p style={{ color: '#94a3b8', marginTop: '1rem' }}>Inference is running on all frames. This may take a minute...</p>}
                </div>
            )}

            {processedUrl && originalUrl && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                        <div className="glass" style={{ padding: '1rem' }}>
                            <h4 style={{ margin: '0 0 1rem 0', color: '#94a3b8' }}>Original Video</h4>
                            <video
                                controls
                                src={originalUrl}
                                style={{ width: '100%', borderRadius: '0.5rem' }}
                            />
                        </div>
                        <div className="glass" style={{ padding: '1rem' }}>
                            <h4 style={{ margin: '0 0 1rem 0', color: '#ec4899' }}>Processed Video</h4>
                            <video
                                controls
                                autoPlay
                                loop
                                src={processedUrl}
                                style={{ width: '100%', borderRadius: '0.5rem' }}
                            />
                        </div>
                    </div>
                    <div style={{ textAlign: 'center' }}>
                        <button className="btn" onClick={() => { setProcessedUrl(null); setOriginalUrl(null); setSelectedFile(null); }}>
                            Upload New Video
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default VideoInference;
