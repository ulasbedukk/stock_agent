# Stock Agent

import yfinance as yf
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables and initialise the Anthropic client
load_dotenv()
client = Anthropic()

def get_stock_prices(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    
    current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    change_percent = info.get("regularMarketChangePercent")
    company_name = info.get("longName", symbol)
    day_high = info.get("dayHigh")
    day_low = info.get("dayLow")
    
    # Native currency and symbol mapping
    currency = info.get("currency", "USD")
    if currency == "TRY":
        currency_symbol = "₺"
    elif currency in ["GBP", "GBp"]:
        currency_symbol = "£"
        if currency == "GBp" and current_price:
            current_price /= 100
            if day_high: day_high /= 100
            if day_low: day_low /= 100
    elif currency == "EUR":
        currency_symbol = "€"
    else:
        currency_symbol = "$"

    news = ticker.news
    top_headline = news[0]["content"]["title"] if news and "content" in news[0] else "No recent news available."

    hist = ticker.history(period="1y")
    prices = hist['Close'].tolist() if not hist.empty else []
    
    return current_price, change_percent, company_name, day_high, day_low, top_headline, prices, currency_symbol


def generate_sparkline(prices):
    if not prices:
        return "N/A"
    num_bars = 30
    if len(prices) > num_bars:
        step = len(prices) / num_bars
        prices = [prices[int(i * step)] for i in range(num_bars)]
    min_p = min(prices)
    max_p = max(prices)
    spread = max_p - min_p
    chars = "_▂▃▄▅▆▇█"
    sparkline = ""
    for p in prices:
        if spread == 0:
            idx = 0
        else:
            idx = int((p - min_p) / spread * (len(chars) - 1))
            idx = max(0, min(idx, len(chars) - 1))
        sparkline += chars[idx]
    return sparkline

# Language selection once at the beginning
print("\n" + "=" * 50)
language_choice = input("Which language would you like to continue in? / Hangi dille devam etmek istersiniz? (English/Türkçe): ").strip()
is_turkish = language_choice.lower() in ["türkçe", "turkce", "turkish", "t"]

# Assign labels and texts based on the selected language
if is_turkish:
    language_name = "Turkish"
    price_label = "💰 Güncel fiyat:"
    analysis_label = "📊 Analiz"
    day_range_label = "📊 Günlük aralık"
    chart_label = "📈 52 Haftalık Fiyat Trendi"
    fetching_text = "🌍 Güncel dünya piyasaları ve haberleri çekiliyor..."
    global_title = "🌍 Güncel Dünya Piyasaları / Makro Görünüm:"
    gold_label = "🥇 Gold (Altın)"
    nasdaq_label = "📊 NASDAQ"
    dow_label = "🇺🇸 Dow Jones"
    uk100_label = "🇬🇧 UK100"
    bist_label = "🇹🇷 BIST 100"
    oil_label = "🛢️ Oil (WTI) (Petrol)"
    score_label = "Güven skoru"
    disclaimer_text = "\033[3m*Yatırım tavsiyesi değildir.*\033[0m"
    prompt_text = "İncelemek istediğiniz hisse sembolünü (örn. AAPL) veya izleme listesini (örn. AAPL, MSFT) girin\n(Dünya piyasaları için doğrudan Enter'a basın, Çıkış için 'q'): "
    closing_msg = "İyi günler dilerim :)"
else:
    language_name = "English"
    price_label = "💰 Current price:"
    analysis_label = "📊 Analysis for"
    day_range_label = "📊 Day range"
    chart_label = "📈 52-Week Price Trend"
    fetching_text = "🌍 Fetching global market data and news..."
    global_title = "🌍 Global Market Context / Macro View:"
    gold_label = "🥇 Gold (Altın)"
    nasdaq_label = "📊 NASDAQ"
    dow_label = "🇺🇸 Dow Jones"
    uk100_label = "🇬🇧 UK100"
    bist_label = "🇹🇷 BIST 100"
    oil_label = "🛢️ Oil (WTI) (Petrol)"
    score_label = "Confidence score"
    disclaimer_text = "\033[3m*Not investment advice.*\033[0m"
    prompt_text = "Enter a stock ticker (e.g. AAPL) or watchlist (e.g. AAPL, MSFT) or press Enter for global markets (Type 'q' to quit): "
    closing_msg = "Have a nice day :)"

keep_going = True

while keep_going:
    print("\n" + "=" * 50)
    user_input = input(prompt_text).strip()

    # Check for quit command
    if user_input.lower() in ['q', 'quit', 'çıkış', 'cikis', 'exit']:
        keep_going = False
        break

    # Scenario 1: User pressed Enter without typing anything -> Global Markets view + expanded news
    if user_input == "":
        print(f"\n{fetching_text}")
        
        gold_price, _, _, _, _, _, _, gold_sym = get_stock_prices("GC=F")
        nasdaq_price, _, _, _, _, nasdaq_news, _, nasdaq_sym = get_stock_prices("^IXIC")
        oil_price, _, _, _, _, _, _, oil_sym = get_stock_prices("CL=F")
        dow_price, _, _, _, _, _, _, dow_sym = get_stock_prices("^DJI")
        uk100_price, _, _, _, _, _, _, uk100_sym = get_stock_prices("^FTSE")
        bist_price, _, _, _, _, _, _, bist_sym = get_stock_prices("XU100.IS")
        
        # Make the news a bit longer and more detailed in the selected language using Claude
        expanded_news = nasdaq_news
        if nasdaq_news != "No recent news available.":
            try:
                news_msg = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=150,
                    messages=[{"role": "user", "content": f"Summarise and expand this financial news headline into a concise 2-sentence market update in {language_name}, keeping it professional (do not use any markdown headers or symbols like #): {nasdaq_news}"}]
                )
                expanded_news = news_msg.content[0].text.replace("#", "").strip()
            except Exception:
                pass
        
        print(f"\n{global_title}")
        print(f"{gold_label}: {gold_sym}{gold_price}" if gold_price else f"{gold_label}: N/A")
        print(f"{nasdaq_label}: {nasdaq_sym}{nasdaq_price}" if nasdaq_price else f"{nasdaq_label}: N/A")
        print(f"{oil_label}: {oil_sym}{oil_price}" if oil_price else f"{oil_label}: N/A")
        print(f"{dow_label}: {dow_sym}{dow_price}" if dow_price else f"{dow_label}: N/A")
        print(f"{uk100_label}: {uk100_sym}{uk100_price}" if uk100_price else f"{uk100_label}: N/A")
        print(f"{bist_label}: {bist_sym}{bist_price}" if bist_price else f"{bist_label}: N/A")
        print(f"📰 {'Güncel piyasa haberi' if is_turkish else 'Latest market news'}: {expanded_news}")

    # Scenario 2: User entered ticker(s) -> Check if single stock or Watchlist (comma separated)
    else:
        symbols = [s.strip().upper() for s in user_input.split(",") if s.strip()]

        # WATCHLIST MODE (Multiple tickers)
        if len(symbols) > 1:
            print(f"\n📊 {'İzleme Listesi Taraması' + ' (' + str(len(symbols)) + ' Hisse)' if is_turkish else 'Watchlist Scan' + ' (' + str(len(symbols)) + ' Stocks)'}:")
            print("-" * 50)
            for sym in symbols:
                price, change_percent, company_name, day_high, day_low, _, prices, currency_symbol = get_stock_prices(sym)
                if price is None:
                    print(f"❌ {sym}: Veri bulunamadı / Data not found.")
                else:
                    trend_emoji = "📈" if change_percent is not None and change_percent >= 0 else "📉"
                    change_str = f"({change_percent:.2f}%)" if change_percent is not None else ""
                    trend_chart = generate_sparkline(prices)
                    print(f"• {company_name} ({sym}): {currency_symbol}{price} {trend_emoji} {change_str}")
                    print(f"  {day_range_label}: {currency_symbol}{day_high} - {currency_symbol}{day_low}")
                    print(f"  {chart_label}: {trend_chart}")
                    print("-" * 30)
            print(f"\n{disclaimer_text}")

        # SINGLE STOCK MODE (Deep AI Analysis)
        else:
            symbol_input = symbols[0]
            price, change_percent, company_name, day_high, day_low, top_headline, prices, currency_symbol = get_stock_prices(symbol_input)

            if price is None:
                print("Veri bulunamadı / Data not found for this symbol.")
            else:
                stock_tool = {
                    "name": "get_stock_prices",
                    "description": "Returns the current stock price for a given symbol",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "The stock ticker symbol, e.g. AAPL"
                            }
                        },
                        "required": ["symbol"]
                    }
                }

                message = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=300,
                    tools=[stock_tool],
                    messages=[
                        {"role": "user", "content": f"What is the current stock price of {symbol_input}? and tell me if you think this is expensive or affordable, considering this recent headline: {top_headline}. Answer in maximum 2 sentences like a professional business person. Please answer in {language_name} At the very end, add a new line with only this format: SCORE: X (where X is a number from 1 to 10 representing your confidence in this stock as a good investment right now)."}
                    ]
                )

                if message.stop_reason == "tool_use":
                    tool_use_block = message.content[0]
                    symbol_requested = tool_use_block.input["symbol"]
                    price, change_percent, company_name, day_high, day_low, top_headline, prices, currency_symbol = get_stock_prices(symbol_requested)
                    
                    trend_emoji = "📈" if change_percent is not None and change_percent >= 0 else "📉"
                    change_str = f"({change_percent:.2f}%)" if change_percent is not None else ""
                    
                    print(f"{price_label} {company_name} ({currency_symbol}{price}) {trend_emoji} {change_str}")
                    print(f"{day_range_label}: {currency_symbol}{day_low} - {currency_symbol}{day_high}")
                    trend_chart = generate_sparkline(prices)
                    print(f"{chart_label}: {trend_chart}")

                combined_result = f"{symbol_input}: {currency_symbol}{price}"

                response = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=300,
                    tools=[stock_tool],
                    messages=[
                        {"role": "user", "content": f"What is the current stock price of {symbol_input}? and tell me if you think this is expensive or affordable, considering this recent headline: {top_headline}. Answer in maximum 2 sentences like a professional business person. Please answer in {language_name} At the very end, add a new line with only this format: SCORE: X (where X is a number from 1 to 10 representing your confidence in this stock as a good investment right now)."},
                        {"role": "assistant", "content": message.content},
                        {"role": "user", "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use_block.id if 'tool_use_block' in locals() else "call_1",
                                "content": combined_result
                            }
                        ]}
                    ]
                )

                print(f"\n{analysis_label} {symbol_input}:")
                full_response = response.content[0].text
                
                try:
                    score_line = full_response.split("SCORE:")[-1].strip()
                    score = int(score_line)
                except ValueError:
                    score = 5

                analysis_text = full_response.split("SCORE:")[0].strip()
                score_emoji = "🚨" if score < 5 else "💡"

                print(analysis_text)
                print(f"\n{score_emoji} {score_label}: {score}/10")
                print(f"\n{disclaimer_text}")

print(closing_msg)