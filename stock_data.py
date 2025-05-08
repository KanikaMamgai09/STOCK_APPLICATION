import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time
from utilities import clear_console, sort_stock_history_by_date
from stock_class import Stock, DailyEntry

# Create the SQLite database for stocks and their history
def create_database():
    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            symbol TEXT PRIMARY KEY,
            name TEXT,
            shares REAL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS dailyData (
            symbol TEXT NOT NULL,
            date TEXT NOT NULL,
            price REAL NOT NULL,
            volume REAL NOT NULL,
            PRIMARY KEY (symbol, date)
        );
    """)

    conn.commit()
    conn.close()

# Save stock objects and their history to the database
def save_stock_data(stock_list):
    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()

    for stock in stock_list:
        try:
            cur.execute("INSERT OR REPLACE INTO stocks (symbol, name, shares) VALUES (?, ?, ?);",
                        (stock.symbol, stock.name, stock.shares))
        except Exception as e:
            print(f"[ERROR] Saving stock {stock.symbol}: {e}")

        for record in stock.history:
            try:
                cur.execute("INSERT OR REPLACE INTO dailyData (symbol, date, price, volume) VALUES (?, ?, ?, ?);",
                            (stock.symbol, record.date.strftime("%m/%d/%y"), record.close, record.volume))
            except Exception as e:
                print(f"[ERROR] Saving data for {stock.symbol} on {record.date}: {e}")

    conn.commit()
    conn.close()

# Loading stock data from database
def load_stock_data(stock_list):
    stock_list.clear()
    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()

    cur.execute("SELECT symbol, name, shares FROM stocks;")
    for symbol, name, shares in cur.fetchall():
        stock = Stock(symbol, name, shares)
        cur2 = conn.cursor()
        cur2.execute("SELECT date, price, volume FROM dailyData WHERE symbol = ?;", (symbol,))
        for row in cur2.fetchall():
            try:
                date = datetime.strptime(row[0], "%m/%d/%y")
                price = float(row[1])
                volume = float(row[2])
                stock.add_entry(DailyEntry(date, price, volume))
            except Exception as e:
                print(f"Reading row is generating an ERROR {row}: {e}")
        stock_list.append(stock)

    conn.close()
    sort_stock_history_by_date(stock_list)

# Scrape data from Yahoo! Finance
def retrieve_stock_web(date_start, date_end, stock_list):
    start_unix = str(int(time.mktime(time.strptime(date_start, "%m/%d/%y"))))
    end_unix = str(int(time.mktime(time.strptime(date_end, "%m/%d/%y"))))
    total_records = 0

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)

        for stock in stock_list:
            url = f"https://finance.yahoo.com/quote/{stock.symbol}/history?period1={start_unix}&period2={end_unix}&interval=1d&filter=history&frequency=1d"
            print(f"Scraping: {url}")
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")

            rows = soup.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                values = [cell.text.strip() for cell in cells]
                if len(values) == 7:
                    try:
                        parsed_date = datetime.strptime(values[0].strip()[:12], "%b %d, %Y")
                        price = float(values[5].replace(",", ""))
                        volume = float(values[6].replace(",", ""))
                        daily_entry = DailyEntry(parsed_date, price, volume)
                        stock.add_entry(daily_entry)
                        total_records += 1
                    except Exception as e:
                        print(f"Could not parse: {values} — {e}")
                        continue
            print(f"Done: {stock.symbol} - {total_records} entries added.")

    except Exception as e:
        raise RuntimeError(f"Web scraping failed: {e}")
    finally:
        if driver:
            driver.quit()

    return total_records

# Loading data from a Yahoo! Finance CSV file
def import_stock_web_csv(stock_list, symbol, filename):
    for stock in stock_list:
        if stock.symbol == symbol:
            try:
                with open(filename, newline='') as f:
                    reader = csv.reader(f)
                    next(reader) 
                    for row in reader:
                        try:
                            date = datetime.strptime(row[0], "%Y-%m-%d")
                            close = float(row[4])
                            volume = float(row[6])
                            stock.add_entry(DailyEntry(date, close, volume))
                        except Exception as e:
                            print(f"[ERROR] Skipped row: {e}")
            except FileNotFoundError:
                print(f"File not found: {filename}")

def main():
    clear_console()
    print("stock_data.py ready for use.")

if __name__ == "__main__":
    main()
