// src/SummaryPage.jsx
import React, { useEffect, useState } from 'react';
import { Pie } from 'react-chartjs-2';
import 'chart.js/auto';

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

  // 1) Holdings Allocation Chart
  const chartData = {
    labels: summary.holdings_percentages.map(item => item.Symbol),
    datasets: [{
      data: summary.holdings_percentages.map(item => item.percent),
      backgroundColor: colors.slice(0, summary.holdings_percentages.length),
      borderWidth: 1,
    }],
  };

  //  2) Holdings by Type (ETF vs Stocks)
  const quoteTypeColors = ['#4e73df', '#1cc88a', '#f6c23e', '#e74a3b'];
  const quoteTypeChartData = {
    labels: Object.keys(summary.quote_type_split || {}),
    datasets: [{
      data: Object.values(summary.quote_type_split || {}),
      backgroundColor: quoteTypeColors.slice(0, Object.keys(summary.quote_type_split || {}).length),
      borderWidth: 1,
    }],
  };

  const chartOptions = {
    plugins: {
      legend: { position: 'bottom', labels: { boxWidth: 20 } },
      tooltip: {
        callbacks: {
          label: function (context) {
            const symbol = context.label;
            const percent = context.parsed.toFixed(2);
            const index = context.dataIndex;
            const currentValue = summary.holdings_percentages[index]?.['Current Value'];
            if (currentValue !== undefined) {
              return `${symbol}: ${percent}% ($${currentValue.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })})`;
            }
            return `${symbol}: ${percent}%`;
          },
        },
      },
    },
  };

  // ✅ Separate options for quote type pie chart
  const quoteTypeChartOptions = {
    plugins: {
      legend: { position: 'bottom', labels: { boxWidth: 20 } },
      tooltip: {
        callbacks: {
          label: function (context) {
            const value = context.parsed;
            const total = context.chart._metasets[0].total;
            const percent = total > 0 ? (value / total * 100).toFixed(2) : '0.00';
            return `${context.label}: ${percent}% ($${value.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })})`;
          },
        },
      },
    },
  };

  const formatNumber = (num) => {
    if (typeof num === 'number') {
      return num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
    return num;
  };

  return (
    <div className="container">
      <h1 className="mb-4 text-center">📊 Portfolio Summary</h1>
      <div className="row">
        {/* Chart 1: Holdings Allocation */}
        <div className="col-lg-6 mb-4">
          <div className="card shadow">
            <div className="card-body">
              <h5 className="card-title">Stock Allocation</h5>
              <Pie data={chartData} options={chartOptions} />
            </div>
          </div>
        </div>

        {/*  Chart 2: Holdings by Type */}
        <div className="col-lg-6 mb-4">
          <div className="card shadow">
            <div className="card-body">
              <h5 className="card-title">Holdings by Type</h5>
              <Pie data={quoteTypeChartData} options={quoteTypeChartOptions} />
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="col-lg-12 mb-4">
          <div className="card shadow">
            <div className="card-body">
              <h5 className="card-title">Key Metrics</h5>
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

      {/* Holdings Table */}
      <div className="card shadow mt-4">
        <div className="card-body">
          <h5 className="card-title">Holdings Breakdown</h5>
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
