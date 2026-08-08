def get_stock_prices(symbol):
    import yfinance as yf
    ticker = yf.Ticker(symbol)
    info = ticker.info
    current_price = info.get("currentPrice")
    return current_price

price = get_stock_prices("AAPL")
print(price)