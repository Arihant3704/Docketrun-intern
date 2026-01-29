import React, { useState } from 'react';
import { Image, Video, Link, Layers, MonitorPlay } from 'lucide-react';
import ImageInference from './components/ImageInference';
import VideoResult from './components/VideoResult';
import UrlInference from './components/UrlInference';

function App() {
  const [activeTab, setActiveTab] = useState('image');
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [threshold, setThreshold] = useState(0.25);

  React.useEffect(() => {
    fetch('http://localhost:8000/models')
      .then(res => res.json())
      .then(data => {
        setModels(data.models);
        if (data.models.length > 0) {
          setSelectedModel(data.models[0]);
        }
      })
      .catch(err => console.error("Failed to load models", err));
  }, []);

  return (
    <div className="container">
      <header style={{ textAlign: 'center', marginBottom: '3rem', paddingTop: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '1rem', marginBottom: '1rem' }}>
          <Layers size={48} color="#6366f1" />
          <h1 className="logo-text">YOLOv26 Segmentation</h1>
        </div>
        <p style={{ color: '#94a3b8', fontSize: '1.1rem' }}>Real-time premium inference for Images and URLs</p>

        <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '2rem', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <label style={{ color: '#e2e8f0' }}>Select Model:</label>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              style={{
                padding: '0.5rem 1rem',
                borderRadius: '0.5rem',
                border: '1px solid #475569',
                background: '#1e293b',
                color: '#f8fafc',
                fontSize: '1rem',
                outline: 'none',
                cursor: 'pointer'
              }}
            >
              {models.map(model => (
                <option key={model} value={model}>{model}</option>
              ))}
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <label style={{ color: '#e2e8f0' }}>Confidence Threshold: {threshold}</label>
            <input
              type="range"
              min="0.01"
              max="1"
              step="0.01"
              value={threshold}
              onChange={(e) => setThreshold(parseFloat(e.target.value))}
              style={{ cursor: 'pointer', width: '200px' }}
            />
          </div>
        </div>
      </header>

      <div className="glass" style={{ padding: '2rem', minHeight: '600px' }}>
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'image' ? 'active' : ''}`}
            onClick={() => setActiveTab('image')}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Image size={18} /> Image Inference
            </div>
          </button>
          <button
            className={`tab ${activeTab === 'video' ? 'active' : ''}`}
            onClick={() => setActiveTab('video')}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Video size={18} /> Video Analysis
            </div>
          </button>
          <button
            className={`tab ${activeTab === 'url' ? 'active' : ''}`}
            onClick={() => setActiveTab('url')}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Link size={18} /> URL Inference
            </div>
          </button>
        </div>

        <div className="content">
          {activeTab === 'image' && <ImageInference modelName={selectedModel} threshold={threshold} />}
          {activeTab === 'video' && <VideoResult />}
          {activeTab === 'url' && <UrlInference modelName={selectedModel} threshold={threshold} />}
        </div>
      </div>
    </div>
  );
}

export default App;
