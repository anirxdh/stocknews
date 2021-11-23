import requests
import os
from twilio.rest import Client

ACCOUT_SID = "ACd33bce417ba921ec550198efa065ada0"
Auth_token = "f8a740f5216a7bd378ff3cba44e450ce"
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "EJH3KPEACBBTSTBT"
NEWS_API_KEY = "07c839a94b1e4c7e92f22b536cea51d8"
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_paras = {
"function" : "TIME_SERIES_DAILY",
"symbol" : STOCK_NAME,
"apikey" : STOCK_API_KEY,

}

response = requests.get(STOCK_ENDPOINT, params = stock_paras)
data =response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterdays_closing_price=data_list[0]["4. close"]
print(yesterdays_closing_price)
#print(yesterdays_closing_price)

 #2. - Get the day before yesterday's closing stock price

day_before_yesterday_data= data_list[1]["4. close"]
print(day_before_yesterday_data)


#3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = float(yesterdays_closing_price) - float(day_before_yesterday_data)
if difference>0:
    emoji ="📈"
else:
    emoji ="📉"

# 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference/ float(yesterdays_closing_price))*100)
print(diff_percent)

#5 - If TODO4 percentage is greater than 5 then print("Get News").

if abs(diff_percent) > 1:
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response =requests.get(NEWS_ENDPOINT, params=news_params)
    article =news_response.json()["articles"]
    print(article
          )
    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

# 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    three_articles = article[:3] #slicing 0 to 3
    print(three_articles)
#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

# 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}:{emoji}{diff_percent}%\nHeadline : {article['title']},\nBrief: {article['description']}" for article in three_articles]
# 9. - Send each article as a separate message via Twilio.

    client =Client(ACCOUT_SID,Auth_token)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+13203442415",
            to="+918124107143"
        )

#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

