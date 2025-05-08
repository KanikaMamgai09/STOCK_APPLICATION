from datetime import datetime
from stock_class import Stock, DailyEntry
from utilities import clear_console, show_price_chart, sort_stocks_by_symbol, sort_stock_history_by_date
from os import path
import stock_data

def show_main_menu(stocks):
    choice = ""
    while choice != "0":
        clear_console()
        print("=== KM Stock Application ===")
        print("1 - Portfolio Management")
        print("2 - Enter Daily Price Data")
        print("3 - View Report")
        print("4 - Plot Price Chart")
        print("5 - Save / Load / Import")
        print("0 - Quit")
        choice = input("Select an option: ")
        if choice == "1":
            manage_portfolio(stocks)
        elif choice == "2":
            add_daily_info(stocks)
        elif choice == "3":
            print_report(stocks)
        elif choice == "4":
            plot_chart(stocks)
        elif choice == "5":
            data_options(stocks)

def manage_portfolio(stocks):
    action = ""
    while action != "0":
        clear_console()
        print("=== Portfolio Menu ===")
        print("1 - Add New Stock")
        print("2 - Modify Share Count")
        print("3 - Remove Stock")
        print("4 - Show All Stocks")
        print("0 - Back to Main Menu")
        action = input("Choose action: ")
        if action == "1":
            create_stock(stocks)
        elif action == "2":
            modify_shares(stocks)
        elif action == "3":
            remove_stock(stocks)
        elif action == "4":
            list_all_stocks(stocks)

def create_stock(stocks):
    symbol = input("Enter ticker symbol: ").upper()
    name = input("Company name: ")
    try:
        shares = float(input("Number of shares: "))
        new_stock = Stock(symbol, name, shares)
        stocks.append(new_stock)
        sort_stocks_by_symbol(stocks)
    except:
        print("Invalid input for shares.")

def modify_shares(stocks):
    list_all_stocks(stocks)
    target = input("Enter ticker symbol to update: ").upper()
    for s in stocks:
        if s.symbol == target:
            action = input("Buy or Sell? (b/s): ").lower()
            try:
                qty = float(input("Enter amount: "))
                if action == "b":
                    s.buy(qty)
                elif action == "s":
                    s.sell(qty)
            except:
                print("Invalid quantity.")
            return
    print("Ticker Symbol not found.")

def remove_stock(stocks):
    list_all_stocks(stocks)
    target = input("Enter ticker symbol to remove: ").upper()
    stocks[:] = [s for s in stocks if s.symbol != target]

def list_all_stocks(stocks):
    print("\nYour Portfolio:")
    for s in stocks:
        print(f"{s.symbol} - {s.name} ({s.shares} shares)")

def add_daily_info(stocks):
    list_all_stocks(stocks)
    ticker = input("Enter ticker symbol: ").upper()
    for s in stocks:
        if s.symbol == ticker:
            try:
                date_input = input("Date (m/d/yy): ")
                date_obj = datetime.strptime(date_input, "%m/%d/%y")
                price = float(input("Closing price: "))
                volume = float(input("Volume: "))
                daily = DailyEntry(date_obj, price, volume)
                s.add_entry(daily)
                sort_stock_history_by_date(stocks)
            except:
                print("Invalid input. Try again.")
            return
    print("Ticker symbol not found.")

def print_report(stocks):
    for s in stocks:
        print(f"\n=== {s.symbol} - {s.name} ===")
        for d in s.history:
            print(f"{d.date.strftime('%m/%d/%y')} | Close: ${d.close:.2f} | Volume: {int(d.volume)}")

def plot_chart(stocks):
    ticker = input("Enter ticker symbol to view chart: ").upper()
    show_price_chart(stocks, ticker)

def data_options(stocks):
    print("\n1 - Save to DB")
    print("2 - Load from DB")
    print("3 - Get Data Online")
    print("4 - Load CSV File")
    choice = input("Select an option: ")
    if choice == "1":
        stock_data.save_stock_data(stocks)
    elif choice == "2":
        stock_data.load_stock_data(stocks)
    elif choice == "3":
        fetch_from_web(stocks)
    elif choice == "4":
        load_csv(stocks)

def fetch_from_web(stocks):
    start = input("Start date (m/d/yy): ")
    end = input("End date (m/d/yy): ")
    try:
        count = stock_data.retrieve_stock_web(start, end, stocks)
        print(f"{count} records downloaded.")
    except Exception as err:
        print(f"Something went wrong: {err}")

def load_csv(stocks):
    ticker = input("Ticker to load CSV for: ").upper()
    filepath = input("Path to CSV file: ")
    stock_data.import_stock_web_csv(stocks, ticker, filepath)

def main():
    if not path.exists("stocks.db"):
        stock_data.create_database()
    portfolio = []
    show_main_menu(portfolio)

if __name__ == "__main__":
    main()
