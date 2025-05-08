from tkinter import *
from tkinter import messagebox, filedialog, simpledialog
import stock_data
from stock_class import Stock
from utilities import *
import csv

class StockApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("KM Stock Application")
        self.root.geometry("1000x600")
        self.root.configure(bg="#cce6ff") 

        self.stocks = []
        self.logs = []

        self.setup_layout()
        self.root.mainloop()

    def setup_layout(self):
        Label(self.root, text="KM Stock Book", font=("Arial", 18, "bold"), bg="#cce6ff").grid(row=0, column=0, columnspan=4, pady=10)

        Label(self.root, text="Stock List", font=("Arial", 14, "bold"), bg="#cce6ff").grid(row=1, column=0, sticky=W, padx=10)
        self.stock_listbox = Listbox(self.root, height=25, width=30)
        self.stock_listbox.grid(row=2, column=0, rowspan=10, padx=10, sticky=N)
        self.stock_listbox.bind("<<ListboxSelect>>", self.show_info)

        Label(self.root, text="Add Stock", font=("Arial", 12, "bold"), bg="#cce6ff").grid(row=1, column=1, columnspan=2, sticky=W, pady=5)
        Label(self.root, text="Ticker Symbol:", bg="#cce6ff").grid(row=2, column=1, sticky=E)
        self.entry_symbol = Entry(self.root)
        self.entry_symbol.grid(row=2, column=2)

        Label(self.root, text="Name:", bg="#cce6ff").grid(row=3, column=1, sticky=E)
        self.entry_name = Entry(self.root)
        self.entry_name.grid(row=3, column=2)

        Label(self.root, text="Shares:", bg="#cce6ff").grid(row=4, column=1, sticky=E)
        self.entry_shares = Entry(self.root)
        self.entry_shares.grid(row=4, column=2)

        Button(self.root, text="Add", width=15, command=self.add_stock).grid(row=5, column=1, columnspan=2, pady=5)

        Label(self.root, text="Update Shares", font=("Arial", 12, "bold"), bg="#cce6ff").grid(row=6, column=1, columnspan=2, sticky=W, pady=5)
        Label(self.root, text="Amount:", bg="#cce6ff").grid(row=7, column=1, sticky=E)
        self.entry_update = Entry(self.root)
        self.entry_update.grid(row=7, column=2)

        Button(self.root, text="Buy", width=10, command=self.buy_shares).grid(row=8, column=1, pady=2)
        Button(self.root, text="Sell", width=10, command=self.sell_shares).grid(row=8, column=2, pady=2)
        Button(self.root, text="Delete Stock", command=self.delete_stock).grid(row=9, column=1, columnspan=2, pady=5)

        Label(self.root, text="Web Data", font=("Arial", 12, "bold"), bg="#cce6ff").grid(row=10, column=1, columnspan=2, pady=(10, 2))
        Button(self.root, text="Scrape Data from Yahoo...!", command=self.scrape_data).grid(row=11, column=1, columnspan=2, pady=2)
        Button(self.root, text="Import CSV", command=self.import_csv).grid(row=12, column=1, columnspan=2, pady=2)

        Button(self.root, text="Show Chart", command=self.show_chart).grid(row=13, column=1, columnspan=2, pady=10)
        Button(self.root, text="Transaction Report", command=self.show_log).grid(row=14, column=1, columnspan=2)

        self.info_box = Text(self.root, width=60, height=20, font=("Courier", 10))
        self.info_box.grid(row=2, column=3, rowspan=10, padx=10, pady=5)

    def add_stock(self):
        try:
            symbol = self.entry_symbol.get().upper()
            name = self.entry_name.get()
            shares = float(self.entry_shares.get())
            stock = Stock(symbol, name, shares)
            self.stocks.append(stock)
            self.stock_listbox.insert(END, symbol)
            self.entry_symbol.delete(0, END)
            self.entry_name.delete(0, END)
            self.entry_shares.delete(0, END)
        except:
            messagebox.showerror("Error", "Please enter valid stock details!!!")

    def show_info(self, event):
        self.info_box.delete("1.0", END)
        if not self.stock_listbox.curselection():
            return
        symbol = self.stock_listbox.get(self.stock_listbox.curselection())
        for stock in self.stocks:
            if stock.symbol == symbol:
                self.info_box.insert(END, f"{stock.name} ({stock.symbol})\nShares: {stock.shares}\n")
                for d in stock.history:  
                    self.info_box.insert(END, f"{d.date.strftime('%m/%d/%y')} - ${d.close:.2f} - Vol: {int(d.volume)}\n")

    def buy_shares(self):
        self._update_shares(buy=True)

    def sell_shares(self):
        self._update_shares(buy=False)

    def _update_shares(self, buy):
        if not self.stock_listbox.curselection():
            return
        try:
            amount = float(self.entry_update.get())
            symbol = self.stock_listbox.get(self.stock_listbox.curselection())
            for stock in self.stocks:
                if stock.symbol == symbol:
                    if buy:
                        stock.buy(amount)
                        self.logs.append(f"Bought {amount} shares of {symbol}")
                    else:
                        stock.sell(amount)
                        self.logs.append(f"Sold {amount} shares of {symbol}")
                    self.show_info(None)
        except:
            messagebox.showerror("Error", "Invalid number.")

    def delete_stock(self):
        if not self.stock_listbox.curselection():
            return
        index = self.stock_listbox.curselection()[0]
        del self.stocks[index]
        self.stock_listbox.delete(index)
        self.info_box.delete("1.0", END)

    def scrape_data(self):
        start = simpledialog.askstring("Start Date", "Enter start date (m/d/yy):")
        end = simpledialog.askstring("End Date", "Enter end date (m/d/yy):")
        try:
            stock_data.retrieve_stock_web(start, end, self.stocks)
            self.show_info(None)
            messagebox.showinfo("Done", "Web data retrieved.")
        except:
            messagebox.showerror("Error", "Failed to retrieve from web.")

    def import_csv(self):
        if not self.stock_listbox.curselection():
            return
        symbol = self.stock_listbox.get(self.stock_listbox.curselection())
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            stock_data.import_stock_web_csv(self.stocks, symbol, file_path)
            self.show_info(None)
            messagebox.showinfo("Import Complete", f"CSV imported for {symbol}")

    def show_chart(self):
        if not self.stock_listbox.curselection():
            return
        symbol = self.stock_listbox.get(self.stock_listbox.curselection())
        show_price_chart(self.stocks, symbol) 

    def show_log(self):
        self.info_box.delete("1.0", END)
        if not self.logs:
            self.info_box.insert(END, "No transactions yet.")
        else:
            self.info_box.insert(END, "Transaction Log:\n")
            for entry in self.logs:
                self.info_box.insert(END, entry + "\n")

if __name__ == "__main__":
    StockApp()
