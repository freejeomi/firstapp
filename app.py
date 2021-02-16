import feedparser

"""
The render_template function is the magic which takes a Jinja template as input
and produces pure HTML, capable of being read by any browser, as the output
"""
from flask import Flask

from flask import render_template
from flask import request
import json
import urllib.parse
import urllib.request


app = Flask(__name__)

RSS_FEEDS = {'hackernews': 'http://feeds.feedburner.com/TheHackersNews',
            'welivesecurity': 'http://feeds.feedburner.com/eset/blog',
            'krebsonsecurity': 'http://feeds.feedburner.com/krebsonsecurity.com/',
            'threatpost': 'http://feeds.feedburner.com/threatpost',
             'nakedsecurity':'http://feeds.feedburner.com/nakedsecurity'}
# set default dictionary values
DEFAULTS = {'publication':'hackernews','city': 'London'}

# app route for default and bbc
@app.route("/", methods=['GET','POST'])
def publish_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "hackernews"
        pass
    else:
        publication = query.lower()
        pass
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("London")
    return render_template("home.html", articles=feed['entries'], weather = weather)

    # rest of code unchanged
    pass


# function that calls the publications ==> no more necessary
# def get_news(publication):
#     feed = feedparser.parse(RSS_FEEDS[publication])
#     #first_article = feed['entries'][0]
#     return render_template("home.html", articles=feed['entries'])

# another function for the weather
def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=6146c3c14476a0b727901203fd042263"
    query = urllib.parse.quote(query) # make this a good html query string
    url = api_url.format(query) # add it to the api_url string above
    data = urllib.request.urlopen(url) # make a request to the url now
    #print(data)
    parsed = json.load(data) # parse the data via Python JSON library
    print(parsed)
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                       parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"]
                   }
    return weather
    pass

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
