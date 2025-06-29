import React, { useEffect, useState } from 'react';
import { Pie } from 'react-chartjs-2';
import 'chart.js/auto';

import './Dashboard.css';

// FontAwesome icons
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartPie, faLayerGroup, faKey, faTable } from '@fortawesome/free-solid-svg-icons';

export default function SummaryPage() {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/summary')
      .then((res) => res.json())
      .then((data) => setSummary(data))
      .catch((err) => console.error(err));
  }, []);

  if (!summary) return <div className="text-center mt-5">Loading...</div>;

  const colors = [
    '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b',
    '#858796', '#fd7e14', '#20c997', '#6610f2', '#d63384',
    '#00a8e8', '#0077b6', '#0096c7', '#48cae4', '#90e0ef',
  ];

  // ✅ 1) Stock allocation chart data
  const chartData = {
    labels: summary.holdings_percentages.map(item => item.Symbol),
    datasets: [{
      data: summary.holdings_percentages.map(item => item.percent),
      backgroundColor: colors.slice(0, summary.holdings_percentages.length),
      borderWidth: 1,
    }],
  };

  // ✅ 2) Quote type chart data
  const totalQuoteValue = Object.values(summary.quote_type_split || {}).reduce((a, b) => a + b, 0);
  const quoteTypeData = Object.entries(summary.quote_type_split || {}).map(([key, val]) => ({
    type: key,
    percent: ((val / totalQuoteValue) * 100).toFixed(2)
  }));

  const quoteTypeChartData = {
    labels: quoteTypeData.map(item => item.type),
    datasets: [{
      data: quoteTypeData.map(item => item.percent),
      backgroundColor: ['#4e73df', '#1cc88a', '#f6c23e', '#e74a3b'],
      borderWidth: 1,
    }],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'bottom', labels: { boxWidth: 20 } },
      tooltip: {
        callbacks: {
          label: function (context) {
            const label = context.label;
            const percent = context.parsed.toFixed(2);
            return `${label}: ${percent}%`;
          },
        },
      },
    },
    layout: {
      padding: 10
    }
  };

  const formatNumber = (num) => {
    if (typeof num === 'number') {
      return num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
    return num;
  };

  return (
    <div className="container-fluid py-4">
      <h1 className="mb-5 text-center">📊 Portfolio Dashboard</h1>
      <div className="row">
        {/* 📊 1) Holdings Allocation */}
        <div className="col-lg-6 col-md-12 mb-4">
          <div className="card shadow">
            <div className="card-body">
              <h5 className="card-title text-primary">
                <FontAwesomeIcon icon={faChartPie} className="me-2" />
                Stock Allocation
              </h5>
              <div style={{ height: "300px" }}>
                <Pie data={chartData} options={chartOptions} />
              </div>
            </div>
          </div>
        </div>

        {/* ✅ 2) Quote Type */}
        <div className="col-lg-6 col-md-12 mb-4">
          <div className="card shadow">
            <div className="card-body">
              <h5 className="card-title text-success">
                <FontAwesomeIcon icon={faLayerGroup} className="me-2" />
                Holdings by Type
              </h5>
              <div style={{ height: "300px" }}>
                <Pie data={quoteTypeChartData} options={chartOptions} />
              </div>
            </div>
          </div>
        </div>

        {/* 💡 Key Metrics */}
        <div className="col-12 mb-4">
          <div className="card shadow">
            <div className="card-body">
              <h5 className="card-title text-info">
                <FontAwesomeIcon icon={faKey} className="me-2" />
                Key Metrics
              </h5>
              <ul className="list-group list-group-flush">
                {Object.entries(summary).map(([key, value]) => {
                  if (['holdings_percentages', 'quote_type_split'].includes(key)) return null;
                  return (
                    <li key={key} className="list-group-item d-flex justify-content-between align-items-center">
                      {key.replace(/_/g, ' ').toUpperCase()}
                      <span className="badge bg-primary rounded-pill">
                        {formatNumber(value)}
                      </span>
                    </li>
                  );
                })}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* 📃 Holdings Breakdown */}
      <div className="card shadow mt-4">
        <div className="card-body">
          <h5 className="card-title text-secondary">
            <FontAwesomeIcon icon={faTable} className="me-2" />
            Holdings Breakdown
          </h5>
          <table className="table table-hover">
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Current Value</th>
                <th>Allocation %</th>
              </tr>
            </thead>
            <tbody>
              {summary.holdings_percentages.map((item) => (
                <tr key={item.Symbol}>
                  <td>{item.Symbol}</td>
                  <td>${formatNumber(item['Current Value'])}</td>
                  <td>{formatNumber(item.percent)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
