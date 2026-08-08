#DO NOT FORGET TO ADD IMPORT AND SETUP FOR THE CLIENT!!!!

import yfinance as yf
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()



keep_going = "yes"




def get_stock_prices(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    current_price = info.get("currentPrice")
    return current_price

while keep_going == "yes":
                print("\n" + "=" * 50)

                symbol_input = input("Which stock symbol would you like to check? (e.g. AAPL): ")

                price = get_stock_prices(symbol_input)

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


                    message = client.messages.create(
                        model="claude-sonnet-4-5",
                        max_tokens=300,
                        tools=[stock_tool],
                        messages=[
                            {"role": "user", "content": f"What is the current stock price of {symbol_input}? and tell me if you think this is expensive or affordable and answer in maximum 2 sentences and answer like a professional business person in UK english?"},

                                ]
                    )

                    if message.stop_reason == "tool_use":
                        tool_use_block = message.content[0]
                        symbol_requested = tool_use_block.input["symbol"]
                        price = get_stock_prices(symbol_requested)
                        print(f"💰 Current price: ${price}")
                    else:
                        print(message.content[0].text)


                    combined_result = f"{symbol_input}: {price}"

                    response = client.messages.create(
                        model="claude-sonnet-4-5",
                        max_tokens=300,
                        tools=[stock_tool],
                        messages=[
                            {"role": "user", "content": f"What is the current stock price of {symbol_input}? and tell me if you think this is expensive or affordable and answer in maximum 2 sentences and answer like a professional business person in UK english?"},
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

                    print(f"\n📊 Analysis for {symbol_input}:")
                    print(response.content[0].text)

                keep_going = input("Would you like to check another stock? (yes/no): ")