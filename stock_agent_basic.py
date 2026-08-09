# Stock Analysis Agent

import yfinance as yf
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()


def get_stock_prices(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    current_price = info.get("currentPrice")
    change_percent = info.get("regularMarketChangePercent")
    company_name = info.get("longName")
    day_high = info.get("dayHigh")
    day_low = info.get("dayLow")
    news = ticker.news
    top_headline = news[0]["content"]["title"]
    return current_price, change_percent, company_name, day_high, day_low, top_headline


keep_going = "yes"

while keep_going == "yes" or keep_going == "evet":
    print("\n" + "=" * 50)
    language_choice = input("Which language would you like the analysis in? / Hangi dille yapmak istersiniz? (English/Türkçe): ")

    if language_choice.lower() == "türkçe" or language_choice.lower() == "turkce" or language_choice.lower() == "turkish":
        price_label = "💰 Güncel fiyat:"
        analysis_label = "📊 Analiz"
        continue_question = "Başka bir hisse kontrol etmek ister misiniz? (evet/hayır): "
        symbol_input = input("Hangi hissenin sembolünü kontrol etmek istersiniz? (örn. AAPL): ")
    else:
        price_label = "💰 Current price:"
        analysis_label = "📊 Analysis for"
        continue_question = "Would you like to check another stock? (yes/no): "
        symbol_input = input("Which stock symbol would you like to check? (e.g. AAPL): ")

    price, change_percent, company_name, day_high, day_low, top_headline = get_stock_prices(symbol_input)

    if price is None:
        print("Sorry, I couldn't find data for that symbol. Please check and try again.")

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

        prompt_content = f"What is the current stock price of {symbol_input}? and tell me if you think this is expensive or affordable, considering this recent headline: '{top_headline}'. Answer in maximum 2 sentences like a professional business person. Please answer in {language_choice}. At the very end, add a new line with only this format: SCORE: X (where X is a number from 1 to 10 representing your confidence in this stock as a good investment right now)."

        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=300,
            tools=[stock_tool],
            messages=[
                {"role": "user", "content": prompt_content},
            ]
        )

        if message.stop_reason == "tool_use":
            tool_use_block = message.content[0]
            symbol_requested = tool_use_block.input["symbol"]
            price, change_percent, company_name, day_high, day_low, top_headline = get_stock_prices(symbol_requested)

            if change_percent >= 0:
                trend_emoji = "📈"
            else:
                trend_emoji = "📉"

            print(f"{price_label} {company_name} (${price}) {trend_emoji} ({change_percent:.2f}%)")
            print(f"📊 Day range: ${day_low} - ${day_high}")
            print(f"📰 Latest news: {top_headline}")

            combined_result = f"{symbol_input}: {price}"

            response = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=300,
                tools=[stock_tool],
                messages=[
                    {"role": "user", "content": prompt_content},
                    {"role": "assistant", "content": message.content},
                    {"role": "user", "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use_block.id,
                            "content": combined_result
                        }
                    ]}
                ]
            )

            full_response = response.content[0].text
        else:
            full_response = message.content[0].text

        score_line = full_response.split("SCORE:")[-1].strip()
        score = int(score_line)
        analysis_text = full_response.split("SCORE:")[0].strip()

        if score < 5:
            score_emoji = "🚨"
        else:
            score_emoji = "💡"

        print(f"\n{analysis_label} {symbol_input}:")
        print(analysis_text)
        print(f"\n{score_emoji} Confidence score: {score}/10")

    keep_going = input(continue_question)

if language_choice.lower() == "türkçe" or language_choice.lower() == "turkce" or language_choice.lower() == "turkish":
    print("İyi günler dilerim :)")
else:
    print("Have a nice day :)")