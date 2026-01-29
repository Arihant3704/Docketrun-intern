import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import HomePage from './pages/HomePage';
import ChapterPage from './pages/ChapterPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="course/:libraryId/:moduleId" element={<ChapterPage />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
