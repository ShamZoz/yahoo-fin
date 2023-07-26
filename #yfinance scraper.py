#yfinance scraper 
import yfinance as yf

def get_stock_data():
    try:
        # Apple Inc. (AAPL) stock data
        aapl_data = yf.Ticker("AAPL").history(period="2mo")

        # S&P 500 index stock data
        sp500_data = yf.Ticker("^GSPC").history(period="2mo")
        

        return aapl_data, sp500_data
    except Exception as e:
        print("Failed to fetch stock data:", e)
        return None, None

if __name__ == "__main__":
    aapl_data, sp500_data,= get_stock_data()

    if aapl_data is not None and sp500_data is not None:
        print("Apple Inc. (AAPL) Stock Data:")
        print(aapl_data)

        print("\nS&P 500 Index Stock Data:")
        print(sp500_data)
    else:
        print("Failed to fetch stock data.")
