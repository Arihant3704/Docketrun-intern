import React, { useState } from 'react';
import { Link, ArrowRight, Loader } from 'lucide-react';

const UrlInference = ({ modelName, threshold }) => {
    const [url, setUrl] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleInference = async () => {
        if (!url) return;

        setLoading(true);
        setResult(null);

        try {
            const response = await fetch(`http://localhost:8000/predict/url?url=${encodeURIComponent(url)}&model_name=${encodeURIComponent(modelName)}&threshold=${threshold}`, {
                method: 'POST',
            });

            if (!response.ok) throw new Error('Inference failed');

            const data = await response.json();
            setResult(`http://localhost:8000${data.image_url}`);
        } catch (error) {
            console.error(error);
            alert('Error fetching or processing URL');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            <div className="glass" style={{ padding: '2rem' }}>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <div style={{ position: 'relative', flex: 1 }}>
                        <Link size={20} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: '#94a3b8' }} />
                        <input
                            type="text"
                            className="input-field"
                            style={{ paddingLeft: '3rem' }}
                            placeholder="Paste Image URL here..."
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                        />
                    </div>
                    <button
                        className="btn"
                        onClick={handleInference}
                        disabled={!url || loading}
                    >
                        {loading ? <Loader className="spin" size={20} /> : 'Analyze'}
                    </button>
                </div>
            </div>

            {(result || (loading && url)) && (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                    <div className="glass" style={{ padding: '1rem' }}>
                        <h4 style={{ margin: '0 0 1rem 0', color: '#94a3b8' }}>Source</h4>
                        <img
                            src={url}
                            alt="Source"
                            style={{ width: '100%', borderRadius: '0.5rem', maxHeight: '400px', objectFit: 'contain' }}
                            onError={(e) => e.target.src = 'https://via.placeholder.com/400x300?text=Invalid+Image+URL'}
                        />
                    </div>

                    <div className="glass" style={{ padding: '1rem' }}>
                        <h4 style={{ margin: '0 0 1rem 0', color: '#ec4899' }}>Result</h4>
                        {result ? (
                            <img
                                src={result}
                                alt="Result"
                                style={{ width: '100%', borderRadius: '0.5rem', maxHeight: '400px', objectFit: 'contain' }}
                            />
                        ) : (
                            <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#94a3b8' }}>
                                {loading ? 'Processing...' : 'Waiting for results...'}
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default UrlInference;
