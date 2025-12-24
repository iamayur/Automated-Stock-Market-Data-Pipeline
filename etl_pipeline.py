import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# --- CONFIGURATION ---
# 1. Load variables from the .env file
load_dotenv() 

# 2. Get the URL securely (returns None if not found)
DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")

# Safety check to ensure it loaded correctly
if not DB_CONNECTION_URL:
    raise ValueError("Database URL not found. Did you create the .env file?")



# --- 1. EXTRACT (Get data from the internet) ---
def extract_stock_data(symbol):
    print(f"Extracting data for {symbol}...")
    # 'period="1y"' gets the last year of data.
    # 'auto_adjust=True' fixes historical prices for splits/dividends.
    data = yf.download(symbol, period="1y", auto_adjust=True)
    return data

# --- 2. TRANSFORM (Clean and format data) ---
def transform_data(df, symbol):
    print("Transforming data...")

    # 1. Reset index so 'Date' becomes a normal column
    df = df.reset_index()
    
    # 2. Fix Column Names (The "MultiIndex" issue)
    # yfinance returns columns like ('Close', 'AAPL'). We just want 'Close'.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    # 3. Select and Rename
    # Ensure these columns exist before selecting
    df = df[['Date', 'Close', 'Volume']]
    df.columns = ['date', 'close_price', 'volume']
    
    # 4. Add the Ticker Symbol
    df['ticker_symbol'] = symbol
    
    # 5. Drop empty rows
    df = df.dropna()
    
    return df

# --- 3. LOAD (Save to Cloud Database) ---
def load_data_to_postgres(df, table_name):
    print(f"Loading {len(df)} rows to NeonDB...")
    
    # Create the connection engine
    engine = create_engine(DB_CONNECTION_URL)
    
    # 'if_exists="replace"' creates the table automatically
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    
    print("Success! Data loaded to Cloud Database.")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # A. Extract
    ticker = "AAPL" # Apple Stock
    raw_data = extract_stock_data(ticker)
    
    # B. Transform
    clean_data = transform_data(raw_data, ticker)
    
    # C. Load
    load_data_to_postgres(clean_data, "stock_prices")