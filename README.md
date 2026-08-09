# STOCK ANALYSIS AGENT

*An AI-powered terminal tool that fetches real-time stock data and generates investment insights using Claude.*

## WHAT IT DOES
- Agentic Tool Use: Claude autonomously pulls live market data and news before analyzing the stock.
- Three Modes: Press Enter for a global market snapshot, type one ticker (e.g., AAPL) for deep AI analysis, or type multiple (e.g., AAPL, MSFT) for a quick watchlist scan.
- Smart Features: Shows ASCII sparkline charts, converts to local currencies automatically, and gives a 1-10 AI confidence score.
- Stable & Bilingual: Fully supports UK English and Turkish. Built with error handling so it does not crash if data is missing.

## TECH STACK
Python, yfinance, Anthropic API, python-dotenv.

## INSTALLATION
1. Download the code: `git clone https://github.com/ulasbedukk/stock_agent.git`
2. Enter the folder: `cd stock_agent`
3. Install dependencies: `pip install -r requirements.txt`
4. Add your API key: Create a `.env` file inside the folder and write `ANTHROPIC_API_KEY=your_key_here`

## HOW TO RUN
Execute this command in your terminal:
`python3 stock_agent_v2.py`

*Disclaimer: Educational purposes only. Not financial advice.*