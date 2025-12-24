# 📈 Automated Stock Market ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-NeonDB-336791)
![GitHub Actions](https://img.shields.io/badge/Tools-GitHub%20Actions-2088FF)
![Pandas](https://img.shields.io/badge/Library-Pandas-150458)

## 📖 Project Overview
This project is an end-to-end **Data Engineering pipeline** that extracts stock market data for tech companies (e.g., Apple), cleans and transforms the data using Python, and loads it into a cloud-based **PostgreSQL** database.

The entire process is fully automated using **GitHub Actions**, which triggers the ETL script daily at 6:00 AM UTC, ensuring the database is always up-to-date without manual intervention.

## 🏗️ Architecture
**Extract** $\rightarrow$ **Transform** $\rightarrow$ **Load** $\rightarrow$ **Automate**

1.  **Extract:** Python script hits the **Yahoo Finance API** to fetch the latest daily stock data (Open, Close, Volume).
2.  **Transform:** **Pandas** is used to:
    * Clean column names.
    * Handle missing values.
    * Format dates and data types for SQL compatibility.
3.  **Load:** **SQLAlchemy** connects to a remote **NeonDB (PostgreSQL)** instance and inserts the processed data.
4.  **Automation:** A **GitHub Actions** YAML workflow spins up an Ubuntu container, installs dependencies, and runs the pipeline on a Cron schedule.

## 🛠️ Tech Stack
* **Language:** Python 3.11
* **Cloud Database:** NeonDB (Serverless PostgreSQL)
* **Orchestration:** GitHub Actions (CI/CD)
* **Libraries:** `pandas`, `yfinance`, `sqlalchemy`, `psycopg2`
* **Security:** Environment Variables (for DB credentials)

## 🚀 How to Run Locally

If you want to run this pipeline on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables:**
    * Create a `.env` file in the root directory.
    * Add your database connection string:
    ```ini
    DB_CONNECTION_URL=postgresql+psycopg2://user:password@host/dbname?sslmode=require
    ```

4.  **Run the ETL script:**
    ```bash
    python etl_pipeline.py
    ```

## 🤖 Automation Details
The workflow is defined in `.github/workflows/daily_etl.yml`.
* **Trigger:** Schedule `cron: '0 6 * * *'` (Daily at 6 AM).
* **Secrets:** Database credentials are stored securely in GitHub Secrets (`DB_CONNECTION_URL`), keeping sensitive data out of the codebase.

## 📊 SQL Verification
Once data is loaded, you can verify it in PostgreSQL:

```sql
SELECT * FROM stock_prices ORDER BY date DESC LIMIT 5;
