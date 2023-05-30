import requests
from datetime import datetime, timedelta
from twilio.rest import Client

ACCOUNT_SID = "AC93da89257da2bd53412455357b8ce65f"
TWILIO_AUTH_TOKEN = "fde5c512940d721a5137aa0f190842b1"
PHONE_NUMBER = "+15855662614"

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Datetime
yesterday = str(datetime.now().date() - timedelta(1))
day_before_yesterday = str(datetime.now().date() - timedelta(2))


# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

STOCK_URL = "https://www.alphavantage.co/query"
STOCK_API = "KPC8NJYNRAXJ6NPO."
parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "apikey": STOCK_API,
    "symbol": STOCK,
    "outputsize": "compact",
}

stock_response = requests.get(url=STOCK_URL, params=parameters)
stock_response.raise_for_status()

yesterday_data = float(stock_response.json()["Time Series (Daily)"][yesterday]["4. close"])
day_before_yesterday_data = float(stock_response.json()["Time Series (Daily)"][day_before_yesterday]["4. close"])
difference = (yesterday_data - day_before_yesterday_data)
up_down = ""
if difference > 0:
    up_down = "🔺"
else:
    updown = "🔻"

percentage_diff = round((difference / yesterday_data) * 100)


# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

NEWS_URL = "https://newsapi.org/v2/everything"
NEWS_API = "088ee1a969714de89405b81c7f15194e"

if abs(percentage_diff) > 1:
    parameters = {
        "apiKey": NEWS_API,
        "q": COMPANY_NAME,
        "language": "en",
        "pageSize": 2,
        "sortBy": "relevancy",
    }

    news_response = requests.get(url=NEWS_URL, params=parameters)
    news_response.raise_for_status()
    news_data = news_response.json()

    client = Client(ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for index in range(2):
        message = client.messages.create(
            body=f"{STOCK}: {up_down}{percentage_diff}%\n"
                 f"Headline: {news_data['articles'][index]['title']}\n"
                 f"Description: {news_data['articles'][index]['description']}",
            from_=PHONE_NUMBER,
            to="+919769494315"
            )
        print(message.status)


# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
