import os
import platform
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Clear the console screen based on the operating system
def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Sort the stock list alphabetically by symbol
def sort_stocks_by_symbol(stock_list):
    stock_list.sort(key=lambda stock: stock.symbol)

# Sort each stock's history list by date (oldest to newest)
def sort_stock_history_by_date(stock_list):
    for stock in stock_list:
        stock.history.sort(key=lambda record: record.date)

# Show a simple price chart (line plot) for a specific stock
def show_price_chart(stock_list, symbol):
    for stock in stock_list:
        if stock.symbol.lower() == symbol.lower():
            if not stock.history:
                print(f"No historical data for {symbol}")
                return

            # Sort history by date to ensure correct plotting
            stock.history.sort(key=lambda record: record.date)
            dates = [r.date for r in stock.history]
            prices = [r.close for r in stock.history]

            plt.figure(figsize=(10, 5))
            plt.plot(dates, prices, marker='o', linestyle='-', label=symbol.upper())
            plt.title(f"{symbol.upper()} Price Chart")
            plt.xlabel("Date")
            plt.ylabel("Close Price ($)")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.tight_layout()
            plt.legend()
            plt.show()
            return

    print(f"{symbol} not found in your stock list.")
