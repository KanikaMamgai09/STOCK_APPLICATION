from datetime import datetime

# Represents a stock with basic information and a history of daily data
class Stock:
    def __init__(self, ticker, company_name, quantity):
        self._ticker = ticker
        self._company_name = company_name
        self._quantity = quantity
        self.history = []  # Holds DailyEntry objects

    @property
    def symbol(self):
        return self._ticker

    @symbol.setter
    def symbol(self, value):
        raise RuntimeWarning("Stock symbol cannot be changed once set.")

    @property
    def name(self):
        return self._company_name

    @name.setter
    def name(self, value):
        self._company_name = value

    @property
    def shares(self):
        return self._quantity

    @shares.setter
    def shares(self, value):
        raise RuntimeWarning("Use buy() or sell() methods to update share count.")

    def buy(self, amount):
        self._quantity += amount

    def sell(self, amount):
        self._quantity -= amount

    def add_entry(self, daily_record):
        self.history.append(daily_record)


# Represents daily trading information for a stock
class DailyEntry:
    def __init__(self, date, closing_price, volume):
        self._date = date
        self._closing_price = closing_price
        self._volume = volume

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def close(self):
        return self._closing_price

    @close.setter
    def close(self, value):
        self._closing_price = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value


# --- Simple Unit Test to Validate Stock Class ---
def main():
    issues = []

    print("Starting Stock Class Tests")

    # Test stock creation
    try:
        stock = Stock("DEMO", "Demo Corp", 100)
        print("Created stock successfully.")
    except:
        print("Could not create stock.")
        issues.append("Stock constructor failed.")

    # Test ticker immutability
    try:
        stock.symbol = "NEW"
        print("Symbol changed. Should be read-only.")
        issues.append("Ticker symbol change allowed (should be blocked).")
    except:
        print("Ticker symbol change blocked.")

    # Test name update
    try:
        stock.name = "New Demo Corp"
        if stock.name == "New Demo Corp":
            print("Company name updated.")
        else:
            print("Company name not updated correctly.")
            issues.append("Name update failed.")
    except:
        print("Error updating company name.")
        issues.append("Name setter exception.")

    # Test shares update (should be blocked)
    try:
        stock.shares = 999
        print("Direct shares update allowed.")
        issues.append("Shares should only be updated via buy/sell.")
    except:
        print("Direct shares update blocked.")

    # Test buy and sell
    stock.buy(50)
    if stock.shares != 150:
        print("Buy operation failed.")
        issues.append("Buy method failed.")
    else:
        print("Buy operation passed.")

    stock.sell(25)
    if stock.shares != 125:
        print("Sell operation failed.")
        issues.append("Sell method failed.")
    else:
        print("Sell operation passed.")

    # Test adding daily entry
    try:
        entry = DailyEntry(datetime.strptime("1/1/20", "%m/%d/%y"), 14.50, 100000)
        stock.add_entry(entry)

        if stock.history[0].date != datetime.strptime("1/1/20", "%m/%d/%y"):
            issues.append("Incorrect date in daily record.")
        if stock.history[0].close != 14.50:
            issues.append("Incorrect closing price.")
        if stock.history[0].volume != 100000:
            issues.append("Incorrect volume.")
        print("Daily entry added and verified.")
    except:
        print("Error adding daily stock entry.")
        issues.append("add_entry method failed.")

    # Test summary
    print("\nTest Results")
    if not issues:
        print("All tests passed!")
    else:
        for issue in issues:
            print("⚠️", issue)

# Run unit test if file is executed
if __name__ == "__main__":
    main()
