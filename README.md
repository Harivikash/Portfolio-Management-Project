# Portfolio Management Project

This is a portfolio management application that allows users to track their investments in various financial instruments. The application fetches real-time data from Yahoo Finance and calculates the unrealized profit for each investment in the portfolio.

## Features

* Upload a CSV of your transactions, including stock symbols and quantities.(The csv parser only parse the particular csv format. csv_parser.py can be edited to parse data from different formats.)
* Automatically fetch the latest price for each stock from Yahoo Finance.
* Calculate the unrealized profit of each stock in the portfolio.
* View the portfolio data in JSON format, including calculated unrealized profits.

## Technologies Used

* **Backend**: FastAPI (Python)
* **Frontend**: React + Vite
* **Data Fetching**: Yahoo Finance API via `yfinance`
* **Libraries**: Pandas, Numpy

## Setup Instructions

### 1. Clone the repository

Clone the repository to your local machine.

```bash
git clone <repository_url>
cd <project_folder>
```

### 2. Install Dependencies

Create a virtual environment and install the required dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Run the Application

After the dependencies are installed, you can start the FastAPI server.

```bash
uvicorn main:app --reload
```

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 4. Endpoints

#### POST `/upload`

* **Description**: Upload a CSV file containing transaction data. The file must include columns for stock symbols and quantities.
* **Request body**: `multipart/form-data` with a CSV file.

#### DELETE `/clear_transactions`

* **Description**: Clear all uploaded transactions.

#### GET `/data_json`

* **Description**: Get the current portfolio data in JSON format, including the calculated unrealized profits for each stock.

### 5. Example CSV

The CSV file should have the following format:

``
Side| Symbol| Name| Order Price| Order Qty| Order| Amount| Filled| Markets| Currency| Fill Qty| Fill Price| Fill Amount| Fill Time|Fees Total

``

### 6. Errors & Logging

* The system will log potential errors, such as **delisted stocks** or missing data from Yahoo Finance.
* A **500 Internal Server Error** is logged if any issues arise when processing the data.

### 7. Possible Improvements

* Adding database support to persist user transactions.
* Integrating with other financial data sources for better reliability.
* Providing user authentication for a more personalized experience.

---

# Portfolio-Management-Project
