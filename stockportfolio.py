import yfinance as yf
import tkinter as tk
class StockPortfolioTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")

        self.portfolio = {}

        self.label = tk.Label(root, text="Welcome to Stock Portfolio Tracker", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Stock", command=self.add_stock)
        self.add_button.grid(row=1, column=0, padx=10, pady=10)

        self.remove_button = tk.Button(root, text="Remove Stock", command=self.remove_stock)
        self.remove_button.grid(row=1, column=1, padx=10, pady=10)

        self.view_button = tk.Button(root, text="View Portfolio", command=self.view_portfolio)
        self.view_button.grid(row=2, column=0, padx=10, pady=10)

        self.track_button = tk.Button(root, text="Track Performance", command=self.track_performance)
        self.track_button.grid(row=2, column=1, padx=10, pady=10)

    def add_stock(self):
        add_window = tk.Toplevel()
        add_window.title("Add Stock")

        symbol_label = tk.Label(add_window, text="Enter stock symbol: ")
        symbol_label.grid(row=0, column=0, padx=10, pady=5)

        self.symbol_entry = tk.Entry(add_window)
        self.symbol_entry.grid(row=0, column=1, padx=10, pady=5)

        quantity_label = tk.Label(add_window, text="Enter quantity: ")
        quantity_label.grid(row=1, column=0, padx=10, pady=5)

        self.quantity_entry = tk.Entry(add_window)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=5)

        add_button = tk.Button(add_window, text="Add Stock", command=self.confirm_add)
        add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def confirm_add(self):
        symbol = self.symbol_entry.get()
        quantity = int(self.quantity_entry.get())
        self.add_stock_to_portfolio(symbol, quantity)
        self.update_portfolio()
        self.symbol_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def add_stock_to_portfolio(self, symbol, quantity):
        if symbol in self.portfolio:
            self.portfolio[symbol]['Quantity'] += quantity
        else:
            self.portfolio[symbol] = {'Quantity': quantity, 'Average Cost': None}

    def remove_stock(self):
        remove_window = tk.Toplevel()
        remove_window.title("Remove Stock")

        symbol_label = tk.Label(remove_window, text="Enter stock symbol to remove: ")
        symbol_label.grid(row=0, column=0, padx=10, pady=5)

        self.symbol_entry = tk.Entry(remove_window)
        self.symbol_entry.grid(row=0, column=1, padx=10, pady=5)

        quantity_label = tk.Label(remove_window, text="Enter quantity to sell: ")
        quantity_label.grid(row=1, column=0, padx=10, pady=5)

        self.quantity_entry = tk.Entry(remove_window)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=5)

        remove_button = tk.Button(remove_window, text="Remove Stock", command=self.confirm_remove)
        remove_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def confirm_remove(self):
        symbol = self.symbol_entry.get()
        quantity = int(self.quantity_entry.get())
        self.remove_stock_from_portfolio(symbol, quantity)
        self.update_portfolio()
        self.symbol_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def remove_stock_from_portfolio(self, symbol, quantity):
        if symbol in self.portfolio:
            if self.portfolio[symbol]['Quantity'] >= quantity:
                self.portfolio[symbol]['Quantity'] -= quantity
                if self.portfolio[symbol]['Quantity'] == 0:
                    del self.portfolio[symbol]
            else:
                print("Error: Insufficient quantity to sell.")
        else:
            print("Error: Stock not found in portfolio.")

    def view_portfolio(self):
        view_window = tk.Toplevel()
        view_window.title("View Portfolio")

        portfolio_label = tk.Label(view_window, text="Stock Portfolio:")
        portfolio_label.grid(row=0, column=0, padx=10, pady=5)

        for i, (symbol, details) in enumerate(self.portfolio.items(), start=1):
            portfolio_info = f"Symbol: {symbol}, Quantity: {details['Quantity']}, Average Cost: {details['Average Cost']}"
            tk.Label(view_window, text=portfolio_info).grid(row=i, column=0, padx=10, pady=5)

    def track_performance(self):
        total_investment = 0
        current_value = 0
        for symbol, details in self.portfolio.items():
            if details['Average Cost'] is not None:
                total_investment += details['Quantity'] * details['Average Cost']
                stock_data = yf.Ticker(symbol).history(period="1d")
                if len(stock_data) > 0:
                    current_value += details['Quantity'] * stock_data['Close'].iloc[-1]
        if total_investment > 0:
            profit_loss = current_value - total_investment
            performance_window = tk.Toplevel()
            performance_window.title("Track Performance")
            tk.Label(performance_window, text=f"Total Investment: {total_investment}").pack()
            tk.Label(performance_window, text=f"Current Value: {current_value}").pack()
            tk.Label(performance_window, text=f"Profit/Loss: {profit_loss}").pack()
        else:
            print("No investments in the portfolio.")

    def update_portfolio(self):
        for symbol in self.portfolio:
            stock_data = yf.Ticker(symbol).history(period="1d")
            if len(stock_data) > 0:
                close_price = stock_data['Close'].iloc[-1]
                if self.portfolio[symbol]['Quantity'] > 0:
                    if self.portfolio[symbol]['Average Cost'] is None:
                        self.portfolio[symbol]['Average Cost'] = close_price
                    else:
                        self.portfolio[symbol]['Average Cost'] = (self.portfolio[symbol]['Average Cost'] +
                                                                  close_price) / 2

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    tracker = StockPortfolioTracker(root)
    tracker.run()