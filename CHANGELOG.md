# 📈 Portfolio Tracker API - Changelog

All notable changes to this project will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/) and [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.0.1] - 2025-06-29

### 🚀 Added
- ✅ Initial FastAPI backend server with hot-reload via WatchFiles.
- 📂 Upload endpoint for portfolio CSV files, parsing stock tickers automatically.
- 🌍 Automatic market detection (`US`) from CSV content.
- 📈 Fetch current prices using `yfinance`; log symbols that may be delisted.
- 💰 Calculate and serve unrealized profit for each position.
- 🔗 `/data_json` endpoint to deliver processed portfolio data as JSON.
- 🗑️ `/clear_transactions` endpoint to reset all uploaded transactions.
- 🛡️ Enabled CORS middleware for local frontend dev.
- 📄 Basic README with setup instructions and API usage.

### Unrealeased
- Additional analysis charts and UI improvements are planned for future releases.

### 🐛 Fixed
- N/A (Initial release).

### 🗑️ Removed
- N/A

### ⚠️ Deprecated
- Nothing deprecated yet.

### 🔒 Security
- No security updates yet.

---

## 📌 Format

✨ This project uses **Semantic Versioning** for clear version bumps.  
📚 Changelog is maintained using [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

Happy tracking! 📊🚀
