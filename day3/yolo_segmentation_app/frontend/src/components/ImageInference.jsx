import React, { useState } from 'react';
import { Upload, ArrowRight, Image as ImageIcon, Loader } from 'lucide-react';

const ImageInference = ({ modelName, threshold }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedFile(file);
            setPreview(URL.createObjectURL(file));
            setResult(null);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            // Append model name and threshold to form data as required by backend
            const formDataWithModel = new FormData();
            formDataWithModel.append('file', selectedFile);
            formDataWithModel.append('model_name', modelName);
            formDataWithModel.append('threshold', threshold);
            const response = await fetch('http://localhost:8000/predict/image', {
                method: 'POST',
                body: formDataWithModel,
            });

            if (!response.ok) throw new Error('Inference failed');

            const data = await response.json();
            setResult(`http://localhost:8000${data.image_url}`);
        } catch (error) {
            console.error(error);
            alert('Error extracting segmentations');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            <div
                className="upload-area"
                onClick={() => document.getElementById('image-upload').click()}
            >
                <input
                    type="file"
                    id="image-upload"
                    hidden
                    accept="image/*"
                    onChange={handleFileChange}
                />
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
                    <Upload size={48} color="#6366f1" />
                    <div>
                        <h3 style={{ margin: 0, marginBottom: '0.5rem' }}>Click or Drag Image Here</h3>
                        <p style={{ margin: 0, color: '#94a3b8' }}>Supports JPG, PNG</p>
                    </div>
                </div>
            </div>

            {preview && (
                <div style={{ display: 'grid', gridTemplateColumns: result ? '1fr 1fr' : '1fr', gap: '2rem' }}>
                    <div className="glass" style={{ padding: '1rem' }}>
                        <h4 style={{ margin: '0 0 1rem 0', color: '#94a3b8' }}>Original</h4>
                        <img
                            src={preview}
                            alt="Preview"
                            style={{ width: '100%', borderRadius: '0.5rem' }}
                        />
                        {!result && (
                            <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                                <button
                                    className="btn"
                                    onClick={handleUpload}
                                    disabled={loading}
                                    style={{ width: '100%', justifyContent: 'center' }}
                                >
                                    {loading ? <Loader className="spin" size={20} /> : <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>Run Segmentation <ArrowRight size={18} /></div>}
                                </button>
                            </div>
                        )}
                    </div>

                    {result && (
                        <div className="glass" style={{ padding: '1rem' }}>
                            <h4 style={{ margin: '0 0 1rem 0', color: '#ec4899' }}>Result</h4>
                            <img
                                src={result}
                                alt="Result"
                                style={{ width: '100%', borderRadius: '0.5rem' }}
                            />
                            <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                                <p style={{ color: '#4ade80' }}>✓ Inference Complete</p>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default ImageInference;
