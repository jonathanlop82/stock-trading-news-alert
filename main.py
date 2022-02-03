import requests
import os
import datetime
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
api_key = os.environ['AV_API_KEY']
news_api_key = os.environ['NEWS_API_KEY']

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

parameters = {
        'function':'TIME_SERIES_DAILY',
        'symbol':STOCK,
        'apikey':api_key
}

url = 'https://www.alphavantage.co/query'

r = requests.get(url, params=parameters)
r.raise_for_status()
data = r.json()
print(data)
print(data['Time Series (Daily)']['2022-02-01']['4. close'])

today = datetime.datetime.today()
yesterday = (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
print(yesterday)
close_yesterday =float(data['Time Series (Daily)'][yesterday]['4. close'])
before_yesterday = (today - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
close_before_yesterday = float(data['Time Series (Daily)'][before_yesterday]['4. close'])
print(close_yesterday, close_before_yesterday)
print(close_yesterday - close_before_yesterday)
percent = round(100*(close_yesterday - close_before_yesterday)/close_yesterday,2)
print(f'{percent}%')

if percent >= 5 or percent <= -5:
        print('Get News')

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

news_parameters = {
        'apiKey':'e9116c4ddde9448e83d889ec9c6e13ba',
        'qinTitle':COMPANY_NAME,
        'from':today.strftime('%Y-%m-%d'),
        'sortBy':'publishedAt'
}

response_news = requests.get('https://newsapi.org/v2/everything', params=news_parameters)
response_news.raise_for_status()
news_data = response_news.json()
three_articles = news_data['articles'][:3]
# for i in range(3):
#         print(news_data['articles'][i]['title'])
#         print(news_data['articles'][i]['description'])
#         print(news_data['articles'][i]['publishedAt'])
#         print()
#print(three_articles)
formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
print(formatted_articles)
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

client = Client(account_sid, auth_token)
for article in formatted_articles:
        message = client.messages \
                .create(
                body=f"Tesla: {percent}%\n{article}",
                from_='+19035680939',
                to='+50760737637'
            )

print(message.status)

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

