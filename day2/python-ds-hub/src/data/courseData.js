
import { Box, FileSpreadsheet, BarChart, Camera, Brain, Rocket } from 'lucide-react';

export const libraries = [
  {
    id: 'numpy',
    name: 'NumPy',
    icon: Box,
    color: 'var(--color-numpy)',
    description: 'The fundamental package for scientific computing with Python.',
    modules: [
      { id: 'intro', title: 'Introduction & Setup' },
      { id: 'creating-arrays', title: 'Creating Arrays' },
      { id: 'operations', title: 'Array Operations' },
      { id: 'indexing', title: 'Indexing & Slicing' },
      { id: 'broadcasting', title: 'Broadcasting & Logic' },
    ]
  },
  {
    id: 'pandas',
    name: 'Pandas',
    icon: FileSpreadsheet,
    color: 'var(--color-pandas)',
    description: 'Fast, flexible, and expressive data structures.',
    modules: [
      { id: 'intro', title: 'Series & DataFrames' },
      { id: 'io', title: 'Reading & Writing Data' },
      { id: 'cleaning', title: 'Data Cleaning' },
      { id: 'manipulation', title: 'Data Manipulation' },
      { id: 'aggregation', title: 'Aggregation & Grouping' },
    ]
  },
  {
    id: 'matplotlib',
    name: 'Matplotlib',
    icon: BarChart,
    color: 'var(--color-matplotlib)',
    description: 'Comprehensive static, animated, and interactive visualization.',
    modules: [
      { id: 'intro', title: 'Basic Plotting' },
      { id: 'customization', title: 'Customizing Plots' },
      { id: 'subplots', title: 'Subplots & Layouts' },
      { id: 'types', title: 'Advanced Plot Types' },
    ]
  },
  {
    id: 'opencv',
    name: 'OpenCV',
    icon: Camera,
    color: 'var(--color-opencv)',
    description: 'Open Source Computer Vision Library.',
    modules: [
      { id: 'intro', title: 'Images & Video' },
      { id: 'drawing', title: 'Drawing Shapes' },
      { id: 'processing', title: 'Image Processing' },
      { id: 'detection', title: 'Object Detection' },
    ]
  },
  {
    id: 'sklearn',
    name: 'Scikit-Learn',
    icon: Brain,
    color: 'var(--color-sklearn)',
    description: 'Simple and efficient tools for predictive data analysis.',
    modules: [
      { id: 'intro', title: 'ML Workflow' },
      { id: 'preprocessing', title: 'Preprocessing' },
      { id: 'supervised', title: 'Supervised Learning' },
      { id: 'unsupervised', title: 'Unsupervised Learning' },
      { id: 'evaluation', title: 'Model Evaluation' },
    ]
  },
  {
    id: 'projects',
    name: 'Real-World Projects',
    icon: Rocket,
    color: '#e11d48', // Rose-600
    description: 'Apply your skills with complete, end-to-end projects.',
    modules: [
      { id: 'crypto-analyzer', title: 'Crypto Market Analyzer' },
      { id: 'smart-attendance', title: 'Smart Attendance System' },
      { id: 'movie-recommender', title: 'Movie Recommendation Engine' },
    ]
  }
];
