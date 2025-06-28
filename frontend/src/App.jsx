import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import SummaryPage from './SummaryPage';
import DataPage from './DataPage';
import UploadPage from './UploadPage';
import Footer from './components/Footer';

import 'bootstrap/dist/css/bootstrap.min.css';

export default function App() {
  return (
    <Router>
      <div className="d-flex flex-column min-vh-100">
        <nav className="navbar navbar-expand navbar-dark bg-primary px-3">
          <Link className="navbar-brand" to="/">Portfolio</Link>
          <div className="navbar-nav">
            <Link className="nav-link" to="/">Home</Link>
            <Link className="nav-link" to="/data">Data</Link>
            <Link className="nav-link" to="/upload">Upload CSV</Link>
          </div>
        </nav>

        <main className="container mt-4 flex-grow-1">
          <Routes>
            <Route path="/" element={<SummaryPage />} />
            <Route path="/data" element={<DataPage />} />
            <Route path="/upload" element={<UploadPage />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </Router>
  );
}
