import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from genvideo import genvideo
from downloadvideo import download_video
import time
import datetime
import functools

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

my_latitude = 16.445370
my_longitude = 80.544980
weather_api_key = "35a8072eec7a1c9db042a3e93151577b"
weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={my_latitude}&lon=" \
              f"{my_longitude}&appid={weather_api_key}"

def get_date():
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%A, %d %B")
    return {
        "date": formatted_date
    }

def get_weather():
    response = requests.get(url=weather_url)
    print("Weather API Response:", response.json())  # Debug statement
    data = response.json()
    print("Weather API Data:", data)  # Debug statement
    try:
        weather_temp = int(data['main']['temp']) - 273
        location_name = data['name']
        weather_description = data['weather'][0]['main']
        return {
            "temp": weather_temp,
            "location": location_name,
            "overall": weather_description,
            "lat": my_latitude,
            "long": my_longitude,
        }
    except Exception as e:
        print("Error getting weather data:", e)  # Debug statement
        return None

import requests

def get_stock(stock_name):
    stock_key = "0Z0KYFWOOVU5SOR0"
    stock_url = "https://www.alphavantage.co/query"
    stock_parameters = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': stock_name,
        'apikey': stock_key,
    }
    
    # Debug statement: Print out the stock URL and parameters
    print("Stock API URL:", stock_url)
    print("Stock API Parameters:", stock_parameters)

    stock_response = requests.get(url=stock_url, params=stock_parameters)
    
    # Debug statement: Print out the stock API response
    print("Stock API Response:", stock_response.json())

    stock_data = stock_response.json()

    stock_data_details = stock_data['Time Series (Daily)']
    stock_timestamp = list(stock_data_details.keys())[:2]
    stock_close_price_today = round(float(stock_data_details[stock_timestamp[0]]['4. close']) * 83.15, 2)
    stock_close_price_yesterday = round(float(stock_data_details[stock_timestamp[1]]['4. close']) * 83.15, 2)

    stock_price_change = round(float(((stock_close_price_today - stock_close_price_yesterday)
                                      / stock_close_price_yesterday) * 100), 2)
    difference = round(float(stock_close_price_today - stock_close_price_yesterday), 2)
    if difference > 0:
        col = "#008561"
        arrow = "%▲"
    elif difference < 0:
        col = "#c1433d"
        arrow = "%▼"
    else:
        col = "black"
        arrow = ""

    # Debug statement: Print out the processed stock data
    print("Processed Stock Data:", {
        "name": stock_name,
        "price": stock_close_price_today,
        "percentage": stock_price_change,
        "change": difference,
        "col": col,
        "arrow": arrow,
    })

    return {
        "name": stock_name,
        "price": stock_close_price_today,
        "percentage": stock_price_change,
        "change": difference,
        "col": col,
        "arrow": arrow,
    }


@functools.lru_cache(maxsize=1)  # Cache the result for get_top_news
def get_top_news(num, country, category):
    NEWS_KEY = "efc64b4ec691448f9baf07a1ca948bc0"
    news_url = "https://newsapi.org/v2/top-headlines?"
    news_parameters = {
        'apiKey': NEWS_KEY,
        'country': country,
        'category': category,
    }
    response = requests.get(url=news_url, params=news_parameters)
    data = response.json()
    news_list = []

    for i in range(num):
        news_source = data['articles'][i]['source']['name']
        news_title = data['articles'][i]['title']
        news_url = data['articles'][i]['url']
        news_img_url = data['articles'][i]['urlToImage']
        publishedAt = data['articles'][i]['publishedAt']
        date = datetime.datetime.strptime(publishedAt, "%Y-%m-%dT%H:%M:%SZ")
        current_time = datetime.datetime.utcnow()
        time_difference = current_time - date
        if time_difference.total_seconds() < 3600:
            minutes_ago = int(time_difference.total_seconds() / 60)
            uploadedIn = f"{minutes_ago} minutes ago"
        elif time_difference.total_seconds() < 86400:
            hours_ago = int(time_difference.total_seconds() / 3600)
            uploadedIn = f"{hours_ago} hours ago"
        else:
            days_ago = int(time_difference.total_seconds() / 86400)
            uploadedIn = f"{days_ago} days ago"
        news_item = {
            "news_source": news_source,
            "news_title": news_title,
            "news_url": news_url,
            "news_img_url": news_img_url,
            "uploadedIn": uploadedIn,
        }
        news_list.append(news_item)

    return news_list

@functools.lru_cache(maxsize=1)  # Cache the result for get_top_news
def get_keyword_news(num, keyword):
    NEWS_KEY = "efc64b4ec691448f9baf07a1ca948bc0"
    news_url = "https://newsapi.org/v2/everything?"
    news_parameters = {
        'apiKey': NEWS_KEY,
        'q': keyword,
    }
    response = requests.get(url=news_url, params=news_parameters)
    data = response.json()
    print(data)
    news_list = []

    for i in range(num):
        news_source = data['articles'][i]['source']['name']
        news_title = data['articles'][i]['title']
        news_url = data['articles'][i]['url']
        news_img_url = data['articles'][i]['urlToImage']
        publishedAt = data['articles'][i]['publishedAt']
        date = datetime.datetime.strptime(publishedAt, "%Y-%m-%dT%H:%M:%SZ")
        current_time = datetime.datetime.utcnow()
        time_difference = current_time - date
        if time_difference.total_seconds() < 3600:
            minutes_ago = int(time_difference.total_seconds() / 60)
            uploadedIn = f"{minutes_ago} minutes ago"
        elif time_difference.total_seconds() < 86400:
            hours_ago = int(time_difference.total_seconds() / 3600)
            uploadedIn = f"{hours_ago} hours ago"
        else:
            days_ago = int(time_difference.total_seconds() / 86400)
            uploadedIn = f"{days_ago} days ago"
        news_item = {
            "news_source": news_source,
            "news_title": news_title,
            "news_url": news_url,
            "news_img_url": news_img_url,
            "uploadedIn": uploadedIn,
        }
        news_list.append(news_item)

    return news_list

def generate_news_and_video(sport):
    news_text = f"Latest news related to {sport}."
    id = genvideo("https://clips-presenters.d-id.com/amy/Aq6OmGZnMt/Vcq0R4a8F0/image.png", news_text, "en-US-SaraNeural")
    time.sleep(100)
    video_url = download_video(id)
    return video_url

@app.route("/")
def home():
    title = "Your briefing"
    currently = "local_label"
    date_data = get_date()
    weather_data = get_weather()

    if 'Rain' in weather_data['overall']:
        weather_icon = "rain.png"
    elif 'Cloud' in weather_data['overall']:
        weather_icon = "cloud.png"
    elif 'Sun' in weather_data['overall']:
        weather_icon = "sun.png"
    else:
        weather_icon = "default.png"

    stock_data = get_stock("TSLA")
    stock_data1 = get_stock("NVDA")
    stock_data2 = get_stock("AMZN")

    news_items = get_top_news(20, country='in', category='general')

    return render_template("index.html", weather_data=weather_data, date_data=date_data, weather_icon=weather_icon,
                           stock_data=stock_data, stock_data1=stock_data1, stock_data2=stock_data2,
                           news_items=news_items, title=title, currently=currently)

@app.route("/sports")
def sports():
    title = "Sports briefing"
    currently = "sports_label"
    date_data = get_date()
    weather_data = get_weather()

    if 'Rain' in weather_data['overall']:
        weather_icon = "rain.png"
    elif 'Cloud' in weather_data['overall']:
        weather_icon = "cloud.png"
    elif 'Sun' in weather_data['overall']:
        weather_icon = "sun.png"
    else:
        weather_icon = "default.png"

    stock_data = get_stock("TSLA")
    stock_data1 = get_stock("NVDA")
    stock_data2 = get_stock("AMZN")

    news_items = get_top_news(20, country='in', category='sports')

    # Generate video for sports news
    video_url = generate_news_and_video("Sports")

    return render_template("index.html", weather_data=weather_data, date_data=date_data, weather_icon=weather_icon,
                           stock_data=stock_data, stock_data1=stock_data1, stock_data2=stock_data2,
                           news_items=news_items, title=title, currently=currently, video_url=video_url)

@app.route("/entertainment")
def entertainment():
    title = "Entertainment briefing"
    currently = "entertainment_label"
    date_data = get_date()
    weather_data = get_weather()

    if 'Rain' in weather_data['overall']:
        weather_icon = "rain.png"
    elif 'Cloud' in weather_data['overall']:
        weather_icon = "cloud.png"
    elif 'Sun' in weather_data['overall']:
        weather_icon = "sun.png"
    else:
        weather_icon = "default.png"

    stock_data = get_stock("TSLA")
    stock_data1 = get_stock("NVDA")
    stock_data2 = get_stock("AMZN")

    news_items = get_top_news(20, country='in', category='entertainment')

    # Generate video for entertainment news
    video_url = generate_news_and_video("Entertainment")

    return render_template("index.html", weather_data=weather_data, date_data=date_data, weather_icon=weather_icon,
                           stock_data=stock_data, stock_data1=stock_data1, stock_data2=stock_data2,
                           news_items=news_items, title=title, currently=currently, video_url=video_url)

@app.route("/technology")
def technology():
    title = "Technology briefing"
    currently = "technology_label"
    date_data = get_date()
    weather_data = get_weather()

    if 'Rain' in weather_data['overall']:
        weather_icon = "rain.png"
    elif 'Cloud' in weather_data['overall']:
        weather_icon = "cloud.png"
    elif 'Sun' in weather_data['overall']:
        weather_icon = "sun.png"
    else:
        weather_icon = "default.png"

    stock_data = get_stock("TSLA")
    stock_data1 = get_stock("NVDA")
    stock_data2 = get_stock("AMZN")

    news_items = get_top_news(20, country='in', category='technology')

    # Generate video for technology news
    video_url = generate_news_and_video("Technology")

    return render_template("index.html", weather_data=weather_data, date_data=date_data, weather_icon=weather_icon,
                           stock_data=stock_data, stock_data1=stock_data1, stock_data2=stock_data2,
                           news_items=news_items, title=title, currently=currently, video_url=video_url)

@app.route("/business")
def business():
    title = "Business briefing"
    currently = "business_label"
    date_data = get_date()
    weather_data = get_weather()

    if 'Rain' in weather_data['overall']:
        weather_icon = "rain.png"
    elif 'Cloud' in weather_data['overall']:
        weather_icon = "cloud.png"
    elif 'Sun' in weather_data['overall']:
        weather_icon = "sun.png"
    else:
        weather_icon = "default.png"

    stock_data = get_stock("TSLA")
    stock_data1 = get_stock("NVDA")
    stock_data2 = get_stock("AMZN")

    news_items = get_top_news(20, country='in', category='business')

    # Generate video for business news
    video_url = generate_news_and_video("Business")

    return render_template("index.html", weather_data=weather_data, date_data=date_data, weather_icon=weather_icon,
                           stock_data=stock_data, stock_data1=stock_data1, stock_data2=stock_data2,
                           news_items=news_items, title=title, currently=currently, video_url=video_url)

@app.route("/science")
def science():
    title = "Science briefing"
    currently = "science_label"
    date_data = get_date()
    weather_data = get_weather()

    if 'Rain' in weather_data['overall']:
        weather_icon = "rain.png"
    elif 'Cloud' in weather_data['overall']:
        weather_icon = "cloud.png"
    elif 'Sun' in weather_data['overall']:
        weather_icon = "sun.png"
    else:
        weather_icon = "default.png"

    stock_data = get_stock("TSLA")
    stock_data1 = get_stock("NVDA")
    stock_data2 = get_stock("AMZN")

    news_items = get_top_news(20, country='in', category='science')

    # Generate video for science news
    video_url = generate_news_and_video("Science")

    return render_template("index.html", weather_data=weather_data, date_data=date_data, weather_icon=weather_icon,
                           stock_data=stock_data, stock_data1=stock_data1, stock_data2=stock_data2,
                           news_items=news_items, title=title, currently=currently, video_url=video_url)

@app.route("/health")
def health():
    title = "Health briefing"
    currently = "health_label"
    date_data = get_date()
    weather_data = get_weather()

    if 'Rain' in weather_data['overall']:
        weather_icon = "rain.png"
    elif 'Cloud' in weather_data['overall']:
        weather_icon = "cloud.png"
    elif 'Sun' in weather_data['overall']:
        weather_icon = "sun.png"
    else:
        weather_icon = "default.png"

    stock_data = get_stock("TSLA")
    stock_data1 = get_stock("NVDA")
    stock_data2 = get_stock("AMZN")

    news_items = get_top_news(20, country='in', category='health')

    # Generate video for health news
    video_url = generate_news_and_video("Health")

    return render_template("index.html", weather_data=weather_data, date_data=date_data, weather_icon=weather_icon,
                           stock_data=stock_data, stock_data1=stock_data1, stock_data2=stock_data2,
                           news_items=news_items, title=title, currently=currently, video_url=video_url)

@app.route("/process", methods=['POST'])
def process():
    input_keyword = request.form['user_input']
    title = input_keyword.capitalize()+" briefing"
    date_data = get_date()
    weather_data = get_weather()

    if 'Rain' in weather_data['overall']:
        weather_icon = "rain.png"
    elif 'Cloud' in weather_data['overall']:
        weather_icon = "cloud.png"
    elif 'Sun' in weather_data['overall']:
        weather_icon = "sun.png"
    else:
        weather_icon = "default.png"

    stock_data = get_stock("TSLA")
    stock_data1 = get_stock("NVDA")
    stock_data2 = get_stock("AMZN")

    news_items = get_keyword_news(20, keyword=input_keyword)
    input_keyword = ""

    return render_template("index.html", weather_data=weather_data, date_data=date_data, weather_icon=weather_icon,
                           stock_data=stock_data, stock_data1=stock_data1, stock_data2=stock_data2,
                           news_items=news_items, input_keyword=input_keyword, title=title)

if __name__ == "__main__":
    app.run(debug=True)
