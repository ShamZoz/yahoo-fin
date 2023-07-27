import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def get_stock_data(stock_tickers, period):
    try:
        stock_data = {}

        for ticker in stock_tickers:
            data = yf.Ticker(ticker).history(period=period)
            stock_data[ticker] = data

        return stock_data
    except Exception as e:
        print("Failed to fetch stock data:", e)
        return None

def calculate_metrics(stock_data):
    try:
        for ticker, data in stock_data.items():
            data['MA_50'] = data['Close'].rolling(window=50).mean()
            data['MA_200'] = data['Close'].rolling(window=200).mean()
            data['Daily_Return'] = data['Close'].pct_change()
            data['Volatility'] = data['Daily_Return'].rolling(window=20).std() * np.sqrt(252)

        return stock_data
    except Exception as e:
        print("Failed to calculate metrics:", e)
        return None

def visualize_data(stock_data):
    try:
        plt.figure(figsize=(12, 8))
        for ticker, data in stock_data.items():
            plt.plot(data.index, data['Close'], label=ticker)
        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.title('Stock Prices')
        plt.legend()
        plt.show()

        plt.figure(figsize=(12, 8))
        for ticker, data in stock_data.items():
            plt.plot(data.index, data['Volatility'], label=ticker)
        plt.xlabel('Date')
        plt.ylabel('Volatility')
        plt.title('Volatility (20-Day Rolling)')
        plt.legend()
        plt.show()
    except Exception as e:
        print("Failed to visualize data:", e)

def fetch_data_and_visualize():
    stock_tickers = tickers_entry.get().split(",")
    period = period_entry.get()

    if not all(stock_tickers) or not period:
        messagebox.showerror("Error", "Please enter valid stock tickers and time period.")
        return

    stock_data = get_stock_data(stock_tickers, period)

    if not stock_data:
        messagebox.showerror("Error", "Failed to fetch stock data. Please check the stock tickers and try again.")
        return

    stock_data_with_metrics = calculate_metrics(stock_data)
    if not stock_data_with_metrics:
        messagebox.showerror("Error", "Failed to calculate metrics.")
        return

    visualize_data(stock_data_with_metrics)

# Create the main application window
app = tk.Tk()
app.title("Stock Data Visualization")

# Create widgets
tickers_label = ttk.Label(app, text="Enter stock tickers separated by commas (e.g., AAPL,MSFT,GOOGL):")
tickers_entry = ttk.Entry(app, width=50)

period_label = ttk.Label(app, text="Enter time period (e.g., '1mo', '3mo', '1y'):")
period_entry = ttk.Entry(app, width=50)

fetch_button = ttk.Button(app, text="Fetch Data and Visualize", command=fetch_data_and_visualize)

# Pack widgets
tickers_label.pack(pady=5)
tickers_entry.pack(pady=5)

period_label.pack(pady=5)
period_entry.pack(pady=5)

fetch_button.pack(pady=10)

# Start the main event loop
app.mainloop()
