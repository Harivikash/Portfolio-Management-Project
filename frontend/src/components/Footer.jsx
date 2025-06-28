// src/components/Footer.jsx
import React from 'react';
import version from '../version.js';


export default function Footer() {
  return (
    <footer className="bg-light text-center text-muted py-3 mt-auto">
      <div className="container">
        <small>Portfolio Management App &mdash; Version {version}</small>
      </div>
    </footer>
  );
}
