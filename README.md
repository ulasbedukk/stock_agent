# Stock Analysis Agent

*An AI-powered agent that fetches real-time stock data and generates investment insights using Claude.*

This is a terminal-based tool that provides real-time stock prices in native currencies and global market context, giving a short comment on whether the current price seems reasonable. It also shows recent price movement via ASCII sparkline charts, the latest relevant news, and a confidence score. It is designed to help investors save time when checking individual stocks, watchlists, and global markets.

## How it works
Run the script, choose your preferred language (English or Turkish), then either press Enter to view current global markets, enter a single ticker symbol for deep AI analysis (e.g., AAPL), or enter a comma-separated watchlist to scan multiple stocks at once (e.g., AAPL, MSFT). The agent fetches real-time data, including local pricing, daily range, and 52-week price trends, and asks Claude to provide a short, professional comment on the valuation along with a confidence score.

## Technologies used
- Python
- yfinance
- Anthropic API
- python-dotenv

## How to run it
Run the following command in the terminal:

```bash
python3 stock_agent_v2.py